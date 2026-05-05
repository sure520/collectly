import React from 'react';
import { motion } from 'framer-motion';
import { Eye, Edit2, Trash2 } from 'lucide-react';
import type { KnowledgeItem } from '../types';
import { getPlatformIcon, getPlatformColor, getPlatformName } from '../utils/platform';
import { getDomainName, getDifficultyName, getDifficultyColor, getStatusName, getStatusColor, formatDate, truncateText } from '../utils/format';

interface KnowledgeCardProps {
  item: KnowledgeItem;
  onView: (item: KnowledgeItem) => void;
  onEdit: (item: KnowledgeItem) => void;
  onDelete: (id: string) => void;
}

export function KnowledgeCard({ item, onView, onEdit, onDelete }: KnowledgeCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -6 }}
      className="glass-card overflow-hidden group"
    >
      <div className="p-5">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-2.5">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center transition-transform group-hover:scale-110"
              style={{ backgroundColor: `${getPlatformColor(item.platform)}15` }}
            >
              <i
                className={`${getPlatformIcon(item.platform)} text-base`}
                style={{ color: getPlatformColor(item.platform) }}
              />
            </div>
            <span className="text-xs text-gray-400">{getPlatformName(item.platform)}</span>
          </div>
          <span
            className="px-2.5 py-1 rounded-lg text-xs font-medium"
            style={{
              backgroundColor: `${getStatusColor(item.status)}15`,
              color: getStatusColor(item.status),
            }}
          >
            {getStatusName(item.status)}
          </span>
        </div>

        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block font-semibold text-white hover:text-blue-400 mb-3 line-clamp-2 leading-snug transition-colors text-[15px]"
        >
          {item.title}
        </a>

        <p className="text-sm text-gray-400 mb-4 line-clamp-2 leading-relaxed">
          {truncateText(item.short_summary, 80)}
        </p>

        <div className="flex items-center gap-1.5 mb-4 flex-wrap">
          {item.domains.map((domain) => (
            <span
              key={domain}
              className="px-2.5 py-1 bg-blue-500/10 text-blue-400 rounded-lg text-xs font-medium"
            >
              {getDomainName(domain)}
            </span>
          ))}
          <span
            className="px-2.5 py-1 rounded-lg text-xs font-medium"
            style={{
              backgroundColor: `${getDifficultyColor(item.difficulty)}15`,
              color: getDifficultyColor(item.difficulty),
            }}
          >
            {getDifficultyName(item.difficulty)}
          </span>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-white/5">
          <div className="flex items-center gap-3 text-xs text-gray-500">
            <span>{item.author}</span>
            <span>{formatDate(item.created_at)}</span>
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={() => onView(item)}
              className="p-2 text-gray-500 hover:text-blue-400 hover:bg-blue-500/10 rounded-lg transition-all"
            >
              <Eye size={15} />
            </button>
            <button
              onClick={() => onEdit(item)}
              className="p-2 text-gray-500 hover:text-green-400 hover:bg-green-500/10 rounded-lg transition-all"
            >
              <Edit2 size={15} />
            </button>
            <button
              onClick={() => onDelete(item.id)}
              className="p-2 text-gray-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all"
            >
              <Trash2 size={15} />
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}