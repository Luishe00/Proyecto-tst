import { apiClient } from './api';

function buildLoginBody(credentials) {
  const params = new URLSearchParams();
  params.set('username', credentials.username ?? credentials.email ?? '');
  params.set('password', credentials.password);
  return params;
}

export function createAuthService(client = apiClient) {
  return {
    login(credentials) {
      return client.post('/auth/login', {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: buildLoginBody(credentials),
      });
    },
    getCurrentUser(token) {
      return client.get('/auth/me', { token });
    },
  };
}

export const authService = createAuthService();
