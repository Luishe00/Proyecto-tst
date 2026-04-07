import { apiClient } from './api';

function toCreateCarFormData(carInput) {
  const formData = new FormData();
  formData.set('marca', carInput.marca);
  formData.set('modelo', carInput.modelo);
  formData.set('cv', String(carInput.cv));
  formData.set('peso', String(carInput.peso));
  formData.set('velocidad_max', String(carInput.velocidad_max));
  formData.set('precio', String(carInput.precio));
  formData.set('year', String(carInput.year));
  formData.set('imagen_url', carInput.imagen_url);
  return formData;
}

function buildCarsPath(filters = {}) {
  const params = new URLSearchParams();

  if (filters.marca) {
    params.set('marca', filters.marca);
  }
  if (Number.isFinite(filters.cv) && filters.cv > 0) {
    params.set('cv', String(filters.cv));
  }
  if (Number.isFinite(filters.precio_min) && filters.precio_min >= 0) {
    params.set('precio_min', String(filters.precio_min));
  }
  if (Number.isFinite(filters.precio_max) && filters.precio_max >= 0) {
    params.set('precio_max', String(filters.precio_max));
  }
  if (Number.isFinite(filters.peso_min) && filters.peso_min >= 0) {
    params.set('peso_min', String(filters.peso_min));
  }
  if (Number.isFinite(filters.peso_max) && filters.peso_max >= 0) {
    params.set('peso_max', String(filters.peso_max));
  }
  if (Number.isFinite(filters.velocidad_max) && filters.velocidad_max > 0) {
    params.set('velocidad_max', String(filters.velocidad_max));
  }

  const query = params.toString();
  return query ? `/cars?${query}` : '/cars';
}

function toUpdatePayload(carInput) {
  return {
    marca: carInput.marca.trim(),
    modelo: carInput.modelo.trim(),
    cv: Number(carInput.cv),
    peso: Number(carInput.peso),
    velocidad_max: Number(carInput.velocidad_max),
    precio: Number(carInput.precio),
    year: Number(carInput.year),
    imagen_url: carInput.imagen_url.trim(),
  };
}

export function createCarService(client = apiClient) {
  return {
    listCars({ token, signal, filters } = {}) {
      return client.get(buildCarsPath(filters), { token, signal });
    },
    createCar(carInput, { token } = {}) {
      return client.post('/cars', {
        token,
        body: toCreateCarFormData(carInput),
      });
    },
    updateCar(carId, carInput, { token } = {}) {
      return client.put(`/cars/${carId}`, {
        token,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(toUpdatePayload(carInput)),
      });
    },
    deleteCar(carId, { token } = {}) {
      return client.delete(`/cars/${carId}`, { token });
    },
  };
}

export const carService = createCarService();
