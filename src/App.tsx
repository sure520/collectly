import React, { useState } from 'react';
import { HashRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Auth } from './components/Auth';
import { Dashboard } from './components/Dashboard';
import { LinkInput } from './components/LinkInput';
import { KnowledgeList } from './components/KnowledgeList';
import { KnowledgeCard } from './components/KnowledgeCard';
import Search from './components/Search';
import FilterPanel from './components/FilterPanel';
import { DetailModal } from './components/DetailModal';
import { Stats } from './components/Stats';
import { Settings } from './components/Settings';
import { useAuth } from './hooks/useAuth';
import { useKnowledge } from './hooks/useKnowledge';
import type { KnowledgeItem, SearchFilters, LearningStatus } from './types';
import { getDomainName, getContentTypeName, getDifficultyName } from './utils/format';

function AppContent() {
  const navigate = useNavigate();
  const { user, signOut } = useAuth();
  const { items, stats, loading, parseAndAddItem, semanticSearch, updateItem, deleteItem, fetchItems } = useKnowledge(user?.id);
  const [selectedItem, setSelectedItem] = useState<KnowledgeItem | null>(null);
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [isParsing, setIsParsing] = useState(false);
  const [parseProgress, setParseProgress] = useState(0);
  const [filters, setFilters] = useState<SearchFilters>({});
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<KnowledgeItem[]>([]);
  const [isSemanticSearch, setIsSemanticSearch] = useState(false);

  const handleParseLinks = async (urls: string[]) => {
    console.log('[DEBUG] handleParseLinks 被调用，urls:', urls);
    setIsParsing(true);
    setParseProgress(0);

    for (let i = 0; i < urls.length; i++) {
      const platform = detectPlatform(urls[i]);
      console.log('[DEBUG] 检测平台:', urls[i], '->', platform);
      if (platform) {
        const result = await parseAndAddItem(urls[i], platform);
        console.log('[DEBUG] parseAndAddItem 返回:', result);
      } else {
        console.log('[DEBUG] 未检测到平台，跳过:', urls[i]);
      }
      setParseProgress(Math.round(((i + 1) / urls.length) * 100));
    }

    setIsParsing(false);
    setParseProgress(0);
    console.log('[DEBUG] 解析完成');
  };

  const handleItemClick = (item: KnowledgeItem) => {
    setSelectedItem(item);
    setIsDetailOpen(true);
  };

  const handleUpdateStatus = async (id: string, status: LearningStatus) => {
    await updateItem(id, { status });
    if (selectedItem?.id === id) {
      setSelectedItem(prev => prev ? { ...prev, status } : null);
    }
  };

  const handleUpdateNote = async (id: string, note: string) => {
    await updateItem(id, { note });
    if (selectedItem?.id === id) {
      setSelectedItem(prev => prev ? { ...prev, note } : null);
    }
  };

  const handleDeleteItem = async (id: string) => {
    await deleteItem(id);
    if (selectedItem?.id === id) {
      setIsDetailOpen(false);
    }
  };

  const handleEditItem = (item: KnowledgeItem) => {
    setSelectedItem(item);
    setIsDetailOpen(true);
  };

  const handleSearch = async (query: string, searchFilters: SearchFilters, useSemantic: boolean) => {
    setSearchQuery(query);
    setFilters(searchFilters);
    setIsSemanticSearch(useSemantic);
    navigate('/search');

    if (useSemantic && query) {
      const { data } = await semanticSearch(query, searchFilters);
      setSearchResults(data || []);
    } else {
      await fetchItems(searchFilters, query);
      setSearchResults([]);
    }
  };

  const handleAddClick = () => {
    navigate('/collect');
  };

  const handleSearchClick = () => {
    navigate('/search');
  };

  const displayItems = isSemanticSearch && searchQuery ? searchResults : items;

  return (
    <Layout user={{ email: user?.email || '', nickname: user?.user_metadata?.nickname }}>
      <Routes>
        <Route
          path="/"
          element={
            <Dashboard
              stats={stats}
              recentItems={items.slice(0, 5)}
              onAddClick={handleAddClick}
              onSearchClick={handleSearchClick}
              onItemClick={handleItemClick}
            />
          }
        />
        <Route
          path="/collect"
          element={
            <div className="space-y-6">
              <LinkInput
                onSubmit={handleParseLinks}
                isParsing={isParsing}
                parseProgress={parseProgress}
                onParsingComplete={() => {
                  console.log('[DEBUG] 解析完成，链接列表已清空');
                }}
              />
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {items.map(item => (
                  <KnowledgeCard
                    key={item.id}
                    item={item}
                    onView={handleItemClick}
                    onEdit={handleEditItem}
                    onDelete={handleDeleteItem}
                  />
                ))}
              </div>
            </div>
          }
        />
        <Route
          path="/search"
          element={
            <div className="space-y-4">
              <Search onSearch={handleSearch} loading={loading} />
              <FilterPanel filters={filters} onChange={setFilters} />
              {isSemanticSearch && searchQuery && (
                <div className="text-sm text-blue-600 bg-blue-50 px-4 py-2 rounded-lg">
                  语义检索模式：共找到 {searchResults.length} 条相关结果
                </div>
              )}
              <KnowledgeList
                items={displayItems}
                onItemClick={handleItemClick}
                onStatusChange={handleUpdateStatus}
              />
            </div>
          }
        />
        <Route
          path="/learn"
          element={<Stats stats={stats} />}
        />
        <Route path="/settings" element={<Settings />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      <DetailModal
        item={selectedItem}
        isOpen={isDetailOpen}
        onClose={() => setIsDetailOpen(false)}
        onUpdateStatus={handleUpdateStatus}
        onUpdateNote={handleUpdateNote}
      />
    </Layout>
  );
}

function detectPlatform(url: string): string | null {
  const patterns: Record<string, RegExp> = {
    wechat: /mp\.weixin\.qq\.com/,
    zhihu: /zhihu\.com/,
    csdn: /csdn\.net/,
    bilibili: /bilibili\.com|b23\.tv/,
    douyin: /douyin\.com|iesdouyin\.com/,
    xiaohongshu: /xiaohongshu\.com|xhslink\.com/,
  };

  for (const [platform, pattern] of Object.entries(patterns)) {
    if (pattern.test(url)) {
      return platform;
    }
  }
  return null;
}

function App() {
  // 简化方案：直接显示主界面，绕过认证
  return (
    <HashRouter future={{ v7_startTransition: true }}>
      <AppContent />
    </HashRouter>
  );
}

export default App;
