import React from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Eye, Star, Clock, Plus, Search, TrendingUp, BookMarked } from 'lucide-react';
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
  visible: { opacity: 1, transition: { staggerChildren: 0.08 } },
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
};

export function Dashboard({ stats, recentItems, onAddClick, onSearchClick, onItemClick }: DashboardProps) {
  const statCards = [
    { label: '总收藏', value: stats?.total_count || 0, icon: BookMarked, color: '#4f8fff', gradient: 'from-blue-500/20 to-cyan-500/5', glow: 'shadow-blue-500/20' },
    { label: '未读', value: stats?.unread_count || 0, icon: Clock, color: '#a0a0b0', gradient: 'from-gray-500/20 to-gray-500/5', glow: 'shadow-gray-500/20' },
    { label: '已读', value: stats?.read_count || 0, icon: Eye, color: '#34d399', gradient: 'from-green-500/20 to-green-500/5', glow: 'shadow-green-500/20' },
    { label: '重点', value: stats?.important_count || 0, icon: Star, color: '#f97316', gradient: 'from-orange-500/20 to-orange-500/5', glow: 'shadow-orange-500/20' },
  ];

  const domainColors: Record<string, string> = {
    llm: 'from-purple-500 to-purple-600',
    agent: 'from-blue-500 to-blue-600',
    rag: 'from-cyan-500 to-cyan-600',
    multimodal: 'from-pink-500 to-pink-600',
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      <motion.div variants={itemVariants}>
        <div className="flex items-center gap-6 mb-8">
          <div>
            <h1 className="text-2xl font-bold text-white mb-1">欢迎回来</h1>
            <p className="text-gray-400 text-sm">今天也要持续学习呀</p>
          </div>
          <div className="ml-auto flex gap-3">
            <button
              onClick={onAddClick}
              className="btn-primary flex items-center gap-2"
            >
              <Plus size={18} />
              添加链接
            </button>
            <button
              onClick={onSearchClick}
              className="btn-secondary flex items-center gap-2"
            >
              <Search size={18} />
              智能检索
            </button>
          </div>
        </div>
      </motion.div>

      <motion.div variants={itemVariants} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card, index) => (
          <motion.div
            key={card.label}
            whileHover={{ y: -4, scale: 1.02 }}
            className="glass-card p-5 relative overflow-hidden group"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className={`absolute inset-0 bg-gradient-to-br ${card.gradient} opacity-50`} />
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-3">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center shadow-lg"
                  style={{ backgroundColor: `${card.color}20`, boxShadow: `0 4px 20px ${card.color}20` }}
                >
                  <card.icon size={18} style={{ color: card.color }} />
                </div>
              </div>
              <div className="text-3xl font-bold text-white mb-1">{card.value}</div>
              <div className="text-sm text-gray-400">{card.label}</div>
            </div>
          </motion.div>
        ))}
      </motion.div>

      <motion.div variants={itemVariants} className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-card p-6">
          <div className="flex items-center gap-2 mb-5">
            <TrendingUp size={18} className="text-blue-400" />
            <h3 className="font-semibold text-white">领域分布</h3>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {Object.entries(stats?.domain_stats || {}).map(([domain, count]) => (
              <div key={domain} className="flex items-center justify-between p-4 glass rounded-xl group hover:bg-white/5 transition-all">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${domainColors[domain] || 'from-gray-500 to-gray-600'} flex items-center justify-center text-white text-xs font-bold`}>
                    {domain.charAt(0).toUpperCase()}
                  </div>
                  <span className="text-sm text-gray-300">{getDomainName(domain as any)}</span>
                </div>
                <span className="text-lg font-bold text-white">{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card p-6">
          <h3 className="font-semibold text-white mb-5">最近添加</h3>
          <div className="space-y-3 max-h-80 overflow-y-auto scrollbar-thin pr-2">
            {recentItems.slice(0, 8).map((item) => (
              <motion.div
                key={item.id}
                whileHover={{ x: 4 }}
                onClick={() => onItemClick(item)}
                className="flex items-start gap-3 p-3 glass rounded-xl cursor-pointer group hover:bg-white/5 transition-all"
              >
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                  style={{ backgroundColor: `${getPlatformColor(item.platform)}15` }}
                >
                  <i
                    className={`${getPlatformIcon(item.platform)} text-sm`}
                    style={{ color: getPlatformColor(item.platform) }}
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-gray-200 truncate group-hover:text-blue-400 transition-colors">
                    {item.title}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">{formatDate(item.created_at)}</div>
                </div>
                <div
                  className="w-2 h-2 rounded-full flex-shrink-0 mt-2"
                  style={{ backgroundColor: getStatusColor(item.status) }}
                />
              </motion.div>
            ))}
            {recentItems.length === 0 && (
              <div className="text-center py-12 text-gray-500 text-sm">
                <div className="mb-3">
                  <BookOpen size={32} className="mx-auto text-gray-600" />
                </div>
                暂无收藏内容
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}