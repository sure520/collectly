import React from 'react';
import { motion } from 'framer-motion';
import { Eye, Edit2, Trash2, Bookmark } from 'lucide-react';
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
      whileHover={{ y: -4 }}
      className="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden"
    >
      <div className="p-5">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{ backgroundColor: `${getPlatformColor(item.platform)}15` }}
            >
              <i
                className={`${getPlatformIcon(item.platform)} text-sm`}
                style={{ color: getPlatformColor(item.platform) }}
              />
            </div>
            <span className="text-xs text-gray-500">{getPlatformName(item.platform)}</span>
          </div>
          <div className="flex items-center gap-1">
            <span
              className="px-2 py-0.5 rounded-full text-xs font-medium"
              style={{
                backgroundColor: `${getStatusColor(item.status)}15`,
                color: getStatusColor(item.status),
              }}
            >
              {getStatusName(item.status)}
            </span>
          </div>
        </div>

        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          onClick={(e) => e.stopPropagation()}
          className="block font-semibold text-blue-600 hover:text-blue-800 mb-2 line-clamp-2 leading-tight transition-colors"
        >
          {item.title}
        </a>

        <p className="text-sm text-gray-600 mb-3 line-clamp-2">
          {truncateText(item.short_summary, 80)}
        </p>

        <div className="flex items-center gap-1.5 mb-3">
          {item.domains.map((domain) => (
            <span
              key={domain}
              className="px-2 py-0.5 bg-blue-50 text-blue-600 rounded text-xs font-medium"
            >
              {getDomainName(domain)}
            </span>
          ))}
          <span
            className="px-2 py-0.5 rounded text-xs font-medium"
            style={{
              backgroundColor: `${getDifficultyColor(item.difficulty)}15`,
              color: getDifficultyColor(item.difficulty),
            }}
          >
            {getDifficultyName(item.difficulty)}
          </span>
        </div>

        <div className="flex items-center justify-between pt-3 border-t border-gray-100">
          <div className="flex items-center gap-3 text-xs text-gray-400">
            <span>{item.author}</span>
            <span>{formatDate(item.created_at)}</span>
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={() => onView(item)}
              className="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
            >
              <Eye size={16} />
            </button>
            <button
              onClick={() => onEdit(item)}
              className="p-1.5 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
            >
              <Edit2 size={16} />
            </button>
            <button
              onClick={() => onDelete(item.id)}
              className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              <Trash2 size={16} />
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
