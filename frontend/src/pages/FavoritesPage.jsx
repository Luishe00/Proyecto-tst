import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { CarCard } from '../components/common/CarCard';
import { CarDetailModal } from '../components/common/CarDetailModal';
import { Container } from '../components/common/Container';
import { StatusMessage } from '../components/common/StatusMessage';
import { useAuth } from '../context/AuthContext';
import { favoriteService } from '../services/favoriteService';

export function FavoritesPage({ favoriteServiceInstance = favoriteService }) {
  const { token } = useAuth();
  const [cars, setCars] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [pendingFavoriteId, setPendingFavoriteId] = useState(0);
  const [selectedCar, setSelectedCar] = useState(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);

  useEffect(() => {
    const abortController = new AbortController();

    async function loadFavorites() {
      setIsLoading(true);
      setError('');

      try {
        const response = await favoriteServiceInstance.listFavorites({
          token,
          signal: abortController.signal,
        });
        setCars(response);
      } catch (loadError) {
        if (loadError.name !== 'AbortError') {
          setError(loadError.message || 'No se pudo cargar favoritos.');
        }
      } finally {
        setIsLoading(false);
      }
    }

    loadFavorites();

    return () => {
      abortController.abort();
    };
  }, [favoriteServiceInstance, token]);

  async function handleRemoveFavorite(car) {
    setPendingFavoriteId(car.id);

    try {
      await favoriteServiceInstance.removeFavorite(car.id, { token });
      setCars((current) => current.filter((item) => item.id !== car.id));
      if (selectedCar?.id === car.id) {
        setIsDetailModalOpen(false);
        setSelectedCar(null);
      }
      toast.success('Coche eliminado de favoritos.');
    } catch (removeError) {
      toast.error(removeError.message || 'No se pudo quitar de favoritos.');
    } finally {
      setPendingFavoriteId(0);
    }
  }

  function handleCardClick(car) {
    setSelectedCar(car);
    setIsDetailModalOpen(true);
  }

  return (
    <main className="pb-16 pt-10 sm:pt-14">
      <Container>
        <section className="rounded-[2rem] border border-white/70 bg-white/80 p-6 shadow-premium backdrop-blur sm:p-8">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">
            Mi coleccion
          </p>
          <h1 className="mt-2 font-display text-4xl text-ink">
            Favoritos
          </h1>
          <p className="mt-2 text-sm text-ink/70">
            Gestiona tus coches guardados y elimina los que ya no quieras seguir.
          </p>
        </section>

        <section className="mt-6">
          {error ? (
            <StatusMessage title="No fue posible cargar favoritos" message={error} tone="error" />
          ) : null}

          {!error && isLoading ? (
            <StatusMessage title="Cargando favoritos" message="Sincronizando con tu lista personal." />
          ) : null}

          {!error && !isLoading && cars.length === 0 ? (
            <StatusMessage
              title="Aun no tienes favoritos"
              message="Anade coches desde el catalogo principal para verlos aqui."
            />
          ) : null}

          {!error && !isLoading && cars.length > 0 ? (
            <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
              {cars.map((car) => (
                <CarCard
                  key={car.id}
                  car={car}
                  canToggleFavorite
                  isFavorite
                  isFavoritePending={pendingFavoriteId === car.id}
                  onToggleFavorite={handleRemoveFavorite}
                  isInteractive
                  onCardClick={handleCardClick}
                />
              ))}
            </div>
          ) : null}
        </section>
      </Container>

      <CarDetailModal
        car={selectedCar}
        isOpen={isDetailModalOpen}
        onClose={() => setIsDetailModalOpen(false)}
      />
    </main>
  );
}
