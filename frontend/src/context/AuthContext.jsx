import {
  createContext,
  useContext,
  useEffect,
  useState,
} from 'react';
import { authService } from '../services/authService';

const AUTH_STORAGE_KEY = 'premium-cars:token';
const AuthContext = createContext(null);

export function AuthProvider({
  children,
  authServiceInstance = authService,
  storage = typeof window !== 'undefined' ? window.localStorage : null,
}) {
  const [token, setToken] = useState(() => storage?.getItem(AUTH_STORAGE_KEY) ?? '');
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoadingUser, setIsLoadingUser] = useState(Boolean(token));

  useEffect(() => {
    let ignore = false;

    async function loadUser() {
      if (!token) {
        setCurrentUser(null);
        setIsLoadingUser(false);
        return;
      }

      setIsLoadingUser(true);

      try {
        const user = await authServiceInstance.getCurrentUser(token);
        if (!ignore) {
          setCurrentUser(user);
        }
      } catch (error) {
        if (!ignore) {
          storage?.removeItem(AUTH_STORAGE_KEY);
          setToken('');
          setCurrentUser(null);
        }
      } finally {
        if (!ignore) {
          setIsLoadingUser(false);
        }
      }
    }

    loadUser();

    return () => {
      ignore = true;
    };
  }, [authServiceInstance, storage, token]);

  async function login(credentials) {
    setIsLoadingUser(true);
    try {
      const response = await authServiceInstance.login(credentials);
      const nextToken = response.access_token;
      storage?.setItem(AUTH_STORAGE_KEY, nextToken);
      setToken(nextToken);
      const user = await authServiceInstance.getCurrentUser(nextToken);
      setCurrentUser(user);
      setIsLoadingUser(false);
      return { ...response, user };
    } catch (error) {
      setIsLoadingUser(false);
      throw error;
    }
  }

  function logout() {
    storage?.removeItem(AUTH_STORAGE_KEY);
    setToken('');
    setCurrentUser(null);
  }

  const value = {
    token,
    currentUser,
    isAuthenticated: Boolean(token),
    isLoadingUser,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }

  return context;
}
