import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Eye, EyeOff, Save, Check, AlertCircle, Loader2, Key, Bot, Shield } from 'lucide-react';
import { getAppSettings, saveAppSettings, AppSettings } from '../utils/api';

const MODEL_DEFAULTS: { field: keyof AppSettings; label: string; icon: string; gradient: string; desc: string }[] = [
  { field: 'llm_model_name', label: '文本模型', icon: '📝', gradient: 'from-blue-500/20 to-cyan-500/20', desc: '用于摘要、标签、知识点提取' },
  { field: 'asr_model_name', label: '音频模型', icon: '🔊', gradient: 'from-orange-500/20 to-orange-500/10', desc: '用于语音识别转文字' },
  { field: 'vision_model_name', label: '视觉模型', icon: '👁️', gradient: 'from-purple-500/20 to-purple-500/10', desc: '用于图片内容理解' },
  { field: 'embedding_model', label: '嵌入模型', icon: '🧮', gradient: 'from-pink-500/20 to-pink-500/10', desc: '用于文本向量化、语义搜索' },
];

export function Settings() {
  const [form, setForm] = useState<AppSettings>({
    tikhub_api_key: '',
    dashscope_api_key: '',
    llm_model_name: 'qwen-plus',
    asr_model_name: 'qwen3-asr-flash',
    vision_model_name: 'qwen3-vl-flash',
    embedding_model: 'text-embedding-v4',
  });
  const [showTikhubKey, setShowTikhubKey] = useState(false);
  const [showDashscopeKey, setShowDashscopeKey] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'success' | 'error'>('idle');
  const [saveMessage, setSaveMessage] = useState('');

  useEffect(() => {
    getAppSettings()
      .then((data) => {
        setForm(data);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  const updateField = (field: keyof AppSettings, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setSaveStatus('saving');
    setSaveMessage('');
    try {
      const result = await saveAppSettings(form);
      setForm(result);
      setSaveStatus('success');
      setSaveMessage('配置已保存并立即生效');
    } catch (e: any) {
      setSaveStatus('error');
      setSaveMessage(e.message || '保存失败');
    }
  };

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto p-4">
        <div className="glass-card flex items-center justify-center h-64">
          <Loader2 className="w-8 h-8 text-blue-400 animate-spin" />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Key className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">API 设置</h1>
              <p className="text-sm text-gray-500">配置阿里百炼 API 及多模态模型</p>
            </div>
          </div>

          <div className="space-y-6">
            <div className="border-b border-white/5 pb-6">
              <h3 className="font-medium text-white flex items-center gap-2 mb-4">
                <Shield size={18} className="text-gray-400" />
                API Keys
              </h3>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  TikHub API Key
                  <span className="text-gray-500 font-normal ml-2">平台内容解析</span>
                </label>
                <div className="relative">
                  <input
                    type={showTikhubKey ? 'text' : 'password'}
                    value={form.tikhub_api_key}
                    onChange={(e) => updateField('tikhub_api_key', e.target.value)}
                    placeholder="请输入 TikHub API Key"
                    className="input-field pr-12"
                  />
                  <button
                    onClick={() => setShowTikhubKey(!showTikhubKey)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white transition-colors"
                  >
                    {showTikhubKey ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  DashScope API Key
                  <span className="text-gray-500 font-normal ml-2">阿里百炼大模型</span>
                </label>
                <div className="relative">
                  <input
                    type={showDashscopeKey ? 'text' : 'password'}
                    value={form.dashscope_api_key}
                    onChange={(e) => updateField('dashscope_api_key', e.target.value)}
                    placeholder="请输入阿里百炼 DashScope API Key"
                    className="input-field pr-12"
                  />
                  <button
                    onClick={() => setShowDashscopeKey(!showDashscopeKey)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white transition-colors"
                  >
                    {showDashscopeKey ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-medium text-white flex items-center gap-2 mb-4">
                <Bot size={18} className="text-gray-400" />
                模型配置
                <span className="text-xs text-gray-500 font-normal">阿里百炼模型</span>
              </h3>

              <div className="space-y-3">
                {MODEL_DEFAULTS.map(({ field, label, icon, gradient, desc }) => (
                  <div key={field} className={`bg-gradient-to-br ${gradient} rounded-xl p-4 border border-white/5`}>
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-base">{icon}</span>
                        <span className="text-sm font-medium text-white">{label}</span>
                        <span className="text-xs text-gray-500">{desc}</span>
                      </div>
                    </div>
                    <input
                      type="text"
                      value={form[field]}
                      onChange={(e) => updateField(field, e.target.value)}
                      className="input-field bg-white/5"
                    />
                  </div>
                ))}
              </div>
            </div>

            {saveStatus !== 'idle' && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className={`flex items-center gap-2 px-4 py-3 rounded-xl ${
                  saveStatus === 'success'
                    ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                    : saveStatus === 'error'
                    ? 'bg-red-500/10 text-red-400 border border-red-500/20'
                    : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                }`}
              >
                {saveStatus === 'saving' ? (
                  <Loader2 size={18} className="animate-spin" />
                ) : saveStatus === 'success' ? (
                  <Check size={18} />
                ) : (
                  <AlertCircle size={18} />
                )}
                <span className="text-sm font-medium">{saveMessage}</span>
              </motion.div>
            )}

            <motion.button
              onClick={handleSave}
              disabled={saveStatus === 'saving'}
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
              className="btn-primary w-full flex items-center justify-center gap-2 py-3 disabled:opacity-40"
            >
              {saveStatus === 'saving' ? <Loader2 size={18} className="animate-spin" /> : <Save size={18} />}
              保存设置
            </motion.button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}