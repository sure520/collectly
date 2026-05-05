import React, { useState, useCallback } from 'react';
import { Link2, Loader2, CheckCircle, AlertCircle, Plus, X, RefreshCw } from 'lucide-react';
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

    if (urls.length === 0) { setError('请输入至少一个链接'); return; }
    if (urls.length > 10) { setError('单次最多支持10条链接'); return; }

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
      if (invalidCount > 0) setError(`检测到 ${invalidCount} 个无效链接`);
      setLinks(prev => [...prev, ...newLinks].slice(0, 10));
      setInputValue('');
    } catch (err) { setError('链接清理失败，请重试'); }
    finally { setIsCleaning(false); }
  }, [inputValue]);

  const removeLink = useCallback((index: number) => { setLinks(prev => prev.filter((_, i) => i !== index)); }, []);

  const handleRetry = useCallback((url: string) => {
    setLinks(prev => prev.map(link => link.url === url ? { ...link, status: 'parsing', errorMsg: undefined } : link));
    onRetry?.(url);
  }, [onRetry]);

  const handleSubmit = useCallback(() => {
    const validUrls = links.filter(l => l.isValid && l.platform).map(l => l.url);
    if (validUrls.length === 0) { setError('没有有效的平台链接'); return; }
    setLinks(prev => prev.map(link => validUrls.includes(link.url) ? { ...link, status: 'parsing' } : link));
    setHasParsed(true);
    onSubmit(validUrls);
  }, [links, onSubmit]);

  const clearAll = useCallback(() => { setLinks([]); setError(''); setHasParsed(false); }, []);

  React.useEffect(() => {
    if (hasParsed && !isParsing && links.length > 0) {
      setLinks(prev => prev.map(link => ({ ...link, status: link.status === 'parsing' ? 'success' : link.status })));
      const timer = setTimeout(() => { clearAll(); onParsingComplete?.(); }, 1500);
      return () => clearTimeout(timer);
    }
  }, [hasParsed, isParsing, links.length, clearAll, onParsingComplete]);

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="rounded-xl p-7" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}>
      <div className="flex items-center gap-4 mb-6">
        <div className="w-11 h-11 rounded-xl flex items-center justify-center" style={{ background: 'linear-gradient(135deg, var(--accent), var(--accent-dark))' }}>
          <Link2 size={20} style={{ color: 'white' }} />
        </div>
        <div>
          <h2 className="serif text-xl font-semibold" style={{ color: 'var(--text)' }}>添加收藏链接</h2>
          <p className="text-sm" style={{ color: 'var(--text-light)' }}>支持微信公众号、知乎、CSDN、B站、抖音、小红书</p>
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
          <span className="text-xs" style={{ color: 'var(--text-light)' }}>已添加 {links.length}/10 条</span>
          <button
            onClick={handleAddLinks}
            disabled={!inputValue.trim() || isParsing || links.length >= 10 || isCleaning}
            className="btn-secondary px-4 py-2 text-sm disabled:opacity-40"
          >
            {isCleaning ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
            {isCleaning ? '清理中...' : '添加'}
          </button>
        </div>
      </div>

      <AnimatePresence>
        {links.length > 0 && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="mt-5 space-y-2 overflow-hidden">
            {links.map((link, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-start gap-3 p-3.5 rounded-xl"
                style={{
                  backgroundColor: link.status === 'success' ? 'rgba(91,138,114,0.08)' : link.status === 'error' ? 'rgba(184,105,77,0.08)' : 'var(--bg)',
                  border: `1px solid ${link.status === 'success' ? 'rgba(91,138,114,0.2)' : link.status === 'error' ? 'rgba(184,105,77,0.2)' : 'var(--border-light)'}`,
                }}
              >
                <div className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" style={{ backgroundColor: link.platform ? `${getPlatformColor(link.platform)}12` : 'var(--bg-warm)' }}>
                  <i className={`${link.platform ? getPlatformIcon(link.platform) : 'fa-solid fa-link'} text-sm`} style={{ color: link.platform ? getPlatformColor(link.platform) : 'var(--text-light)' }} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold" style={{ color: 'var(--text)' }}>{link.platform ? getPlatformName(link.platform) : '未知平台'}</p>
                  <p className="text-xs break-all leading-tight" style={{ color: 'var(--text-light)' }}>{link.url}</p>
                  {link.errorMsg && <p className="text-xs mt-1" style={{ color: 'var(--accent-dark)' }}>{link.errorMsg}</p>}
                </div>
                <div className="flex flex-shrink-0 gap-1">
                  {link.status === 'parsing' ? <Loader2 className="w-5 h-5 animate-spin" style={{ color: 'var(--accent)' }} />
                    : link.status === 'success' ? <CheckCircle className="w-5 h-5" style={{ color: 'var(--accent2)' }} />
                    : link.status === 'error' ? (
                      <button onClick={() => handleRetry(link.url)} className="p-1 rounded-lg hover:bg-red-100 transition-colors" title="重试">
                        <RefreshCw className="w-4 h-4" style={{ color: 'var(--accent-dark)' }} />
                      </button>
                    ) : link.isValid && link.platform ? <CheckCircle className="w-5 h-5" style={{ color: 'var(--text-light)' }} />
                    : <AlertCircle className="w-5 h-5" style={{ color: 'var(--accent-dark)' }} />
                  }
                  <button onClick={() => removeLink(index)} className="p-1 rounded-lg hover:bg-gray-200 transition-colors"><X className="w-4 h-4" style={{ color: 'var(--text-light)' }} /></button>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {error && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-3 rounded-xl flex items-center gap-2" style={{ backgroundColor: 'rgba(184,105,77,0.08)', border: '1px solid rgba(184,105,77,0.2)' }}>
          <AlertCircle className="w-4 h-4" style={{ color: 'var(--accent-dark)' }} />
          <span className="text-sm" style={{ color: 'var(--accent-dark)' }}>{error}</span>
        </motion.div>
      )}

      {isParsing && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-5 p-4 rounded-xl" style={{ backgroundColor: 'rgba(212,133,106,0.08)', border: '1px solid rgba(212,133,106,0.2)' }}>
          <div className="flex items-center gap-3 mb-2">
            <Loader2 className="w-5 h-5 animate-spin" style={{ color: 'var(--accent)' }} />
            <span className="text-sm font-semibold" style={{ color: 'var(--accent)' }}>正在解析内容...</span>
          </div>
          <div className="w-full h-2 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--border-light)' }}>
            <motion.div className="h-full rounded-full" style={{ background: 'linear-gradient(135deg, var(--accent), var(--accent-dark))' }} initial={{ width: 0 }} animate={{ width: `${parseProgress}%` }} transition={{ duration: 0.3 }} />
          </div>
          <p className="text-xs mt-1" style={{ color: 'var(--accent)' }}>{parseProgress}% 完成</p>
        </motion.div>
      )}

      <div className="mt-6 flex items-center gap-3">
        {links.length > 0 && (
          <button onClick={clearAll} disabled={isParsing} className="btn-secondary px-5 py-2.5 disabled:opacity-40">清空</button>
        )}
        <button
          onClick={handleSubmit}
          disabled={links.length === 0 || isParsing}
          className="btn-primary flex-1 flex items-center justify-center gap-2 py-2.5 disabled:opacity-40"
        >
          {isParsing ? <><Loader2 className="w-4 h-4 animate-spin" />解析中...</> : <><Link2 className="w-4 h-4" />开始解析 ({links.filter(l => l.isValid && l.platform).length})</>}
        </button>
      </div>
    </motion.div>
  );
}
