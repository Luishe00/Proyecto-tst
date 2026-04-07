import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export function ProtectedRoute({
  requireAdmin = false,
  redirectTo = '/login',
}) {
  const { currentUser, isAuthenticated, isLoadingUser } = useAuth();

  if (isLoadingUser) {
    return null;
  }

  if (!isAuthenticated) {
    return <Navigate to={redirectTo} replace />;
  }

  if (requireAdmin && currentUser?.role !== 'admin') {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
