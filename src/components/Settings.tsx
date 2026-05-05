import React from 'react';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Shield, Bell, Palette, Database } from 'lucide-react';

const SETTINGS_CATEGORIES = [
  { icon: Shield, label: '账户安全', description: '密码修改、双重认证', color: 'var(--accent2)' },
  { icon: Bell, label: '通知设置', description: '邮件通知、消息提醒', color: 'var(--accent)' },
  { icon: Palette, label: '外观主题', description: '深色模式、字体大小', color: 'var(--accent3)' },
  { icon: Database, label: '数据管理', description: '导入导出、数据备份', color: 'var(--accent-dark)' },
];

export default function Settings() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-4 space-y-6 max-w-3xl mx-auto"
    >
      <div className="flex items-center gap-4 mb-8">
        <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ background: 'linear-gradient(135deg, var(--accent), var(--accent-dark))' }}>
          <SettingsIcon size={24} style={{ color: 'white' }} />
        </div>
        <div>
          <h2 className="serif text-2xl font-semibold" style={{ color: 'var(--text)' }}>设置</h2>
          <p className="text-sm" style={{ color: 'var(--text-light)' }}>管理你的个性化偏好</p>
        </div>
      </div>

      <div className="grid gap-4">
        {SETTINGS_CATEGORIES.map((item, index) => (
          <motion.div
            key={item.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -2 }}
            className="rounded-xl p-6 card-hover cursor-pointer"
            style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}
          >
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ backgroundColor: `${item.color}12` }}>
                <item.icon size={22} style={{ color: item.color }} />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold" style={{ color: 'var(--text)' }}>{item.label}</h3>
                <p className="text-sm" style={{ color: 'var(--text-light)' }}>{item.description}</p>
              </div>
              <svg className="w-5 h-5" style={{ color: 'var(--text-light)' }} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="rounded-xl p-6" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}>
        <h3 className="serif text-lg font-semibold mb-4" style={{ color: 'var(--text)' }}>账户信息</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between py-3" style={{ borderBottom: '1px solid var(--border-light)' }}>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider mb-0.5" style={{ color: 'var(--text-light)' }}>用户名</p>
              <p className="font-medium" style={{ color: 'var(--text)' }}>user@example.com</p>
            </div>
            <button className="btn-secondary px-4 py-2 text-sm">修改</button>
          </div>
          <div className="flex items-center justify-between py-3" style={{ borderBottom: '1px solid var(--border-light)' }}>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider mb-0.5" style={{ color: 'var(--text-light)' }}>API 密钥</p>
              <p className="font-mono text-sm" style={{ color: 'var(--text-light)' }}>sk-****-****-****</p>
            </div>
            <button className="btn-secondary px-4 py-2 text-sm">重新生成</button>
          </div>
          <div className="flex items-center justify-between py-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider mb-0.5" style={{ color: 'var(--text-light)' }}>数据使用量</p>
              <p className="font-medium" style={{ color: 'var(--text)' }}>42 / 100 条</p>
            </div>
            <div className="w-32 h-2 rounded-full overflow-hidden" style={{ backgroundColor: 'var(--bg-warm)' }}>
              <div className="h-full rounded-full" style={{ width: '42%', background: 'linear-gradient(90deg, var(--accent), var(--accent-dark))' }} />
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
