const DEFAULT_BASE_URL = 'http://localhost:8000';

function joinUrl(baseUrl, path) {
  const normalizedBase = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${normalizedBase}${normalizedPath}`;
}

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') ?? '';
  const isJson = contentType.includes('application/json');
  const payload = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const message = typeof payload === 'string' && payload
      ? payload
      : payload?.detail || 'La API devolvio un error.';
    const error = new Error(message);
    error.status = response.status;
    error.payload = payload;
    throw error;
  }

  return payload;
}

export function createApiClient({ baseUrl = DEFAULT_BASE_URL, fetchImpl = fetch } = {}) {
  async function request(path, options = {}) {
    const {
      method = 'GET',
      headers = {},
      token,
      body,
      signal,
    } = options;

    const finalHeaders = new Headers(headers);

    if (token) {
      finalHeaders.set('Authorization', `Bearer ${token}`);
    }

    const response = await fetchImpl(joinUrl(baseUrl, path), {
      method,
      headers: finalHeaders,
      body,
      signal,
    });

    return parseResponse(response);
  }

  return {
    request,
    get(path, options) {
      return request(path, { ...options, method: 'GET' });
    },
    post(path, options) {
      return request(path, { ...options, method: 'POST' });
    },
    put(path, options) {
      return request(path, { ...options, method: 'PUT' });
    },
    delete(path, options) {
      return request(path, { ...options, method: 'DELETE' });
    },
  };
}

export const apiClient = createApiClient({
  baseUrl: import.meta.env.VITE_API_URL ?? DEFAULT_BASE_URL,
});
