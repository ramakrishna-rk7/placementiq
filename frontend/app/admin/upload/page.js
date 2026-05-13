'use client';
import { useState } from 'react';
import { UploadCloud, CheckCircle2, XCircle } from 'lucide-react';
import { uploadDocument } from '@/services/api';

export default function AdminUpload() {
  const [file, setFile] = useState(null);
  const [company, setCompany] = useState('');
  const [roundType, setRoundType] = useState('');
  const [topic, setTopic] = useState('');
  const [year, setYear] = useState('2025');
  const [status, setStatus] = useState('');
  const [files, setFiles] = useState([]);

  const submit = async () => {
    if (!file) return;
    setStatus('Uploading...');
    setFiles(prev => [{ name: file.name, status: 'processing' }, ...prev]);
    const res = await uploadDocument({ file, company, round_type: roundType, topic, year });
    if (res.message) {
      setFiles(prev => prev.map(f => f.name === file.name ? { ...f, status: 'completed' } : f));
    } else {
      setFiles(prev => prev.map(f => f.name === file.name ? { ...f, status: 'failed' } : f));
    }
    setStatus(res.message || 'Uploaded');
  };

  return (
    <main className="space-y-10 fade-in">
      <section className="glass-card p-8">
        <h1 className="text-3xl font-bold">Admin Upload</h1>
        <p className="text-textSecondary mt-2">Upload placement documents and tag metadata for retrieval.</p>
      </section>

      <section className="glass-card p-6 space-y-5">
        <div className="border-2 border-dashed border-indigo-500/30 bg-indigo-500/5 rounded-2xl p-8 text-center hover:border-indigo-500/60 hover:bg-indigo-500/10 transition">
          <UploadCloud size={32} className="mx-auto text-indigo-400 animate-pulse" />
          <div className="text-textSecondary mt-2">Drag & drop or click to upload</div>
          <input className="mt-4 w-full text-sm" type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <input className="bg-surface border border-white/10 rounded-xl px-4 py-3" placeholder="Company" value={company} onChange={e => setCompany(e.target.value)} />
          <input className="bg-surface border border-white/10 rounded-xl px-4 py-3" placeholder="Round Type" value={roundType} onChange={e => setRoundType(e.target.value)} />
          <input className="bg-surface border border-white/10 rounded-xl px-4 py-3" placeholder="Topic" value={topic} onChange={e => setTopic(e.target.value)} />
          <input className="bg-surface border border-white/10 rounded-xl px-4 py-3" placeholder="Year" value={year} onChange={e => setYear(e.target.value)} />
        </div>

        <button className="px-6 py-3 rounded-xl text-white font-semibold bg-gradient-to-r from-indigo-500 to-violet-500 hover:brightness-110 transition" onClick={submit}>
          Upload Document
        </button>

        {status && <div className="text-sm text-textSecondary">{status}</div>}

        <div className="mt-6 space-y-3">
          {files.map((f, i) => (
            <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-white/10">
              <div className="text-sm text-textSecondary">{f.name}</div>
              <div className="text-xs flex items-center gap-2">
                {f.status === 'processing' && <span className="px-2 py-1 rounded-full bg-amber-500/20 text-amber-300">Processing</span>}
                {f.status === 'completed' && <span className="px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-300"><CheckCircle2 size={14} className="inline" /> Completed</span>}
                {f.status === 'failed' && <span className="px-2 py-1 rounded-full bg-red-500/20 text-red-300"><XCircle size={14} className="inline" /> Failed</span>}
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
