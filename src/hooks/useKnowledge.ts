import { useState, useEffect, useCallback, useRef } from 'react';
import * as api from '../utils/api';
import type { ContentResponse, SearchQuery as ApiSearchQuery } from '../utils/types';
import type { KnowledgeItem, SearchFilters, UserStats, Platform, Domain, Difficulty, ContentType, LearningStatus } from '../types';

const MAX_RETRIES = 3;
const RETRY_DELAY = 1000;

export function useKnowledge(userId: string | undefined) {
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [parseError, setParseError] = useState<string | null>(null);

  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const lastFiltersRef = useRef<SearchFilters | undefined>(undefined);
  const lastQueryRef = useRef<string | undefined>(undefined);
  const lastSemanticRef = useRef<{ query: string; filters?: SearchFilters } | null>(null);

  const domainMap: Record<string, Domain> = {
    '大模型': 'llm',
    'Agent': 'agent',
    'RAG': 'rag',
    '多模态': 'multimodal',
  };

  const difficultyMap: Record<string, Difficulty> = {
    '入门': 'beginner',
    '进阶': 'intermediate',
    '高阶': 'advanced',
    '论文级': 'paper',
  };

  const contentTypeMap: Record<string, ContentType> = {
    '教程': 'tutorial',
    '综述': 'review',
    '实践': 'practice',
    '论文': 'paper',
    '面试': 'interview',
    '解读': 'analysis',
  };

  const platformMap: Record<string, Platform> = {
    '抖音': 'douyin',
    '小红书': 'xiaohongshu',
    '微信公众号': 'wechat',
    'B站': 'bilibili',
    '知乎': 'zhihu',
    'CSDN': 'csdn',
  };

  const mapDomainToTag = (domain: Domain): string => {
    const reverseMap: Record<Domain, string> = {
      'llm': '大模型',
      'agent': 'Agent',
      'rag': 'RAG',
      'multimodal': '多模态',
    };
    return reverseMap[domain] || '';
  };

  const formatItems = (results: any[]): KnowledgeItem[] => {
    return results.map(item => ({
      id: item.content_id,
      title: item.title,
      content: '',
      short_summary: item.short_summary || item.summary || '',
      long_summary: item.long_summary || item.summary || '',
      author: item.author,
      platform: (platformMap[item.source] || 'zhihu') as Platform,
      status: (item.learning_status === '未读' ? 'unread' : item.learning_status === '已读' ? 'read' : item.learning_status === '重点' ? 'important' : 'review') as LearningStatus,
      domains: item.tags.filter((tag: string) => domainMap[tag]).map((tag: string) => domainMap[tag]),
      difficulty: item.tags.find((tag: string) => difficultyMap[tag]) ? difficultyMap[item.tags.find((tag: string) => difficultyMap[tag])!] : 'beginner',
      content_type: item.tags.find((tag: string) => contentTypeMap[tag]) ? contentTypeMap[item.tags.find((tag: string) => contentTypeMap[tag])!] : 'tutorial',
      key_points: item.knowledge_points,
      tags: item.tags,
      url: item.url || '',
      publish_time: item.update,
      created_at: item.create_time,
      updated_at: item.update,
      is_deleted: false,
      user_id: userId || '',
    }));
  };

  const fetchItems = useCallback(async (filters?: SearchFilters, searchQuery?: string, currentPage?: number, currentPageSize?: number) => {
    const p = currentPage ?? page;
    const ps = currentPageSize ?? pageSize;

    lastFiltersRef.current = filters;
    lastQueryRef.current = searchQuery;
    lastSemanticRef.current = null;

    setLoading(true);

    try {
      const apiQuery: ApiSearchQuery = {
        text: searchQuery || '',
        domains: filters?.domains?.map(d => mapDomainToTag(d)),
        sources: filters?.platforms?.map(p => p),
        difficulty: filters?.difficulty?.[0],
        content_type: filters?.contentTypes?.[0],
        start_date: filters?.startDate,
        end_date: filters?.endDate,
        learning_status: filters?.status?.[0],
        page: p,
        page_size: ps,
      };

      const result = await api.search(apiQuery);

      setItems(formatItems(result.items));
      setTotal(result.total);
      setTotalPages(result.total_pages);
      setPage(result.page);
    } catch (error) {
      console.error('Error fetching items:', error);
    } finally {
      setLoading(false);
    }
  }, [userId, page, pageSize]);

  const fetchStats = useCallback(async () => {
    try {
      const statsData = await api.getLearningStats();
      
      const domainStats: Record<Domain, number> = {
        llm: 0,
        agent: 0,
        rag: 0,
        multimodal: 0,
      };
      
      if (statsData.domain_counts) {
        Object.entries(statsData.domain_counts).forEach(([key, value]) => {
          if (domainMap[key] && typeof value === 'number') {
            domainStats[domainMap[key]] = value;
          }
        });
      }
      
      setStats({
        total_count: statsData.total_count || 0,
        unread_count: statsData.status_counts?.未读 || 0,
        read_count: statsData.status_counts?.已读 || 0,
        important_count: statsData.status_counts?.重点 || 0,
        domain_stats: domainStats,
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  }, []);

  const parseAndAddItem = useCallback(async (url: string, platform: string) => {
    setParseError(null);

    try {
      const content = await api.parseLink(url);
      const saveResult = await api.saveContent(content);
      
      const newItem: KnowledgeItem = {
        id: saveResult.content_id,
        title: content.title,
        content: '',
        short_summary: content.short_summary || '',
        long_summary: content.long_summary || '',
        author: content.author,
        platform: (platformMap[content.source] || 'zhihu') as Platform,
        status: 'unread',
        domains: content.tags.filter(tag => domainMap[tag]).map(tag => domainMap[tag]),
        difficulty: content.tags.find(tag => difficultyMap[tag]) ? difficultyMap[content.tags.find(tag => difficultyMap[tag])!] : 'beginner',
        content_type: content.tags.find(tag => contentTypeMap[tag]) ? contentTypeMap[content.tags.find(tag => contentTypeMap[tag])!] : 'tutorial',
        key_points: content.knowledge_points,
        tags: content.tags,
        url: content.url,
        publish_time: content.update,
        created_at: content.create_time,
        updated_at: content.update,
        is_deleted: false,
        user_id: userId || '',
      };

      setItems(prev => [newItem, ...prev]);
      setTotal(prev => prev + 1);
      fetchStats();

      return { data: newItem, error: null };
    } catch (err: any) {
      console.error('[DEBUG] Parse error:', err);
      setParseError(err.message || '解析失败');
      return { data: null, error: err };
    }
  }, [userId, fetchStats]);

  const semanticSearch = useCallback(async (query: string, filters?: SearchFilters, currentPage?: number, currentPageSize?: number) => {
    const p = currentPage ?? 1;
    const ps = currentPageSize ?? pageSize;

    lastSemanticRef.current = { query, filters };
    lastFiltersRef.current = undefined;
    lastQueryRef.current = undefined;

    try {
      const apiQuery: ApiSearchQuery = {
        text: query,
        domains: filters?.domains?.map(d => mapDomainToTag(d)),
        sources: filters?.platforms?.map(p => p),
        difficulty: filters?.difficulty?.[0],
        content_type: filters?.contentTypes?.[0],
        start_date: filters?.startDate,
        end_date: filters?.endDate,
        learning_status: filters?.status?.[0],
        page: p,
        page_size: ps,
      };

      const result = await api.search(apiQuery);

      setItems(formatItems(result.items));
      setTotal(result.total);
      setTotalPages(result.total_pages);
      setPage(result.page);

      return { data: formatItems(result.items), error: null };
    } catch (error) {
      console.error('Error in semantic search:', error);
      return { data: [], error };
    }
  }, [userId, pageSize]);

  const goToPage = useCallback((newPage: number) => {
    setPage(newPage);
    if (lastSemanticRef.current) {
      const { query, filters } = lastSemanticRef.current;
      semanticSearch(query, filters, newPage, pageSize);
    } else {
      fetchItems(lastFiltersRef.current, lastQueryRef.current, newPage, pageSize);
    }
  }, [fetchItems, semanticSearch, pageSize]);

  const changePageSize = useCallback((newPageSize: number) => {
    setPageSize(newPageSize);
    setPage(1);
    if (lastSemanticRef.current) {
      const { query, filters } = lastSemanticRef.current;
      semanticSearch(query, filters, 1, newPageSize);
    } else {
      fetchItems(lastFiltersRef.current, lastQueryRef.current, 1, newPageSize);
    }
  }, [fetchItems, semanticSearch]);

  const updateItem = useCallback(async (id: string, updates: Partial<KnowledgeItem>) => {
    try {
      if (updates.status) {
        const statusMap: Record<LearningStatus, string> = {
          unread: '未读',
          read: '已读',
          important: '重点',
          review: '待复习',
        };
        await api.updateLearningStatus(id, statusMap[updates.status]);
      }
      
      if (updates.domains || updates.difficulty || updates.content_type || updates.tags) {
        const tags = [
          ...(updates.domains?.map(d => mapDomainToTag(d)) || []),
          updates.difficulty ? difficultyMap[updates.difficulty] : '',
          updates.content_type ? contentTypeMap[updates.content_type] : '',
          ...(updates.tags || []),
        ].filter((tag): tag is string => tag !== '');
        await api.updateTags(id, tags);
      }
      
      if (updates.long_summary) {
        await api.updateNote(id, updates.long_summary);
      }
      
      fetchStats();
      return { data: null, error: null };
    } catch (error) {
      console.error('Error updating item:', error);
      return { data: null, error };
    }
  }, [fetchStats]);

  const deleteItem = useCallback(async (id: string) => {
    try {
      await api.deleteContent(id);
      setItems(prev => prev.filter(item => item.id !== id));
      setTotal(prev => prev - 1);
      fetchStats();
      return { error: null };
    } catch (error) {
      console.error('Error deleting item:', error);
      return { error };
    }
  }, [fetchStats]);

  useEffect(() => {
    fetchItems();
    fetchStats();
  }, []);

  return {
    items,
    stats,
    loading,
    parseError,
    page,
    pageSize,
    total,
    totalPages,
    fetchItems,
    fetchStats,
    parseAndAddItem,
    semanticSearch,
    updateItem,
    deleteItem,
    goToPage,
    changePageSize,
  };
}
