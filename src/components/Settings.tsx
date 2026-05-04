import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Eye, EyeOff, Save, Check, AlertCircle, Loader2, Key, Bot, Globe } from 'lucide-react';
import { getAppSettings, saveAppSettings, AppSettings } from '../utils/api';

const MODEL_DEFAULTS: { field: keyof AppSettings; label: string; icon: string; color: string; desc: string }[] = [
  { field: 'llm_model_name', label: '文本模型', icon: '📝', color: 'bg-blue-100 text-blue-700', desc: '用于摘要、标签、知识点提取' },
  { field: 'asr_model_name', label: '音频模型', icon: '🔊', color: 'bg-orange-100 text-orange-700', desc: '用于语音识别转文字' },
  { field: 'vision_model_name', label: '视觉模型', icon: '👁️', color: 'bg-purple-100 text-purple-700', desc: '用于图片内容理解' },
  { field: 'embedding_model', label: '嵌入模型', icon: '🧮', color: 'bg-pink-100 text-pink-700', desc: '用于文本向量化、语义搜索' },
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
        <div className="bg-white rounded-2xl shadow-sm border p-6 flex items-center justify-center h-64">
          <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-2xl shadow-sm border p-6"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
            <Key className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">API 设置</h1>
            <p className="text-sm text-gray-500">配置阿里百炼 API 及多模态模型</p>
          </div>
        </div>

        <div className="space-y-6">
          <div className="border-b pb-6">
            <h3 className="font-medium text-gray-900 flex items-center gap-2 mb-4">
              <Globe size={18} />
              API Keys
            </h3>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                TikHub API Key
                <span className="text-gray-400 font-normal ml-2">平台内容解析</span>
              </label>
              <div className="relative">
                <input
                  type={showTikhubKey ? 'text' : 'password'}
                  value={form.tikhub_api_key}
                  onChange={(e) => updateField('tikhub_api_key', e.target.value)}
                  placeholder="请输入 TikHub API Key"
                  className="w-full px-4 py-3 pr-12 bg-gray-50 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                />
                <button
                  onClick={() => setShowTikhubKey(!showTikhubKey)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showTikhubKey ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                DashScope API Key
                <span className="text-gray-400 font-normal ml-2">阿里百炼大模型</span>
              </label>
              <div className="relative">
                <input
                  type={showDashscopeKey ? 'text' : 'password'}
                  value={form.dashscope_api_key}
                  onChange={(e) => updateField('dashscope_api_key', e.target.value)}
                  placeholder="请输入阿里百炼 DashScope API Key"
                  className="w-full px-4 py-3 pr-12 bg-gray-50 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                />
                <button
                  onClick={() => setShowDashscopeKey(!showDashscopeKey)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showDashscopeKey ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>
          </div>

          <div>
            <h3 className="font-medium text-gray-900 flex items-center gap-2 mb-4">
              <Bot size={18} />
              模型配置
              <span className="text-xs text-gray-400 font-normal">阿里百炼模型</span>
            </h3>

            <div className="space-y-4">
              {MODEL_DEFAULTS.map(({ field, label, icon, color, desc }) => (
                <div key={field} className="bg-gray-50 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg text-sm font-medium ${color}`}
                      >
                        <span>{icon}</span>
                        <span>{label}</span>
                      </span>
                      <span className="text-xs text-gray-400">{desc}</span>
                    </div>
                  </div>
                  <input
                    type="text"
                    value={form[field]}
                    onChange={(e) => updateField(field, e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg bg-white text-gray-900 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
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
                  ? 'bg-green-50 text-green-700'
                  : saveStatus === 'error'
                    ? 'bg-red-50 text-red-700'
                    : 'bg-blue-50 text-blue-700'
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
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 disabled:opacity-60"
          >
            {saveStatus === 'saving' ? <Loader2 size={18} className="animate-spin" /> : <Save size={18} />}
            保存设置
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}
