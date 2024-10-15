# Instrucciones para levantar el servicio

Este proyecto consta de dos partes: un **backend** construido con Python y un **frontend** construido con Next.js.

## Backend

El backend se levanta utilizando Docker. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.

### Pasos para iniciar el backend:

1. Navega al directorio del backend:

   ```bash
   cd backend
   ```

2. Construye y levanta los contenedores Docker:

   ```bash
   docker-compose up --build
   ```

   Esto iniciará el servicio y lo pondrá a escuchar en el puerto configurado (por defecto, el puerto `8000`).

Para más detalles y documentación del backend, consulta el archivo `backend/README.md`.

## Frontend

El frontend se inicia utilizando `npm`. Necesitas tener instalado Node.js y npm.

### Pasos para iniciar el frontend:

1. Navega al directorio del frontend:

   ```bash
   cd frontend
   ```

2. Instala las dependencias:

   ```bash
   npm install
   ```

3. Inicia el servidor de desarrollo:

   ```bash
   npm run dev
   ```

   El frontend estará disponible en `http://localhost:3000`.

## Notas adicionales

- Asegúrate de que el backend esté corriendo antes de iniciar el frontend, ya que este último consume la API del backend.


¡Listo! Con estos pasos, deberías poder levantar tanto el backend como el frontend y comenzar a trabajar en el proyecto.
### Endpoints del Backend

El backend ofrece los siguientes endpoints:

- **GET `/books`**

  Obtiene una lista de libros basada en los criterios de búsqueda proporcionados.

  **Parámetros de consulta:**

  - `list` (opcional): Código de la lista de libros a consultar (por defecto, `combined-print-fiction`).
  - `offset` (opcional): Desplazamiento para paginación de resultados.

  **Respuesta exitosa:**

  - Código 200: Retorna una lista de libros según los criterios especificados.

- **GET `/books/genres`**

  Obtiene una lista de géneros disponibles.

  **Respuesta exitosa:**

  - Código 200: Retorna una lista de géneros con sus códigos y nombres de visualización.

- **GET `/books/fill`**

  Rellena la caché de libros para todos los géneros disponibles. Este endpoint publica mensajes en la cola para que el consumidor procese y almacene en caché los libros correspondientes a cada género.

  **Respuesta exitosa:**

  - Código 200: Indica que los libros se están procesando y almacenando en caché.

