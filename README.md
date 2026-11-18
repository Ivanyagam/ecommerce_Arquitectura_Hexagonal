# Tienda Hexagonal (E-commerce)

Aplicación web de comercio electrónico con **Arquitectura Hexagonal**, **Código Limpio**, **Refactoring** y **principios SOLID**.

- **Backend:** Python + Flask + SQLite
- **Frontend:** React (Vite)
- **Problema:** gestionar un catálogo y registrar pedidos descontando stock. Es un buen caso para hexagonal porque la lógica de negocio (reglas de stock, total del pedido) debe sobrevivir a cambios de base de datos, framework web o interfaz.

## Arquitectura (Backend)

```
backend/app
├── domain/            # Núcleo: entidades y reglas (sin dependencias externas)
├── application/
│   ├── ports/         # Puertos de salida (interfaces abstractas de repositorios)
│   └── use_cases/     # Puertos de entrada: ListProducts, CreateProduct, PlaceOrder
├── infrastructure/
│   ├── persistence/   # Adaptador de salida: SQLite
│   └── web/           # Adaptador de entrada: API REST con Flask
└── main.py            # Raíz de composición (inyección de dependencias)
```

Regla de dependencias: `infrastructure → application → domain`. Nunca al revés.
Cambiar SQLite por PostgreSQL = escribir otro adaptador; el dominio y los casos de uso no se tocan.

El frontend replica la idea: `domain/cart.js` (funciones puras), `application/useShop.js` (caso de uso, recibe la API inyectada) e `infrastructure/httpShopApi.js` (adaptador HTTP).

## Evidencia de SOLID

| Principio | Dónde se ve |
|---|---|
| **S** – Responsabilidad única | Cada caso de uso hace una sola cosa; `routes.py` sólo traduce HTTP; los repositorios sólo persisten. |
| **O** – Abierto/Cerrado | Se añade otro repositorio (Postgres, Mongo) sin modificar `PlaceOrder`. |
| **L** – Sustitución de Liskov | `InMemoryProducts` (tests) y `SqliteProductRepository` son intercambiables por `ProductRepository`. |
| **I** – Segregación de interfaces | `ProductRepository` y `OrderRepository` son puertos pequeños y separados. |
| **D** – Inversión de dependencias | `PlaceOrder` depende de abstracciones (`ports/`), que se inyectan en `main.py`. |

## Evidencia de Código Limpio y Refactoring

- Nombres expresivos (`reserve`, `InsufficientStock`), funciones cortas, sin comentarios innecesarios.
- Reglas de negocio dentro de las entidades (`Product.reserve`), no en los controladores.
- **Refactoring aplicado** (ver historial de commits): `PlaceOrder.execute` era un método largo con validaciones y lógica mezcladas → *Extract Method* a `_ensure_not_empty`, `_find_product`, `_reserve_and_add`. Los `if` de errores en la ruta se reemplazaron por un único manejador de `DomainError`.
- Tests unitarios del núcleo con fakes en memoria (sin Flask ni base de datos).

## Ejecutar

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                      # pruebas
python -m app.main          # http://localhost:5000

# Frontend (otra terminal)
cd frontend
npm install
npm run dev                 # http://localhost:5173
```

## API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/products` | Lista productos |
| POST | `/api/products` | Crea producto `{name, price, stock}` |
| POST | `/api/orders` | Crea pedido `{email, items:[{productId, quantity}]}` |

## Mejoras futuras
Unit of Work para confirmar pedido y descuento de stock en una sola transacción; autenticación y pagos como nuevos puertos.
