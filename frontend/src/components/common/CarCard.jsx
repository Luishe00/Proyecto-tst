export function CarCard({
  car,
  canToggleFavorite = false,
  isFavorite = false,
  isFavoritePending = false,
  onToggleFavorite,
  isInteractive = false,
  onCardClick,
}) {
  function handleFavoriteClick(event) {
    event.stopPropagation();
    if (!onToggleFavorite || isFavoritePending) {
      return;
    }
    onToggleFavorite(car);
  }

  function handleCardClick() {
    if (!isInteractive || !onCardClick) {
      return;
    }
    onCardClick(car);
  }

  function handleCardKeyDown(event) {
    if (!isInteractive || !onCardClick) {
      return;
    }

    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      onCardClick(car);
    }
  }

  return (
    <article
      role={isInteractive ? 'button' : undefined}
      tabIndex={isInteractive ? 0 : undefined}
      onClick={handleCardClick}
      onKeyDown={handleCardKeyDown}
      className={`group overflow-hidden rounded-[2rem] border border-white/70 bg-white/80 shadow-premium backdrop-blur transition duration-300 ${
        isInteractive ? 'cursor-pointer hover:-translate-y-1 hover:border-gold/35 focus:outline-none focus:ring-4 focus:ring-gold/15' : ''
      }`}
    >
      <div className="relative aspect-[4/3] overflow-hidden bg-sand/50">
        <button
          type="button"
          aria-label={isFavorite ? 'Quitar de favoritos' : 'Anadir a favoritos'}
          disabled={!canToggleFavorite || isFavoritePending}
          onClick={handleFavoriteClick}
          className={`absolute right-4 top-4 z-10 inline-flex h-10 w-10 items-center justify-center rounded-full border text-lg backdrop-blur transition ${
            isFavorite
              ? 'border-red-200 bg-red-500/90 text-white'
              : 'border-white/50 bg-black/25 text-white/90'
          } disabled:cursor-not-allowed disabled:opacity-70`}
        >
          {isFavorite ? '♥' : '♡'}
        </button>

        <img
          src={car.imagen_url}
          alt={`${car.marca} ${car.modelo}`}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-ink/55 via-transparent to-transparent" />
        <div className="absolute bottom-4 left-4 flex items-center gap-2 rounded-full border border-white/20 bg-black/20 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-white backdrop-blur-sm">
          <span>Catalogo</span>
          <span className="h-1 w-1 rounded-full bg-gold" />
          <span>#{car.id}</span>
        </div>
      </div>

      <div className="space-y-4 p-6">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">
            {car.marca}
          </p>
          <h2 className="mt-2 font-display text-2xl text-ink">
            {car.modelo}
          </h2>
          <p className="mt-2 text-sm font-semibold text-ink/80">
            {typeof car.precio === 'number' ? `${Number(car.precio).toLocaleString('es-ES')} EUR` : 'Precio no disponible'}
          </p>
        </div>

        <div className="grid grid-cols-3 gap-2 border-t border-ink/10 pt-4 text-xs text-ink/70">
          <div className="rounded-xl bg-white px-3 py-2 text-center">
            <p className="uppercase tracking-[0.12em] text-ink/45">CV</p>
            <p className="mt-1 font-semibold text-ink">{car.cv ?? '-'}</p>
          </div>
          <div className="rounded-xl bg-white px-3 py-2 text-center">
            <p className="uppercase tracking-[0.12em] text-ink/45">Peso</p>
            <p className="mt-1 font-semibold text-ink">{car.peso ?? '-'} kg</p>
          </div>
          <div className="rounded-xl bg-white px-3 py-2 text-center">
            <p className="uppercase tracking-[0.12em] text-ink/45">Vmax</p>
            <p className="mt-1 font-semibold text-ink">{car.velocidad_max ?? '-'} km/h</p>
          </div>
        </div>
      </div>
    </article>
  );
}
