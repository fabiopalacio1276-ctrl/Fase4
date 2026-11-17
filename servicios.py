"""Jerarquía de servicios y cálculo flexible de costos."""

from abc import abstractmethod
from typing import overload

from entidades import Entidad
from excepciones import ErrorValidacion, ServicioNoDisponible


class Servicio(Entidad):
    """Clase abstracta que define el comportamiento común de un servicio."""

    def __init__(self, identificador, nombre, descripcion, tarifa, disponible=True):
        super().__init__(identificador)
        nombre = str(nombre).strip()
        if not nombre:
            raise ErrorValidacion("El nombre del servicio es obligatorio.")
        self._nombre = nombre
        self._descripcion = str(descripcion).strip()
        self._tarifa = self._validar_tarifa(tarifa)
        self._disponible = bool(disponible)

    @staticmethod
    def _validar_tarifa(tarifa):
        try:
            valor = float(tarifa)
        except (TypeError, ValueError) as error:
            raise ErrorValidacion("La tarifa debe ser numérica.") from error
        if valor <= 0:
            raise ErrorValidacion("La tarifa debe ser un número positivo.")
        return valor

    @property
    def nombre(self):
        return self._nombre

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    @overload
    def calcular_costo(self, duracion: float) -> float:
        ...

    @overload
    def calcular_costo(self, duracion: float, descuento: float) -> float:
        ...

    @overload
    def calcular_costo(self, duracion: float, descuento: float, impuesto: float) -> float:
        ...

    def calcular_costo(self, duracion, descuento=0.0, impuesto=19.0):
        """Calcula tarifa × duración, aplica descuento e impuesto porcentuales."""
        if not self.disponible:
            raise ServicioNoDisponible("El servicio no está disponible.")
        try:
            duracion = float(duracion)
            descuento = float(descuento)
            impuesto = float(impuesto)
        except (TypeError, ValueError) as error:
            raise ErrorValidacion("Duración, descuento e impuesto deben ser numéricos.") from error
        if duracion <= 0:
            raise ErrorValidacion("La duración debe ser mayor que cero.")
        if not 0 <= descuento <= 100:
            raise ErrorValidacion("El descuento debe estar entre 0 y 100.")
        if not 0 <= impuesto <= 100:
            raise ErrorValidacion("El impuesto debe estar entre 0 y 100.")
        subtotal = self.tarifa * duracion
        subtotal_con_descuento = subtotal * (1 - descuento / 100)
        return round(subtotal_con_descuento * (1 + impuesto / 100), 2)

    @abstractmethod
    def detalles(self):
        """Devuelve los atributos específicos de cada tipo de servicio."""

    def resumen(self):
        return "{}: {} | Tarifa: ${:,.0f}".format(self.id, self.nombre, self.tarifa)


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, descripcion, tarifa, capacidad, disponible=True):
        super().__init__(identificador, nombre, descripcion, tarifa, disponible)
        if int(capacidad) <= 0:
            raise ErrorValidacion("La capacidad de la sala debe ser positiva.")
        self._capacidad = int(capacidad)

    @property
    def capacidad(self):
        return self._capacidad

    def detalles(self):
        return "Capacidad: {}".format(self.capacidad)


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, descripcion, tarifa, equipo, disponible=True):
        super().__init__(identificador, nombre, descripcion, tarifa, disponible)
        equipo = str(equipo).strip()
        if not equipo:
            raise ErrorValidacion("Debe especificar el equipo que se alquila.")
        self._equipo = equipo

    @property
    def equipo(self):
        return self._equipo

    def detalles(self):
        return "Equipo: {}".format(self.equipo)


class Asesoria(Servicio):
    def __init__(self, identificador, nombre, descripcion, tarifa, especialidad, disponible=True):
        super().__init__(identificador, nombre, descripcion, tarifa, disponible)
        especialidad = str(especialidad).strip()
        if not especialidad:
            raise ErrorValidacion("Debe especificar la especialidad de la asesoría.")
        self._especialidad = especialidad

    @property
    def especialidad(self):
        return self._especialidad

    def detalles(self):
        return "Especialidad: {}".format(self.especialidad)
