import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Filter } from 'lucide-react';
import type { Domain, Platform, Difficulty, ContentType, LearningStatus, SearchFilters } from '../types';
import { getDomainName, getContentTypeName, getDifficultyName, getStatusName } from '../utils/format';
import { getPlatformName } from '../utils/platform';

interface FilterPanelProps {
  filters: SearchFilters;
  onChange: (filters: SearchFilters) => void;
}

const DOMAINS: Domain[] = ['llm', 'agent', 'rag', 'multimodal'];
const PLATFORMS: Platform[] = ['wechat', 'zhihu', 'csdn', 'bilibili', 'douyin', 'xiaohongshu'];
const DIFFICULTIES: Difficulty[] = ['beginner', 'intermediate', 'advanced', 'paper'];
const CONTENT_TYPES: ContentType[] = ['tutorial', 'review', 'practice', 'paper', 'interview', 'analysis'];
const STATUSES: LearningStatus[] = ['unread', 'read', 'important', 'review'];

export default function FilterPanel({ filters, onChange }: FilterPanelProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const updateFilter = (key: keyof SearchFilters, value: any) => {
    onChange({ ...filters, [key]: value });
  };

  const toggleArrayFilter = (current: any[] | undefined, value: any) => {
    const arr = current || [];
    return arr.includes(value) ? arr.filter(v => v !== value) : [...arr, value];
  };

  const hasActiveFilters = Object.values(filters).some(v => v && (Array.isArray(v) ? v.length > 0 : true));

  return (
    <div className="glass-card">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-white/5 transition-colors rounded-xl"
      >
        <div className="flex items-center gap-2">
          <Filter size={18} className="text-blue-400" />
          <span className="font-medium text-white">筛选条件</span>
          {hasActiveFilters && (
            <span className="px-2 py-0.5 bg-blue-500/20 text-blue-400 text-xs rounded-full">
              已启用
            </span>
          )}
        </div>
        <ChevronDown
          size={18}
          className={`text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
        />
      </button>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-300 mb-2 block">领域</label>
                <div className="flex flex-wrap gap-2">
                  {DOMAINS.map(d => (
                    <button
                      key={d}
                      onClick={() => updateFilter('domains', toggleArrayFilter(filters.domains, d))}
                      className={`px-3 py-1.5 text-sm rounded-xl transition-all ${
                        filters.domains?.includes(d)
                          ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                          : 'bg-white/5 text-gray-400 border border-white/5 hover:bg-white/10 hover:text-gray-200'
                      }`}
                    >
                      {getDomainName(d)}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-300 mb-2 block">来源平台</label>
                <div className="flex flex-wrap gap-2">
                  {PLATFORMS.map(p => (
                    <button
                      key={p}
                      onClick={() => updateFilter('platforms', toggleArrayFilter(filters.platforms, p))}
                      className={`px-3 py-1.5 text-sm rounded-xl transition-all ${
                        filters.platforms?.includes(p)
                          ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                          : 'bg-white/5 text-gray-400 border border-white/5 hover:bg-white/10 hover:text-gray-200'
                      }`}
                    >
                      {getPlatformName(p)}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-300 mb-2 block">难度</label>
                <div className="flex flex-wrap gap-2">
                  {DIFFICULTIES.map(d => (
                    <button
                      key={d}
                      onClick={() => updateFilter('difficulty', toggleArrayFilter(filters.difficulty, d))}
                      className={`px-3 py-1.5 text-sm rounded-xl transition-all ${
                        filters.difficulty?.includes(d)
                          ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                          : 'bg-white/5 text-gray-400 border border-white/5 hover:bg-white/10 hover:text-gray-200'
                      }`}
                    >
                      {getDifficultyName(d)}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-300 mb-2 block">内容类型</label>
                <div className="flex flex-wrap gap-2">
                  {CONTENT_TYPES.map(t => (
                    <button
                      key={t}
                      onClick={() => updateFilter('contentTypes', toggleArrayFilter(filters.contentTypes, t))}
                      className={`px-3 py-1.5 text-sm rounded-xl transition-all ${
                        filters.contentTypes?.includes(t)
                          ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                          : 'bg-white/5 text-gray-400 border border-white/5 hover:bg-white/10 hover:text-gray-200'
                      }`}
                    >
                      {getContentTypeName(t)}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-300 mb-2 block">学习状态</label>
                <div className="flex flex-wrap gap-2">
                  {STATUSES.map(s => (
                    <button
                      key={s}
                      onClick={() => updateFilter('status', toggleArrayFilter(filters.status, s))}
                      className={`px-3 py-1.5 text-sm rounded-xl transition-all ${
                        filters.status?.includes(s)
                          ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                          : 'bg-white/5 text-gray-400 border border-white/5 hover:bg-white/10 hover:text-gray-200'
                      }`}
                    >
                      {getStatusName(s)}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex gap-2 pt-2 border-t border-white/5">
                <button
                  onClick={() => onChange({})}
                  className="btn-secondary px-5 py-2 text-sm"
                >
                  重置筛选
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}