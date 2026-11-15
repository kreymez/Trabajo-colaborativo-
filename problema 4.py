from abc import ABC, abstractmethod
from datetime import datetime
import logging


# ==========================================
# CONFIGURACIÓN DEL ARCHIVO DE LOGS
# ==========================================

logging.basicConfig(
    filename="software_fj_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================

class DatosInvalidosError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


class ReservaInvalidaError(Exception):
    pass


class OperacionNoPermitidaError(Exception):
    pass


# ==========================================
# CLASE ABSTRACTA ENTIDAD
# ==========================================

class Entidad(ABC):

    def __init__(self, identificacion, nombre):
        if not identificacion or not nombre:
            raise DatosInvalidosError(
                "La identificación y el nombre son obligatorios."
            )

        self._identificacion = identificacion
        self._nombre = nombre

    @property
    def identificacion(self):
        return self._identificacion

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ==========================================
# CLASE CLIENTE
# ==========================================

class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion, nombre)

        if "@" not in correo or "." not in correo:
            raise DatosInvalidosError("El correo electrónico no es válido.")

        if not telefono.isdigit() or len(telefono) < 7:
            raise DatosInvalidosError("El teléfono no es válido.")

        self.__correo = correo
        self.__telefono = telefono

    def mostrar_informacion(self):
        return (
            f"Cliente: {self.nombre} | "
            f"ID: {self.identificacion} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )


# ==========================================
# CLASE ABSTRACTA SERVICIO
# ==========================================

class Servicio(Entidad, ABC):

    def __init__(self, identificacion, nombre, precio):
        super().__init__(identificacion, nombre)

        if not isinstance(precio, (int, float)) or precio <= 0:
            raise DatosInvalidosError("El precio debe ser mayor que cero.")

        self._precio = precio
        self._disponible = True

    @abstractmethod
    def calcular_costo(self, *args):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre} no está disponible."
            )

    def mostrar_informacion(self):
        return (
            f"Servicio: {self.nombre} | "
            f"Precio: ${self._precio:,.2f} | "
            f"Disponible: {self._disponible}"
        )


# ==========================================
# SERVICIO 1: RESERVA DE SALAS
# ==========================================

class ReservaSala(Servicio):

    def calcular_costo(self, *args):

        if len(args) < 1 or len(args) > 3:
            raise DatosInvalidosError(
                "Utilice duración, duración e impuesto, "
                "o duración, impuesto y descuento."
            )

        duracion = args[0]
        impuesto = args[1] if len(args) >= 2 else 0
        descuento = args[2] if len(args) == 3 else 0

        validar_parametros(duracion, impuesto, descuento)

        costo = self._precio * duracion
        costo += costo * impuesto / 100
        costo -= costo * descuento / 100

        return costo

    def describir_servicio(self):
        return "Reserva de salas de reuniones y conferencias."


# ==========================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# ==========================================

class AlquilerEquipos(Servicio):

    def calcular_costo(self, *args):

        if len(args) < 1 or len(args) > 3:
            raise DatosInvalidosError("Cantidad incorrecta de parámetros.")

        duracion = args[0]
        impuesto = args[1] if len(args) >= 2 else 0
        descuento = args[2] if len(args) == 3 else 0

        validar_parametros(duracion, impuesto, descuento)

        costo = self._precio * duracion
        costo += costo * impuesto / 100
        costo -= costo * descuento / 100

        return costo

    def describir_servicio(self):
        return "Alquiler de computadores, proyectores y equipos tecnológicos."


# ==========================================
# SERVICIO 3: ASESORÍAS ESPECIALIZADAS
# ==========================================

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, *args):

        if len(args) < 1 or len(args) > 3:
            raise DatosInvalidosError("Cantidad incorrecta de parámetros.")

        duracion = args[0]
        impuesto = args[1] if len(args) >= 2 else 0
        descuento = args[2] if len(args) == 3 else 0

        validar_parametros(duracion, impuesto, descuento)

        costo = self._precio * duracion
        costo += costo * impuesto / 100
        costo -= costo * descuento / 100

        return costo

    def describir_servicio(self):
        return "Asesorías profesionales en tecnología y sistemas."


# ==========================================
# VALIDACIÓN DE PARÁMETROS
# ==========================================

def validar_parametros(duracion, impuesto, descuento):

    if not isinstance(duracion, (int, float)) or duracion <= 0:
        raise DatosInvalidosError("La duración debe ser mayor que cero.")

    if not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 100:
        raise DatosInvalidosError("El impuesto debe estar entre 0 y 100.")

    if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
        raise DatosInvalidosError("El descuento debe estar entre 0 y 100.")


# ==========================================
# CLASE RESERVA
# ==========================================

class Reserva:

    def __init__(self, identificacion, cliente, servicio, duracion):

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente no es válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio no es válido.")

        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser positiva.")

        servicio.validar_disponibilidad()

        self.identificacion = identificacion
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo = 0

    def confirmar(self):

        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.costo = self.servicio.calcular_costo(self.duracion)
        self.estado = "Confirmada"

        logging.info(
            f"Reserva {self.identificacion} confirmada."
        )

        return self.costo

    def cancelar(self):

        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya está cancelada."
            )

        self.estado = "Cancelada"

        logging.info(
            f"Reserva {self.identificacion} cancelada."
        )

    def procesar(self):

        try:
            if self.estado == "Pendiente":
                self.confirmar()

            elif self.estado == "Cancelada":
                raise OperacionNoPermitidaError(
                    "No se puede procesar una reserva cancelada."
                )

            print(f"Reserva {self.identificacion} procesada correctamente.")

        except Exception as error:
            logging.exception("Error al procesar la reserva.")
            raise ReservaInvalidaError(
                "No fue posible procesar la reserva."
            ) from error

        finally:
            print("Finalizó el proceso de reserva.")

    def mostrar_informacion(self):

        return (
            f"Reserva: {self.identificacion} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} horas | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo:,.2f}"
        )


# ==========================================
# CLASE PRINCIPAL DEL SISTEMA
# ==========================================

class SistemaSoftwareFJ:

    def __init__(self):

        self.clientes = []
        self.servicios = []
        self.reservas = []

    # REGISTRAR CLIENTES

    def registrar_cliente(self, cliente):

        try:
            if not isinstance(cliente, Cliente):
                raise DatosInvalidosError("El cliente no es válido.")

            for existente in self.clientes:
                if existente.identificacion == cliente.identificacion:
                    raise DatosInvalidosError("El cliente ya está registrado.")

            self.clientes.append(cliente)

            logging.info(
                f"Cliente registrado: {cliente.nombre}"
            )

            print("Cliente registrado correctamente.")

        except Exception as error:
            logging.exception("Error al registrar cliente.")
            raise DatosInvalidosError(
                "No se pudo registrar el cliente."
            ) from error

    # REGISTRAR SERVICIOS

    def registrar_servicio(self, servicio):

        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError("El servicio no es válido.")

            for existente in self.servicios:
                if existente.identificacion == servicio.identificacion:
                    raise DatosInvalidosError("El servicio ya existe.")

            self.servicios.append(servicio)

            logging.info(
                f"Servicio registrado: {servicio.nombre}"
            )

            print("Servicio registrado correctamente.")

        except Exception as error:
            logging.exception("Error al registrar servicio.")
            raise DatosInvalidosError(
                "No se pudo registrar el servicio."
            ) from error

    # CREAR RESERVAS

    def crear_reserva(self, identificacion, id_cliente, id_servicio, duracion):

        try:

            cliente = next(
                (c for c in self.clientes
                 if c.identificacion == id_cliente),
                None
            )

            servicio = next(
                (s for s in self.servicios
                 if s.identificacion == id_servicio),
                None
            )

            if cliente is None:
                raise ReservaInvalidaError("Cliente no encontrado.")

            if servicio is None:
                raise ReservaInvalidaError("Servicio no encontrado.")

            reserva = Reserva(
                identificacion,
                cliente,
                servicio,
                duracion
            )

            self.reservas.append(reserva)

            logging.info(
                f"Reserva creada: {identificacion}"
            )

            print("Reserva creada correctamente.")

            return reserva

        except Exception as error:
            logging.exception("Error al crear reserva.")
            raise ReservaInvalidaError(
                "No fue posible crear la reserva."
            ) from error

        finally:
            print("Finalizó la operación de creación de reserva.")

    # MOSTRAR CLIENTES

    def mostrar_clientes(self):

        print("\n========== CLIENTES ==========")

        for cliente in self.clientes:
            print(cliente.mostrar_informacion())

    # MOSTRAR SERVICIOS

    def mostrar_servicios(self):

        print("\n========== SERVICIOS ==========")

        for servicio in self.servicios:
            print(servicio.mostrar_informacion())
            print(servicio.describir_servicio())

    # MOSTRAR RESERVAS

    def mostrar_reservas(self):

        print("\n========== RESERVAS ==========")

        for reserva in self.reservas:
            print(reserva.mostrar_informacion())


# ==========================================
# PROGRAMA PRINCIPAL Y PRUEBAS
# ==========================================

def ejecutar_sistema():

    sistema = SistemaSoftwareFJ()

    print("\n========================================")
    print("     SISTEMA INTEGRAL SOFTWARE FJ")
    print("========================================")

    # OPERACIÓN 1: Registrar primer cliente

    print("\nOPERACIÓN 1")

    try:
        cliente1 = Cliente(
            "1001",
            "Carlos Pérez",
            "carlos@gmail.com",
            "3001234567"
        )

        sistema.registrar_cliente(cliente1)

    except Exception as error:
        print("Error:", error)

    # OPERACIÓN 2: Registrar segundo cliente

    print("\nOPERACIÓN 2")

    try:
        cliente2 = Cliente(
            "1002",
            "María Rodríguez",
            "maria@gmail.com",
            "3019876543"
        )

        sistema.registrar_cliente(cliente2)

    except Exception as error:
        print("Error:", error)

    # OPERACIÓN 3: Registrar cliente inválido

    print("\nOPERACIÓN 3")

    try:
        cliente3 = Cliente(
            "1003",
            "Pedro López",
            "correo_invalido",
            "3001234567"
        )

        sistema.registrar_cliente(cliente3)

    except Exception as error:
        print("Error controlado:", error)

    # OPERACIÓN 4: Crear servicio de salas

    print("\nOPERACIÓN 4")

    try:
        sala = ReservaSala(
            "S01",
            "Reserva de salas",
            50000
        )

        sistema.registrar_servicio(sala)

    except Exception as error:
        print("Error:", error)

    # OPERACIÓN 5: Crear servicio de equipos

    print("\nOPERACIÓN 5")

    try:
        equipos = AlquilerEquipos(
            "S02",
            "Alquiler de equipos",
            30000
        )

        sistema.registrar_servicio(equipos)

    except Exception as error:
        print("Error:", error)

    # OPERACIÓN 6: Crear servicio de asesorías

    print("\nOPERACIÓN 6")

    try:
        asesoria = AsesoriaEspecializada(
            "S03",
            "Asesoría especializada",
            80000
        )

        sistema.registrar_servicio(asesoria)

    except Exception as error:
        print("Error:", error)

    # OPERACIÓN 7: Intentar crear servicio inválido

    print("\nOPERACIÓN 7")

    try:
        servicio_invalido = ReservaSala(
            "S04",
            "Sala inválida",
            -5000
        )

        sistema.registrar_servicio(servicio_invalido)

    except Exception as error:
        print("Error controlado:", error)

    # OPERACIÓN 8: Crear reserva válida

    print("\nOPERACIÓN 8")

    try:
        reserva1 = sistema.crear_reserva(
            "R001",
            "1001",
            "S01",
            3
        )

        costo = reserva1.confirmar()

        print(f"Costo de la reserva: ${costo:,.2f}")

    except Exception as error:
        print("Error:", error)

    # OPERACIÓN 9: Crear reserva con cliente inexistente

    print("\nOPERACIÓN 9")

    try:
        sistema.crear_reserva(
            "R002",
            "9999",
            "S02",
            2
        )

    except Exception as error:
        print("Error controlado:", error)

    # OPERACIÓN 10: Crear reserva con duración inválida

    print("\nOPERACIÓN 10")

    try:
        sistema.crear_reserva(
            "R003",
            "1002",
            "S02",
            -2
        )

    except Exception as error:
        print("Error controlado:", error)

    # OPERACIÓN 11: Crear y cancelar reserva

    print("\nOPERACIÓN 11")

    try:
        reserva2 = sistema.crear_reserva(
            "R004",
            "1002",
            "S03",
            2
        )

        reserva2.cancelar()

        print("Reserva cancelada correctamente.")

    except Exception as error:
        print("Error:", error)

    # OPERACIÓN 12: Procesar una reserva

    print("\nOPERACIÓN 12")

    try:
        reserva3 = sistema.crear_reserva(
            "R005",
            "1001",
            "S02",
            4
        )

        reserva3.procesar()

    except Exception as error:
        print("Error:", error)

    # OPERACIÓN 13: Calcular costo con impuesto

    print("\nOPERACIÓN 13")

    try:
        costo = sala.calcular_costo(3, 19)

        print(f"Costo con impuesto: ${costo:,.2f}")

    except Exception as error:
        print("Error:", error)

    # OPERACIÓN 14: Calcular costo con impuesto y descuento

    print("\nOPERACIÓN 14")

    try:
        costo = asesoria.calcular_costo(2, 19, 10)

        print(f"Costo con impuesto y descuento: ${costo:,.2f}")

    except Exception as error:
        print("Error:", error)

    # MOSTRAR INFORMACIÓN FINAL

    sistema.mostrar_clientes()
    sistema.mostrar_servicios()
    sistema.mostrar_reservas()

    print("\n========================================")
    print("       RESUMEN DEL SISTEMA")
    print("========================================")

    print("Total de clientes:", len(sistema.clientes))
    print("Total de servicios:", len(sistema.servicios))
    print("Total de reservas:", len(sistema.reservas))

    print("\nLos eventos y errores se guardaron en:")
    print("software_fj_logs.txt")

    print("\nSistema ejecutado correctamente.")


# ==========================================
# INICIO DEL PROGRAMA
# ==========================================

if __name__ == "__main__":

    try:
        ejecutar_sistema()

    except Exception as error:
        logging.critical(
            f"Error crítico del sistema: {error}",
            exc_info=True
        )

        print("Se presentó un error crítico:", error)

    finally:
        print("\nEjecución del programa finalizada.")