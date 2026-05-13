import { ArrowRight, Sparkles, ShieldCheck, Zap } from 'lucide-react';
import MeshBackground from '@/components/MeshBackground';

const features = [
  { icon: Sparkles, title: 'RAG-Powered Retrieval', desc: 'Ask company-specific questions and get high-signal answers instantly.' },
  { icon: Zap, title: 'Semantic Analytics', desc: 'Cluster embeddings to detect real interview trends, not raw counts.' },
  { icon: ShieldCheck, title: 'Verified Sources', desc: 'Citations linked to document pages for trust and accountability.' },
];

export default function Home() {
  return (
    <main className="space-y-20 fade-in">
      <section className="glass-card p-10 md:p-14 relative overflow-hidden">
        <MeshBackground />
        <div className="absolute -top-24 -right-20 h-64 w-64 rounded-full bg-indigo-500/30 blur-3xl float" />
        <div className="absolute -bottom-24 -left-20 h-64 w-64 rounded-full bg-cyan-500/20 blur-3xl float" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(99,102,241,0.15),transparent_40%),radial-gradient(circle_at_80%_30%,rgba(139,92,246,0.15),transparent_45%)]" />

        <div className="relative z-10">
          <div className="inline-flex items-center gap-2 text-xs uppercase tracking-wider text-textSecondary">Premium AI Placement Intelligence</div>
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight leading-tight mt-4">
            <span className="gradient-text">PlacementIQ</span> helps you prepare smarter.
          </h1>
          <p className="text-textSecondary text-lg mt-4 max-w-2xl">
            Centralize company interview materials, retrieve the most repeated questions, and get trusted answers with citations.
          </p>

          <div className="flex flex-wrap gap-3 mt-8">
            <a className="px-6 py-3 rounded-xl text-white font-semibold bg-gradient-to-r from-indigo-500 to-violet-500 shadow-lg shadow-indigo-500/25 hover:brightness-110 transition" href="/query">
              Get Started <ArrowRight className="inline ml-2" size={16} />
            </a>
            <a className="px-6 py-3 rounded-xl border border-white/10 text-textSecondary hover:text-textPrimary hover:bg-white/5 transition" href="/dashboard">
              View Demo
            </a>
          </div>
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-6">
        {features.map((f, i) => (
          <div key={i} className="glass-card p-6 hover:-translate-y-1 transition">
            <f.icon size={24} className="text-secondary" />
            <h3 className="text-lg font-semibold mt-3">{f.title}</h3>
            <p className="text-textSecondary mt-2">{f.desc}</p>
          </div>
        ))}
      </section>
    </main>
  );
}
