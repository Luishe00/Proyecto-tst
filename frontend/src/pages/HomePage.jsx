import { useEffect, useMemo, useState } from 'react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { CarCard } from '../components/common/CarCard';
import { CarDetailModal } from '../components/common/CarDetailModal';
import { Container } from '../components/common/Container';
import { SectionHeader } from '../components/common/SectionHeader';
import { StatusMessage } from '../components/common/StatusMessage';
import { useAuth } from '../context/AuthContext';
import { carService } from '../services/carService';
import { favoriteService } from '../services/favoriteService';

const initialFilters = {
  precio_min: '',
  precio_max: '',
  cv: '',
  peso_min: '',
  peso_max: '',
  velocidad_max: '',
};

function toApiFilters(filters) {
  return {
    precio_min: filters.precio_min === '' ? undefined : Number(filters.precio_min),
    precio_max: filters.precio_max === '' ? undefined : Number(filters.precio_max),
    cv: filters.cv === '' ? undefined : Number(filters.cv),
    peso_min: filters.peso_min === '' ? undefined : Number(filters.peso_min),
    peso_max: filters.peso_max === '' ? undefined : Number(filters.peso_max),
    velocidad_max: filters.velocidad_max === '' ? undefined : Number(filters.velocidad_max),
  };
}

export function HomePage({
  carServiceInstance = carService,
  favoriteServiceInstance = favoriteService,
}) {
  const navigate = useNavigate();
  const { currentUser, isAuthenticated, isLoadingUser, token } = useAuth();
  const [cars, setCars] = useState([]);
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState(initialFilters);
  const [areFiltersOpen, setAreFiltersOpen] = useState(false);
  const [favoriteIds, setFavoriteIds] = useState([]);
  const [pendingFavoriteId, setPendingFavoriteId] = useState(0);
  const [selectedCar, setSelectedCar] = useState(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [isGuestPromptOpen, setIsGuestPromptOpen] = useState(false);
  const [isLoadingCars, setIsLoadingCars] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const abortController = new AbortController();

    async function loadCars() {
      setIsLoadingCars(true);
      setError('');

      try {
        const response = await carServiceInstance.listCars({
          token: isAuthenticated ? token : undefined,
          signal: abortController.signal,
          filters: isAuthenticated ? toApiFilters(filters) : {},
        });
        setCars(response);
      } catch (loadError) {
        if (loadError.name !== 'AbortError') {
          setError(loadError.message || 'No se pudo cargar el catalogo.');
        }
      } finally {
        setIsLoadingCars(false);
      }
    }

    loadCars();

    return () => {
      abortController.abort();
    };
  }, [carServiceInstance, filters, isAuthenticated, token]);

  useEffect(() => {
    const abortController = new AbortController();

    async function loadFavorites() {
      if (!isAuthenticated || !token) {
        setFavoriteIds([]);
        return;
      }

      try {
        const favorites = await favoriteServiceInstance.listFavorites({
          token,
          signal: abortController.signal,
        });
        setFavoriteIds(favorites.map((car) => car.id));
      } catch (favoritesError) {
        if (favoritesError.name !== 'AbortError') {
          toast.error('No se pudieron sincronizar tus favoritos.');
        }
      }
    }

    loadFavorites();

    return () => {
      abortController.abort();
    };
  }, [favoriteServiceInstance, isAuthenticated, token]);

  const visibleCars = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    if (!normalizedQuery) {
      return cars;
    }

    return cars.filter((car) => {
      const model = car.modelo?.toLowerCase() ?? '';
      const brand = car.marca?.toLowerCase() ?? '';
      return model.includes(normalizedQuery) || brand.includes(normalizedQuery);
    });
  }, [cars, query]);

  async function handleToggleFavorite(car) {
    if (!isAuthenticated || !token) {
      toast.error('Inicia sesion para gestionar favoritos.');
      return;
    }

    setPendingFavoriteId(car.id);
    const isFavorite = favoriteIds.includes(car.id);

    try {
      if (isFavorite) {
        await favoriteServiceInstance.removeFavorite(car.id, { token });
        setFavoriteIds((current) => current.filter((id) => id !== car.id));
        toast.success('Coche eliminado de favoritos.');
      } else {
        await favoriteServiceInstance.addFavorite(car.id, { token });
        setFavoriteIds((current) => [...current, car.id]);
        toast.success('Coche anadido a favoritos.');
      }
    } catch (toggleError) {
      toast.error(toggleError.message || 'No se pudo actualizar favoritos.');
    } finally {
      setPendingFavoriteId(0);
    }
  }

  function handleCardClick(car) {
    if (!isAuthenticated) {
      setIsGuestPromptOpen(true);
      return;
    }

    setSelectedCar(car);
    setIsDetailModalOpen(true);
  }

  function handleFilterChange(event) {
    const { name, value } = event.target;
    setFilters((current) => ({ ...current, [name]: value }));
  }

  function handleClearFilters() {
    setFilters(initialFilters);
  }

  return (
    <main className="pb-16">
      <section className="relative overflow-hidden py-10 sm:py-14 lg:py-20">
        <Container>
          <div className="grid gap-10 lg:grid-cols-[1.3fr_0.7fr] lg:items-end">
            <SectionHeader
              eyebrow="Premium Car Catalog"
              title="Un escaparate minimalista para un catalogo de alto rendimiento."
              description="La Home consume el backend desde una capa de servicios aislada, de forma que la UI solo conoce casos de uso sencillos y facilmente testeables."
            />

            <div className="rounded-[2rem] border border-white/70 bg-white/70 p-6 shadow-premium backdrop-blur">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                Estado de sesion
              </p>
              <div className="mt-4 space-y-3 text-sm text-ink/75">
                <p>
                  <span className="font-semibold text-ink">Modo:</span>{' '}
                  {isAuthenticated ? 'Autenticado' : 'Publico'}
                </p>
                <p>
                  <span className="font-semibold text-ink">Usuario:</span>{' '}
                  {currentUser?.username ?? (isLoadingUser ? 'Validando token...' : 'Invitado')}
                </p>
                <p>
                  <span className="font-semibold text-ink">Catalogo cargado:</span>{' '}
                  {isLoadingCars ? 'Sincronizando...' : `${cars.length} coches`}
                </p>
                <p>
                  <span className="font-semibold text-ink">Favoritos:</span>{' '}
                  {isAuthenticated ? `${favoriteIds.length} guardados` : 'Disponible tras login'}
                </p>
              </div>
            </div>
          </div>
        </Container>
      </section>

      <section>
        <Container>
          <div className="mb-6 rounded-[1.6rem] border border-white/70 bg-white/80 p-4 shadow-premium backdrop-blur sm:p-5">
            <label className="mb-2 block text-xs font-semibold uppercase tracking-[0.2em] text-gold" htmlFor="search-cars">
              Busqueda reactiva
            </label>
            <input
              id="search-cars"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Filtrar por marca o modelo..."
              className="w-full rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15"
            />

            <div className="mt-4">
              <button
                type="button"
                onClick={() => setAreFiltersOpen((current) => !current)}
                className="rounded-2xl border border-ink/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-ink/70 transition hover:border-gold/40 hover:text-ink"
              >
                {areFiltersOpen ? 'Ocultar filtros' : 'Mostrar filtros avanzados'}
              </button>
            </div>

            <div
              className={`grid overflow-hidden transition-all duration-300 ${
                areFiltersOpen ? 'mt-4 max-h-[420px] opacity-100' : 'max-h-0 opacity-0'
              }`}
            >
              <div className="relative">
                {!isAuthenticated && (
                  <div className="group absolute inset-0 z-10 cursor-not-allowed rounded-2xl">
                    <span className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 whitespace-nowrap rounded-xl bg-ink px-4 py-2 text-xs font-semibold text-white opacity-0 shadow-lg transition-opacity duration-200 group-hover:opacity-100">
                      Registrate para usar los filtros avanzados
                    </span>
                  </div>
                )}
                <div className={`grid gap-4 rounded-2xl border border-ink/10 bg-white/70 p-4 sm:grid-cols-2 lg:grid-cols-3${!isAuthenticated ? ' pointer-events-none select-none opacity-40' : ''}`}>
                <input
                  name="precio_min"
                  type="number"
                  min="0"
                  value={filters.precio_min}
                  onChange={handleFilterChange}
                  placeholder="Precio minimo"
                  className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15"
                />
                <input
                  name="precio_max"
                  type="number"
                  min="0"
                  value={filters.precio_max}
                  onChange={handleFilterChange}
                  placeholder="Precio maximo"
                  className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15"
                />
                <input
                  name="cv"
                  type="number"
                  min="1"
                  value={filters.cv}
                  onChange={handleFilterChange}
                  placeholder="CV minimo"
                  className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15"
                />
                <input
                  name="peso_min"
                  type="number"
                  min="0"
                  value={filters.peso_min}
                  onChange={handleFilterChange}
                  placeholder="Peso minimo (kg)"
                  className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15"
                />
                <input
                  name="peso_max"
                  type="number"
                  min="0"
                  value={filters.peso_max}
                  onChange={handleFilterChange}
                  placeholder="Peso maximo (kg)"
                  className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15"
                />
                <input
                  name="velocidad_max"
                  type="number"
                  min="1"
                  value={filters.velocidad_max}
                  onChange={handleFilterChange}
                  placeholder="Velocidad minima (km/h)"
                  className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15"
                />

                <div className="sm:col-span-2 lg:col-span-3">
                  <button
                    type="button"
                    onClick={handleClearFilters}
                    className="rounded-2xl border border-ink/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-ink/70 transition hover:border-gold/40 hover:text-ink"
                  >
                    Limpiar filtros
                  </button>
                </div>
                </div>
              </div>
            </div>
          </div>

          {error ? (
            <StatusMessage
              title="No fue posible cargar el catalogo"
              message={error}
              tone="error"
            />
          ) : null}

          {!error && isLoadingCars ? (
            <StatusMessage
              title="Cargando coches premium"
              message="Recuperando el catalogo desde la API para pintar la grid inicial."
            />
          ) : null}

          {!error && !isLoadingCars && visibleCars.length === 0 ? (
            <StatusMessage
              title="Catalogo vacio"
              message={cars.length === 0
                ? 'La API no devolvio coches. Revisa el backend o el estado del seed en memoria.'
                : 'No hay coincidencias para tu busqueda. Prueba con otra marca o modelo.'}
            />
          ) : null}

          {!error && !isLoadingCars && visibleCars.length > 0 ? (
            <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
              {visibleCars.map((car) => (
                <CarCard
                  key={car.id}
                  car={car}
                  canToggleFavorite={isAuthenticated}
                  isFavorite={favoriteIds.includes(car.id)}
                  isFavoritePending={pendingFavoriteId === car.id}
                  onToggleFavorite={handleToggleFavorite}
                  isInteractive
                  onCardClick={handleCardClick}
                />
              ))}
            </div>
          ) : null}
        </Container>
      </section>

      <CarDetailModal
        car={selectedCar}
        isOpen={isDetailModalOpen}
        onClose={() => setIsDetailModalOpen(false)}
      />

      {isGuestPromptOpen ? (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-ink/45 p-4 backdrop-blur-sm"
          onClick={() => setIsGuestPromptOpen(false)}
        >
          <article
            className="w-full max-w-lg rounded-[1.8rem] border border-white/60 bg-white/90 p-6 shadow-premium backdrop-blur sm:p-8"
            onClick={(event) => event.stopPropagation()}
          >
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">
              Acceso premium
            </p>
            <h3 className="mt-3 font-display text-3xl text-ink">
              Inicia sesion para ver la ficha tecnica completa.
            </h3>
            <p className="mt-4 text-sm leading-7 text-ink/75">
              Como invitado puedes explorar el catalogo visual. Para desbloquear datos tecnicos detallados, entra con tu cuenta.
            </p>

            <div className="mt-7 flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() => {
                  setIsGuestPromptOpen(false);
                  navigate('/login');
                }}
                className="rounded-2xl bg-ink px-5 py-3 text-sm font-semibold uppercase tracking-[0.18em] text-white transition hover:bg-pine"
              >
                Ir a login
              </button>
              <button
                type="button"
                onClick={() => setIsGuestPromptOpen(false)}
                className="rounded-2xl border border-ink/10 px-5 py-3 text-sm font-semibold uppercase tracking-[0.18em] text-ink/70 transition hover:border-gold/40 hover:text-ink"
              >
                Seguir explorando
              </button>
            </div>
          </article>
        </div>
      ) : null}
    </main>
  );
}
