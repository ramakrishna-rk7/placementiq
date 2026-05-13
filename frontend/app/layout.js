import './globals.css';
import { Inter } from 'next/font/google';
import Providers from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'PlacementIQ',
  description: 'AI Placement Intelligence System',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`noise ${inter.className}`}>
        <Providers>
          <div className="max-w-[1280px] mx-auto px-6 md:px-8 py-8 md:py-12 relative z-10">
            <div className="fixed top-0 left-0 right-0 z-40 border-b border-white/10 bg-[#0A0A0F]/80 backdrop-blur-md">
              <div className="max-w-[1280px] mx-auto px-6 md:px-8 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="text-lg font-bold tracking-tight">PlacementIQ</div>
                  <div className="text-xs px-3 py-1 rounded-full border border-white/10 text-textSecondary">RAG • Groq Llama-3.3</div>
                </div>
                <div className="hidden md:flex items-center gap-4 text-sm text-textSecondary">
                  <a className="hover:text-textPrimary" href="/">Home</a>
                  <a className="hover:text-textPrimary" href="/dashboard">Dashboard</a>
                  <a className="hover:text-textPrimary" href="/query">AI Query</a>
                  <a className="hover:text-textPrimary" href="/admin/upload">Admin Upload</a>
                  <a className="hover:text-textPrimary" href="/admin/analytics">Analytics</a>
                </div>
              </div>
            </div>

            <div className="pt-20">
              {children}
            </div>

            <div className="text-center text-xs text-textMuted mt-16">PlacementIQ • AI Placement Intelligence System</div>
          </div>
        </Providers>
      </body>
    </html>
  );
}
