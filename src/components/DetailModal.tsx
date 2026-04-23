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
            className="fixed inset-0 bg-black/50 z-40"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed inset-4 md:inset-10 bg-white rounded-2xl z-50 overflow-hidden flex flex-col"
          >
            <div className="flex items-center justify-between p-4 border-b">
              <div className="flex items-center gap-3">
                <i
                  className={`${getPlatformIcon(item.platform)} text-lg`}
                  style={{ color: getPlatformColor(item.platform) }}
                />
                <span className="text-sm text-gray-500">{getPlatformName(item.platform)}</span>
              </div>
              <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                <X size={20} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6">
              <h2 className="text-xl font-bold mb-2">{item.title}</h2>
              <div className="flex items-center gap-4 text-sm text-gray-500 mb-6">
                <span>{item.author}</span>
                <span>{formatDate(item.publish_time)}</span>
              </div>

              <div className="flex flex-wrap gap-2 mb-6">
                {item.domains.map(domain => (
                  <span key={domain} className="px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-xs">
                    {getDomainName(domain)}
                  </span>
                ))}
                <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
                  {getContentTypeName(item.content_type)}
                </span>
                <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
                  {getDifficultyName(item.difficulty)}
                </span>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold mb-2">短摘要</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{item.short_summary}</p>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold mb-2">长摘要</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{item.long_summary}</p>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold mb-2">核心知识点</h3>
                <ul className="space-y-2">
                  {item.key_points.map((point, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm text-gray-600">
                      <span className="w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs flex-shrink-0">
                        {idx + 1}
                      </span>
                      {point}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mb-6">
                <h3 className="font-semibold mb-2">标签</h3>
                <div className="flex flex-wrap gap-2">
                  {item.tags.map(tag => (
                    <span key={tag} className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold">学习笔记</h3>
                  <button
                    onClick={() => isEditingNote ? handleNoteSave() : setIsEditingNote(true)}
                    className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-700"
                  >
                    <Edit3 size={14} />
                    {isEditingNote ? '保存' : '编辑'}
                  </button>
                </div>
                {isEditingNote ? (
                  <textarea
                    value={note}
                    onChange={(e) => setNote(e.target.value)}
                    className="w-full p-3 border rounded-lg text-sm min-h-[100px] resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="添加学习笔记..."
                  />
                ) : (
                  <div className="p-3 bg-gray-50 rounded-lg text-sm text-gray-600 min-h-[60px]">
                    {note || '暂无笔记'}
                  </div>
                )}
              </div>
            </div>

            <div className="p-4 border-t flex items-center justify-between">
              <div className="flex gap-2">
                {statusOptions.map(status => (
                  <button
                    key={status}
                    onClick={() => onUpdateStatus(item.id, status)}
                    className={`flex items-center gap-1 px-3 py-2 rounded-lg text-sm transition-colors ${
                      item.status === status
                        ? 'text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
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
                className="flex items-center gap-1 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors"
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
