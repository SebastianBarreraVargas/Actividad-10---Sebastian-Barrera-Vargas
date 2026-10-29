# Sistema de Biblioteca - Patrones de Diseno

Modulo de prestamos y devoluciones de una biblioteca universitaria que implementa patrones de diseno Creacionales, Estructurales y de Comportamiento.

## Autor

Sebastian Barrera Vargas - 202308240

## Descripcion

Sistema de gestion de prestamos de una biblioteca universitaria. Permite registrar prestamos y devoluciones de libros para diferentes tipos de usuario (estudiantes, docentes e invitados), cada uno con distintos limites de prestamos y dias permitidos. Incluye un sistema de notificaciones configurable y una lista de espera que notifica automaticamente cuando un libro vuelve a estar disponible.

## Requisitos

- Python 3.8 o superior

No se requieren dependencias externas.

## Ejecucion

```
python main.py
```

## Estructura del Proyecto

```
models.py      - Clases Book, User (Student, Teacher, Guest) y UserFactory
notifiers.py   - Interfaz Notifier y notificadores ConsoleNotifier, EmailNotifier
decorators.py  - Decoradores TimestampNotifier y UrgentNotifier
repository.py  - Interfaz LoanRepository e implementacion InMemoryLoanRepository
observers.py   - Interfaz BookReturnObserver e implementacion WaitList
service.py     - Servicio principal LibraryService
main.py        - Funcion principal con demostracion de todos los patrones
```

## Patrones de Diseno Implementados

### Patron Creacional: Factory Method

La clase `UserFactory` en `models.py` centraliza la creacion de usuarios. En lugar de instanciar directamente `Student`, `Teacher` o `Guest`, se usa `UserFactory.create(tipo, nombre, email)` que devuelve la instancia correcta segun el tipo indicado. Esto permite agregar nuevos tipos de usuario registrandolos en el diccionario `_types` sin modificar el codigo que los crea ni el servicio de biblioteca.

### Patron Estructural: Decorator

En `decorators.py`, la clase `NotifierDecorator` envuelve un `Notifier` existente y le agrega funcionalidad extra sin modificar su codigo. `TimestampNotifier` agrega la hora actual al mensaje antes de delegarlo al notificador envuelto. `UrgentNotifier` marca el mensaje como urgente. Estos decoradores se pueden apilar: por ejemplo, se puede envolver un `EmailNotifier` con `UrgentNotifier` para obtener emails urgentes, o un `ConsoleNotifier` con `TimestampNotifier` para mensajes con hora en consola.

### Patron de Comportamiento: Observer

`LibraryService` en `service.py` mantiene una lista de observadores que implementan la interfaz `BookReturnObserver`. Cuando se devuelve un libro mediante `give_back()`, el servicio notifica a todos los observadores registrados llamando a `on_book_returned(book)`. La clase `WaitList` en `observers.py` implementa este observador: los usuarios se agregan a la lista de espera de un libro, y cuando ese libro es devuelto, la lista de espera avisa automaticamente a todos los usuarios que lo estaban esperando.
