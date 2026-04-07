import { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { Container } from '../components/common/Container';
import { useAuth } from '../context/AuthContext';

function validateLoginForm(values) {
  const errors = {};
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const demoUsernamePattern = /^[a-zA-Z0-9_.-]{3,}$/;

  if (!values.email.trim()) {
    errors.email = 'Introduce tu email o identificador de acceso.';
  } else if (
    !emailPattern.test(values.email.trim()) &&
    !demoUsernamePattern.test(values.email.trim())
  ) {
    errors.email = 'Introduce un email valido o un identificador compatible.';
  }

  if (!values.password.trim()) {
    errors.password = 'Introduce tu password.';
  } else if (values.password.trim().length < 6) {
    errors.password = 'La password debe tener al menos 6 caracteres.';
  }

  return errors;
}

export function LoginPage() {
  const navigate = useNavigate();
  const { isAuthenticated, login } = useAuth();
  const [values, setValues] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  function handleChange(event) {
    const { name, value } = event.target;
    setValues((current) => ({ ...current, [name]: value }));
    setErrors((current) => ({ ...current, [name]: '' }));
    setSubmitError('');
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const nextErrors = validateLoginForm(values);

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      return;
    }

    setIsSubmitting(true);
    setSubmitError('');

    try {
      await login({
        email: values.email.trim(),
        password: values.password,
      });
      navigate('/', { replace: true });
    } catch (error) {
      if (error.status === 401) {
        setSubmitError('Credenciales incorrectas. Revisa tus datos e intentalo de nuevo.');
      } else {
        setSubmitError(error.message || 'No se pudo iniciar sesion.');
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="flex min-h-[calc(100vh-88px)] items-center py-10 sm:py-16">
      <Container>
        <div className="mx-auto grid max-w-6xl overflow-hidden rounded-[2rem] border border-white/60 bg-white/70 shadow-premium backdrop-blur lg:grid-cols-[0.95fr_1.05fr]">
          <section className="relative overflow-hidden bg-ink px-8 py-10 text-white sm:px-10 sm:py-12">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(181,138,60,0.28),transparent_30%),linear-gradient(180deg,rgba(24,24,27,0.96),rgba(20,20,24,0.88))]" />
            <div className="relative z-10 flex h-full flex-col justify-between gap-10">
              <div>
                <span className="inline-flex rounded-full border border-white/15 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                  Acceso privado
                </span>
                <h1 className="mt-6 font-display text-4xl leading-tight sm:text-5xl">
                  Entra al catalogo premium con una experiencia limpia y directa.
                </h1>
                <p className="mt-5 max-w-md text-sm leading-7 text-white/72 sm:text-base">
                  El login utiliza la capa de servicios del frontend y delega la persistencia del JWT al contexto de autenticacion.
                </p>
              </div>

              <div className="grid gap-4 text-sm text-white/72 sm:grid-cols-2">
                <div className="rounded-3xl border border-white/10 bg-white/5 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                    Arquitectura
                  </p>
                  <p className="mt-2 leading-6">
                    UI desacoplada de la red y preparada para tests con Vitest.
                  </p>
                </div>
                <div className="rounded-3xl border border-white/10 bg-white/5 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                    Seguridad
                  </p>
                  <p className="mt-2 leading-6">
                    Gestion centralizada del token y consulta del usuario autenticado.
                  </p>
                </div>
              </div>
            </div>
          </section>

          <section className="bg-mist px-8 py-10 sm:px-10 sm:py-12">
            <div className="mx-auto max-w-md">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                Login
              </p>
              <h2 className="mt-4 font-display text-3xl text-ink sm:text-4xl">
                Identificate para desbloquear la vista completa.
              </h2>
              <p className="mt-4 text-sm leading-7 text-ink/70">
                Usa tu email corporativo o el identificador de demo configurado en el backend.
              </p>

              {submitError ? (
                <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm leading-6 text-red-700">
                  {submitError}
                </div>
              ) : null}

              <form className="mt-8 space-y-5" onSubmit={handleSubmit} noValidate>
                <div>
                  <label className="mb-2 block text-sm font-semibold text-ink" htmlFor="email">
                    Email
                  </label>
                  <input
                    id="email"
                    name="email"
                    type="text"
                    value={values.email}
                    onChange={handleChange}
                    autoComplete="username"
                    placeholder="admin o tu@email.com"
                    className="w-full rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm text-ink outline-none transition duration-200 placeholder:text-ink/35 focus:border-gold focus:ring-4 focus:ring-gold/15"
                  />
                  {errors.email ? (
                    <p className="mt-2 text-sm text-red-700">{errors.email}</p>
                  ) : null}
                </div>

                <div>
                  <label className="mb-2 block text-sm font-semibold text-ink" htmlFor="password">
                    Password
                  </label>
                  <input
                    id="password"
                    name="password"
                    type="password"
                    value={values.password}
                    onChange={handleChange}
                    autoComplete="current-password"
                    placeholder="Introduce tu password"
                    className="w-full rounded-2xl border border-ink/10 bg-white px-4 py-3 text-sm text-ink outline-none transition duration-200 placeholder:text-ink/35 focus:border-gold focus:ring-4 focus:ring-gold/15"
                  />
                  {errors.password ? (
                    <p className="mt-2 text-sm text-red-700">{errors.password}</p>
                  ) : null}
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="inline-flex w-full items-center justify-center rounded-2xl bg-ink px-5 py-3 text-sm font-semibold uppercase tracking-[0.18em] text-white transition duration-300 hover:bg-pine disabled:cursor-not-allowed disabled:opacity-65"
                >
                  {isSubmitting ? 'Cargando...' : 'Iniciar sesion'}
                </button>
              </form>
            </div>
          </section>
        </div>
      </Container>
    </main>
  );
}
