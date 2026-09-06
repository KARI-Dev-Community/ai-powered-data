import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-6 py-20 text-center">
          <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">
            AI-Powered Data & Lead Platform
          </p>
          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl md:text-6xl text-balance">
            Turn local market data into <span className="text-blue-600">warm leads</span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-600 text-balance">
            We accumulate proprietary market history, score business prospects, and deliver ready-to-act leads to Malaysian and Singaporean service businesses — with AI quality control at every step.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="#pricing"
              className="rounded-full bg-blue-600 px-8 py-3 text-base font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
            >
              View pricing
            </Link>
            <Link
              href="#how-it-works"
              className="rounded-full border border-slate-300 px-8 py-3 text-base font-semibold text-slate-700 hover:bg-slate-50"
            >
              How it works
            </Link>
          </div>
          <p className="mt-6 text-sm text-slate-500">
            Free 30-day pilots · No credit card required · Cancel anytime
          </p>
        </div>
      </section>

      {/* Problem */}
      <section className="border-b border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-6xl px-6 py-20">
          <h2 className="text-center text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Local businesses are leaving money on the table
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-lg text-slate-600">
            Most SMBs still rely on word-of-mouth, generic ads, and reactive reputation management. The result is high customer acquisition cost, low conversion, and owner burnout.
          </p>
          <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                title: 'Poor lead quality',
                desc: 'Social ads and directory listings return cold, unqualified prospects that waste time.',
              },
              {
                title: 'Reactive reputation',
                desc: 'Bad reviews sit unanswered for weeks, damaging trust before the owner notices.',
              },
              {
                title: 'Missing market intel',
                desc: 'Owners don’t know competitor pricing, review velocity, or demand trends in their area.',
              },
              {
                title: 'Agency overpromises',
                desc: 'Marketing agencies charge RM1,000–5,000/mo for SEO and ads that don’t track to revenue.',
              },
            ].map((item) => (
              <div key={item.title} className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
                <h3 className="text-lg font-semibold text-slate-900">{item.title}</h3>
                <p className="mt-2 text-slate-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Solution */}
      <section className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-6 py-20">
          <h2 className="text-center text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            One data layer. Three products.
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-lg text-slate-600">
            Everything starts with a proprietary history layer that compounds in value. On top of that, we deliver products that generate revenue immediately.
          </p>
          <div className="mt-16 grid gap-8 lg:grid-cols-3">
            {[
              {
                name: 'Public Data API',
                tag: '#11',
                price: 'RM200–800/mo',
                desc: 'Package proprietary datasets as REST API endpoints. Competitor pricing, market signals, lead enrichment — clean, time-series, and documented.',
                cta: 'Start API trial',
                href: '#pricing',
              },
              {
                name: 'Lead Generation',
                tag: '#17',
                price: 'RM800–2,000/mo',
                desc: 'Scrape local directories, detect pain signals (unanswered reviews, slow sites), score prospects, and deliver warm leads with AI-drafted outreach.',
                cta: 'Get leads',
                href: '#pricing',
              },
              {
                name: 'Review Response',
                tag: '#30',
                price: 'RM800/mo',
                desc: 'Monitor reviews across Google, Facebook, and TripAdvisor. AI drafts responses in the business owner’s voice within 24 hours. Sensitive reviews flagged for approval.',
                cta: 'Start pilot',
                href: '#pricing',
              },
            ].map((product) => (
              <div key={product.name} className="flex flex-col rounded-2xl border border-slate-200 p-8 shadow-sm">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-slate-900">{product.name}</h3>
                  <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                    {product.tag}
                  </span>
                </div>
                <p className="mt-4 text-3xl font-bold text-slate-900">{product.price}</p>
                <p className="mt-4 text-slate-600">{product.desc}</p>
                <Link
                  href={product.href}
                  className="mt-8 block w-full rounded-full bg-blue-600 px-6 py-3 text-center text-sm font-semibold text-white hover:bg-blue-500"
                >
                  {product.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="border-b border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-6xl px-6 py-20">
          <h2 className="text-center text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            How it works
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-lg text-slate-600">
            From raw public data to booked calls in three steps.
          </p>
          <div className="mt-16 grid gap-8 lg:grid-cols-3">
            {[
              {
                step: '01',
                title: 'Collect',
                desc: 'We scrape and archive public market data continuously — Google Maps listings, retailer prices, review velocity, competitor rates. Every snapshot is validated by AI for schema drift and anomalies.',
              },
              {
                step: '02',
                title: 'Score',
                desc: 'Business prospects are scored on observable pain signals: unanswered reviews, slow websites, missing booking systems, and recent openings. Only the hottest leads advance.',
              },
              {
                step: '03',
                title: 'Deliver',
                desc: 'You receive scored leads, API access, or managed review responses — depending on your product. We handle the automation, monitoring, and quality control.',
              },
            ].map((item) => (
              <div key={item.step} className="relative rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <span className="text-5xl font-bold text-blue-100">{item.step}</span>
                <h3 className="mt-4 text-xl font-semibold text-slate-900">{item.title}</h3>
                <p className="mt-2 text-slate-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-6 py-20">
          <h2 className="text-center text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Simple, transparent pricing
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-lg text-slate-600">
            Start free. Upgrade when you see the value. All prices in Malaysian Ringgit (RM).
          </p>
          <div className="mt-16 grid gap-8 lg:grid-cols-3">
            {[
              {
                name: 'Data API',
                price: 'RM200–800/mo',
                features: [
                  '1 dataset included',
                  'REST API with OpenAPI docs',
                  'Time-series queries',
                  '99.5% uptime SLA',
                  'Email support',
                ],
                cta: 'Start free trial',
                href: '#',
              },
              {
                name: 'Lead Generation',
                price: 'RM800–2,000/mo',
                features: [
                  '20–50 scored leads/month',
                  'Pain-signal detection',
                  'AI-drafted outreach',
                  'Weekly CSV / CRM sync',
                  'Dedicated support',
                ],
                cta: 'Book a pilot',
                href: '#',
              },
              {
                name: 'Review Response',
                price: 'RM800/mo',
                features: [
                  'Unlimited review monitoring',
                  'AI responses within 24h',
                  'Approval workflow',
                  'Sentiment reporting',
                  'Dedicated support',
                ],
                cta: 'Start free pilot',
                href: '#',
              },
            ].map((plan) => (
              <div key={plan.name} className="flex flex-col rounded-2xl border border-slate-200 p-8 shadow-sm">
                <h3 className="text-xl font-semibold text-slate-900">{plan.name}</h3>
                <p className="mt-4 text-3xl font-bold text-slate-900">{plan.price}</p>
                <ul className="mt-6 space-y-3">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-start">
                      <span className="mr-2 text-blue-600">✓</span>
                      <span className="text-slate-600">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  href={plan.href}
                  className="mt-8 block w-full rounded-full bg-blue-600 px-6 py-3 text-center text-sm font-semibold text-white hover:bg-blue-500"
                >
                  {plan.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="border-b border-slate-200 bg-slate-50">
        <div className="mx-auto max-w-4xl px-6 py-20">
          <h2 className="text-center text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
            Frequently asked questions
          </h2>
          <div className="mt-16 grid gap-8">
            {[
              {
                q: 'What industries do you cover?',
                a: 'We start with local services — HVAC, plumbing, dental, legal, fitness — in Kuala Lumpur and Singapore. We add new verticals monthly based on demand.',
              },
              {
                q: 'How is your data different from Google Maps or Yelp?',
                a: 'We don’t just list businesses. We accumulate a proprietary time-series history with AI-driven quality signals. A 90-day price history is a commodity; a 3-year history with anomaly detection is a moat.',
              },
              {
                q: 'Do you guarantee leads or results?',
                a: 'No. We guarantee delivery and data quality. We offer free pilots so you can verify quality before paying. Past reply rates have been 15–25%, but results vary by niche and offer.',
              },
              {
                q: 'Is my data safe?',
                a: 'Yes. We process client customer data only to perform the service, delete it on request, and never resell personal contact lists. See our PDPA-compliant data handling clause.',
              },
              {
                q: 'Can I cancel anytime?',
                a: 'Yes. All plans are month-to-month with 30-day notice. No lock-in contracts.',
              },
            ].map((item) => (
              <div key={item.q} className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
                <h3 className="text-lg font-semibold text-slate-900">{item.q}</h3>
                <p className="mt-2 text-slate-600">{item.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-slate-900">
        <div className="mx-auto max-w-6xl px-6 py-20 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Ready to see what your market looks like?
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-300">
            Start with a free 30-day pilot. No credit card. No long-term commitment. Just data and leads.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="#pricing"
              className="rounded-full bg-blue-600 px-8 py-3 text-base font-semibold text-white shadow-sm hover:bg-blue-500"
            >
              Get started
            </Link>
            <Link
              href="mailto:hello@example.com"
              className="rounded-full border border-slate-600 px-8 py-3 text-base font-semibold text-white hover:bg-slate-800"
            >
              Contact sales
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200">
        <div className="mx-auto max-w-6xl px-6 py-12 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-slate-500">
            © {new Date().getFullYear()} Moat Leads. All rights reserved.
          </p>
          <div className="flex gap-6 text-sm text-slate-500">
            <Link href="/privacy" className="hover:text-slate-900">Privacy</Link>
            <Link href="/terms" className="hover:text-slate-900">Terms</Link>
            <Link href="mailto:hello@example.com" className="hover:text-slate-900">Contact</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
