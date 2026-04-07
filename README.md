# 🚀 Premium Cars Platform

Proyecto Fullstack orientado a producto, con foco en mantenibilidad, escalabilidad y una experiencia de usuario premium.

---

## 🏗️ Diseño de Sistema

Este sistema combina dos enfoques arquitectónicos complementarios:

- **Backend**: Arquitectura Hexagonal (Ports & Adapters), que desacopla el dominio de la infraestructura.
- **Frontend**: Arquitectura por Capas (Servicios, Contexto, Componentes, Páginas), para una UI limpia, testeable y extensible.

### Vista de alto nivel

```text
[ Frontend React ]
      |
      | HTTP (REST)
      v
[ API FastAPI ] ---> [ Use Cases ] ---> [ Domain ]
      |                                  |
      v                                  v
[ Adapters ] ----------------------> [ Ports ]
```

---

## ✅ Estado del Proyecto

### Calidad

- **Cobertura de pruebas backend**: **99%** con **Pytest**.
- Suite orientada a validar casos de uso, repositorios y comportamiento de API.
- Base preparada para mantener calidad al escalar funcionalidades.

---

## ⚡ Guía de Ejecución Rápida

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🧠 Funcionalidades de Negocio

- 🔧 **CRUD completo de vehículos (Admin)**
- ❤️ **Sistema de Favoritos persistente (Usuario)**
- 🎯 **Filtros avanzados de alto rendimiento** (Peso, Velocidad, Precio) con acceso protegido para usuarios registrados
- 🖼️ **Galería Premium** con imágenes servidas desde **Cloudinary**

---

## 🧰 Stack Tecnológico

| Capa | Tecnologías | Objetivo |
|---|---|---|
| Backend | Python, FastAPI, Pytest | API robusta, casos de uso y alta cobertura |
| Arquitectura Backend | Hexagonal (Ports & Adapters) | Aislar dominio y facilitar testabilidad |
| Frontend | React, Vite, Tailwind CSS | UI moderna, rápida y mantenible |
| Estado y Rutas | Context API, React Router | Sesión global, protección de rutas y navegación |
| Integraciones | Cloudinary | Gestión de imágenes de catálogo |

---

## 📚 Documentación Extendida

- Backend: [backend/README.md](backend/README.md)
- Frontend: [frontend/README_FRONTEND.md](frontend/README_FRONTEND.md)

---

## 🙌 Créditos

Gracias por revisar este proyecto.

Este repositorio está diseñado con estándares de ingeniería orientados a portfolio profesional: arquitectura clara, responsabilidades bien separadas y foco en evolución sostenible.
