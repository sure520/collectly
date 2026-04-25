import re
import requests
from urllib.parse import urlparse, parse_qs

# ==============================================
# 1. 从文本中提取 http 链接（处理带文案的分享内容）
# ==============================================
def extract_url(text: str) -> str:
    text = str(text).strip()
    # 精准匹配：抖音/小红书/B站/知乎 合法链接，遇到中文、符号自动截断
    pattern = re.compile(
        r"https?://(?:www\.|v\.|b23\.tv|xhslink\.com|zhuanlan\.zhihu\.com)"
        r"[a-zA-Z0-9_\-\/.?&=]+",
        re.I
    )
    match = pattern.search(text)
    return match.group(0) if match else text

# ==============================================
# 2. 小红书短链还原：追踪重定向，得到真实长链接
# ==============================================
def resolve_xhs_short(url: str) -> str:
    if "xhslink.com" not in url:
        return url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Referer": "https://www.xiaohongshu.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "sec-ch-ua": '"Chromium";v="130", "Not=A?Brand";v="99", "Google Chrome";v="130"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }

    try:
        # 必须用 GET，不能只用 HEAD
        with requests.Session() as s:
            resp = s.get(url, headers=headers, allow_redirects=True, timeout=10)
            return resp.url
    except Exception as e:
        print(f"[xhs还原失败] {e}")
        return url

# ==============================================
# 2. 短链还原：追踪重定向，得到真实长链接
# ==============================================
def resolve_short_url(url: str) -> str:
    if "xhslink.com" in url:
        return resolve_xhs_short(url)

    short_domains = ["b23.tv", "v.douyin.com"]
    if not any(d in url for d in short_domains):
        return url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0.0.0 Safari/537.36"
    }
    try:
        with requests.Session() as s:
            resp = s.head(url, headers=headers, allow_redirects=True, timeout=10)
            return resp.url
    except Exception:
        return url

# ==============================================
# 3. 核心：清理成永久纯净链接（你所有平台都支持）
# ==============================================
def clean_pure_url(url: str) -> str:
    parsed = urlparse(url)
    netloc = parsed.netloc
    path = parsed.path.rstrip("/")
    query = parse_qs(parsed.query)

    # --- 抖音：特殊处理 modal_id → 标准视频链接 ---
    if "douyin.com" in netloc:
        modal_id = query.get("modal_id", [None])[0]
        if modal_id:
            return f"https://www.douyin.com/video/{modal_id}"
        return f"https://{netloc}{path}"

    # --- B站：保留 p= 分P，删除所有追踪参数 ---
    elif "bilibili.com" in netloc:
        p = query.get("p", [None])[0]
        base = f"https://www.bilibili.com{path}"
        return f"{base}?p={p}" if p else base

    # --- 知乎专栏 ---
    elif "zhuanlan.zhihu.com" in netloc:
        return f"https://zhuanlan.zhihu.com{path}"

    # --- 小红书：必须保留 xsec_token 和 xsec_source，否则无法访问 ---
    elif "xiaohongshu.com" in netloc:
        xsec_token = query.get("xsec_token", [None])[0]
        xsec_source = query.get("xsec_source", [None])[0]
        
        params = []
        if xsec_token:
            params.append(f"xsec_token={xsec_token}")
        if xsec_source:
            params.append(f"xsec_source={xsec_source}")
        
        base = f"https://www.xiaohongshu.com{path}"
        return f"{base}?{'&'.join(params)}" if params else base

    # --- 其他 ---
    else:
        return f"{parsed.scheme}://{netloc}{path}"

# ==============================================
# 4. 总调度函数：一键处理所有链接
# ==============================================
def process_url(raw_text: str) -> str:
    url = extract_url(raw_text)
    url = resolve_short_url(url)
    url = clean_pure_url(url)
    return url

# ==============================================
# 测试：你提供的全部用例
# ==============================================
if __name__ == "__main__":
    test_cases = [
        # ==================== 抖音 APP 短链接 ====================
        "6.17 复制打开抖音，看看【涛哥AIGC实战的作品】太好用了，架构图Skills # 架构图 # 画图... https://v.douyin.com/GiwKX3xWbD4/ HVl:/ x@F.hb 08/24",
        "4.12 复制打开抖音，看看【阿甘探AI的作品】港大又开源，让AI越用越聪明还越来越省钱！  https://v.douyin.com/cwYFf5dp6qo/ V@Y.zG 01/19 KJV:/",
        "2.56 复制打开抖音，看看【AI大白话的作品】港大新开源 OpenHarness，两天斩获 1.... https://v.douyin.com/L4RtoSyHs2I/ 02/20 U@Y.MW fBT:/",

        # ==================== 抖音 WEB 长链接（含modal_id） ====================
        "https://www.douyin.com/user/self?modal_id=7627013109139475762&showSubTab=favorite_folder&showTab=favorite_collection",
        "https://www.douyin.com/user/self?modal_id=7624545950140874609&showSubTab=favorite_folder&showTab=favorite_collection",
        "https://www.douyin.com/user/self?modal_id=7624441069962317107&showSubTab=favorite_folder&showTab=favorite_collection",

        # ==================== B站 APP 短链接 ====================
        "【4月最新Claude Code使用安装教程，手把手教你在国内怎么免费使用安装Claude Code！-哔哩哔哩】 https://b23.tv/XZeyxg6",
        "【【2026最新】手把手带你用GraphRAG+Neo4j搭建知识图谱本地RAG知识库！轻松实现图谱可视化，全程干货，零基础也能快速上手！-哔哩哔哩】 https://b23.tv/NRmRC6a",
        "【从零构建知识图谱：迪哥手把手教你用知识图谱做医疗问答系统！零基础也能搞定（附完整代码）-哔哩哔哩】 https://b23.tv/R3A7BG6",
        "【Claude code 原理拆解：Bash就是一切-哔哩哔哩】 https://b23.tv/Q5FqErt",

        # ==================== B站 WEB 长链接 ====================
        "https://www.bilibili.com/video/BV1aTp1zRENj/?spm_id_from=333.1387.favlist.content.click&vd_source=ba077cb5048f0562112e9d805ce8721f",
        "https://www.bilibili.com/video/BV1aTp1zRENj?spm_id_from=333.788.videopod.episodes&vd_source=ba077cb5048f0562112e9d805ce8721f&p=2",
        "https://www.bilibili.com/video/BV1a7411z75u/?spm_id_from=333.1387.favlist.content.click&vd_source=ba077cb5048f0562112e9d805ce8721f",

        # ==================== 知乎 ====================
        "https://zhuanlan.zhihu.com/p/731785401?share_code=UaCZQIyom9Iu&utm_psn=2031311064101544538",
        "https://zhuanlan.zhihu.com/p/2020434886146672550?share_code=c9q4bAbQ2T3R&utm_psn=2031311130996500392",
        "https://zhuanlan.zhihu.com/p/1998542842180678006?share_code=11bJr7SkQvSol&utm_psn=2031311186206180951",
        "https://zhuanlan.zhihu.com/p/25763072556",

        # ==================== 小红书 APP 短链接 ====================
        "分享帮我拿到字节暑期岗位的agent项目 这绝对不是那种... http://xhslink.com/o/8YzrpsvySjv 把口令复制下来，进入【小红书】看笔记~",
        "https://www.xiaohongshu.com/explore/69e4ff92000000002102c20a?app_platform=android&ignoreEngage=true&app_version=9.19.4&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CBp1u60MOyhTUlsWyg6e_27zA_u8TyvJSoe-Phwv10evc=&author_share=1&shareRedId=ODc3RURLOkE2NzUyOTgwNjY1OTk1PkxB&apptime=1777082359&share_id=b2abd496003449f5863ffeb566f952b2&share_channel=copy_link&appuid=615eaf6800000000020219f8&xhsshare=CopyLink"
        "弃坑Verl，转向 Slime！ 为了训 Fully-Async RL 和 Ag... http://xhslink.com/o/9lAi5W4L4qT 留住这段口令，去【小红书】瞅瞅笔记~",
        "nanorllm开源 agentic RL 最核心的训练闭环 最近写了... http://xhslink.com/o/5XFQl07XLD2前往【小红书】看看这篇分享吧！",

        # ==================== 小红书 WEB 长链接 ====================
        "https://www.xiaohongshu.com/explore/69e4ff92000000002102c20a?xsec_token=ABNq2ZZ0Q9oow_EwSy-N9d7LTDU5gStg381dNEAIv6LwU=&xsec_source=pc_collect",
        "https://www.xiaohongshu.com/explore/67e89dac000000001d0382c6?xsec_token=ABIz86rB8YD8u3DIsGwA51r-ZKAMn2F0ja-LR-mkyQz-4=&xsec_source=pc_collect",
        "https://www.xiaohongshu.com/explore/69b215f10000000026033cde?xsec_token=ABINNE_oPidQLZOKXpZLIpMMck67jugyHnrP5IthciXUQ=&xsec_source=pc_collect",
        "https://www.xiaohongshu.com/explore/69a5aea300000000220395ac?xsec_token=ABKIRuldqCZKSc6JOTrTWxqfD1c9dcL29qOul0QRM7C08=&xsec_source=pc_collect",
    ]

    for i, link in enumerate(test_cases, 1):
        pure = process_url(link)
        print(f"[{i}] 纯净链接：{pure}")
        print("-" * 110)