import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { Container } from '../components/common/Container';
import { useAuth } from '../context/AuthContext';
import { carService } from '../services/carService';

const emptyForm = {
  marca: '',
  modelo: '',
  cv: '',
  peso: '',
  velocidad_max: '',
  precio: '',
  year: '',
  imagen_url: '',
};

function toPayload(formValues) {
  return {
    marca: formValues.marca.trim(),
    modelo: formValues.modelo.trim(),
    cv: Number(formValues.cv),
    peso: Number(formValues.peso),
    velocidad_max: Number(formValues.velocidad_max),
    precio: Number(formValues.precio),
    year: Number(formValues.year),
    imagen_url: formValues.imagen_url.trim(),
  };
}

function sortByIdAsc(cars) {
  return [...cars].sort((a, b) => a.id - b.id);
}

export function AdminPage({
  carServiceInstance = carService,
}) {
  const { token } = useAuth();
  const [cars, setCars] = useState([]);
  const [isLoadingCars, setIsLoadingCars] = useState(true);
  const [loadError, setLoadError] = useState('');
  const [formValues, setFormValues] = useState(emptyForm);
  const [editingCarId, setEditingCarId] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState(0);

  useEffect(() => {
    let ignore = false;

    async function loadCars() {
      setIsLoadingCars(true);
      setLoadError('');

      try {
        const response = await carServiceInstance.listCars({ token });
        if (!ignore) {
          setCars(sortByIdAsc(response));
        }
      } catch (error) {
        if (!ignore) {
          setLoadError(error.message || 'No se pudo cargar el inventario.');
        }
      } finally {
        if (!ignore) {
          setIsLoadingCars(false);
        }
      }
    }

    loadCars();

    return () => {
      ignore = true;
    };
  }, [carServiceInstance, token]);

  function handleInputChange(event) {
    const { name, value } = event.target;
    setFormValues((current) => ({ ...current, [name]: value }));
  }

  async function handleDeleteCar(carId) {
    setPendingDeleteId(carId);
    try {
      await carServiceInstance.deleteCar(carId, { token });
      setCars((current) => current.filter((car) => car.id !== carId));
      toast.success('Coche eliminado del catalogo.');
    } catch (error) {
      toast.error(error.message || 'No se pudo eliminar el coche.');
    } finally {
      setPendingDeleteId(0);
    }
  }

  function beginEdit(car) {
    setEditingCarId(car.id);
    setFormValues({
      marca: car.marca ?? '',
      modelo: car.modelo ?? '',
      cv: String(car.cv ?? ''),
      peso: String(car.peso ?? ''),
      velocidad_max: String(car.velocidad_max ?? ''),
      precio: String(car.precio ?? ''),
      year: String(car.year ?? ''),
      imagen_url: car.imagen_url ?? '',
    });
  }

  function cancelEdit() {
    setEditingCarId(0);
    setFormValues(emptyForm);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsSubmitting(true);

    try {
      const payload = toPayload(formValues);

      if (editingCarId) {
        const updatedCar = await carServiceInstance.updateCar(editingCarId, payload, { token });
        setCars((current) => current.map((car) => (car.id === editingCarId ? updatedCar : car)));
        toast.success('Coche actualizado correctamente.');
        cancelEdit();
      } else {
        const createdCar = await carServiceInstance.createCar(payload, { token });
        setCars((current) => sortByIdAsc([...current, createdCar]));
        setFormValues(emptyForm);
        toast.success('Nuevo coche anadido al catalogo.');
      }
    } catch (error) {
      toast.error(error.message || 'No se pudo guardar el coche.');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="pb-16 pt-10 sm:pt-14">
      <Container>
        <section className="rounded-[2rem] border border-white/70 bg-white/80 p-6 shadow-premium backdrop-blur sm:p-8">
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                Admin Panel
              </p>
              <h1 className="mt-2 font-display text-4xl text-ink">
                Gestion del catalogo
              </h1>
              <p className="mt-2 text-sm text-ink/70">
                {cars.length} coches activos en el inventario.
              </p>
            </div>
          </div>

          <div className="mt-8 overflow-x-auto rounded-2xl border border-ink/10">
            <table className="min-w-full divide-y divide-ink/10 text-left text-sm">
              <thead className="bg-ink/5 text-xs uppercase tracking-[0.12em] text-ink/60">
                <tr>
                  <th className="px-4 py-3">ID</th>
                  <th className="px-4 py-3">Marca</th>
                  <th className="px-4 py-3">Modelo</th>
                  <th className="px-4 py-3">Precio</th>
                  <th className="px-4 py-3">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-ink/10 bg-white/60 text-ink/80">
                {isLoadingCars ? (
                  <tr>
                    <td colSpan={5} className="px-4 py-6 text-center text-ink/60">
                      Cargando inventario...
                    </td>
                  </tr>
                ) : null}
                {!isLoadingCars && loadError ? (
                  <tr>
                    <td colSpan={5} className="px-4 py-6 text-center text-red-700">
                      {loadError}
                    </td>
                  </tr>
                ) : null}
                {cars.map((car) => (
                  <tr key={car.id}>
                    <td className="px-4 py-3 font-semibold">#{car.id}</td>
                    <td className="px-4 py-3">{car.marca}</td>
                    <td className="px-4 py-3">{car.modelo}</td>
                    <td className="px-4 py-3">{Number(car.precio).toLocaleString('es-ES')} EUR</td>
                    <td className="px-4 py-3">
                      <div className="flex flex-wrap gap-2">
                        <button
                          type="button"
                          onClick={() => beginEdit(car)}
                          className="rounded-full border border-ink/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.12em] text-ink/70 transition hover:border-gold/40 hover:text-ink"
                        >
                          Editar
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDeleteCar(car.id)}
                          disabled={pendingDeleteId === car.id}
                          className="rounded-full border border-red-200 px-4 py-2 text-xs font-semibold uppercase tracking-[0.12em] text-red-700 transition hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                          {pendingDeleteId === car.id ? 'Eliminando...' : 'Eliminar'}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="mt-8 rounded-[2rem] border border-white/70 bg-white/80 p-6 shadow-premium backdrop-blur sm:p-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <h2 className="font-display text-3xl text-ink">
              {editingCarId ? `Editar coche #${editingCarId}` : 'Anadir Nuevo'}
            </h2>
            {editingCarId ? (
              <button
                type="button"
                onClick={cancelEdit}
                className="rounded-2xl border border-ink/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-ink/70 transition hover:border-gold/40 hover:text-ink"
              >
                Cancelar edicion
              </button>
            ) : null}
          </div>

          <form className="mt-6 grid gap-4 sm:grid-cols-2 transition-all duration-300" onSubmit={handleSubmit}>
            <input name="marca" value={formValues.marca} onChange={handleInputChange} required placeholder="Marca" className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15" />
            <input name="modelo" value={formValues.modelo} onChange={handleInputChange} required placeholder="Modelo" className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15" />
            <input name="cv" type="number" value={formValues.cv} onChange={handleInputChange} required min="1" placeholder="CV" className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15" />
            <input name="peso" type="number" value={formValues.peso} onChange={handleInputChange} required min="1" placeholder="Peso" className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15" />
            <input name="velocidad_max" type="number" value={formValues.velocidad_max} onChange={handleInputChange} required min="1" placeholder="Velocidad maxima" className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15" />
            <input name="precio" type="number" step="0.01" value={formValues.precio} onChange={handleInputChange} required min="1" placeholder="Precio" className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15" />
            <input name="year" type="number" value={formValues.year} onChange={handleInputChange} required min="1886" placeholder="Ano" className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15" />
            <input name="imagen_url" value={formValues.imagen_url} onChange={handleInputChange} required placeholder="URL de imagen" className="rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm outline-none transition focus:border-gold focus:ring-4 focus:ring-gold/15" />

            <div className="sm:col-span-2">
              <button
                type="submit"
                disabled={isSubmitting}
                className="inline-flex items-center justify-center rounded-2xl bg-ink px-6 py-3 text-sm font-semibold uppercase tracking-[0.16em] text-white transition hover:bg-pine disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isSubmitting
                  ? 'Guardando...'
                  : editingCarId
                    ? 'Guardar cambios'
                    : 'Anadir nuevo coche'}
              </button>
            </div>
          </form>
        </section>
      </Container>
    </main>
  );
}
