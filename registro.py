"""Configuración centralizada del registro de eventos mediante logging."""

import logging
from pathlib import Path

RUTA_LOG = Path(__file__).resolve().with_name("eventos.log")
_logger = logging.getLogger("software_fj")
_logger.setLevel(logging.INFO)
_logger.propagate = False

if not _logger.handlers:
    manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    formato = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    manejador.setFormatter(formato)
    _logger.addHandler(manejador)


def registrar_evento(mensaje):
    """Guarda un evento informativo en eventos.log."""
    _logger.info(mensaje)


def registrar_error(mensaje):
    """Guarda un error controlado en eventos.log."""
    _logger.error(mensaje)


def registrar_excepcion(mensaje):
    """Guarda un error con información de excepción."""
    _logger.exception(mensaje)
