import React, { useState, useCallback } from 'react';
import { Link2, Loader2, CheckCircle, AlertCircle, Plus, X, RefreshCw, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { detectPlatform, getPlatformName, getPlatformIcon, getPlatformColor } from '../utils/platform';
import { cleanUrls } from '../utils/api';
import type { Platform } from '../types';

interface LinkInputProps {
  onSubmit: (urls: string[]) => void;
  isParsing: boolean;
  parseProgress: number;
  parseErrors?: Record<string, string>;
  onRetry?: (url: string) => void;
  onParsingComplete?: () => void;
}

interface LinkItem {
  url: string;
  platform: Platform | null;
  isValid: boolean;
  status: 'pending' | 'parsing' | 'success' | 'error';
  errorMsg?: string;
}

export function LinkInput({ onSubmit, isParsing, parseProgress, parseErrors, onRetry, onParsingComplete }: LinkInputProps) {
  const [inputValue, setInputValue] = useState('');
  const [links, setLinks] = useState<LinkItem[]>([]);
  const [error, setError] = useState('');
  const [hasParsed, setHasParsed] = useState(false);
  const [isCleaning, setIsCleaning] = useState(false);

  const handleAddLinks = useCallback(async () => {
    setError('');
    const urls = inputValue
      .replace(/\r\n/g, '\n')
      .replace(/\r/g, '\n')
      .split('\n')
      .map(u => u.trim())
      .filter(u => u.length > 0);

    if (urls.length === 0) {
      setError('请输入至少一个链接');
      return;
    }
    if (urls.length > 10) {
      setError('单次最多支持10条链接');
      return;
    }

    setIsCleaning(true);

    try {
      const cleanedResults = await cleanUrls(urls);

      const newLinks: LinkItem[] = cleanedResults.map((result: { cleaned_url: string; is_valid: boolean }) => {
        const trimmed = result.cleaned_url.trim();
        const isValid = result.is_valid;
        const platform = isValid ? detectPlatform(trimmed) : null;
        return { url: trimmed, platform, isValid, status: 'pending' };
      });

      const invalidCount = newLinks.filter(l => !l.isValid).length;
      if (invalidCount > 0) {
        setError(`检测到 ${invalidCount} 个无效链接`);
      }

      setLinks(prev => [...prev, ...newLinks].slice(0, 10));
      setInputValue('');
    } catch (err) {
      setError('链接清理失败，请重试');
    } finally {
      setIsCleaning(false);
    }
  }, [inputValue]);

  const removeLink = useCallback((index: number) => {
    setLinks(prev => prev.filter((_, i) => i !== index));
  }, []);

  const handleRetry = useCallback((url: string) => {
    setLinks(prev => prev.map(link => 
      link.url === url ? { ...link, status: 'parsing', errorMsg: undefined } : link
    ));
    onRetry?.(url);
  }, [onRetry]);

  const handleSubmit = useCallback(() => {
    const validUrls = links.filter(l => l.isValid && l.platform).map(l => l.url);
    if (validUrls.length === 0) {
      setError('没有有效的平台链接');
      return;
    }
    setLinks(prev => prev.map(link => 
      validUrls.includes(link.url) ? { ...link, status: 'parsing' } : link
    ));
    setHasParsed(true);
    onSubmit(validUrls);
  }, [links, onSubmit]);

  const clearAll = useCallback(() => {
    setLinks([]);
    setError('');
    setHasParsed(false);
  }, []);

  React.useEffect(() => {
    if (hasParsed && !isParsing && links.length > 0) {
      setLinks(prev => prev.map(link => ({
        ...link,
        status: link.status === 'parsing' ? 'success' : link.status
      })));
      
      const timer = setTimeout(() => {
        clearAll();
        onParsingComplete?.();
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, [hasParsed, isParsing, links.length, clearAll, onParsingComplete]);

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Link2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-white">添加收藏链接</h2>
            <p className="text-sm text-gray-500">支持微信公众号、知乎、CSDN、B站、抖音、小红书</p>
          </div>
        </div>

        <div className="space-y-3">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="粘贴链接，每行一个，最多10条..."
            className="input-field h-24 resize-none"
            disabled={isParsing}
          />
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500">已添加 {links.length}/10 条</span>
            <button
              onClick={handleAddLinks}
              disabled={!inputValue.trim() || isParsing || links.length >= 10 || isCleaning}
              className="btn-secondary px-4 py-2 text-sm disabled:opacity-40"
            >
              {isCleaning ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Plus className="w-4 h-4" />
              )}
              {isCleaning ? '清理中...' : '添加'}
            </button>
          </div>
        </div>

        <AnimatePresence>
          {links.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-4 space-y-2 overflow-hidden"
            >
              {links.map((link, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className={`flex items-start gap-3 p-3 rounded-xl border transition-all ${
                    link.status === 'error' ? 'bg-red-500/10 border-red-500/20' :
                    link.status === 'success' ? 'bg-green-500/10 border-green-500/20' :
                    link.status === 'parsing' ? 'bg-blue-500/10 border-blue-500/20' :
                    link.isValid && link.platform ? 'bg-white/5 border-white/5' :
                    'bg-red-500/10 border-red-500/20'
                  }`}
                >
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                    style={{ backgroundColor: link.platform ? `${getPlatformColor(link.platform)}15` : 'rgba(255,255,255,0.05)' }}
                  >
                    <i
                      className={`${link.platform ? getPlatformIcon(link.platform) : 'fa-solid fa-link'} text-sm`}
                      style={{ color: link.platform ? getPlatformColor(link.platform) : '#6a6a7a' }}
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-200 truncate">
                      {link.platform ? getPlatformName(link.platform) : '未知平台'}
                    </p>
                    <p className="text-xs text-gray-500 break-all leading-tight">{link.url}</p>
                    {link.errorMsg && (
                      <p className="text-xs text-red-400 mt-1">{link.errorMsg}</p>
                    )}
                  </div>
                  <div className="flex flex-shrink-0 gap-1">
                  {link.status === 'parsing' ? (
                    <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
                  ) : link.status === 'success' ? (
                    <CheckCircle className="w-5 h-5 text-green-400" />
                  ) : link.status === 'error' ? (
                    <button
                      onClick={() => handleRetry(link.url)}
                      className="p-1 hover:bg-red-500/20 rounded transition-colors"
                      title="重试"
                    >
                      <RefreshCw className="w-4 h-4 text-red-400" />
                    </button>
                  ) : link.isValid && link.platform ? (
                    <CheckCircle className="w-5 h-5 text-gray-600" />
                  ) : (
                    <AlertCircle className="w-5 h-5 text-red-400" />
                  )}
                  <button
                    onClick={() => removeLink(index)}
                    className="p-1 hover:bg-white/10 rounded transition-colors"
                  >
                    <X className="w-4 h-4 text-gray-500" />
                  </button>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-4 p-3 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-2"
          >
            <AlertCircle className="w-4 h-4 text-red-400" />
            <span className="text-sm text-red-400">{error}</span>
          </motion.div>
        )}

        {isParsing && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-4 p-4 bg-blue-500/10 border border-blue-500/20 rounded-xl"
          >
            <div className="flex items-center gap-3 mb-2">
              <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
              <span className="text-sm font-medium text-blue-400">正在解析内容...</span>
            </div>
            <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${parseProgress}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
            <p className="text-xs text-blue-400/70 mt-1">{parseProgress}% 完成</p>
          </motion.div>
        )}

        <div className="mt-6 flex items-center gap-3">
          {links.length > 0 && (
            <button
              onClick={clearAll}
              disabled={isParsing}
              className="btn-secondary px-5 py-2.5 disabled:opacity-40"
            >
              清空
            </button>
          )}
          <button
            onClick={handleSubmit}
            disabled={links.length === 0 || isParsing}
            className="btn-primary flex-1 flex items-center justify-center gap-2 py-3 disabled:opacity-40"
          >
            {isParsing ? (
              <><Loader2 className="w-4 h-4 animate-spin" />解析中...</>
            ) : (
              <><Sparkles className="w-4 h-4" />开始解析 ({links.filter(l => l.isValid && l.platform).length})</>
            )}
          </button>
        </div>
      </motion.div>
    </div>
  );
}