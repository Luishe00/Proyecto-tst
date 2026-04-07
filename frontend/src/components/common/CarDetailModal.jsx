import { useEffect } from 'react';

function formatCurrency(value) {
  if (typeof value !== 'number') {
    return 'No disponible';
  }

  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(value);
}

export function CarDetailModal({
  car,
  isOpen,
  onClose,
}) {
  useEffect(() => {
    if (!isOpen) {
      return undefined;
    }

    function onKeyDown(event) {
      if (event.key === 'Escape') {
        onClose();
      }
    }

    document.addEventListener('keydown', onKeyDown);
    return () => {
      document.removeEventListener('keydown', onKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen || !car) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/45 p-4 backdrop-blur-sm" onClick={onClose}>
      <article
        className="max-h-[92vh] w-full max-w-5xl overflow-auto rounded-[2rem] border border-white/60 bg-white/90 shadow-premium backdrop-blur"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="grid lg:grid-cols-[1.1fr_0.9fr]">
          <div className="relative min-h-[280px] overflow-hidden bg-sand/50">
            <img
              src={car.imagen_url}
              alt={`${car.marca} ${car.modelo}`}
              className="h-full w-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-ink/60 via-transparent to-transparent" />
            <div className="absolute bottom-4 left-4 rounded-full border border-white/20 bg-black/25 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-white backdrop-blur-sm">
              Ficha tecnica
            </div>
          </div>

          <div className="p-6 sm:p-8">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">
                  {car.marca}
                </p>
                <h2 className="mt-2 font-display text-4xl leading-tight text-ink">
                  {car.modelo}
                </h2>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="rounded-full border border-ink/10 px-3 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-ink/70 transition hover:border-gold/40 hover:text-ink"
              >
                Cerrar
              </button>
            </div>

            <div className="mt-6 grid grid-cols-2 gap-3 text-sm sm:grid-cols-3">
              <div className="rounded-2xl border border-ink/10 bg-white px-4 py-3">
                <p className="text-xs uppercase tracking-[0.16em] text-ink/50">Potencia</p>
                <p className="mt-1 font-semibold text-ink">{car.cv ?? 'No disponible'} CV</p>
              </div>
              <div className="rounded-2xl border border-ink/10 bg-white px-4 py-3">
                <p className="text-xs uppercase tracking-[0.16em] text-ink/50">Peso</p>
                <p className="mt-1 font-semibold text-ink">{car.peso ?? 'No disponible'} kg</p>
              </div>
              <div className="rounded-2xl border border-ink/10 bg-white px-4 py-3">
                <p className="text-xs uppercase tracking-[0.16em] text-ink/50">Velocidad Max.</p>
                <p className="mt-1 font-semibold text-ink">{car.velocidad_max ?? 'No disponible'} km/h</p>
              </div>
              <div className="rounded-2xl border border-ink/10 bg-white px-4 py-3">
                <p className="text-xs uppercase tracking-[0.16em] text-ink/50">Precio</p>
                <p className="mt-1 font-semibold text-ink">{formatCurrency(car.precio)}</p>
              </div>
              <div className="rounded-2xl border border-ink/10 bg-white px-4 py-3">
                <p className="text-xs uppercase tracking-[0.16em] text-ink/50">Ano</p>
                <p className="mt-1 font-semibold text-ink">{car.year ?? 'No disponible'}</p>
              </div>
              <div className="rounded-2xl border border-gold/30 bg-gold/10 px-4 py-3 sm:col-span-2">
                <p className="text-xs uppercase tracking-[0.16em] text-ink/60">Rendimiento destacado</p>
                <p className="mt-1 text-sm font-semibold text-ink">
                  {car.peso ?? 'N/A'} kg · {car.velocidad_max ?? 'N/A'} km/h · {car.cv ?? 'N/A'} CV
                </p>
              </div>
            </div>
          </div>
        </div>
      </article>
    </div>
  );
}
