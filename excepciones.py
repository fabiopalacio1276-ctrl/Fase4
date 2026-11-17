"""Excepciones personalizadas del sistema SOFTWARE FJ."""


class ErrorSistema(Exception):
    """Excepción base para los errores controlados de la aplicación."""


class ErrorValidacion(ErrorSistema):
    """Los datos recibidos no cumplen las reglas de validación."""


class ErrorCliente(ErrorSistema):
    """Error relacionado con el registro o consulta de clientes."""


class ErrorServicio(ErrorSistema):
    """Error relacionado con los servicios disponibles."""


class ErrorReserva(ErrorSistema):
    """Error relacionado con el ciclo de vida de una reserva."""


class ServicioNoDisponible(ErrorServicio):
    """Se intentó reservar o procesar un servicio no disponible."""


class OperacionNoPermitida(ErrorSistema):
    """La operación no está permitida para el estado actual del objeto."""
