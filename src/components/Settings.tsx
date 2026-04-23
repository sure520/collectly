import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Eye, EyeOff, Save, Check, AlertCircle, Loader2, Key, Trash2, Star, Bot } from 'lucide-react';

interface ModelConfig {
  id: string;
  name: string;
  modality: 'text' | 'vision' | 'audio' | 'code' | 'math';
  isDefault: boolean;
}

interface ApiConfig {
  apiKey: string;
  models: ModelConfig[];
}

const MODALITY_LABELS: Record<string, { label: string; icon: string; color: string }> = {
  text: { label: '文本', icon: '📝', color: 'bg-blue-100 text-blue-700' },
  vision: { label: '视觉', icon: '👁️', color: 'bg-purple-100 text-purple-700' },
  audio: { label: '音频', icon: '🔊', color: 'bg-orange-100 text-orange-700' },
  code: { label: '代码', icon: '💻', color: 'bg-green-100 text-green-700' },
  math: { label: '数学', icon: '🔢', color: 'bg-pink-100 text-pink-700' },
};

const STORAGE_KEY = 'ai_knowledge_api_config';

export function Settings() {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [models, setModels] = useState<ModelConfig[]>([]);
  const [newModelName, setNewModelName] = useState('');
  const [newModelModality, setNewModelModality] = useState<ModelConfig['modality']>('text');
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'success' | 'error'>('idle');
  const [saveMessage, setSaveMessage] = useState('');

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const config: ApiConfig = JSON.parse(saved);
        setApiKey(config.apiKey || '');
        setModels(config.models || []);
      } catch {}
    }
  }, []);

  const handleAddModel = () => {
    if (!newModelName.trim()) return;
    const newModel: ModelConfig = {
      id: Date.now().toString(),
      name: newModelName.trim(),
      modality: newModelModality,
      isDefault: !models.some(m => m.modality === newModelModality),
    };
    setModels([...models, newModel]);
    setNewModelName('');
  };

  const handleDeleteModel = (id: string) => {
    const model = models.find(m => m.id === id);
    const newModels = models.filter(m => m.id !== id);
    if (model?.isDefault) {
      const sameModality = newModels.find(m => m.modality === model.modality);
      if (sameModality) sameModality.isDefault = true;
    }
    setModels(newModels);
  };

  const handleSetDefault = (id: string) => {
    const model = models.find(m => m.id === id);
    if (!model) return;
    setModels(models.map(m => ({
      ...m,
      isDefault: m.modality === model.modality ? m.id === id : m.isDefault,
    })));
  };

  const handleSave = async () => {
    if (!apiKey.trim()) {
      setSaveStatus('error');
      setSaveMessage('请输入 API Key');
      return;
    }
    setSaveStatus('saving');
    try {
      const config: ApiConfig = { apiKey: apiKey.trim(), models };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(config));
      setSaveStatus('success');
      setSaveMessage('配置已保存');
    } catch {
      setSaveStatus('error');
      setSaveMessage('保存失败');
    }
  };

  const getModelsByModality = (modality: string) => models.filter(m => m.modality === modality);

  return (
    <div className="max-w-3xl mx-auto p-4">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-white rounded-2xl shadow-sm border p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
            <Key className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">API 设置</h1>
            <p className="text-sm text-gray-500">配置多模态模型</p>
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">API Key</label>
            <div className="relative">
              <input
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="请输入阿里百炼 API Key"
                className="w-full px-4 py-3 pr-12 bg-gray-50 border rounded-xl focus:ring-2 focus:ring-blue-500"
              />
              <button onClick={() => setShowKey(!showKey)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                {showKey ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <div className="border-t pt-6">
            <h3 className="font-medium text-gray-900 flex items-center gap-2 mb-4">
              <Bot size={18} />
              模型配置
            </h3>

            <div className="bg-gray-50 rounded-xl p-4 mb-4">
              <div className="text-sm font-medium text-gray-700 mb-3">添加新模型</div>
              <div className="flex gap-3">
                <input
                  type="text"
                  value={newModelName}
                  onChange={(e) => setNewModelName(e.target.value)}
                  placeholder="模型名称，如 qwen-vl-max"
                  className="flex-1 px-3 py-2 border rounded-lg"
                />
                <select
                  value={newModelModality}
                  onChange={(e) => setNewModelModality(e.target.value as ModelConfig['modality'])}
                  className="px-3 py-2 border rounded-lg"
                >
                  {Object.entries(MODALITY_LABELS).map(([key, { label }]) => (
                    <option key={key} value={key}>{label}</option>
                  ))}
                </select>
                <button onClick={handleAddModel} className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">添加</button>
              </div>
            </div>

            <div className="space-y-4">
              {Object.entries(MODALITY_LABELS).map(([modality, { label, icon, color }]) => {
                const modalityModels = getModelsByModality(modality);
                if (modalityModels.length === 0) return null;
                return (
                  <div key={modality} className="bg-gray-50 rounded-xl p-4">
                    <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg text-sm font-medium mb-3 ${color}`}>
                      <span>{icon}</span>
                      <span>{label}</span>
                    </div>
                    <div className="space-y-2">
                      {modalityModels.map((model) => (
                        <div key={model.id} className="flex items-center justify-between bg-white p-3 rounded-lg border">
                          <div className="flex items-center gap-2">
                            <span className="font-medium text-gray-900">{model.name}</span>
                            {model.isDefault && (
                              <span className="px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full flex items-center gap-1">
                                <Star size={10} />
                                默认
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-2">
                            {!model.isDefault && (
                              <button onClick={() => handleSetDefault(model.id)} className="text-xs text-blue-600 hover:underline">设为默认</button>
                            )}
                            <button onClick={() => handleDeleteModel(model.id)} className="p-1.5 text-red-500 hover:bg-red-50 rounded-lg">
                              <Trash2 size={16} />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
              {models.length === 0 && (
                <div className="text-center py-8 text-gray-400">暂无模型配置，请在上方添加</div>
              )}
            </div>
          </div>

          {saveStatus !== 'idle' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className={`flex items-center gap-2 px-4 py-3 rounded-xl ${
              saveStatus === 'success' ? 'bg-green-50 text-green-700' : saveStatus === 'error' ? 'bg-red-50 text-red-700' : 'bg-blue-50 text-blue-700'
            }`}>
              {saveStatus === 'saving' ? <Loader2 size={18} className="animate-spin" /> : saveStatus === 'success' ? <Check size={18} /> : <AlertCircle size={18} />}
              <span className="text-sm font-medium">{saveMessage}</span>
            </motion.div>
          )}

          <motion.button
            onClick={handleSave}
            disabled={saveStatus === 'saving'}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white font-medium rounded-xl"
          >
            {saveStatus === 'saving' ? <Loader2 size={18} className="animate-spin" /> : <Save size={18} />}
            保存设置
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}