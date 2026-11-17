# SOFTWARE FJ
## Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto académico de consola desarrollado en Python 3.9 o superior. Implementa programación orientada a objetos, arquitectura modular, validaciones, excepciones personalizadas y registro de eventos con `logging`.

## Estructura

```text
Software_FJ/
├── main.py
├── entidades.py
├── servicios.py
├── reservas.py
├── excepciones.py
├── registro.py
├── README.md
└── eventos.log       # Se crea automáticamente al ejecutar el programa
```

## Requisitos

- Python 3.9 o superior.
- No requiere paquetes externos.
- No utiliza bases de datos; los datos se mantienen en memoria durante la ejecución.

## Ejecución

Abra una terminal dentro de la carpeta `Software_FJ` y ejecute:

```bash
python main.py
```

El programa presenta 16 operaciones demostrativas. Los errores esperados se capturan y se muestran como errores controlados, por lo que una prueba fallida no interrumpe las siguientes. Al finalizar se muestra el resumen de reservas.

## Funcionalidades

- Registro de clientes con validación de nombre, correo y teléfono.
- Registro de salas, equipos y asesorías.
- Creación, confirmación, cancelación y procesamiento de reservas.
- Estados de reserva: `Pendiente`, `Confirmada`, `Procesada` y `Cancelada`.
- Cálculo del costo por duración, descuento porcentual e impuesto porcentual.
- Excepciones propias para validación, clientes, servicios y reservas.
- Registro cronológico de eventos y errores en `eventos.log`.

## Diseño orientado a objetos

- `Entidad`: clase abstracta base con identificador y fecha de creación.
- `Cliente`: entidad concreta con propiedades encapsuladas y validaciones.
- `Servicio`: clase abstracta con cálculo de costos y contrato `detalles()`.
- `ReservaSala`, `AlquilerEquipo` y `Asesoria`: especializaciones de `Servicio`.
- `Reserva`: controla el ciclo de vida y las transiciones de estado.
- `GestorReservas`: administra las colecciones en memoria.

El método `calcular_costo` documenta tres firmas mediante `typing.overload`; en tiempo de ejecución utiliza una implementación única con argumentos opcionales, que es el patrón compatible con Python.

## Reglas de cálculo

El costo se calcula así:

1. Subtotal = tarifa × duración.
2. Subtotal con descuento = subtotal × (1 − descuento / 100).
3. Total = subtotal con descuento × (1 + impuesto / 100).

El impuesto predeterminado es 19 %. El descuento y el impuesto aceptan valores entre 0 y 100.

## Registro de eventos

`registro.py` configura el módulo estándar `logging`. El archivo `eventos.log` se crea junto a los módulos y guarda fecha, hora, nivel y descripción. Cada nueva ejecución agrega eventos al registro existente.

## Alcance

Este proyecto es una aplicación demostrativa de consola. Los datos de clientes, servicios y reservas no persisten entre ejecuciones; el archivo de eventos sí permanece en disco.
