// 链接输入类型
export interface LinkInput {
  url: string;
}

// 内容响应类型
export interface ContentResponse {
  title: string;
  content: string;
  author: string;
  update: string;
  create_time: string;
  url: string;
  source: string;
  tags: string[];
  knowledge_points: string[];
  summary: string;
}

// 搜索查询类型
export interface SearchQuery {
  text: string;
  domains?: string[];
  sources?: string[];
  difficulty?: string;
  content_type?: string;
  start_date?: string;
  end_date?: string;
  learning_status?: string;
}

// 搜索结果类型
export interface SearchResult {
  content_id: string;
  title: string;
  summary: string;
  author: string;
  source: string;
  update: string;
  create_time: string;
  tags: string[];
  knowledge_points: string[];
  learning_status: string;
  relevance_score: number;
  url?: string;
}

// 学习状态更新类型
export interface LearningStatusUpdate {
  content_id: string;
  status: string;
}

// 标签更新类型
export interface TagUpdate {
  content_id: string;
  tags: string[];
}

// 笔记更新类型
export interface NoteUpdate {
  content_id: string;
  note: string;
}