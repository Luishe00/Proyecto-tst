export function StatusMessage({ title, message, tone = 'neutral' }) {
  const toneClasses = {
    neutral: 'border-ink/10 bg-white/75 text-ink/70',
    error: 'border-red-200 bg-red-50 text-red-700',
  };

  return (
    <div className={`rounded-3xl border p-6 shadow-premium ${toneClasses[tone]}`}>
      <h2 className="font-display text-2xl text-ink">{title}</h2>
      <p className="mt-2 text-sm leading-7">{message}</p>
    </div>
  );
}
