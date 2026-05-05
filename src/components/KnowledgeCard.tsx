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
      className="rounded-xl p-7 card-hover cursor-pointer"
      style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}
    >
      <div className="flex items-start justify-between mb-5">
        <div className="flex items-center gap-2.5">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ backgroundColor: `${getPlatformColor(item.platform)}12` }}
          >
            <i className={`${getPlatformIcon(item.platform)} text-sm`} style={{ color: getPlatformColor(item.platform) }} />
          </div>
          <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-light)' }}>
            {getPlatformName(item.platform)}
          </span>
        </div>
        <span className="px-2.5 py-1 rounded-full text-xs font-semibold" style={{ backgroundColor: getStatusColor(item.status) + '15', color: getStatusColor(item.status) }}>
          {getStatusName(item.status)}
        </span>
      </div>

      <a
        href={item.url}
        target="_blank"
        rel="noopener noreferrer"
        className="serif text-base font-semibold block mb-3 leading-snug"
        style={{ color: 'var(--text)', letterSpacing: '-0.2px' }}
        onClick={(e) => e.stopPropagation()}
      >
        {item.title}
      </a>

      <p className="text-sm mb-4" style={{ color: 'var(--text-mid)', lineHeight: '1.7' }}>
        {truncateText(item.short_summary, 80)}
      </p>

      <div className="flex items-center gap-1.5 mb-5 flex-wrap">
        {item.domains.map((domain) => (
          <span key={domain} className="px-2.5 py-1 rounded-full text-xs font-semibold" style={{ backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent-dark)' }}>
            {getDomainName(domain)}
          </span>
        ))}
        <span className="px-2.5 py-1 rounded-full text-xs font-semibold" style={{ backgroundColor: `${getDifficultyColor(item.difficulty)}15`, color: getDifficultyColor(item.difficulty) }}>
          {getDifficultyName(item.difficulty)}
        </span>
      </div>

      <div className="flex items-center justify-between pt-4" style={{ borderTop: '1px solid var(--border-light)' }}>
        <div className="flex items-center gap-3 text-xs" style={{ color: 'var(--text-light)', fontWeight: 500 }}>
          <span>{item.author}</span>
          <span>{formatDate(item.created_at)}</span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={(e) => { e.stopPropagation(); onView(item); }}
            className="p-1.5 rounded-lg transition-colors"
            style={{ color: 'var(--text-light)' }}
            onMouseEnter={(e) => { e.currentTarget.style.color = 'var(--accent)'; e.currentTarget.style.backgroundColor = 'rgba(212,133,106,0.08)'; }}
            onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--text-light)'; e.currentTarget.style.backgroundColor = 'transparent'; }}
          >
            <Eye size={15} />
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); onEdit(item); }}
            className="p-1.5 rounded-lg transition-colors"
            style={{ color: 'var(--text-light)' }}
            onMouseEnter={(e) => { e.currentTarget.style.color = 'var(--accent2)'; e.currentTarget.style.backgroundColor = 'rgba(91,138,114,0.08)'; }}
            onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--text-light)'; e.currentTarget.style.backgroundColor = 'transparent'; }}
          >
            <Edit2 size={15} />
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); onDelete(item.id); }}
            className="p-1.5 rounded-lg transition-colors"
            style={{ color: 'var(--text-light)' }}
            onMouseEnter={(e) => { e.currentTarget.style.color = 'var(--accent-dark)'; e.currentTarget.style.backgroundColor = 'rgba(184,105,77,0.08)'; }}
            onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--text-light)'; e.currentTarget.style.backgroundColor = 'transparent'; }}
          >
            <Trash2 size={15} />
          </button>
        </div>
      </div>
    </motion.div>
  );
}
