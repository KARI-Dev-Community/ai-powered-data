import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Moat Leads — AI-Powered Data & Lead Platform for Malaysian SMBs',
  description: 'Proprietary market data, scored leads, and AI-driven review management for local service businesses. Built for Malaysia and Singapore.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
