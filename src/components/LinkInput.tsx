import React, { useState, useCallback } from 'react';
import { Link2, Loader2, CheckCircle, AlertCircle, Plus, X, RefreshCw } from 'lucide-react';
import { detectPlatform, getPlatformName, getPlatformIcon, getPlatformColor } from '../utils/platform';
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
      const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';
      const response = await fetch(`${API_BASE_URL}/clean-urls`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_texts: urls }),
      });

      if (!response.ok) {
        throw new Error('链接清理失败');
      }

      const cleanedResults = await response.json();

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
    setHasParsed(true); // 标记已经开始解析
    onSubmit(validUrls);
  }, [links, onSubmit]);

  const clearAll = useCallback(() => {
    setLinks([]);
    setError('');
    setHasParsed(false); // 重置标记
  }, []);

  // 监听解析完成，更新链接状态
  React.useEffect(() => {
    // 只有在已经解析过且当前不是解析状态时才清空
    if (hasParsed && !isParsing && links.length > 0) {
      // 解析完成，更新所有链接状态为 success
      setLinks(prev => prev.map(link => ({
        ...link,
        status: link.status === 'parsing' ? 'success' : link.status
      })));
      
      // 1.5 秒后清空列表
      const timer = setTimeout(() => {
        clearAll();
        onParsingComplete?.();
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, [hasParsed, isParsing, links.length, clearAll, onParsingComplete]);

  return (
    <div className="w-full max-w-2xl mx-auto p-2 sm:p-3">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-4 sm:p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
            <Link2 className="w-5 h-5 text-white" />
          </div>
          <div className="min-w-0">
            <h2 className="text-lg font-semibold text-gray-900">添加收藏链接</h2>
            <p className="text-sm text-gray-500">支持微信公众号、知乎、CSDN、B站、抖音、小红书</p>
          </div>
        </div>

        <div className="space-y-3">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="粘贴链接，每行一个，最多10条..."
            className="w-full h-24 px-4 py-3 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 resize-none text-sm"
            disabled={isParsing}
          />
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-400">已添加 {links.length}/10 条</span>
            <button
              onClick={handleAddLinks}
              disabled={!inputValue.trim() || isParsing || links.length >= 10 || isCleaning}
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
            >
              {isCleaning ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
              {isCleaning ? '清理中...' : '添加'}
            </button>
          </div>
        </div>

        {links.length > 0 && (
          <div className="mt-4 space-y-2">
            {links.map((link, index) => (
              <div
                key={index}
                className={`flex items-start gap-2 sm:gap-3 p-2 sm:p-3 rounded-xl border ${
                  link.status === 'error' ? 'bg-red-50 border-red-200' :
                  link.status === 'success' ? 'bg-green-50 border-green-200' :
                  link.status === 'parsing' ? 'bg-blue-50 border-blue-200' :
                  link.isValid && link.platform ? 'bg-gray-50 border-gray-200' :
                  'bg-red-50 border-red-200'
                }`}
              >
                <i
                  className={`${link.platform ? getPlatformIcon(link.platform) : 'fa-solid fa-link'} text-base sm:text-lg flex-shrink-0 mt-0.5`}
                  style={{ color: link.platform ? getPlatformColor(link.platform) : '#9CA3AF' }}
                />
                <div className="flex-1 min-w-0">
                  <p className="text-xs sm:text-sm font-medium text-gray-900 truncate">
                    {link.platform ? getPlatformName(link.platform) : '未知平台'}
                  </p>
                  <p className="text-xs text-gray-500 break-all leading-tight">{link.url}</p>
                  {link.errorMsg && (
                    <p className="text-xs text-red-500 mt-1">{link.errorMsg}</p>
                  )}
                </div>
                <div className="flex flex-shrink-0 gap-1">
                {link.status === 'parsing' ? (
                  <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
                ) : link.status === 'success' ? (
                  <CheckCircle className="w-5 h-5 text-green-500" />
                ) : link.status === 'error' ? (
                  <button
                    onClick={() => handleRetry(link.url)}
                    className="p-1 hover:bg-red-200 rounded transition-colors"
                    title="重试"
                  >
                    <RefreshCw className="w-4 h-4 text-red-500" />
                  </button>
                ) : link.isValid && link.platform ? (
                  <CheckCircle className="w-5 h-5 text-gray-300" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-red-500" />
                )}
                <button
                  onClick={() => removeLink(index)}
                  className="p-1 hover:bg-gray-200 rounded transition-colors"
                >
                  <X className="w-4 h-4 text-gray-400" />
                </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-500" />
            <span className="text-sm text-red-600">{error}</span>
          </div>
        )}

        {isParsing && (
          <div className="mt-4 p-4 bg-blue-50 rounded-xl">
            <div className="flex items-center gap-3 mb-2">
              <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
              <span className="text-sm font-medium text-blue-700">正在解析内容...</span>
            </div>
            <div className="w-full h-2 bg-blue-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-500 rounded-full transition-all duration-300"
                style={{ width: `${parseProgress}%` }}
              />
            </div>
            <p className="text-xs text-blue-600 mt-1">{parseProgress}% 完成</p>
          </div>
        )}

        <div className="mt-4 sm:mt-6 flex flex-col sm:flex-row items-stretch sm:items-center gap-2 sm:gap-3">
          {links.length > 0 && (
            <button
              onClick={clearAll}
              disabled={isParsing}
              className="px-4 py-2.5 text-gray-600 hover:bg-gray-100 rounded-xl font-medium transition-colors"
            >
              清空
            </button>
          )}
          <button
            onClick={handleSubmit}
            disabled={links.length === 0 || isParsing}
            className="flex-1 py-2.5 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white rounded-xl font-medium transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {isParsing ? (
              <><Loader2 className="w-4 h-4 animate-spin" />解析中...</>
            ) : (
              <><Link2 className="w-4 h-4" />开始解析 ({links.filter(l => l.isValid && l.platform).length})</>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
