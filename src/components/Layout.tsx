import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Home,
  Bookmark,
  Search,
  GraduationCap,
  Settings,
  Menu,
  X,
  LogOut,
  Sparkles,
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface LayoutProps {
  children: React.ReactNode;
  onLogout?: () => void;
}

const navItems = [
  { path: '/', icon: Home, label: '首页' },
  { path: '/collect', icon: Bookmark, label: '收藏' },
  { path: '/search', icon: Search, label: '检索' },
  { path: '/learn', icon: GraduationCap, label: '学习' },
  { path: '/settings', icon: Settings, label: '设置' },
];

export function Layout({ children, onLogout }: LayoutProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleNavClick = (path: string) => {
    navigate(path);
    setSidebarOpen(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0a0f] via-[#12121a] to-[#0a0a0f] flex relative overflow-hidden">
      <div className="fixed inset-0 bg-gradient-ambient pointer-events-none" />
      <div className="fixed top-20 left-10 w-72 h-72 bg-blue-500/5 rounded-full blur-3xl animate-float pointer-events-none" />
      <div className="fixed bottom-20 right-20 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl animate-float pointer-events-none" style={{ animationDelay: '-3s' }} />

      <aside className="hidden lg:flex flex-col w-72 h-screen fixed left-0 top-0 z-10 border-r border-white/5 bg-[#0a0a0f]/80 backdrop-blur-xl">
        <div className="p-6 pt-8">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Sparkles size={20} className="text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">Collectly</h1>
              <p className="text-xs text-gray-500">AI 知识管家</p>
            </div>
          </div>

          <nav className="space-y-1">
            {navItems.map((item, index) => {
              const isActive = location.pathname === item.path;
              return (
                <motion.button
                  key={item.path}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  onClick={() => handleNavClick(item.path)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group ${
                    isActive
                      ? 'bg-white/8 text-white shadow-lg shadow-blue-500/10'
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`}
                >
                  {isActive && (
                    <motion.div
                      layoutId="activeNav"
                      className="absolute left-0 w-1 h-8 bg-gradient-to-b from-blue-500 to-purple-500 rounded-r-full"
                      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                    />
                  )}
                  <item.icon size={18} className={isActive ? 'text-blue-400' : 'group-hover:text-white transition-colors'} />
                  {item.label}
                </motion.button>
              );
            })}
          </nav>
        </div>

        <div className="mt-auto p-4 border-t border-white/5">
          <div className="flex items-center gap-3 px-4 py-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold shadow-lg shadow-purple-500/20">
              我
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white">
                个人知识库
              </p>
              <p className="text-xs text-gray-500">单用户模式</p>
            </div>
            {onLogout && (
              <button
                onClick={onLogout}
                className="ml-auto p-2 text-gray-500 hover:text-white hover:bg-white/10 rounded-lg transition-all"
                title="退出登录"
              >
                <LogOut size={16} />
              </button>
            )}
          </div>
        </div>
      </aside>

      <div className="lg:hidden fixed top-0 left-0 right-0 h-16 bg-[#0a0a0f]/90 backdrop-blur-xl border-b border-white/5 z-20 flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Sparkles size={16} className="text-white" />
          </div>
          <span className="text-lg font-bold text-white">Collectly</span>
        </div>
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 text-gray-400 hover:text-white transition-colors"
        >
          {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      <AnimatePresence>
        {sidebarOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden fixed inset-0 bg-black/60 z-30 backdrop-blur-sm"
            />
            <motion.aside
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="lg:hidden fixed left-0 top-0 bottom-0 w-72 bg-[#0a0a0f] z-40 flex flex-col border-r border-white/5"
            >
              <div className="p-6 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                    <Sparkles size={16} className="text-white" />
                  </div>
                  <h1 className="text-lg font-bold text-white">Collectly</h1>
                </div>
                <button onClick={() => setSidebarOpen(false)} className="p-2 text-gray-400 hover:text-white">
                  <X size={20} />
                </button>
              </div>
              <nav className="flex-1 px-4 space-y-1">
                {navItems.map((item) => {
                  const isActive = location.pathname === item.path;
                  return (
                    <button
                      key={item.path}
                      onClick={() => handleNavClick(item.path)}
                      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                        isActive
                          ? 'bg-white/8 text-white'
                          : 'text-gray-400 hover:text-white hover:bg-white/5'
                      }`}
                    >
                      <item.icon size={18} className={isActive ? 'text-blue-400' : ''} />
                      {item.label}
                    </button>
                  );
                })}
              </nav>
              <div className="p-4 border-t border-white/5">
                <div className="flex items-center gap-3 px-4 py-3">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold">
                    我
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white">个人知识库</p>
                  </div>
                  {onLogout && (
                    <button
                      onClick={onLogout}
                      className="ml-auto p-2 text-gray-500 hover:text-white hover:bg-white/10 rounded-lg transition-all"
                    >
                      <LogOut size={16} />
                    </button>
                  )}
                </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      <main className="flex-1 lg:ml-72 pt-16 lg:pt-0 min-h-screen overflow-x-hidden relative z-0">
        <div className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}