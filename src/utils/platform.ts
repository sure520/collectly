import type { Platform } from '../types';

export function detectPlatform(url: string): Platform | null {
  const patterns: Record<Platform, RegExp> = {
    wechat: /mp\.weixin\.qq\.com/,
    zhihu: /zhihu\.com/,
    csdn: /csdn\.net/,
    bilibili: /bilibili\.com|b23\.tv/,
    douyin: /douyin\.com|iesdouyin\.com/,
    xiaohongshu: /xiaohongshu\.com|xhslink\.com/,
  };

  for (const [platform, pattern] of Object.entries(patterns)) {
    if (pattern.test(url)) {
      return platform as Platform;
    }
  }
  return null;
}

export function getPlatformName(platform: Platform): string {
  const names: Record<Platform, string> = {
    wechat: '微信公众号',
    zhihu: '知乎',
    csdn: 'CSDN',
    bilibili: '哔哩哔哩',
    douyin: '抖音',
    xiaohongshu: '小红书',
  };
  return names[platform] || platform;
}

export function getPlatformIcon(platform: Platform): string {
  const icons: Record<Platform, string> = {
    wechat: 'fa-brands fa-weixin',
    zhihu: 'fa-brands fa-zhihu',
    csdn: 'fa-solid fa-code',
    bilibili: 'fa-brands fa-bilibili',
    douyin: 'fa-brands fa-tiktok',
    xiaohongshu: 'fa-solid fa-book-open',
  };
  return icons[platform] || 'fa-solid fa-link';
}

export function getPlatformColor(platform: Platform): string {
  const colors: Record<Platform, string> = {
    wechat: '#07C160',
    zhihu: '#0084FF',
    csdn: '#FC5531',
    bilibili: '#00A1D6',
    douyin: '#000000',
    xiaohongshu: '#FF2442',
  };
  return colors[platform] || '#666666';
}
