import { LayoutGrid, Activity, FolderOpen, Sparkles } from 'lucide-react';

export default function Dashboard() {
  return (
    <main className="space-y-10">
      <section className="glass-card p-8">
        <div className="text-xs uppercase tracking-wider text-textSecondary">Overview</div>
        <h1 className="text-3xl font-bold mt-2">Student Dashboard</h1>
        <p className="text-textSecondary mt-2">Track recent queries, saved questions, and preparation focus areas.</p>
      </section>

      <section className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Companies tracked', value: '18' },
          { label: 'Questions reviewed', value: '142' },
          { label: 'Topics trending', value: '12' },
          { label: 'Docs indexed', value: '64' },
        ].map((s, i) => (
          <div key={i} className="glass-card p-5">
            <div className="text-sm text-textSecondary">{s.label}</div>
            <div className="text-2xl font-bold mt-2 gradient-text">{s.value}</div>
          </div>
        ))}
      </section>

      <section className="grid lg:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <div className="flex items-center gap-2 text-textSecondary"><Activity size={16} /> Recent Activity</div>
          <ul className="mt-4 space-y-2 text-sm text-textSecondary">
            <li>Queried: Most repeated Infosys coding questions</li>
            <li>Saved: SQL joins with examples</li>
            <li>Uploaded: Accenture HR guide (2024)</li>
          </ul>
        </div>
        <div className="glass-card p-6">
          <div className="flex items-center gap-2 text-textSecondary"><FolderOpen size={16} /> Quick Actions</div>
          <div className="mt-4 space-y-2 text-sm text-textSecondary">
            <div className="p-3 rounded-lg border border-white/10 hover:bg-white/5">Upload a new document</div>
            <div className="p-3 rounded-lg border border-white/10 hover:bg-white/5">Ask an AI question</div>
            <div className="p-3 rounded-lg border border-white/10 hover:bg-white/5">View analytics</div>
          </div>
        </div>
      </section>
    </main>
  );
}
