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
    <div className="min-h-screen flex" style={{ backgroundColor: 'var(--bg)' }}>
      <aside className="hidden lg:flex flex-col w-64 fixed left-0 top-0 h-screen z-10" style={{ backgroundColor: 'var(--surface)', borderRight: '1px solid var(--border-light)' }}>
        <div className="p-6 pt-8 pb-6" style={{ borderBottom: '1px solid var(--border-light)' }}>
          <h1 className="serif text-2xl font-bold" style={{ color: 'var(--text)', letterSpacing: '-0.5px' }}>
            Collect<span style={{ color: 'var(--accent)', fontStyle: 'italic' }}>ly</span>
          </h1>
          <p className="text-xs font-semibold uppercase tracking-widest mt-1" style={{ color: 'var(--text-light)' }}>
            Your knowledge, curated
          </p>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1">
          {navItems.map((item, index) => {
            const isActive = location.pathname === item.path;
            return (
              <motion.button
                key={item.path}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                onClick={() => handleNavClick(item.path)}
                className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm transition-all"
                style={{
                  color: isActive ? 'var(--text)' : 'var(--text-mid)',
                  backgroundColor: isActive ? 'var(--surface2)' : 'transparent',
                  fontWeight: isActive ? 600 : 500,
                }}
              >
                <item.icon size={18} style={{ opacity: isActive ? 1 : 0.5 }} />
                {item.label}
              </motion.button>
            );
          })}
        </nav>

        <div className="p-4" style={{ borderTop: '1px solid var(--border-light)' }}>
          <div className="flex items-center gap-3 px-2">
            <div className="w-9 h-9 rounded-full flex items-center justify-center text-white text-sm font-bold" style={{ background: 'linear-gradient(135deg, var(--accent), var(--accent-dark))' }}>
              我
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold" style={{ color: 'var(--text)' }}>个人知识库</p>
              <p className="text-xs" style={{ color: 'var(--text-light)' }}>单用户模式</p>
            </div>
            {onLogout && (
              <button
                onClick={onLogout}
                className="p-1.5 rounded-lg transition-colors"
                style={{ color: 'var(--text-light)' }}
                onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--text)')}
                onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-light)')}
                title="退出登录"
              >
                <LogOut size={16} />
              </button>
            )}
          </div>
        </div>
      </aside>

      <div className="lg:hidden fixed top-0 left-0 right-0 h-14 z-20 flex items-center justify-between px-4" style={{ backgroundColor: 'var(--surface)', borderBottom: '1px solid var(--border-light)' }}>
        <div className="flex items-center gap-2">
          <span className="serif text-xl font-bold" style={{ color: 'var(--text)' }}>
            Collect<span style={{ color: 'var(--accent)', fontStyle: 'italic' }}>ly</span>
          </span>
        </div>
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 rounded-lg"
          style={{ color: 'var(--text-mid)' }}
        >
          {sidebarOpen ? <X size={22} /> : <Menu size={22} />}
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
              className="lg:hidden fixed inset-0 z-30"
              style={{ backgroundColor: 'rgba(0,0,0,0.2)' }}
            />
            <motion.aside
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="lg:hidden fixed left-0 top-0 bottom-0 w-64 z-40 flex flex-col"
              style={{ backgroundColor: 'var(--surface)', borderRight: '1px solid var(--border-light)' }}
            >
              <div className="p-5 flex items-center justify-between" style={{ borderBottom: '1px solid var(--border-light)' }}>
                <span className="serif text-xl font-bold" style={{ color: 'var(--text)' }}>
                  Collect<span style={{ color: 'var(--accent)', fontStyle: 'italic' }}>ly</span>
                </span>
                <button onClick={() => setSidebarOpen(false)} className="p-1.5" style={{ color: 'var(--text-mid)' }}>
                  <X size={20} />
                </button>
              </div>
              <nav className="flex-1 px-3 py-4 space-y-1">
                {navItems.map((item) => {
                  const isActive = location.pathname === item.path;
                  return (
                    <button
                      key={item.path}
                      onClick={() => handleNavClick(item.path)}
                      className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all"
                      style={{
                        color: isActive ? 'var(--text)' : 'var(--text-mid)',
                        backgroundColor: isActive ? 'var(--surface2)' : 'transparent',
                        fontWeight: isActive ? 600 : 500,
                      }}
                    >
                      <item.icon size={18} style={{ opacity: isActive ? 1 : 0.5 }} />
                      {item.label}
                    </button>
                  );
                })}
              </nav>
              <div className="p-4" style={{ borderTop: '1px solid var(--border-light)' }}>
                <div className="flex items-center gap-3 px-2">
                  <div className="w-9 h-9 rounded-full flex items-center justify-center text-white text-sm font-bold" style={{ background: 'linear-gradient(135deg, var(--accent), var(--accent-dark))' }}>
                    我
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold" style={{ color: 'var(--text)' }}>个人知识库</p>
                  </div>
                  {onLogout && (
                    <button
                      onClick={onLogout}
                      className="p-1.5 rounded-lg"
                      style={{ color: 'var(--text-light)' }}
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

      <main className="flex-1 lg:ml-64 pt-14 lg:pt-0 min-h-screen">
        <div className="p-5 sm:p-8 lg:p-12 max-w-6xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
