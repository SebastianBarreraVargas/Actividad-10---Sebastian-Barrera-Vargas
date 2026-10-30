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
models.py      - Clases Book, User (Student, Teacher, Guest) y jerarquia UserCreator (StudentCreator, TeacherCreator, GuestCreator)
notifiers.py   - Interfaz Notifier y notificadores ConsoleNotifier, EmailNotifier
decorators.py  - Decoradores TimestampNotifier y UrgentNotifier
repository.py  - Interfaz LoanRepository e implementacion InMemoryLoanRepository (Patron Repositorio)
observers.py   - Interfaz BookReturnObserver e implementacion WaitList
service.py     - Servicio principal LibraryService (Gestion de prestamos y Subject del Observer)
main.py        - Funcion principal con demostracion de todos los patrones y flujo completo
```

## Patrones de Diseno Implementados

### Patron Creacional: Factory Method (GoF)

Cumple con la estructura canonica del patron segun la guia de diseno:
- **Creator abstracto (`UserCreator`)**: declara el metodo de fabricacion abstracto `create_user(name, email)` y contiene la logica comun de registro `register(name, email)`.
- **ConcreteCreators (`StudentCreator`, `TeacherCreator`, `GuestCreator`)**: cada uno sobreescribe el metodo de fabricacion para instanciar su producto concreto (`Student`, `Teacher`, `Guest`).
- **Product (`User`) y ConcreteProducts**: definen la interfaz comun de usuario y sus politicas especificas (prestamos maximos y dias permitidos).

### Patron Estructural: Decorator

En `decorators.py`, la clase `NotifierDecorator` envuelve un `Notifier` existente y le agrega funcionalidad extra sin modificar su codigo (principio Abierto/Cerrado):
- `TimestampNotifier` agrega la hora actual al mensaje antes de delegarlo al notificador envuelto.
- `UrgentNotifier` antepone la etiqueta `URGENTE:` al mensaje.
Estos decoradores se pueden apilar dinamicamente (e.g. `UrgentNotifier(EmailNotifier())`).

### Patron de Comportamiento: Observer

`LibraryService` en `service.py` actua como el **Subject** (sujeto observable) y mantiene la lista de observadores con metodos para suscribir (`add_observer`) y cancelar suscripcion (`remove_observer`).
- **Observer abstracto (`BookReturnObserver`)**: declara el contrato `on_book_returned(book)`.
- **ConcreteObserver (`WaitList`)**: gestiona los usuarios en cola de espera por libro y, al recibir la notificacion de devolucion, avisa automaticamente a todos los usuarios interesados a traves de su notificador inyectado.

## Arquitectura y Principios de Diseno

- **Arquitectura en Capas**:
  - **Capa de Datos**: `repository.py` (Patron Repositorio para persistencia de prestamos desacoplada de la base de datos).
  - **Capa de Dominio / Negocio**: `models.py`, `service.py`, `observers.py`, `notifiers.py`, `decorators.py`.
  - **Capa de Presentacion / Aplicacion**: `main.py`.
- **Principio de Inversion de Dependencias (DIP)**: `LibraryService` depende exclusivamente de abstracciones (`LoanRepository`, `Notifier`, `BookReturnObserver`), nunca de implementaciones concretas.

