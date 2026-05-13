'use client';
import { useState } from 'react';
import { Send } from 'lucide-react';

export default function QueryPage() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const submit = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer('');
    setSources([]);

    setHistory(prev => [question, ...prev].slice(0, 8));

    const res = await fetch('http://localhost:18081/query/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });

    if (!res.body) {
      setLoading(false);
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      const parts = buffer.split('\n\n');
      buffer = parts.pop() || '';

      for (const part of parts) {
        if (!part.startsWith('data: ')) continue;
        const payload = part.replace('data: ', '');
        if (payload === '[DONE]') continue;
        try {
          const obj = JSON.parse(payload);
          if (obj.type === 'sources') {
            setSources(obj.items || []);
          } else if (obj.type === 'answer') {
            if (obj.delta) setAnswer(prev => prev + obj.delta);
            if (obj.content) setAnswer(obj.content);
          }
        } catch {}
      }
    }

    setLoading(false);
  };

  return (
    <main className="grid lg:grid-cols-[280px_1fr] gap-6 fade-in">
      <aside className="glass-card p-4 h-fit sticky top-24">
        <div className="text-xs uppercase tracking-wider text-textSecondary">History</div>
        <div className="mt-4 space-y-2 text-sm text-textSecondary">
          {history.length === 0 && <div className="text-textMuted">No queries yet</div>}
          {history.map((h, i) => (
            <div key={i} className="p-2 rounded-lg hover:bg-white/5 cursor-pointer">
              {h}
            </div>
          ))}
        </div>
      </aside>

      <section className="glass-card p-6 flex flex-col min-h-[70vh]">
        <div className="text-lg font-semibold">Chat</div>

        <div className="flex-1 space-y-4 mt-4">
          {answer && (
            <div className="self-start bg-surface/70 border border-white/10 rounded-2xl rounded-tl-sm p-4">
              <p className="text-textSecondary whitespace-pre-wrap">{answer}{loading && <span className="cursor-blink" />}</p>
            </div>
          )}
          {loading && !answer && (
            <div className="self-start bg-surface/70 border border-white/10 rounded-2xl rounded-tl-sm p-4">
              <div className="flex items-center">
                <span className="dot" /><span className="dot" /><span className="dot" />
              </div>
            </div>
          )}
        </div>

        {sources.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {sources.map((s, i) => (
              <span key={i} className="px-3 py-1 text-xs rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition">
                {s.filename || 'Unknown'}{s.page ? ` • p${s.page}` : ''}
              </span>
            ))}
          </div>
        )}

        <div className="mt-6 flex items-center gap-3">
          <input
            className="flex-1 bg-surface border border-white/10 rounded-full px-4 py-3 outline-none focus:ring-2 focus:ring-indigo-500/50"
            placeholder="Ask a question..."
            value={question}
            onChange={e => setQuestion(e.target.value)}
          />
          <button
            className="w-11 h-11 rounded-full bg-gradient-to-r from-indigo-500 to-violet-500 flex items-center justify-center hover:brightness-110 transition active:scale-[0.98]"
            onClick={submit}
            disabled={loading}
          >
            <Send size={18} />
          </button>
        </div>
      </section>
    </main>
  );
}
