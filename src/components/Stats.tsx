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
import { BookmarkCheck, CheckCircle, Star, Clock } from 'lucide-react';
import type { UserStats } from '../types';

interface StatsProps {
  stats: UserStats | null;
}

const COLORS = ['#d4856a', '#7b6e96', '#5b8a72', '#b8694d', '#7a6e64', '#b0a49a'];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="px-3 py-2 rounded-lg text-xs" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)', boxShadow: '0 4px 12px var(--shadow)' }}>
        <p style={{ color: 'var(--text-light)' }}>{label}</p>
        <p className="font-semibold" style={{ color: 'var(--text)' }}>{payload[0].value}</p>
      </div>
    );
  }
  return null;
};

export function Stats({ stats }: StatsProps) {
  if (!stats) return null;

  const domainData = Object.entries(stats.domain_stats).map(([name, value]) => ({ name, value }));

  const statusData = [
    { name: '未读', value: stats.unread_count, fill: 'var(--text-light)' },
    { name: '已读', value: stats.read_count, fill: 'var(--accent2)' },
    { name: '重点', value: stats.important_count, fill: 'var(--accent-dark)' },
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
    { icon: BookmarkCheck, label: '总收藏', value: stats.total_count, color: 'var(--accent)' },
    { icon: CheckCircle, label: '已学习', value: stats.read_count, color: 'var(--accent2)' },
    { icon: Star, label: '重点标记', value: stats.important_count, color: 'var(--accent-dark)' },
    { icon: Clock, label: '待阅读', value: stats.unread_count, color: 'var(--text-light)' },
  ];

  return (
    <div className="p-4 space-y-8">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ staggerChildren: 0.08 }} className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card, index) => (
          <motion.div
            key={card.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -2 }}
            className="rounded-xl p-6 card-hover"
            style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ backgroundColor: `${card.color}12` }}>
                <card.icon size={18} style={{ color: card.color }} />
              </div>
            </div>
            <p className="text-xs font-semibold uppercase tracking-wider mb-1" style={{ color: 'var(--text-light)' }}>{card.label}</p>
            <p className="serif text-3xl font-bold" style={{ color: 'var(--text)', letterSpacing: '-1px' }}>{card.value}</p>
          </motion.div>
        ))}
      </motion.div>

      <div className="grid lg:grid-cols-2 gap-8">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="rounded-xl p-6" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}>
          <h3 className="serif text-xl font-semibold mb-6" style={{ color: 'var(--text)' }}>领域分布</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={domainData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value" stroke="none">
                {domainData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontSize: '12px', fontWeight: 500 }} formatter={(value: string) => <span style={{ color: 'var(--text-mid)' }}>{value}</span>} />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="rounded-xl p-6" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}>
          <h3 className="serif text-xl font-semibold mb-6" style={{ color: 'var(--text)' }}>学习状态</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-light)" />
              <XAxis dataKey="name" tick={{ fill: 'var(--text-light)', fontSize: 12, fontWeight: 500 }} axisLine={{ stroke: 'var(--border-light)' }} tickLine={false} />
              <YAxis tick={{ fill: 'var(--text-light)', fontSize: 12 }} axisLine={{ stroke: 'var(--border-light)' }} tickLine={false} />
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

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="rounded-xl p-6" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-light)' }}>
        <h3 className="serif text-xl font-semibold mb-6" style={{ color: 'var(--text)' }}>本周学习趋势</h3>
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={trendData}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border-light)" />
            <XAxis dataKey="date" tick={{ fill: 'var(--text-light)', fontSize: 12, fontWeight: 500 }} axisLine={{ stroke: 'var(--border-light)' }} tickLine={false} />
            <YAxis tick={{ fill: 'var(--text-light)', fontSize: 12 }} axisLine={{ stroke: 'var(--border-light)' }} tickLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Line type="monotone" dataKey="count" stroke="var(--accent)" strokeWidth={2.5} dot={{ fill: 'var(--accent)', r: 4, strokeWidth: 0 }} activeDot={{ r: 6, fill: 'var(--accent)' }} />
          </LineChart>
        </ResponsiveContainer>
      </motion.div>
    </div>
  );
}
