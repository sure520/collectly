import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const MEOO_PROJECT_API_KEY = Deno.env.get('MEOO_PROJECT_API_KEY') || '';
const DASHSCOPE_BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1';

interface ParseResult {
  title: string;
  author: string;
  publishTime: string;
  content: string;
  shortSummary: string;
  longSummary: string;
  domains: string[];
  contentType: string;
  difficulty: string;
  keyPoints: string[];
  tags: string[];
}

interface ModelConfig {
  text?: string;
  vision?: string;
  audio?: string;
  default?: string;
}

function getPlatformModality(platform: string): 'text' | 'vision' | 'audio' {
  const visionPlatforms = ['bilibili', 'douyin', 'xiaohongshu', 'youtube', 'tiktok'];
  const audioPlatforms = ['podcast', 'audio', 'music'];
  
  if (visionPlatforms.includes(platform)) return 'vision';
  if (audioPlatforms.includes(platform)) return 'audio';
  return 'text';
}

function selectModel(platform: string, modelConfig: ModelConfig): string {
  const modality = getPlatformModality(platform);
  
  if (modality === 'vision' && modelConfig.vision) return modelConfig.vision;
  if (modality === 'audio' && modelConfig.audio) return modelConfig.audio;
  if (modelConfig.text) return modelConfig.text;
  if (modelConfig.default) return modelConfig.default;
  
  return 'qwen-max';
}

async function analyzeUrlWithLLM(url: string, platform: string, apiKey: string, model: string): Promise<ParseResult> {
  const prompt = `请分析以下${platform}平台的链接，提取关键信息并以JSON格式返回：

链接：${url}

请返回以下格式的JSON：
{
  "title": "内容标题",
  "author": "作者名称",
  "content": "内容摘要或描述",
  "shortSummary": "一句话总结",
  "longSummary": "详细内容摘要（100-200字）",
  "domains": ["领域标签，如llm, ai, frontend等"],
  "contentType": "内容类型：article/tutorial/video/news/other",
  "difficulty": "难度：beginner/intermediate/advanced",
  "keyPoints": ["关键要点1", "关键要点2"],
  "tags": ["标签1", "标签2", "标签3"]
}

请基于链接特征和平台类型进行合理推断，给出尽可能详细和准确的信息。`;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);

  try {
    const response = await fetch(`${DASHSCOPE_BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: model,
        messages: [
          { role: 'system', content: '你是一个内容分析助手，擅长从链接中提取和推断内容信息。' },
          { role: 'user', content: prompt }
        ],
        temperature: 0.7,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`LLM API error: ${response.status} - ${errorText}`);
    }

    const result = await response.json();
    const content = result.choices?.[0]?.message?.content;

    if (!content) {
      throw new Error('LLM returned empty content');
    }

    const jsonMatch = content.match(/\{[\s\S]*\}/);
    const jsonStr = jsonMatch ? jsonMatch[0] : content;
    const parsed = JSON.parse(jsonStr);

    return {
      title: parsed.title || `内容来自 ${platform}`,
      author: parsed.author || '未知作者',
      publishTime: new Date().toISOString(),
      content: parsed.content || `链接: ${url}`,
      shortSummary: parsed.shortSummary || '暂无摘要',
      longSummary: parsed.longSummary || '暂无详细摘要',
      domains: Array.isArray(parsed.domains) ? parsed.domains : ['general'],
      contentType: parsed.contentType || 'article',
      difficulty: parsed.difficulty || 'intermediate',
      keyPoints: Array.isArray(parsed.keyPoints) ? parsed.keyPoints : [],
      tags: Array.isArray(parsed.tags) ? parsed.tags : [platform],
    };
  } catch (error: any) {
    if (error.name === 'AbortError') {
      throw new Error('LLM request timeout');
    }
    if (error.message.includes('JSON')) {
      return {
        title: `内容来自 ${platform}`,
        author: '未知作者',
        publishTime: new Date().toISOString(),
        content: `链接: ${url}`,
        shortSummary: 'AI技术内容摘要',
        longSummary: '无法解析详细内容',
        domains: ['general'],
        contentType: 'article',
        difficulty: 'intermediate',
        keyPoints: [],
        tags: [platform],
      };
    }
    throw error;
  }
}

Deno.serve(async (req) => {
  const corsHeaders = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  };

  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const body = await req.json();
    const { url, platform, userId, apiKey: userApiKey, modelConfig } = body;

    console.log('[EdgeFunction] Received request:', { url, platform, userId, hasUserApiKey: !!userApiKey, hasModelConfig: !!modelConfig });

    if (!url || !platform || !userId) {
      return new Response(
        JSON.stringify({ error: 'Missing required fields', details: { url, platform, userId } }),
        { status: 400, headers: corsHeaders }
      );
    }

    const apiKey = userApiKey || MEOO_PROJECT_API_KEY;
    
    if (!apiKey) {
      throw new Error('API Key not configured. Please provide your API Key in settings.');
    }

    const model = selectModel(platform, modelConfig || {});
    
    console.log('[EdgeFunction] Platform:', platform, 'Modality:', getPlatformModality(platform), 'Selected model:', model);
    console.log('[EdgeFunction] Calling LLM...');
    
    const parseResult = await analyzeUrlWithLLM(url, platform, apiKey, model);
    console.log('[EdgeFunction] LLM result:', parseResult);

    const supabaseUrl = Deno.env.get('SUPABASE_URL');
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
    
    if (!supabaseUrl || !supabaseKey) {
      throw new Error('Supabase credentials not configured');
    }
    
    const supabaseAdmin = createClient(supabaseUrl, supabaseKey);

    console.log('[EdgeFunction] Inserting to database...');
    const { data: item, error: insertError } = await supabaseAdmin
      .from('knowledge_items')
      .insert({
        user_id: userId,
        platform,
        url,
        title: parseResult.title,
        author: parseResult.author,
        publish_time: parseResult.publishTime,
        content: parseResult.content,
        short_summary: parseResult.shortSummary,
        long_summary: parseResult.longSummary,
        domains: parseResult.domains,
        content_type: parseResult.contentType,
        difficulty: parseResult.difficulty,
        key_points: parseResult.keyPoints,
        tags: parseResult.tags,
        status: 'unread',
        is_deleted: false,
      })
      .select()
      .single();

    if (insertError) {
      throw new Error(`Database insert failed: ${insertError.message}`);
    }

    console.log('[EdgeFunction] Success:', item.id);
    return new Response(
      JSON.stringify({ success: true, data: item }),
      { headers: corsHeaders }
    );
  } catch (error: any) {
    console.error('[EdgeFunction] Error:', error.message);
    return new Response(
      JSON.stringify({ error: error.message, stack: error.stack }),
      { status: 500, headers: corsHeaders }
    );
  }
});
