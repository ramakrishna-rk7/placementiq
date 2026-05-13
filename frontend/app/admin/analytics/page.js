'use client';
import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

const COLORS = ['#6366F1', '#8B5CF6', '#06B6D4', '#10B981', '#F59E0B'];

export default function Analytics() {
  const [clusters, setClusters] = useState([]);

  useEffect(() => {
    fetch('http://localhost:18081/analytics/semantic-topics')
      .then(r => r.json())
      .then(res => setClusters(res.clusters || []));
  }, []);

  return (
    <main className="space-y-10 fade-in">
      <section className="glass-card p-8">
        <h1 className="text-3xl font-bold">Semantic Analytics</h1>
        <p className="text-textSecondary mt-2">Embedding clusters and trend signals (not raw counts).</p>
      </section>

      <section className="grid lg:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <div className="text-textSecondary text-sm mb-4">Cluster Distribution</div>
          <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={clusters} dataKey="count" nameKey="label" innerRadius={60} outerRadius={90} paddingAngle={4}>
                  {clusters.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-card p-6">
          <div className="text-textSecondary text-sm mb-4">Top Cluster Labels</div>
          <div className="space-y-3">
            {clusters.map((c, i) => (
              <div key={i} className="p-3 rounded-xl bg-white/5 border border-white/10">
                <div className="text-sm font-semibold">{c.label}</div>
                <div className="text-xs text-textSecondary">Docs: {c.count}</div>
                <div className="text-xs text-textMuted">Terms: {c.top_terms?.join(', ')}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="glass-card p-6">
        <div className="text-textSecondary text-sm mb-4">Frequency Bars</div>
        <div style={{ width: '100%', height: 260 }}>
          <ResponsiveContainer>
            <BarChart data={clusters} margin={{ left: 10, right: 10 }}>
              <XAxis dataKey="label" hide />
              <YAxis hide />
              <Tooltip contentStyle={{ background: '#13131F', border: '1px solid rgba(255,255,255,0.1)', color: '#F8FAFC' }} />
              <Bar dataKey="count" radius={[8,8,8,8]} fill="#6366F1" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>
    </main>
  );
}
