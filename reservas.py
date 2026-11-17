"""Reservas y gestor en memoria para clientes, servicios y reservas."""

from datetime import datetime

from entidades import Entidad, Cliente
from excepciones import (
    ErrorCliente, ErrorReserva, ErrorServicio, ErrorValidacion,
    OperacionNoPermitida, ServicioNoDisponible,
)
from registro import registrar_evento, registrar_error


class Reserva(Entidad):
    """Reserva individual con estados Pendiente, Confirmada, Procesada o Cancelada."""

    ESTADOS = ("Pendiente", "Confirmada", "Procesada", "Cancelada")

    def __init__(self, identificador, cliente, servicio, duracion, descuento=0.0, impuesto=19.0):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ErrorValidacion("La reserva requiere un cliente válido.")
        if not hasattr(servicio, "calcular_costo"):
            raise ErrorValidacion("La reserva requiere un servicio válido.")
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as error:
            raise ErrorValidacion("La duración debe ser numérica.") from error
        if duracion <= 0:
            raise ErrorValidacion("La duración debe ser mayor que cero.")
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._descuento = float(descuento)
        self._impuesto = float(impuesto)
        self._estado = "Pendiente"
        self._total = None
        self._fecha_actualizacion = datetime.now()

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def descuento(self):
        return self._descuento

    @property
    def estado(self):
        return self._estado

    @property
    def total(self):
        return self._total

    def _cambiar_estado(self, nuevo_estado):
        self._estado = nuevo_estado
        self._fecha_actualizacion = datetime.now()

    def confirmar(self):
        if self.estado != "Pendiente":
            raise OperacionNoPermitida("Solo se pueden confirmar reservas pendientes.")
        if not self.servicio.disponible:
            raise ServicioNoDisponible("El servicio no está disponible.")
        self._cambiar_estado("Confirmada")
        registrar_evento("Reserva confirmada: {}".format(self.id))
        return self.estado

    def cancelar(self):
        if self.estado not in ("Pendiente", "Confirmada"):
            raise OperacionNoPermitida("No se puede cancelar una reserva en estado {}.".format(self.estado))
        self._cambiar_estado("Cancelada")
        registrar_evento("Reserva cancelada: {}".format(self.id))
        return self.estado

    def procesar(self):
        if self.estado != "Confirmada":
            raise ErrorReserva("Solo se pueden procesar reservas confirmadas.")
        try:
            self._total = self.servicio.calcular_costo(
                self.duracion, self.descuento, self._impuesto
            )
        except ServicioNoDisponible:
            raise
        except Exception as error:
            raise ErrorReserva("No fue posible procesar la reserva {}.".format(self.id)) from error
        self._cambiar_estado("Procesada")
        registrar_evento("Reserva procesada: {} | Total: ${:,.2f}".format(self.id, self.total))
        return self.total

    def resumen(self):
        total = "Pendiente de cálculo" if self.total is None else "${:,.2f}".format(self.total)
        return "{} | {} | {} | {}".format(
            self.id, self.cliente.nombre, self.servicio.nombre, self.estado
        ) + " | Total: " + total


class GestorReservas:
    """Administra colecciones de objetos durante la ejecución del programa."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    @staticmethod
    def _buscar_por_id(elementos, identificador):
        for elemento in elementos:
            if elemento.id == str(identificador):
                return elemento
        raise KeyError(str(identificador))

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ErrorCliente("El objeto suministrado no es un cliente.")
        if any(c.id == cliente.id for c in self._clientes):
            raise ErrorCliente("Ya existe un cliente con ese identificador.")
        self._clientes.append(cliente)
        registrar_evento("Cliente registrado: {} - {}".format(cliente.id, cliente.nombre))
        registrar_evento("Cliente agregado al gestor: {}".format(cliente.id))
        return cliente

    def obtener_cliente(self, identificador):
        try:
            return self._buscar_por_id(self._clientes, identificador)
        except KeyError as error:
            raise ErrorCliente("El cliente {} no está registrado.".format(identificador)) from error

    def registrar_servicio(self, servicio):
        if not hasattr(servicio, "calcular_costo"):
            raise ErrorServicio("El objeto suministrado no es un servicio válido.")
        if any(s.id == servicio.id for s in self._servicios):
            raise ErrorServicio("Ya existe un servicio con ese identificador.")
        self._servicios.append(servicio)
        registrar_evento("Servicio registrado: {} - {}".format(servicio.id, servicio.nombre))
        return servicio

    def obtener_servicio(self, identificador):
        try:
            return self._buscar_por_id(self._servicios, identificador)
        except KeyError as error:
            raise ErrorServicio("El servicio {} no está registrado.".format(identificador)) from error

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion,
                      descuento=0.0, impuesto=19.0):
        if any(r.id == str(identificador) for r in self._reservas):
            raise ErrorReserva("Ya existe una reserva con ese identificador.")
        cliente = self.obtener_cliente(id_cliente)
        servicio = self.obtener_servicio(id_servicio)
        if not servicio.disponible:
            raise ServicioNoDisponible("El servicio no está disponible.")
        reserva = Reserva(identificador, cliente, servicio, duracion, descuento, impuesto)
        self._reservas.append(reserva)
        registrar_evento("Reserva creada: {}".format(reserva.id))
        return reserva

    def obtener_reserva(self, identificador):
        try:
            return self._buscar_por_id(self._reservas, identificador)
        except KeyError as error:
            raise ErrorReserva("La reserva {} no existe.".format(identificador)) from error
