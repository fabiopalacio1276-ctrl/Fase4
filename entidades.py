"""Entidades del dominio: abstracción general y clientes."""

from abc import ABC, abstractmethod
from datetime import datetime
import re

from excepciones import ErrorValidacion


class Entidad(ABC):
    """Clase abstracta base para las entidades identificables del sistema."""

    def __init__(self, identificador):
        identificador = str(identificador).strip()
        if not identificador:
            raise ErrorValidacion("El identificador no puede estar vacío.")
        self._id = identificador
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def resumen(self):
        """Devuelve una descripción legible de la entidad."""


class Cliente(Entidad):
    """Representa a una persona registrada como cliente."""

    PATRON_CORREO = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self._nombre = self._validar_nombre(nombre)
        self._correo = self._validar_correo(correo)
        self._telefono = self._validar_telefono(telefono)

    @staticmethod
    def _validar_nombre(nombre):
        nombre = " ".join(str(nombre).split())
        if len(nombre) < 3 or not all(c.isalpha() or c in " -'áéíóúÁÉÍÓÚñÑ" for c in nombre):
            raise ErrorValidacion("El nombre debe contener al menos 3 caracteres válidos.")
        return nombre

    @classmethod
    def _validar_correo(cls, correo):
        correo = str(correo).strip()
        if not cls.PATRON_CORREO.fullmatch(correo):
            raise ErrorValidacion("El correo electrónico no es válido.")
        return correo.lower()

    @staticmethod
    def _validar_telefono(telefono):
        telefono = re.sub(r"[\s()-]", "", str(telefono))
        if not re.fullmatch(r"\+?\d{7,15}", telefono):
            raise ErrorValidacion("El teléfono debe contener entre 7 y 15 dígitos.")
        return telefono

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    def resumen(self):
        return "{}: {} | {}".format(self.id, self.nombre, self.correo)

    def __str__(self):
        return self.resumen()
