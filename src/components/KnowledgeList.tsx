import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Grid3X3, List, ExternalLink, Bookmark, Clock, Tag } from 'lucide-react';
import type { KnowledgeItem, ViewMode, SortBy, LearningStatus } from '../types';
import { getPlatformName, getPlatformIcon, getPlatformColor } from '../utils/platform';
import { getDomainName, getDifficultyName, getDifficultyColor, getStatusName, getStatusColor, formatDate, truncateText } from '../utils/format';
import { Pagination } from './Pagination';

interface KnowledgeListProps {
  items: KnowledgeItem[];
  onItemClick: (item: KnowledgeItem) => void;
  onStatusChange: (id: string, status: LearningStatus) => void;
  page?: number;
  pageSize?: number;
  total?: number;
  totalPages?: number;
  onPageChange?: (page: number) => void;
  onPageSizeChange?: (pageSize: number) => void;
}

export function KnowledgeList({ items, onItemClick, onStatusChange, page, pageSize, total, totalPages, onPageChange, onPageSizeChange }: KnowledgeListProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [sortBy, setSortBy] = useState<SortBy>('created_at');

  const sortedItems = [...items].sort((a, b) => {
    if (sortBy === 'created_at') return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    if (sortBy === 'publish_time') return new Date(b.publish_time).getTime() - new Date(a.publish_time).getTime();
    return 0;
  });

  const showPagination = page !== undefined && total !== undefined && total > 0;

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-5 px-4">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium" style={{ color: 'var(--text-mid)' }}>共 {total ?? items.length} 条</span>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortBy)}
            className="text-sm px-3 py-1.5 rounded-xl font-medium"
            style={{ backgroundColor: 'var(--surface)', border: '1.5px solid var(--border)', color: 'var(--text-mid)', outline: 'none' }}
          >
            <option value="created_at">按收藏时间</option>
            <option value="publish_time">按发布时间</option>
          </select>
          <div className="flex items-center gap-1 p-1 rounded-xl" style={{ backgroundColor: 'var(--bg)' }}>
            <button
              onClick={() => setViewMode('grid')}
              className="p-1.5 rounded-lg transition-all"
              style={viewMode === 'grid' ? { backgroundColor: 'var(--surface)', color: 'var(--accent)', boxShadow: '0 1px 3px var(--shadow)' } : { color: 'var(--text-light)' }}
            >
              <Grid3X3 size={16} />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className="p-1.5 rounded-lg transition-all"
              style={viewMode === 'list' ? { backgroundColor: 'var(--surface)', color: 'var(--accent)', boxShadow: '0 1px 3px var(--shadow)' } : { color: 'var(--text-light)' }}
            >
              <List size={16} />
            </button>
          </div>
        </div>
      </div>

      <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 px-4' : 'flex flex-col gap-3 px-4'}>
        {sortedItems.map((item, index) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            onClick={() => onItemClick(item)}
            className={`rounded-xl p-6 card-hover cursor-pointer ${viewMode === 'list' ? 'flex items-center gap-4' : ''}`}
            style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}
          >
            <div className={`${viewMode === 'list' ? 'flex-1' : ''}`}>
              <div className="flex items-start justify-between gap-2 mb-3">
                <div className="flex items-center gap-2.5">
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: `${getPlatformColor(item.platform)}12` }}
                  >
                    <i className={`${getPlatformIcon(item.platform)} text-sm`} style={{ color: getPlatformColor(item.platform) }} />
                  </div>
                  <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-light)' }}>{getPlatformName(item.platform)}</span>
                </div>
                <span className="text-xs px-2.5 py-1 rounded-full font-semibold" style={{ backgroundColor: getStatusColor(item.status) + '15', color: getStatusColor(item.status) }}>
                  {getStatusName(item.status)}
                </span>
              </div>

              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="serif text-base font-semibold block mb-3 leading-snug"
                style={{ color: 'var(--text)', letterSpacing: '-0.2px' }}
              >
                {item.title}
              </a>

              <p className="text-sm mb-4" style={{ color: 'var(--text-mid)', lineHeight: '1.7' }}>{truncateText(item.short_summary, 80)}</p>

              <div className="flex items-center gap-1.5 mb-4">
                <span className="text-xs px-2.5 py-1 rounded-full font-semibold" style={{ backgroundColor: `${getDifficultyColor(item.difficulty)}15`, color: getDifficultyColor(item.difficulty) }}>
                  {getDifficultyName(item.difficulty)}
                </span>
                {item.domains.slice(0, 2).map((domain) => (
                  <span key={domain} className="text-xs px-2.5 py-1 rounded-full font-semibold" style={{ backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent-dark)' }}>
                    {getDomainName(domain)}
                  </span>
                ))}
              </div>

              <div className="flex items-center justify-between text-xs font-medium" style={{ color: 'var(--text-light)' }}>
                <div className="flex items-center gap-3">
                  <span className="flex items-center gap-1">
                    <Clock size={12} />
                    {formatDate(item.created_at)}
                  </span>
                  <span>{item.author}</span>
                </div>
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="flex items-center gap-1 font-semibold transition-colors"
                  style={{ color: 'var(--accent)' }}
                >
                  <ExternalLink size={12} />
                  原文
                </a>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {showPagination && page && total && totalPages && onPageChange && (
        <div className="mt-5">
          <Pagination
            page={page}
            pageSize={pageSize || 20}
            total={total}
            totalPages={totalPages}
            onPageChange={onPageChange}
            onPageSizeChange={onPageSizeChange}
          />
        </div>
      )}

      {items.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16" style={{ color: 'var(--text-light)' }}>
          <Bookmark size={48} className="mb-4" style={{ opacity: 0.3 }} />
          <p className="text-sm">暂无收藏内容</p>
          <p className="text-xs mt-1" style={{ color: 'var(--text-light)', opacity: 0.7 }}>快去添加你的第一条知识吧</p>
        </div>
      )}
    </div>
  );
}
