import type { Domain, ContentType, Difficulty, LearningStatus } from '../types';

export function getDomainName(domain: Domain): string {
  const names: Record<Domain, string> = {
    llm: '大模型',
    agent: 'Agent',
    rag: 'RAG',
    multimodal: '多模态',
  };
  return names[domain] || domain;
}

export function getContentTypeName(type: ContentType): string {
  const names: Record<ContentType, string> = {
    tutorial: '教程',
    review: '综述',
    practice: '实践',
    paper: '论文',
    interview: '面试',
    analysis: '解读',
  };
  return names[type] || type;
}

export function getDifficultyName(difficulty: Difficulty): string {
  const names: Record<Difficulty, string> = {
    beginner: '入门',
    intermediate: '进阶',
    advanced: '高阶',
    paper: '论文级',
  };
  return names[difficulty] || difficulty;
}

export function getDifficultyColor(difficulty: Difficulty): string {
  const colors: Record<Difficulty, string> = {
    beginner: '#22C55E',
    intermediate: '#3B82F6',
    advanced: '#F59E0B',
    paper: '#EF4444',
  };
  return colors[difficulty] || '#6B7280';
}

export function getStatusName(status: LearningStatus): string {
  const names: Record<LearningStatus, string> = {
    unread: '未读',
    read: '已读',
    important: '重点',
    review: '待复习',
  };
  return names[status] || status;
}

export function getStatusColor(status: LearningStatus): string {
  const colors: Record<LearningStatus, string> = {
    unread: '#9CA3AF',
    read: '#22C55E',
    important: '#EF4444',
    review: '#F59E0B',
  };
  return colors[status] || '#6B7280';
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (days === 0) {
    const hours = Math.floor(diff / (1000 * 60 * 60));
    if (hours === 0) {
      const minutes = Math.floor(diff / (1000 * 60));
      return minutes === 0 ? '刚刚' : `${minutes}分钟前`;
    }
    return `${hours}小时前`;
  }
  if (days === 1) return '昨天';
  if (days < 7) return `${days}天前`;
  if (days < 30) return `${Math.floor(days / 7)}周前`;

  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

export function timestampToDate(timestamp: string): string {
  // 将字符串时间戳转换为数字，然后转换为毫秒
  const date = new Date(parseInt(timestamp) * 1000);
  
  // 格式化为年月日格式
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
}
