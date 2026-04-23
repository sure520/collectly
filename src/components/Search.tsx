import React, { useState } from 'react';
import { Search as SearchIcon, Filter, X } from 'lucide-react';
import type { SearchFilters, Domain, Platform, Difficulty, ContentType, LearningStatus } from '../types';
import { getDomainName, getContentTypeName, getDifficultyName, getStatusName } from '../utils/format';
import { getPlatformName } from '../utils/platform';

interface SearchProps {
  onSearch: (query: string, filters: SearchFilters, useSemantic: boolean) => void;
  loading?: boolean;
}

const DOMAINS: Domain[] = ['llm', 'agent', 'rag', 'multimodal'];
const PLATFORMS: Platform[] = ['wechat', 'zhihu', 'csdn', 'bilibili', 'douyin', 'xiaohongshu'];
const DIFFICULTIES: Difficulty[] = ['beginner', 'intermediate', 'advanced', 'paper'];
const CONTENT_TYPES: ContentType[] = ['tutorial', 'review', 'practice', 'paper', 'interview', 'analysis'];
const STATUSES: LearningStatus[] = ['unread', 'read', 'important', 'review'];

export default function Search({ onSearch, loading }: SearchProps) {
  const [query, setQuery] = useState('');
  const [searchMode, setSearchMode] = useState<'semantic' | 'keyword'>('semantic');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState<SearchFilters>({});

  const handleSearch = () => {
    onSearch(query, filters, searchMode === 'semantic');
  };

  const toggleFilter = <T extends string>(key: keyof SearchFilters, value: T, current: T[] | undefined) => {
    const updated = current?.includes(value)
      ? current.filter(v => v !== value)
      : [...(current || []), value];
    setFilters(prev => ({ ...prev, [key]: updated.length > 0 ? updated : undefined }));
  };

  const clearFilters = () => {
    setFilters({});
  };

  const FilterGroup = <T extends string>({ title, options, keyName, getLabel }: { title: string; options: T[]; keyName: keyof SearchFilters; getLabel: (v: T) => string }) => (
    <div className="mb-4">
      <h4 className="text-sm font-medium text-gray-700 mb-2">{title}</h4>
      <div className="flex flex-wrap gap-2">
        {options.map(opt => {
          const selected = (filters[keyName] as T[] | undefined)?.includes(opt);
          return (
            <button
              key={opt}
              onClick={() => toggleFilter(keyName, opt, filters[keyName] as T[] | undefined)}
              className={`px-3 py-1 text-xs rounded-full transition-colors ${
                selected
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {getLabel(opt)}
            </button>
          );
        })}
      </div>
    </div>
  );

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div className="flex items-center gap-3 mb-4">
          <div className="flex-1 relative">
            <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder={searchMode === 'semantic' ? '输入自然语言描述，如"Agent记忆机制实现"' : '输入关键词搜索'}
              className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={loading}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 transition-colors"
          >
            {loading ? '搜索中...' : '搜索'}
          </button>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setSearchMode('semantic')}
              className={`px-3 py-1.5 text-sm rounded-lg transition-colors ${
                searchMode === 'semantic'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              语义检索
            </button>
            <button
              onClick={() => setSearchMode('keyword')}
              className={`px-3 py-1.5 text-sm rounded-lg transition-colors ${
                searchMode === 'keyword'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              关键词
            </button>
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Filter size={16} />
            筛选
            {Object.values(filters).some(v => v !== undefined) && (
              <span className="w-2 h-2 bg-blue-500 rounded-full" />
            )}
          </button>
        </div>

        {showFilters && (
          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-medium text-gray-800">筛选条件</h3>
              <button
                onClick={clearFilters}
                className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
              >
                <X size={14} />
                清除全部
              </button>
            </div>
            <FilterGroup title="领域" options={DOMAINS} keyName="domains" getLabel={getDomainName} />
            <FilterGroup title="来源平台" options={PLATFORMS} keyName="platforms" getLabel={getPlatformName as (v: Platform) => string} />
            <FilterGroup title="难度" options={DIFFICULTIES} keyName="difficulty" getLabel={getDifficultyName as (v: Difficulty) => string} />
            <FilterGroup title="内容类型" options={CONTENT_TYPES} keyName="contentTypes" getLabel={getContentTypeName as (v: ContentType) => string} />
            <FilterGroup title="学习状态" options={STATUSES} keyName="status" getLabel={getStatusName as (v: LearningStatus) => string} />
          </div>
        )}
      </div>
    </div>
  );
}