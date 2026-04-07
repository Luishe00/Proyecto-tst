import { BrowserRouter, NavLink, Outlet, Route, Routes } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { Container } from './components/common/Container';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './context/AuthContext';
import { AdminPage } from './pages/AdminPage';
import { FavoritesPage } from './pages/FavoritesPage';
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';

function AppShell() {
  const { currentUser, isAuthenticated, logout } = useAuth();

  return (
    <div className="min-h-screen bg-grain">
      <header className="border-b border-ink/10 bg-white/50 backdrop-blur">
        <Container className="flex items-center justify-between py-5">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">
              Frontend React
            </p>
            <p className="mt-2 font-display text-2xl text-ink">
              Premium Cars
            </p>
          </div>
          <div className="flex items-center gap-3">
            <nav className="hidden items-center gap-2 sm:flex">
              <NavLink
                to="/"
                className={({ isActive }) =>
                  `rounded-full px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] transition ${
                    isActive ? 'bg-ink text-white' : 'border border-ink/10 text-ink/70 hover:border-gold/40 hover:text-ink'
                  }`
                }
              >
                Home
              </NavLink>
              <NavLink
                to="/login"
                className={({ isActive }) =>
                  `rounded-full px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] transition ${
                    isActive ? 'bg-ink text-white' : 'border border-ink/10 text-ink/70 hover:border-gold/40 hover:text-ink'
                  }`
                }
              >
                Login
              </NavLink>
              {isAuthenticated ? (
                <NavLink
                  to="/favorites"
                  className={({ isActive }) =>
                    `rounded-full px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] transition ${
                      isActive ? 'bg-ink text-white' : 'border border-ink/10 text-ink/70 hover:border-gold/40 hover:text-ink'
                    }`
                  }
                >
                  Favoritos
                </NavLink>
              ) : null}
              {currentUser?.role === 'admin' ? (
                <NavLink
                  to="/admin"
                  className={({ isActive }) =>
                    `rounded-full px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] transition ${
                      isActive ? 'bg-ink text-white' : 'border border-ink/10 text-ink/70 hover:border-gold/40 hover:text-ink'
                    }`
                  }
                >
                  Admin
                </NavLink>
              ) : null}
            </nav>

            {isAuthenticated ? (
              <div className="hidden items-center gap-3 lg:flex">
                <span className="rounded-full border border-ink/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.16em] text-ink/70">
                  {currentUser?.username ?? 'Sesion activa'}
                </span>
                <button
                  type="button"
                  onClick={logout}
                  className="rounded-full border border-ink/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-ink/70 transition hover:border-gold/40 hover:text-ink"
                >
                  Logout
                </button>
              </div>
            ) : (
              <span className="rounded-full border border-ink/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-ink/70">
                Vite + Tailwind
              </span>
            )}
          </div>
        </Container>
      </header>

      <Outlet />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 2400,
            style: {
              borderRadius: '14px',
              border: '1px solid rgba(24,24,27,0.08)',
              background: '#fff',
              color: '#18181b',
            },
          }}
        />
        <Routes>
          <Route path="/" element={<AppShell />}>
            <Route index element={<HomePage />} />
            <Route path="login" element={<LoginPage />} />
            <Route element={<ProtectedRoute />}>
              <Route path="favorites" element={<FavoritesPage />} />
            </Route>
            <Route element={<ProtectedRoute requireAdmin />}>
              <Route path="admin" element={<AdminPage />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
