import React from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Eye, Star, Clock, Plus, Search, TrendingUp, BookmarkCheck } from 'lucide-react';
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
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
};

export function Dashboard({ stats, recentItems, onAddClick, onSearchClick, onItemClick }: DashboardProps) {
  const statCards = [
    { label: '总收藏', value: stats?.total_count || 0, icon: BookmarkCheck, color: 'var(--accent)' },
    { label: '未读', value: stats?.unread_count || 0, icon: Clock, color: 'var(--text-light)' },
    { label: '已读', value: stats?.read_count || 0, icon: Eye, color: 'var(--accent2)' },
    { label: '重点', value: stats?.important_count || 0, icon: Star, color: 'var(--accent-dark)' },
  ];

  const domainColors: Record<string, string> = {
    llm: 'var(--accent3)',
    agent: 'var(--accent)',
    rag: 'var(--accent2)',
    multimodal: 'var(--accent-dark)',
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-8"
    >
      <motion.div variants={itemVariants}>
        <div className="mb-10">
          <p className="text-sm font-semibold uppercase tracking-widest mb-2" style={{ color: 'var(--accent)' }}>
            Welcome back
          </p>
          <h1 className="serif text-4xl font-bold mb-3" style={{ color: 'var(--text)', letterSpacing: '-0.5px', lineHeight: '1.2' }}>
            Your knowledge garden is growing
          </h1>
          <p className="text-base" style={{ color: 'var(--text-mid)', maxWidth: '500px', lineHeight: '1.7' }}>
            A curated collection of insights, ideas, and discoveries from across the web.
          </p>
        </div>
      </motion.div>

      <motion.div variants={itemVariants} className="flex gap-3">
        <button onClick={onAddClick} className="btn-primary flex items-center gap-2">
          <Plus size={18} />
          添加链接
        </button>
        <button onClick={onSearchClick} className="btn-secondary flex items-center gap-2">
          <Search size={18} />
          智能检索
        </button>
      </motion.div>

      <motion.div variants={itemVariants} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card) => (
          <motion.div
            key={card.label}
            whileHover={{ y: -2 }}
            className="rounded-xl p-6 card-hover"
            style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}
          >
            <div className="flex items-center justify-between mb-3">
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center"
                style={{ backgroundColor: `${card.color}12` }}
              >
                <card.icon size={18} style={{ color: card.color }} />
              </div>
            </div>
            <div className="serif text-3xl font-bold mb-1" style={{ color: 'var(--text)', letterSpacing: '-1px' }}>
              {card.value}
            </div>
            <div className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-light)' }}>
              {card.label}
            </div>
          </motion.div>
        ))}
      </motion.div>

      <motion.div variants={itemVariants} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 rounded-xl p-6" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}>
          <div className="flex items-center gap-2 mb-6">
            <TrendingUp size={18} style={{ color: 'var(--accent)' }} />
            <h3 className="serif text-xl font-semibold" style={{ color: 'var(--text)' }}>领域分布</h3>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {Object.entries(stats?.domain_stats || {}).map(([domain, count]) => (
              <div
                key={domain}
                className="flex items-center justify-between p-4 rounded-xl card-hover"
                style={{ backgroundColor: 'var(--bg)', border: '1px solid var(--border-light)' }}
              >
                <div className="flex items-center gap-3">
                  <div
                    className="w-9 h-9 rounded-lg flex items-center justify-center text-white text-xs font-bold"
                    style={{ backgroundColor: domainColors[domain] || 'var(--text-light)' }}
                  >
                    {domain.charAt(0).toUpperCase()}
                  </div>
                  <span className="text-sm font-medium" style={{ color: 'var(--text-mid)' }}>
                    {getDomainName(domain as any)}
                  </span>
                </div>
                <span className="serif text-lg font-bold" style={{ color: 'var(--text)' }}>{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-xl p-6" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}>
          <h3 className="serif text-xl font-semibold mb-5" style={{ color: 'var(--text)' }}>最近添加</h3>
          <div className="space-y-3 max-h-80 overflow-y-auto scrollbar-thin pr-2">
            {recentItems.slice(0, 8).map((item) => (
              <motion.div
                key={item.id}
                whileHover={{ x: 2 }}
                onClick={() => onItemClick(item)}
                className="flex items-start gap-3 p-3 rounded-xl cursor-pointer card-hover"
                style={{ backgroundColor: 'var(--bg)', border: '1px solid var(--border-light)' }}
              >
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                  style={{ backgroundColor: `${getPlatformColor(item.platform)}15` }}
                >
                  <i className={`${getPlatformIcon(item.platform)} text-sm`} style={{ color: getPlatformColor(item.platform) }} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold truncate" style={{ color: 'var(--text)' }}>
                    {item.title}
                  </div>
                  <div className="text-xs mt-0.5" style={{ color: 'var(--text-light)' }}>
                    {formatDate(item.created_at)}
                  </div>
                </div>
                <div
                  className="w-2 h-2 rounded-full flex-shrink-0 mt-1.5"
                  style={{ backgroundColor: getStatusColor(item.status) }}
                />
              </motion.div>
            ))}
            {recentItems.length === 0 && (
              <div className="text-center py-12" style={{ color: 'var(--text-light)' }}>
                <BookOpen size={36} className="mx-auto mb-3" style={{ opacity: 0.3 }} />
                <p className="text-sm">暂无收藏内容</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
