import type { ContentResponse, SearchQuery, SearchResult, LearningStatusUpdate, TagUpdate, NoteUpdate } from './types';

const API_BASE_URL = 'http://localhost:8000/api';

// 解析链接
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

// 批量解析链接
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

// 保存内容
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

// 搜索内容
export async function search(query: SearchQuery): Promise<SearchResult[]> {
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

// 更新学习状态
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

// 更新标签
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

// 更新笔记
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

// 获取内容详情
export async function getContent(contentId: string): Promise<ContentResponse> {
  const response = await fetch(`${API_BASE_URL}/content/${contentId}`);
  
  if (!response.ok) {
    throw new Error('获取内容详情失败');
  }
  
  return response.json();
}

// 获取学习统计
export async function getLearningStats(): Promise<Record<string, any>> {
  const response = await fetch(`${API_BASE_URL}/learning-stats`);
  
  if (!response.ok) {
    throw new Error('获取学习统计失败');
  }
  
  return response.json();
}