"""Punto de entrada y batería demostrativa de SOFTWARE FJ."""

from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reservas import GestorReservas
from excepciones import ErrorSistema, ErrorValidacion, ErrorReserva, ServicioNoDisponible
from registro import registrar_evento, registrar_error


def ejecutar_prueba(numero, descripcion, accion):
    """Ejecuta una prueba aislada para que un error no detenga las demás."""
    print("\n>>> {}. {}".format(numero, descripcion))
    try:
        resultado = accion()
    except ErrorSistema as error:
        print("[ERROR CONTROLADO] {}: {}".format(type(error).__name__, error))
        registrar_error("{}: {}".format(type(error).__name__, error))
    except Exception as error:
        print("[ERROR INESPERADO] {}: {}".format(type(error).__name__, error))
        registrar_error("Error inesperado: {}: {}".format(type(error).__name__, error))
    else:
        if resultado is not None:
            print("[OK] {}".format(resultado))
        print("[FIN] Prueba finalizada.")
    finally:
        # Se ejecuta tanto si la operación termina bien como si genera una excepción.
        pass


def main():
    gestor = GestorReservas()

    print("=" * 69)
    print(" SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print(" Clientes | Servicios | Reservas")
    print("=" * 69)
    print("Proyecto académico ilustrativo | Python 3.9+")

    # 1 y 2: clientes válidos
    ejecutar_prueba(1, "Registrar cliente válido", lambda: gestor.registrar_cliente(
        Cliente("C001", "Carlos Pérez", "carlos@email.com", "3001234567")
    ).resumen())

    ejecutar_prueba(2, "Registrar segundo cliente válido", lambda: gestor.registrar_cliente(
        Cliente("C002", "María Gómez", "maria@email.com", "3107654321")
    ).resumen())

    # 3: validación de correo
    ejecutar_prueba(3, "Validar cliente con correo inválido", lambda: Cliente(
        "C003", "Cliente Inválido", "correo-no-valido", "3001112233"
    ))

    # 4 a 6: tres servicios y polimorfismo
    sala = ReservaSala("S001", "Reserva de salas", "Sala para reuniones y eventos",
                       100000, 30)
    equipo = AlquilerEquipo("E001", "Alquiler de equipos", "Préstamo de equipo tecnológico",
                            50000, "Computador portátil")
    asesoria = Asesoria("A001", "Asesorías especializadas", "Acompañamiento profesional",
                        80000, "Ingeniería de sistemas")

    ejecutar_prueba(4, "Registrar servicio de reserva de salas",
                    lambda: gestor.registrar_servicio(sala).resumen() + " | " + sala.detalles())
    ejecutar_prueba(5, "Registrar servicio de alquiler de equipos",
                    lambda: gestor.registrar_servicio(equipo).resumen() + " | " + equipo.detalles())
    ejecutar_prueba(6, "Registrar servicio de asesorías",
                    lambda: gestor.registrar_servicio(asesoria).resumen() + " | " + asesoria.detalles())

    # 7: tarifa negativa, excepción de validación
    ejecutar_prueba(7, "Rechazar servicio con tarifa negativa", lambda: ReservaSala(
        "S099", "Sala inválida", "Prueba de tarifa", -1000, 10
    ))

    # 8 y 9: reserva válida y cliente inexistente
    ejecutar_prueba(8, "Crear reserva válida", lambda: gestor.crear_reserva(
        "R001", "C001", "S001", 1.8, descuento=10, impuesto=19
    ).resumen())

    ejecutar_prueba(9, "Rechazar reserva con cliente no registrado",
                    lambda: gestor.crear_reserva("R002", "C999", "S001", 1))

    # 10 a 12: confirmar, procesar y rechazar segundo procesamiento
    ejecutar_prueba(10, "Confirmar reserva", lambda: (
        "Reserva R001 confirmada. Estado: " + gestor.obtener_reserva("R001").confirmar()
    ))
    ejecutar_prueba(11, "Procesar reserva confirmada", lambda: (
        "Reserva procesada. Total: ${:,.2f}".format(
            gestor.obtener_reserva("R001").procesar()
        )
    ))
    ejecutar_prueba(12, "Rechazar segundo procesamiento",
                    lambda: gestor.obtener_reserva("R001").procesar())

    # 13: crear y cancelar reserva
    ejecutar_prueba(13, "Crear y cancelar reserva", lambda: (
        "Reserva R003. Estado: " +
        (lambda r: (r.cancelar() if r.estado == "Pendiente" else r.estado))(
            gestor.crear_reserva("R003", "C002", "E001", 2)
        )
    ))

    # 14: servicio no disponible
    equipo.disponible = False
    ejecutar_prueba(14, "Rechazar confirmación de servicio no disponible", lambda: (
        gestor.crear_reserva("R004", "C001", "E001", 1).confirmar()
    ))

    # 15: descuento fuera de rango
    ejecutar_prueba(15, "Validar descuento fuera de rango",
                    lambda: sala.calcular_costo(2, 150, 19))

    # 16: sobrecarga lógica: una, dos y tres entradas opcionales
    ejecutar_prueba(16, "Comprobar cálculo de costos y descuento", lambda: (
        "Costo base: ${:,.2f} | Con descuento: ${:,.2f} | Con impuesto: ${:,.2f}".format(
            sala.calcular_costo(1),
            sala.calcular_costo(1, 10),
            sala.calcular_costo(1, 10, 19)
        )
    ))

    print("\nRESUMEN DE RESERVAS:")
    for reserva in gestor.reservas:
        print(reserva.resumen())

    registrar_evento("Ejecución del sistema finalizada.")
    print("\n[FIN] SOFTWARE FJ finalizó la batería de pruebas.")
    print("[INFO] Registro de eventos guardado en eventos.log.")


if __name__ == "__main__":
    main()
