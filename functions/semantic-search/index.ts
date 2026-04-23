import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const DASHSCOPE_API_KEY = Deno.env.get('DASHSCOPE_API_KEY') || '';
const DASHSCOPE_BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1';

interface SearchRequest {
  query: string;
  userId: string;
  filters?: {
    domains?: string[];
    platforms?: string[];
    difficulty?: string[];
    contentTypes?: string[];
    status?: string[];
  };
}

async function generateEmbedding(text: string): Promise<number[]> {
  const response = await fetch(`${DASHSCOPE_BASE_URL}/embeddings`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${DASHSCOPE_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'text-embedding-v2',
      input: text,
    }),
  });

  if (!response.ok) {
    throw new Error(`Embedding API error: ${response.status}`);
  }

  const data = await response.json();
  return data.data[0]?.embedding || [];
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
      },
    });
  }

  const corsHeaders = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  };

  try {
    const { query, userId, filters }: SearchRequest = await req.json();

    if (!query || !userId) {
      return new Response(
        JSON.stringify({ error: 'Missing required fields' }),
        { status: 400, headers: corsHeaders }
      );
    }

    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    );

    const queryEmbedding = await generateEmbedding(query);

    if (queryEmbedding.length === 0) {
      return new Response(
        JSON.stringify({ error: 'Failed to generate embedding' }),
        { status: 500, headers: corsHeaders }
      );
    }

    const embeddingString = `[${queryEmbedding.join(',')}]`;

    let sql = `
      SELECT 
        ki.*,
        kv.embedding <=> '${embeddingString}'::vector as distance
      FROM knowledge_items ki
      JOIN knowledge_vectors kv ON ki.id = kv.knowledge_item_id
      WHERE ki.user_id = '${userId}'
        AND ki.is_deleted = false
    `;

    if (filters?.domains?.length) {
      sql += ` AND ki.domains && ARRAY[${filters.domains.map(d => `'${d}'`).join(',')}]`;
    }
    if (filters?.platforms?.length) {
      sql += ` AND ki.platform IN (${filters.platforms.map(p => `'${p}'`).join(',')})`;
    }
    if (filters?.difficulty?.length) {
      sql += ` AND ki.difficulty IN (${filters.difficulty.map(d => `'${d}'`).join(',')})`;
    }
    if (filters?.contentTypes?.length) {
      sql += ` AND ki.content_type IN (${filters.contentTypes.map(t => `'${t}'`).join(',')})`;
    }
    if (filters?.status?.length) {
      sql += ` AND ki.status IN (${filters.status.map(s => `'${s}'`).join(',')})`;
    }

    sql += ` ORDER BY distance ASC LIMIT 20`;

    const { data: results, error } = await supabaseAdmin.rpc('semantic_search', {
      query_embedding: embeddingString,
      user_id: userId,
      match_threshold: 0.7,
      match_count: 20,
    });

    if (error) {
      const { data: fallbackResults, error: fallbackError } = await supabaseAdmin
        .from('knowledge_items')
        .select('*')
        .eq('user_id', userId)
        .eq('is_deleted', false)
        .or(`title.ilike.%${query}%,short_summary.ilike.%${query}%,content.ilike.%${query}%`)
        .order('created_at', { ascending: false })
        .limit(20);

      if (fallbackError) {
        throw new Error(`Search error: ${fallbackError.message}`);
      }

      return new Response(
        JSON.stringify({ success: true, data: fallbackResults || [], mode: 'keyword' }),
        { headers: corsHeaders }
      );
    }

    return new Response(
      JSON.stringify({ success: true, data: results || [], mode: 'semantic' }),
      { headers: corsHeaders }
    );
  } catch (error: any) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: corsHeaders }
    );
  }
});
