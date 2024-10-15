

Un ávido lector usa tu servicio de integraciones para comprar libros en Amazon recomendados por el New York Times.

Tu proyecto debe implementar una integración con el API de libros del NYT. Tu entregable debe incluir:

Integración con NYT funcional corriendo con un proceso en segundo plano (background). Además:
Incluye diagramas de secuencia de tu integración con NYT
Llevas registros de ejecución (logs)
Implementa políticas de reintentos
Interfaz de usuario que incluye:
Filtro de búsqueda por género
Consume un endpoint que trae los datos básicos de libro.
Diagramas de secuencia de una posible integración con Amazon que permita buscar el libro e incluir un botón que redireccione a la página del producto (esto no tiene que implementarse). No uses una base de datos, implementa un almacenamiento en memoria
Diagramas de secuencia de una posible integración con O'Reilly para obtener el precio de los libros técnicos.
Sube tu código en un repositorio en un proyecto en Github y envía la URL a la vuelta de correo.

Incluye un readme con instrucciones para ejecutar el código.

No uses una base de datos, es suficiente con mantener la información en memoria. Te sugerimos esta estructura de datos:

Ganas puntos extra si:

Sigues convenciones
Agregas tests
Usas arquitectura limpia o hexagonal en tu implementación
Usas Python en el backend y Typescript (con React) en el frontend.