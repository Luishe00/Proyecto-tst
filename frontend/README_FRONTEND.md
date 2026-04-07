# 🚀 Frontend Premium Cars

Una SPA construida con **React + Vite + Tailwind CSS** para ofrecer una experiencia de catálogo premium, con una arquitectura limpia que facilita mantenimiento, pruebas y evolución del producto.

---

## 🏗️ Arquitectura del Proyecto

El frontend está organizado por capas para separar responsabilidades y evitar acoplamientos innecesarios.

### 1) Capa de Servicios (`src/services`)
- Centraliza toda la comunicación HTTP con la API.
- Ningún componente visual hace `fetch` directo.
- Expone servicios especializados:
    - `api.js`: cliente base y manejo estándar de errores.
    - `authService.js`: login y obtención de usuario actual.
    - `carService.js`: listado/creación/edición/eliminación de coches.
    - `favoriteService.js`: sincronización de favoritos.

### 2) Capa de Contexto (`src/context`)
- `AuthContext.jsx` gestiona el estado global de sesión.
- Mantiene `token`, `currentUser`, estado de carga y acciones `login/logout`.
- Permite condicionar rutas y comportamiento UI en tiempo real.

### 3) Capa de Componentes (`src/components/common`)
- Componentes reutilizables y orientados a presentación.
- Reciben datos por props y disparan eventos hacia páginas.
- Son fáciles de testear y reutilizar en distintas vistas.

### 4) Capa de Páginas (`src/pages`)
- Orquestan casos de uso completos de interfaz.
- Conectan contexto + servicios + componentes.
- Implementan flujos de negocio (home, login, favoritos, admin).

Esta división hace que el sistema sea **mantenible hoy** y **escalable mañana**.

---

## 🗺️ Mapa de la Estructura de Carpetas

```text
frontend/
├── index.html                  # Entrada HTML de Vite
├── package.json                # Scripts y dependencias (React, Router, Tailwind, Toaster)
├── postcss.config.js           # Pipeline CSS (Tailwind + autoprefixer)
├── tailwind.config.js          # Tema, paleta y utilidades visuales premium
├── vite.config.js              # Configuración del bundler
├── README_FRONTEND.md          # Esta guía
├── dist/                       # Build de producción
└── src/
    ├── main.jsx                # Bootstrap de React + montaje de la app
    ├── App.jsx                 # Router principal, layout y rutas protegidas
    ├── index.css               # Tokens visuales y estilos globales
    ├── services/               # Comunicación con API
    │   ├── api.js              # Cliente HTTP base + normalización de errores
    │   ├── authService.js      # Login + usuario autenticado
    │   ├── carService.js       # Catálogo + CRUD de coches
    │   └── favoriteService.js  # Añadir/quitar/listar favoritos
    ├── context/                # Estado global transversal
    │   └── AuthContext.jsx     # Token, usuario, login, logout, carga inicial
    ├── components/
    │   └── common/             # Bloques reutilizables de UI
    │       ├── CarCard.jsx         # Tarjeta de coche + favoritos + click detalle
    │       ├── CarDetailModal.jsx  # Modal técnico completo del coche
    │       ├── ProtectedRoute.jsx  # Guardia de rutas por autenticación/rol
    │       ├── Container.jsx       # Contenedor responsive consistente
    │       ├── SectionHeader.jsx   # Encabezados de sección reutilizables
    │       └── StatusMessage.jsx   # Estados vacíos, loading y error
    └── pages/                  # Vistas de alto nivel
     ├── HomePage.jsx        # Catálogo, búsqueda y filtros avanzados
     ├── LoginPage.jsx       # Autenticación del usuario
     ├── FavoritesPage.jsx   # Gestión de favoritos
     └── AdminPage.jsx       # CRUD administrativo de coches
```

---

## 🔐 Flujo de Autenticación

El flujo está diseñado para que la seguridad y la UX vayan de la mano:

1. El usuario inicia sesión en `LoginPage`.
2. `AuthContext` guarda `token` y carga el perfil (`currentUser`).
3. `ProtectedRoute` valida sesión/rol antes de renderizar rutas sensibles:
     - `/favorites` requiere login.
     - `/admin` requiere rol `admin`.
4. En `HomePage`, la autenticación condiciona la experiencia:
     - Si no hay sesión, abrir detalles muestra un prompt de acceso.
     - Si no hay sesión, los filtros avanzados se muestran deshabilitados con aviso.
     - Solo si `isAuthenticated === true` se envían parámetros de filtrado al backend.

Resultado: una interfaz clara para invitados, pero con capacidades premium para usuarios autenticados.

---

## 🧩 Componentes Clave

### `CarCard`
- Tarjeta base del catálogo.
- Muestra datos reales (precio, CV, peso, velocidad).
- Permite toggle de favorito con feedback visual y estado pending.

### `FilterPanel` (bloque de filtros avanzados en `HomePage`)
- Panel de filtros por precio, potencia y rendimiento.
- Funciona como módulo de refinamiento de resultados.
- Estado protegido: deshabilitado para invitados con mensaje contextual.

### `CarDetailModal`
- Ficha técnica ampliada con datos clave del vehículo.
- Modal accesible (cierre por overlay y tecla Escape).
- Reutilizado tanto en Home como en Favoritos para coherencia UX.

---

## 🎨 Guía de Estilo

El look & feel se apoya en **Tailwind CSS** con una dirección visual “Premium”:

- Paleta cuidada (`ink`, `mist`, `sand`, `gold`, `pine`).
- Tipografía y espaciado orientados a legibilidad y elegancia.
- Superficies translúcidas, bordes suaves y sombras selectivas.
- Componentes consistentes entre desktop y mobile.

Este enfoque acelera el desarrollo y mantiene una identidad visual sólida sin sacrificar escalabilidad.

---

## ⚙️ Instalación

Desde la carpeta `frontend`:

```bash
npm install
```

---

## ▶️ Ejecución en Desarrollo

```bash
npm run dev
```

Por defecto, la app espera la API en:

```text
http://localhost:8000
```

---

## ✅ ¿Por qué este frontend es mantenible y escalable?

- Separación de responsabilidades por capas.
- Servicios desacoplados de la UI.
- Estado global de auth centralizado y predecible.
- Rutas protegidas por composición (`ProtectedRoute`).
- Componentes reutilizables y fáciles de extender.
- Preparado para crecer con testing, nuevas páginas y nuevos módulos sin rehacer la base.
