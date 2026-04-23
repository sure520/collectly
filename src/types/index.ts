export type Platform = 'wechat' | 'zhihu' | 'csdn' | 'bilibili' | 'douyin' | 'xiaohongshu';

export type Domain = 'llm' | 'agent' | 'rag' | 'multimodal';

export type ContentType = 'tutorial' | 'review' | 'practice' | 'paper' | 'interview' | 'analysis';

export type Difficulty = 'beginner' | 'intermediate' | 'advanced' | 'paper';

export type LearningStatus = 'unread' | 'read' | 'important' | 'review';

export interface KnowledgeItem {
  id: string;
  user_id: string;
  platform: Platform;
  url: string;
  title: string;
  author: string;
  publish_time: string;
  content: string;
  short_summary: string;
  long_summary: string;
  domains: Domain[];
  content_type: ContentType;
  difficulty: Difficulty;
  key_points: string[];
  tags: string[];
  status: LearningStatus;
  is_deleted: boolean;
  note?: string;
  created_at: string;
  updated_at: string;
}

export interface SearchFilters {
  domains?: Domain[];
  platforms?: Platform[];
  difficulty?: Difficulty[];
  contentTypes?: ContentType[];
  status?: LearningStatus[];
  startDate?: string;
  endDate?: string;
}

export interface UserProfile {
  id: string;
  email: string;
  nickname: string;
  avatar_url: string;
  created_at: string;
}

export interface UserStats {
  total_count: number;
  unread_count: number;
  read_count: number;
  important_count: number;
  domain_stats: Record<Domain, number>;
}

export interface ParseResult {
  platform: Platform;
  title: string;
  author: string;
  publish_time: string;
  content: string;
  cover_image?: string;
}

export interface LinkInputForm {
  urls: string[];
}

export type ViewMode = 'grid' | 'list';

export type SortBy = 'relevance' | 'created_at' | 'publish_time';
