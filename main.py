from models import Book, StudentCreator, TeacherCreator, GuestCreator
from notifiers import ConsoleNotifier, EmailNotifier
from decorators import TimestampNotifier, UrgentNotifier
from repository import InMemoryLoanRepository
from observers import WaitList
from service import LibraryService


def main():
    print("=" * 60)
    print("  SISTEMA DE BIBLIOTECA - PATRONES DE DISENO")
    print("=" * 60)

    clean = Book("Clean Code", "978-0132350884")
    refactoring = Book("Refactoring", "978-0201485677")
    quijote = Book("Don Quijote", "978-8420412146")
    patterns = Book("Design Patterns", "978-0201633610")

    print("\n[FACTORY METHOD] Creando usuarios con ConcreteCreators (UserCreator):")
    ana = StudentCreator().register("Ana", "ana@umss.edu")
    luis = TeacherCreator().register("Luis", "luis@umss.edu")
    carlos = GuestCreator().register("Carlos", "carlos@gmail.com")


    loans = InMemoryLoanRepository()

    base = ConsoleNotifier()
    with_time = TimestampNotifier(base)
    urgent_email = UrgentNotifier(EmailNotifier())

    service = LibraryService(loans, with_time)

    waitlist = WaitList(urgent_email)
    service.add_observer(waitlist)

    print("\n[DECORATOR] Notificador con timestamp (ConsoleNotifier + TimestampNotifier):")
    print("--- Ana (estudiante, max 2) pide 3 libros ---")
    for book in (clean, refactoring, quijote):
        service.borrow(ana, book)

    print("\n--- Carlos (invitado) quiere 'Clean Code' pero no esta disponible ---")
    service.borrow(carlos, clean)

    print("\n[OBSERVER] Carlos se agrega a la lista de espera de 'Clean Code':")
    waitlist.add(carlos, clean)

    print("\n--- Luis (docente) pide 'Design Patterns' ---")
    service.borrow(luis, patterns)

    print("\n--- Ana devuelve 'Clean Code' -> Observer notifica a Carlos ---")
    service.give_back(ana, clean)

    print("\n--- Carlos ahora puede pedir 'Clean Code' ---")
    service.borrow(carlos, clean)

    print("\n[DECORATOR] Servicio con notificador urgente por email:")
    urgent_service = LibraryService(loans, urgent_email)
    urgent_service.add_observer(waitlist)
    print("--- Luis intenta pedir un libro que ya tiene Carlos ---")
    urgent_service.borrow(luis, clean)
    waitlist.add(luis, clean)

    print("\n--- Carlos devuelve 'Clean Code' -> Observer notifica a Luis ---")
    urgent_service.give_back(carlos, clean)

    print("\n--- Luis pide 'Clean Code' ---")
    urgent_service.borrow(luis, clean)

if __name__ == "__main__":
    main()
