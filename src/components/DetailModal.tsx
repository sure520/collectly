import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ExternalLink, Bookmark, CheckCircle, Clock, Star, Edit3 } from 'lucide-react';
import type { KnowledgeItem, LearningStatus } from '../types';
import { getPlatformName, getPlatformIcon, getPlatformColor } from '../utils/platform';
import { getStatusName, getStatusColor, formatDate, getDifficultyName, getContentTypeName, getDomainName } from '../utils/format';

interface DetailModalProps {
  item: KnowledgeItem | null;
  isOpen: boolean;
  onClose: () => void;
  onUpdateStatus: (id: string, status: LearningStatus) => void;
  onUpdateNote: (id: string, note: string) => void;
}

const statusOptions: LearningStatus[] = ['unread', 'read', 'important', 'review'];

const statusIcons: Record<LearningStatus, React.ReactNode> = {
  unread: <Clock size={16} />,
  read: <CheckCircle size={16} />,
  important: <Star size={16} />,
  review: <Bookmark size={16} />,
};

export function DetailModal({ item, isOpen, onClose, onUpdateStatus, onUpdateNote }: DetailModalProps) {
  const [note, setNote] = useState(item?.note || '');
  const [isEditingNote, setIsEditingNote] = useState(false);

  if (!item) return null;

  const handleNoteSave = () => {
    onUpdateNote(item.id, note);
    setIsEditingNote(false);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40"
            style={{ backgroundColor: 'rgba(44,36,32,0.3)', backdropFilter: 'blur(4px)' }}
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.97, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.97, y: 20 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed inset-6 md:inset-12 lg:inset-16 z-50 overflow-hidden flex flex-col rounded-xl"
            style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)', boxShadow: '0 20px 60px rgba(0,0,0,0.15)' }}
          >
            <div className="flex items-center justify-between px-6 py-4" style={{ borderBottom: '1px solid var(--border-light)' }}>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${getPlatformColor(item.platform)}12` }}>
                  <i className={`${getPlatformIcon(item.platform)} text-sm`} style={{ color: getPlatformColor(item.platform) }} />
                </div>
                <span className="text-sm" style={{ color: 'var(--text-light)' }}>{getPlatformName(item.platform)}</span>
              </div>
              <button onClick={onClose} className="p-2 rounded-lg hover:bg-gray-100 transition-colors" style={{ color: 'var(--text-mid)' }}>
                <X size={20} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 scrollbar-thin">
              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="serif text-xl font-semibold block mb-3 leading-snug"
                style={{ color: 'var(--text)', letterSpacing: '-0.3px' }}
              >
                {item.title}
              </a>
              <div className="flex items-center gap-4 text-sm mb-6" style={{ color: 'var(--text-light)' }}>
                <span>{item.author}</span>
                <span>{formatDate(item.publish_time)}</span>
              </div>

              <div className="flex flex-wrap gap-2 mb-6">
                {item.domains.map(domain => (
                  <span key={domain} className="px-3 py-1 rounded-full text-xs font-semibold" style={{ backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent-dark)' }}>
                    {getDomainName(domain)}
                  </span>
                ))}
                <span className="px-3 py-1 rounded-full text-xs font-semibold" style={{ backgroundColor: 'var(--bg-warm)', color: 'var(--text-mid)' }}>
                  {getContentTypeName(item.content_type)}
                </span>
                <span className="px-3 py-1 rounded-full text-xs font-semibold" style={{ backgroundColor: 'var(--bg-warm)', color: 'var(--text-mid)' }}>
                  {getDifficultyName(item.difficulty)}
                </span>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="text-sm font-semibold uppercase tracking-wider mb-2" style={{ color: 'var(--text-light)' }}>短摘要</h3>
                  <p className="text-sm leading-relaxed" style={{ color: 'var(--text-mid)' }}>{item.short_summary}</p>
                </div>

                <div>
                  <h3 className="text-sm font-semibold uppercase tracking-wider mb-2" style={{ color: 'var(--text-light)' }}>长摘要</h3>
                  <p className="text-sm leading-relaxed" style={{ color: 'var(--text-mid)' }}>{item.long_summary}</p>
                </div>

                <div>
                  <h3 className="text-sm font-semibold uppercase tracking-wider mb-3" style={{ color: 'var(--text-light)' }}>核心知识点</h3>
                  <div className="space-y-2.5">
                    {item.key_points.map((point, idx) => (
                      <div key={idx} className="flex items-start gap-3 text-sm" style={{ color: 'var(--text-mid)', lineHeight: '1.6' }}>
                        <span className="w-5 h-5 rounded-lg flex items-center justify-center text-xs flex-shrink-0 font-semibold mt-0.5" style={{ backgroundColor: 'rgba(212,133,106,0.12)', color: 'var(--accent)' }}>
                          {idx + 1}
                        </span>
                        {point}
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-semibold uppercase tracking-wider mb-2" style={{ color: 'var(--text-light)' }}>标签</h3>
                  <div className="flex flex-wrap gap-2">
                    {item.tags.map(tag => (
                      <span key={tag} className="px-2.5 py-1 rounded-full text-xs font-semibold" style={{ backgroundColor: 'var(--bg-warm)', color: 'var(--text-mid)' }}>
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-semibold uppercase tracking-wider" style={{ color: 'var(--text-light)' }}>学习笔记</h3>
                    <button
                      onClick={() => isEditingNote ? handleNoteSave() : setIsEditingNote(true)}
                      className="flex items-center gap-1 text-sm font-semibold transition-colors"
                      style={{ color: 'var(--accent)' }}
                    >
                      <Edit3 size={14} />
                      {isEditingNote ? '保存' : '编辑'}
                    </button>
                  </div>
                  {isEditingNote ? (
                    <textarea
                      value={note}
                      onChange={(e) => setNote(e.target.value)}
                      className="input-field min-h-[100px] resize-none"
                      placeholder="添加学习笔记..."
                    />
                  ) : (
                    <div className="p-4 rounded-xl text-sm leading-relaxed" style={{ backgroundColor: 'var(--bg)', color: 'var(--text-mid)', border: '1px solid var(--border-light)' }}>
                      {note || '暂无笔记'}
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div className="px-6 py-4 flex items-center justify-between" style={{ borderTop: '1px solid var(--border-light)', backgroundColor: 'var(--surface2)' }}>
              <div className="flex gap-2">
                {statusOptions.map(status => (
                  <button
                    key={status}
                    onClick={() => onUpdateStatus(item.id, status)}
                    className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all"
                    style={
                      item.status === status
                        ? { backgroundColor: getStatusColor(status), color: 'white' }
                        : { backgroundColor: 'var(--bg)', color: 'var(--text-mid)', border: `1px solid ${getStatusColor(status)}30` }
                    }
                  >
                    {statusIcons[status]}
                    {getStatusName(status)}
                  </button>
                ))}
              </div>
              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary flex items-center gap-1.5"
              >
                <ExternalLink size={14} />
                查看原文
              </a>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
