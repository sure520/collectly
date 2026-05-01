import type { ContentResponse, SearchQuery, PaginatedSearchResult, LearningStatusUpdate, TagUpdate, NoteUpdate } from './types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

export function getApiBaseUrl(): string {
  return API_BASE_URL;
}

export async function parseLink(url: string): Promise<ContentResponse> {
  const response = await fetch(`${API_BASE_URL}/parse-link`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url }),
  });
  
  if (!response.ok) {
    throw new Error('解析链接失败');
  }
  
  return response.json();
}

export async function parseLinks(urls: string[]): Promise<ContentResponse[]> {
  const response = await fetch(`${API_BASE_URL}/parse-links`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(urls.map(url => ({ url }))),
  });
  
  if (!response.ok) {
    throw new Error('批量解析链接失败');
  }
  
  return response.json();
}

export async function saveContent(content: ContentResponse): Promise<{ content_id: string; message: string }> {
  const response = await fetch(`${API_BASE_URL}/save-content`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(content),
  });
  
  if (!response.ok) {
    throw new Error('保存内容失败');
  }
  
  return response.json();
}

export async function search(query: SearchQuery): Promise<PaginatedSearchResult> {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(query),
  });
  
  if (!response.ok) {
    throw new Error('搜索失败');
  }
  
  return response.json();
}

export async function updateLearningStatus(contentId: string, status: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/update-learning-status`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ content_id: contentId, status }),
  });
  
  if (!response.ok) {
    throw new Error('更新学习状态失败');
  }
  
  return response.json();
}

export async function updateTags(contentId: string, tags: string[]): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/update-tags`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ content_id: contentId, tags }),
  });
  
  if (!response.ok) {
    throw new Error('更新标签失败');
  }
  
  return response.json();
}

export async function updateNote(contentId: string, note: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/update-note`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ content_id: contentId, note }),
  });
  
  if (!response.ok) {
    throw new Error('更新笔记失败');
  }
  
  return response.json();
}

export async function deleteContent(contentId: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/content/${contentId}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    throw new Error('删除内容失败');
  }
  
  return response.json();
}

export async function getContent(contentId: string): Promise<ContentResponse> {
  const response = await fetch(`${API_BASE_URL}/content/${contentId}`);
  
  if (!response.ok) {
    throw new Error('获取内容失败');
  }
  
  return response.json();
}

export async function getLearningStats(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/learning-stats`);
  
  if (!response.ok) {
    throw new Error('获取学习统计失败');
  }
  
  return response.json();
}

export async function getVectorStats(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/vector-stats`);
  
  if (!response.ok) {
    throw new Error('获取向量统计失败');
  }
  
  return response.json();
}

export async function reEmbedContent(contentId: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/re-embed/${contentId}`, {
    method: 'POST',
  });
  
  if (!response.ok) {
    throw new Error('重新嵌入失败');
  }
  
  return response.json();
}

export async function rebuildAllVectors(): Promise<{ message: string; success_count: number; total: number }> {
  const response = await fetch(`${API_BASE_URL}/rebuild-vectors`, {
    method: 'POST',
  });
  
  if (!response.ok) {
    throw new Error('重建向量失败');
  }
  
  return response.json();
}

export interface AppSettings {
  tikhub_api_key: string;
  dashscope_api_key: string;
  llm_model_name: string;
  asr_model_name: string;
  vision_model_name: string;
  embedding_model: string;
}

export async function getAppSettings(): Promise<AppSettings> {
  const response = await fetch(`${API_BASE_URL}/settings`);
  if (!response.ok) {
    throw new Error('获取设置失败');
  }
  return response.json();
}

export async function saveAppSettings(settings: AppSettings): Promise<AppSettings> {
  const response = await fetch(`${API_BASE_URL}/settings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings),
  });
  if (!response.ok) {
    throw new Error('保存设置失败');
  }
  return response.json();
}
