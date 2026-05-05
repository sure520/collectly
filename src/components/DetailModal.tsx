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
            className="fixed inset-0 bg-black/70 backdrop-blur-sm z-40"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed inset-4 md:inset-12 lg:inset-16 bg-[#0f0f17] rounded-2xl z-50 overflow-hidden flex flex-col border border-white/10 shadow-2xl"
          >
            <div className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-[#0f0f17]/80 backdrop-blur-xl">
              <div className="flex items-center gap-3">
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center"
                  style={{ backgroundColor: `${getPlatformColor(item.platform)}15` }}
                >
                  <i
                    className={`${getPlatformIcon(item.platform)} text-sm`}
                    style={{ color: getPlatformColor(item.platform) }}
                  />
                </div>
                <span className="text-sm text-gray-400">{getPlatformName(item.platform)}</span>
              </div>
              <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-xl transition-colors text-gray-400 hover:text-white">
                <X size={18} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 scrollbar-thin">
              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block text-xl font-bold mb-3 text-white hover:text-blue-400 transition-colors leading-snug"
              >
                {item.title}
              </a>
              <div className="flex items-center gap-4 text-sm text-gray-500 mb-6">
                <span>{item.author}</span>
                <span>{formatDate(item.publish_time)}</span>
              </div>

              <div className="flex flex-wrap gap-2 mb-6">
                {item.domains.map(domain => (
                  <span key={domain} className="px-3 py-1 bg-blue-500/10 text-blue-400 rounded-lg text-xs font-medium">
                    {getDomainName(domain)}
                  </span>
                ))}
                <span className="px-3 py-1 bg-white/5 text-gray-400 rounded-lg text-xs">
                  {getContentTypeName(item.content_type)}
                </span>
                <span className="px-3 py-1 bg-white/5 text-gray-400 rounded-lg text-xs">
                  {getDifficultyName(item.difficulty)}
                </span>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold text-white mb-2 text-sm">短摘要</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{item.short_summary}</p>
                </div>

                <div>
                  <h3 className="font-semibold text-white mb-2 text-sm">长摘要</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{item.long_summary}</p>
                </div>

                <div>
                  <h3 className="font-semibold text-white mb-3 text-sm">核心知识点</h3>
                  <div className="space-y-2.5">
                    {item.key_points.map((point, idx) => (
                      <div key={idx} className="flex items-start gap-3 text-sm text-gray-400">
                        <span className="w-5 h-5 bg-blue-500/15 text-blue-400 rounded-lg flex items-center justify-center text-xs flex-shrink-0 font-medium mt-0.5">
                          {idx + 1}
                        </span>
                        {point}
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-white mb-2 text-sm">标签</h3>
                  <div className="flex flex-wrap gap-2">
                    {item.tags.map(tag => (
                      <span key={tag} className="px-2.5 py-1 bg-white/5 text-gray-400 rounded-lg text-xs">
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-white text-sm">学习笔记</h3>
                    <button
                      onClick={() => isEditingNote ? handleNoteSave() : setIsEditingNote(true)}
                      className="flex items-center gap-1 text-sm text-blue-400 hover:text-blue-300 transition-colors"
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
                    <div className="p-4 bg-white/5 rounded-xl text-sm text-gray-400 min-h-[60px]">
                      {note || '暂无笔记'}
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div className="px-6 py-4 border-t border-white/5 flex items-center justify-between bg-[#0f0f17]/80 backdrop-blur-xl">
              <div className="flex gap-2">
                {statusOptions.map(status => (
                  <button
                    key={status}
                    onClick={() => onUpdateStatus(item.id, status)}
                    className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm transition-all ${
                      item.status === status
                        ? 'text-white shadow-lg'
                        : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
                    }`}
                    style={item.status === status ? { backgroundColor: getStatusColor(status) } : {}}
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