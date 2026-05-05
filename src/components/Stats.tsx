import React from 'react';
import { motion } from 'framer-motion';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
} from 'recharts';
import { BookMarked, CheckCircle, Star, Clock } from 'lucide-react';
import type { UserStats } from '../types';

interface StatsProps {
  stats: UserStats | null;
}

const COLORS = ['#4f8fff', '#8b5cf6', '#f472b6', '#22d3ee', '#f97316', '#34d399'];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="glass px-3 py-2 rounded-lg text-xs">
        <p className="text-gray-300">{label}</p>
        <p className="text-white font-medium">{payload[0].value}</p>
      </div>
    );
  }
  return null;
};

export function Stats({ stats }: StatsProps) {
  if (!stats) return null;

  const domainData = Object.entries(stats.domain_stats).map(([name, value]) => ({
    name,
    value,
  }));

  const statusData = [
    { name: '未读', value: stats.unread_count, fill: '#a0a0b0' },
    { name: '已读', value: stats.read_count, fill: '#34d399' },
    { name: '重点', value: stats.important_count, fill: '#f97316' },
  ];

  const trendData = [
    { date: '周一', count: 3 },
    { date: '周二', count: 5 },
    { date: '周三', count: 2 },
    { date: '周四', count: 8 },
    { date: '周五', count: 6 },
    { date: '周六', count: 4 },
    { date: '周日', count: 7 },
  ];

  const statCards = [
    { icon: BookMarked, label: '总收藏', value: stats.total_count, color: '#4f8fff', gradient: 'from-blue-500/20 to-cyan-500/5' },
    { icon: CheckCircle, label: '已学习', value: stats.read_count, color: '#34d399', gradient: 'from-green-500/20 to-green-500/5' },
    { icon: Star, label: '重点标记', value: stats.important_count, color: '#f97316', gradient: 'from-orange-500/20 to-orange-500/5' },
    { icon: Clock, label: '待阅读', value: stats.unread_count, color: '#a0a0b0', gradient: 'from-gray-500/20 to-gray-500/5' },
  ];

  return (
    <div className="p-4 space-y-6">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ staggerChildren: 0.08 }}
        className="grid grid-cols-2 lg:grid-cols-4 gap-4"
      >
        {statCards.map((card, index) => (
          <motion.div
            key={card.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -4, scale: 1.02 }}
            className="glass-card p-5 relative overflow-hidden"
          >
            <div className={`absolute inset-0 bg-gradient-to-br ${card.gradient} opacity-50`} />
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-3">
                <div
                  className="w-10 h-10 rounded-xl flex items-center justify-center"
                  style={{ backgroundColor: `${card.color}20` }}
                >
                  <card.icon size={18} style={{ color: card.color }} />
                </div>
              </div>
              <p className="text-gray-400 text-sm mb-1">{card.label}</p>
              <p className="text-2xl font-bold text-white">{card.value}</p>
            </div>
          </motion.div>
        ))}
      </motion.div>

      <div className="grid lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-card p-6"
        >
          <h3 className="text-lg font-semibold text-white mb-4">领域分布</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie
                data={domainData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
                stroke="none"
              >
                {domainData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend
                wrapperStyle={{ color: '#a0a0b0', fontSize: '12px' }}
                formatter={(value: string) => (
                  <span style={{ color: '#a0a0b0' }}>{value}</span>
                )}
              />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-card p-6"
        >
          <h3 className="text-lg font-semibold text-white mb-4">学习状态</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" tick={{ fill: '#a0a0b0', fontSize: 12 }} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} tickLine={false} />
              <YAxis tick={{ fill: '#a0a0b0', fontSize: 12 }} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {statusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <h3 className="text-lg font-semibold text-white mb-4">本周学习趋势</h3>
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={trendData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="date" tick={{ fill: '#a0a0b0', fontSize: 12 }} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} tickLine={false} />
            <YAxis tick={{ fill: '#a0a0b0', fontSize: 12 }} axisLine={{ stroke: 'rgba(255,255,255,0.1)' }} tickLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="count"
              stroke="#4f8fff"
              strokeWidth={3}
              dot={{ fill: '#4f8fff', r: 5, strokeWidth: 0 }}
              activeDot={{ r: 7, fill: '#4f8fff' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </motion.div>
    </div>
  );
}