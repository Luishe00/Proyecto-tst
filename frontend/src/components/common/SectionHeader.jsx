export function SectionHeader({ eyebrow, title, description, align = 'left' }) {
  const alignment = align === 'center' ? 'text-center items-center' : 'text-left items-start';

  return (
    <div className={`flex flex-col gap-3 ${alignment}`}>
      <span className="inline-flex rounded-full border border-gold/30 bg-white/70 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
        {eyebrow}
      </span>
      <h1 className="max-w-3xl font-display text-4xl leading-tight text-ink sm:text-5xl lg:text-6xl">
        {title}
      </h1>
      <p className="max-w-2xl text-sm leading-7 text-ink/70 sm:text-base">
        {description}
      </p>
    </div>
  );
}
