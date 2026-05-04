import type { ContentResponse, SearchQuery, PaginatedSearchResult, LearningStatusUpdate, TagUpdate, NoteUpdate } from './types';
import { getToken, clearToken } from './auth';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

let onUnauthorized: (() => void) | null = null;

export function setOnUnauthorizedHandler(handler: () => void) {
  onUnauthorized = handler;
}

function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (response.status === 401) {
    clearToken();
    if (onUnauthorized) onUnauthorized();
    throw new Error('认证已过期，请重新登录');
  }
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || `请求失败 (${response.status})`);
  }
  return response.json();
}

export function getApiBaseUrl(): string {
  return API_BASE_URL;
}

export async function cleanUrls(rawTexts: string[]): Promise<{ cleaned_url: string; is_valid: boolean }[]> {
  const response = await fetch(`${API_BASE_URL}/clean-urls`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ raw_texts: rawTexts }),
  });
  return handleResponse<{ cleaned_url: string; is_valid: boolean }[]>(response);
}

export async function parseLink(url: string): Promise<ContentResponse> {
  const response = await fetch(`${API_BASE_URL}/parse-link`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ url }),
  });
  return handleResponse<ContentResponse>(response);
}

export async function parseLinks(urls: string[]): Promise<ContentResponse[]> {
  const response = await fetch(`${API_BASE_URL}/parse-links`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(urls.map(url => ({ url }))),
  });
  return handleResponse<ContentResponse[]>(response);
}

export async function saveContent(content: ContentResponse): Promise<{ content_id: string; message: string }> {
  const response = await fetch(`${API_BASE_URL}/save-content`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(content),
  });
  return handleResponse<{ content_id: string; message: string }>(response);
}

export async function search(query: SearchQuery): Promise<PaginatedSearchResult> {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(query),
  });
  return handleResponse<PaginatedSearchResult>(response);
}

export async function updateLearningStatus(contentId: string, status: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/update-learning-status`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ content_id: contentId, status }),
  });
  return handleResponse<{ message: string }>(response);
}

export async function updateTags(contentId: string, tags: string[]): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/update-tags`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ content_id: contentId, tags }),
  });
  return handleResponse<{ message: string }>(response);
}

export async function updateNote(contentId: string, note: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/update-note`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ content_id: contentId, note }),
  });
  return handleResponse<{ message: string }>(response);
}

export async function deleteContent(contentId: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/content/${contentId}`, {
    method: 'DELETE',
    headers: { ...authHeaders() },
  });
  return handleResponse<{ message: string }>(response);
}

export async function getContent(contentId: string): Promise<ContentResponse> {
  const response = await fetch(`${API_BASE_URL}/content/${contentId}`, {
    headers: { ...authHeaders() },
  });
  return handleResponse<ContentResponse>(response);
}

export async function getLearningStats(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/learning-stats`, {
    headers: { ...authHeaders() },
  });
  return handleResponse<any>(response);
}

export async function getVectorStats(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/vector-stats`, {
    headers: { ...authHeaders() },
  });
  return handleResponse<any>(response);
}

export async function reEmbedContent(contentId: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/re-embed/${contentId}`, {
    method: 'POST',
    headers: { ...authHeaders() },
  });
  return handleResponse<{ message: string }>(response);
}

export async function rebuildAllVectors(): Promise<{ message: string; success_count: number; total: number }> {
  const response = await fetch(`${API_BASE_URL}/rebuild-vectors`, {
    method: 'POST',
    headers: { ...authHeaders() },
  });
  return handleResponse<{ message: string; success_count: number; total: number }>(response);
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
  const response = await fetch(`${API_BASE_URL}/settings`, {
    headers: { ...authHeaders() },
  });
  return handleResponse<AppSettings>(response);
}

export async function saveAppSettings(settings: AppSettings): Promise<AppSettings> {
  const response = await fetch(`${API_BASE_URL}/settings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(settings),
  });
  return handleResponse<AppSettings>(response);
}
