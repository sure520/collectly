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
    <div className="rounded-xl" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}>
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between px-5 py-3.5 transition-colors"
        style={{ borderBottom: isExpanded ? '1px solid var(--border-light)' : 'none' }}
        onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = 'var(--surface2)')}
        onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
      >
        <div className="flex items-center gap-2">
          <Filter size={18} style={{ color: 'var(--accent)' }} />
          <span className="font-semibold" style={{ color: 'var(--text)' }}>筛选条件</span>
          {hasActiveFilters && (
            <span className="px-2 py-0.5 rounded-full text-xs font-semibold" style={{ backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent-dark)' }}>
              已启用
            </span>
          )}
        </div>
        <ChevronDown size={18} className="transition-transform" style={{ color: 'var(--text-light)', transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }} />
      </button>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="px-5 pb-5 space-y-4">
              <div>
                <label className="text-xs font-semibold uppercase tracking-wider mb-2 block" style={{ color: 'var(--text-light)' }}>领域</label>
                <div className="flex flex-wrap gap-2">
                  {DOMAINS.map(d => (
                    <button
                      key={d}
                      onClick={() => updateFilter('domains', toggleArrayFilter(filters.domains, d))}
                      className="px-3 py-1.5 text-sm rounded-full transition-all font-medium"
                      style={filters.domains?.includes(d)
                        ? { backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent-dark)', border: '1px solid rgba(212,133,106,0.3)' }
                        : { backgroundColor: 'var(--bg)', color: 'var(--text-mid)', border: '1px solid var(--border-light)' }
                      }
                    >
                      {getDomainName(d)}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold uppercase tracking-wider mb-2 block" style={{ color: 'var(--text-light)' }}>来源平台</label>
                <div className="flex flex-wrap gap-2">
                  {PLATFORMS.map(p => (
                    <button
                      key={p}
                      onClick={() => updateFilter('platforms', toggleArrayFilter(filters.platforms, p))}
                      className="px-3 py-1.5 text-sm rounded-full transition-all font-medium"
                      style={filters.platforms?.includes(p)
                        ? { backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent-dark)', border: '1px solid rgba(212,133,106,0.3)' }
                        : { backgroundColor: 'var(--bg)', color: 'var(--text-mid)', border: '1px solid var(--border-light)' }
                      }
                    >
                      {getPlatformName(p)}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold uppercase tracking-wider mb-2 block" style={{ color: 'var(--text-light)' }}>难度</label>
                <div className="flex flex-wrap gap-2">
                  {DIFFICULTIES.map(d => (
                    <button
                      key={d}
                      onClick={() => updateFilter('difficulty', toggleArrayFilter(filters.difficulty, d))}
                      className="px-3 py-1.5 text-sm rounded-full transition-all font-medium"
                      style={filters.difficulty?.includes(d)
                        ? { backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent-dark)', border: '1px solid rgba(212,133,106,0.3)' }
                        : { backgroundColor: 'var(--bg)', color: 'var(--text-mid)', border: '1px solid var(--border-light)' }
                      }
                    >
                      {getDifficultyName(d)}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold uppercase tracking-wider mb-2 block" style={{ color: 'var(--text-light)' }}>内容类型</label>
                <div className="flex flex-wrap gap-2">
                  {CONTENT_TYPES.map(t => (
                    <button
                      key={t}
                      onClick={() => updateFilter('contentTypes', toggleArrayFilter(filters.contentTypes, t))}
                      className="px-3 py-1.5 text-sm rounded-full transition-all font-medium"
                      style={filters.contentTypes?.includes(t)
                        ? { backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent-dark)', border: '1px solid rgba(212,133,106,0.3)' }
                        : { backgroundColor: 'var(--bg)', color: 'var(--text-mid)', border: '1px solid var(--border-light)' }
                      }
                    >
                      {getContentTypeName(t)}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold uppercase tracking-wider mb-2 block" style={{ color: 'var(--text-light)' }}>学习状态</label>
                <div className="flex flex-wrap gap-2">
                  {STATUSES.map(s => (
                    <button
                      key={s}
                      onClick={() => updateFilter('status', toggleArrayFilter(filters.status, s))}
                      className="px-3 py-1.5 text-sm rounded-full transition-all font-medium"
                      style={filters.status?.includes(s)
                        ? { backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent-dark)', border: '1px solid rgba(212,133,106,0.3)' }
                        : { backgroundColor: 'var(--bg)', color: 'var(--text-mid)', border: '1px solid var(--border-light)' }
                      }
                    >
                      {getStatusName(s)}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex gap-2 pt-3" style={{ borderTop: '1px solid var(--border-light)' }}>
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
