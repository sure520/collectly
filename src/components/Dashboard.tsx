import React from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Eye, Star, Clock, Plus, Search, TrendingUp } from 'lucide-react';
import type { UserStats, KnowledgeItem } from '../types';
import { getDomainName, getStatusColor, formatDate, truncateText } from '../utils/format';
import { getPlatformIcon, getPlatformColor } from '../utils/platform';

interface DashboardProps {
  stats: UserStats | null;
  recentItems: KnowledgeItem[];
  onAddClick: () => void;
  onSearchClick: () => void;
  onItemClick: (item: KnowledgeItem) => void;
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export function Dashboard({ stats, recentItems, onAddClick, onSearchClick, onItemClick }: DashboardProps) {
  const statCards = [
    { label: '总收藏', value: stats?.total_count || 0, icon: BookOpen, color: 'bg-blue-500' },
    { label: '未读', value: stats?.unread_count || 0, icon: Clock, color: 'bg-gray-500' },
    { label: '已读', value: stats?.read_count || 0, icon: Eye, color: 'bg-green-500' },
    { label: '重点', value: stats?.important_count || 0, icon: Star, color: 'bg-red-500' },
  ];

  const domainColors: Record<string, string> = {
    llm: 'bg-purple-500',
    agent: 'bg-indigo-500',
    rag: 'bg-cyan-500',
    multimodal: 'bg-pink-500',
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="p-6 space-y-6"
    >
      <motion.div variants={itemVariants} className="flex gap-4">
        <button
          onClick={onAddClick}
          className="flex-1 flex items-center justify-center gap-2 bg-blue-600 text-white py-4 rounded-xl font-medium hover:bg-blue-700 transition-colors"
        >
          <Plus size={20} />
          添加链接
        </button>
        <button
          onClick={onSearchClick}
          className="flex-1 flex items-center justify-center gap-2 bg-gray-100 text-gray-700 py-4 rounded-xl font-medium hover:bg-gray-200 transition-colors"
        >
          <Search size={20} />
          智能检索
        </button>
      </motion.div>

      <motion.div variants={itemVariants} className="grid grid-cols-4 gap-4">
        {statCards.map((card) => (
          <div key={card.label} className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
            <div className={`${card.color} w-10 h-10 rounded-lg flex items-center justify-center mb-3`}>
              <card.icon size={20} className="text-white" />
            </div>
            <div className="text-2xl font-bold text-gray-900">{card.value}</div>
            <div className="text-sm text-gray-500">{card.label}</div>
          </div>
        ))}
      </motion.div>

      <motion.div variants={itemVariants} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp size={20} className="text-blue-600" />
          <h3 className="font-semibold text-gray-900">领域分布</h3>
        </div>
        <div className="grid grid-cols-2 gap-3">
          {Object.entries(stats?.domain_stats || {}).map(([domain, count]) => (
            <div key={domain} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full ${domainColors[domain] || 'bg-gray-400'}`} />
                <span className="text-sm text-gray-700">{getDomainName(domain as any)}</span>
              </div>
              <span className="text-sm font-medium text-gray-900">{count}</span>
            </div>
          ))}
        </div>
      </motion.div>

      <motion.div variants={itemVariants} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <h3 className="font-semibold text-gray-900 mb-4">最近添加</h3>
        <div className="space-y-3">
          {recentItems.slice(0, 5).map((item) => (
            <div
              key={item.id}
              onClick={() => onItemClick(item)}
              className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
            >
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                style={{ backgroundColor: getPlatformColor(item.platform) + '20' }}
              >
                <i className={`${getPlatformIcon(item.platform)} text-sm`} style={{ color: getPlatformColor(item.platform) }} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-gray-900 truncate">{item.title}</div>
                <div className="text-xs text-gray-500 mt-1">{formatDate(item.created_at)}</div>
              </div>
              <div
                className="w-2 h-2 rounded-full flex-shrink-0 mt-2"
                style={{ backgroundColor: getStatusColor(item.status) }}
              />
            </div>
          ))}
          {recentItems.length === 0 && (
            <div className="text-center py-8 text-gray-400 text-sm">暂无收藏内容</div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}
