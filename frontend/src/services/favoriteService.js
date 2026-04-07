import { apiClient } from './api';

export function createFavoriteService(client = apiClient) {
  return {
    listFavorites({ token, signal } = {}) {
      return client.get('/me/favorites', { token, signal });
    },
    addFavorite(carId, { token } = {}) {
      return client.post(`/me/favorites/${carId}`, { token });
    },
    removeFavorite(carId, { token } = {}) {
      return client.delete(`/me/favorites/${carId}`, { token });
    },
  };
}

export const favoriteService = createFavoriteService();
