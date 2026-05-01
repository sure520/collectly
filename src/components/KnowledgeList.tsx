import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Grid3X3, List, ExternalLink, Bookmark, Clock, Tag } from 'lucide-react';
import type { KnowledgeItem, ViewMode, SortBy, LearningStatus } from '../types';
import { getPlatformName, getPlatformIcon, getPlatformColor } from '../utils/platform';
import { getDifficultyName, getDifficultyColor, getStatusName, getStatusColor, formatDate, truncateText } from '../utils/format';
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
    if (sortBy === 'created_at') {
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    }
    if (sortBy === 'publish_time') {
      return new Date(b.publish_time).getTime() - new Date(a.publish_time).getTime();
    }
    return 0;
  });

  const showPagination = page !== undefined && total !== undefined && total > 0;

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-4 px-4">
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">共 {total ?? items.length} 条</span>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortBy)}
            className="text-sm px-3 py-1.5 rounded-lg border border-gray-200 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="created_at">按收藏时间</option>
            <option value="publish_time">按发布时间</option>
          </select>
          <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-md transition-colors ${viewMode === 'grid' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'}`}
            >
              <Grid3X3 size={16} className={viewMode === 'grid' ? 'text-blue-600' : 'text-gray-500'} />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-md transition-colors ${viewMode === 'list' ? 'bg-white shadow-sm' : 'hover:bg-gray-200'}`}
            >
              <List size={16} className={viewMode === 'list' ? 'text-blue-600' : 'text-gray-500'} />
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
            className={`bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all cursor-pointer overflow-hidden ${viewMode === 'list' ? 'flex items-center gap-4 p-4' : 'p-4'}`}
          >
            <div className={`${viewMode === 'list' ? 'flex-1' : ''}`}>
              <div className="flex items-start justify-between gap-2 mb-2">
                <div className="flex items-center gap-2">
                  <i className={`${getPlatformIcon(item.platform)} text-lg`} style={{ color: getPlatformColor(item.platform) }} />
                  <span className="text-xs text-gray-500">{getPlatformName(item.platform)}</span>
                </div>
                <span
                  className="text-xs px-2 py-0.5 rounded-full font-medium"
                  style={{ backgroundColor: getStatusColor(item.status) + '20', color: getStatusColor(item.status) }}
                >
                  {getStatusName(item.status)}
                </span>
              </div>

              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="block font-semibold text-blue-600 hover:text-blue-800 mb-2 line-clamp-2 transition-colors"
              >
                {item.title}
              </a>

              <p className="text-sm text-gray-600 mb-3 line-clamp-2">{item.short_summary}</p>

              <div className="flex items-center gap-2 mb-3">
                <span
                  className="text-xs px-2 py-0.5 rounded-full"
                  style={{ backgroundColor: getDifficultyColor(item.difficulty) + '20', color: getDifficultyColor(item.difficulty) }}
                >
                  {getDifficultyName(item.difficulty)}
                </span>
                {item.domains.slice(0, 2).map((domain) => (
                  <span key={domain} className="text-xs px-2 py-0.5 rounded-full bg-blue-50 text-blue-600">
                    {domain}
                  </span>
                ))}
              </div>

              <div className="flex items-center justify-between text-xs text-gray-400">
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
                  className="flex items-center gap-1 text-blue-600 hover:text-blue-700"
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
        <div className="mt-4">
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
        <div className="flex flex-col items-center justify-center py-16 text-gray-400">
          <Bookmark size={48} className="mb-4 opacity-50" />
          <p>暂无收藏内容</p>
          <p className="text-sm mt-1">快去添加你的第一条知识吧</p>
        </div>
      )}
    </div>
  );
}
