import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Lock, Eye, EyeOff, BookOpen } from 'lucide-react';

interface LoginProps {
  onLoginSuccess: (token: string, expiresIn: number) => void;
}

export function Login({ onLoginSuccess }: LoginProps) {
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [checking, setChecking] = useState(true);
  const [needAuth, setNeedAuth] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/auth/status')
      .then(res => res.json())
      .then(data => {
        if (!data.auth_required) {
          onLoginSuccess('', 0);
        } else {
          setNeedAuth(true);
        }
      })
      .catch(() => setNeedAuth(true))
      .finally(() => setChecking(false));
  }, [onLoginSuccess]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!password.trim()) return;

    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });
      const data = await res.json();
      if (res.ok) {
        onLoginSuccess(data.access_token, data.expires_in);
      } else {
        setError(data.detail || '密码错误');
      }
    } catch {
      setError('网络连接失败，请确认后端已启动');
    } finally {
      setLoading(false);
    }
  };

  if (checking) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--bg)' }}>
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 rounded-full animate-spin" style={{ borderColor: 'var(--border-light)', borderTopColor: 'var(--accent)' }} />
          <span className="text-sm" style={{ color: 'var(--text-light)' }}>检查服务状态...</span>
        </div>
      </div>
    );
  }

  if (!needAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--bg)' }}>
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 rounded-full animate-spin" style={{ borderColor: 'var(--border-light)', borderTopColor: 'var(--accent)' }} />
          <span className="text-sm" style={{ color: 'var(--text-light)' }}>无需认证，正在进入...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{ backgroundColor: 'var(--bg)' }}>
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-sm"
      >
        <div className="rounded-2xl p-8" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)', boxShadow: '0 8px 40px var(--shadow)' }}>
          <div className="text-center mb-8">
            <div className="w-16 h-16 rounded-2xl mx-auto mb-4 flex items-center justify-center" style={{ background: 'linear-gradient(135deg, var(--accent), var(--accent-dark))' }}>
              <BookOpen size={28} style={{ color: 'white' }} />
            </div>
            <h1 className="serif text-3xl font-bold" style={{ color: 'var(--text)', letterSpacing: '-0.5px' }}>
              Collect<span style={{ color: 'var(--accent)', fontStyle: 'italic' }}>ly</span>
            </h1>
            <p className="text-sm mt-2" style={{ color: 'var(--text-light)' }}>AI 驱动的知识管家</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider mb-2 block" style={{ color: 'var(--text-light)' }}>访问密码</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2" size={18} style={{ color: 'var(--text-light)' }} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="请输入访问密码"
                  className="input-field"
                  style={{ paddingLeft: '44px', paddingRight: '44px' }}
                  autoFocus
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 transition-colors"
                  style={{ color: 'var(--text-light)' }}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            {error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="p-3 rounded-xl flex items-center gap-2 text-sm"
                style={{ backgroundColor: 'rgba(184,105,77,0.08)', border: '1px solid rgba(184,105,77,0.2)', color: 'var(--accent-dark)' }}
              >
                {error}
              </motion.div>
            )}

            <button type="submit" disabled={loading} className="btn-primary w-full flex items-center justify-center py-3 disabled:opacity-40">
              {loading ? '验证中...' : '进入 Collectly'}
            </button>
          </form>

          <p className="mt-6 text-center text-xs" style={{ color: 'var(--text-light)', opacity: 0.6 }}>
            在 .env 中设置 ACCESS_PASSWORD 可修改密码
          </p>
        </div>

        <p className="text-center mt-6 text-xs" style={{ color: 'var(--text-light)', opacity: 0.4 }}>
          © 2024 Collectly &middot; 你的数据，始终在你手中
        </p>
      </motion.div>
    </div>
  );
}
