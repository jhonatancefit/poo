# SISTEMA DE GIMNASIO - ESTRUCTURA COMPLETA
# Implementación de 4 pilares de POO: Encapsulamiento, Herencia, Polimorfismo, Abstracción

"""
ESTRUCTURA DEL PROYECTO:
gym_system/
├── main.py
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── membresia.py      # Ejercicio 10.1
│   │   ├── clase.py           # Ejercicio 10.2
│   │   ├── empleado.py        # Ejercicio 10.3
│   │   └── equipo.py          # Ejercicio 10.4
│   ├── services/
│   │   ├── __init__.py
│   │   ├── membresia_service.py
│   │   ├── clase_service.py
│   │   ├── empleado_service.py
│   │   └── equipo_service.py
│   ├── storage/
│   │   ├── __init__.py
│   │   └── json_storage.py
│   └── ui/
│       ├── __init__.py
│       └── menu.py
└── data/
    ├── membresias.json
    ├── clases.json
    ├── empleados.json
    └── equipos.json
"""

# =============================================================================
# EJERCICIO 10.1: PLANES Y MEMBRESIAS
# src/models/membresia.py
# =============================================================================

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Membresia(ABC):
    """
    Clase abstracta base para membresías del gimnasio.
    Implementa ABSTRACCIÓN como pilar fundamental.
    """
    
    def __init__(self, numero_membresia, titular, fecha_inicio, estado="activa"):
        # ENCAPSULAMIENTO: Atributos privados
        self.__numero_membresia = numero_membresia
        self.__titular = titular
        self.__fecha_inicio = fecha_inicio
        self.__estado = estado
        self.__historial_pagos = []
        
        # Atributo protegido
        self._servicios_incluidos = []
    
    # Getters y Setters (ENCAPSULAMIENTO)
    @property
    def numero_membresia(self):
        return self.__numero_membresia
    
    @property
    def titular(self):
        return self.__titular
    
    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, nuevo_estado):
        if nuevo_estado in ["activa", "suspendida", "cancelada"]:
            self.__estado = nuevo_estado
        else:
            raise ValueError("Estado inválido")
    
    # Métodos abstractos (ABSTRACCIÓN)
    @abstractmethod
    def calcular_costo_mensual(self):
        """Calcula el costo mensual según el tipo de membresía"""
        pass
    
    @abstractmethod
    def obtener_horarios_permitidos(self):
        """Retorna los horarios permitidos según el tipo de membresía"""
        pass
    
    # Método privado (ENCAPSULAMIENTO)
    def __calcular_descuento(self, meses):
        """Calcula descuento por pago anticipado"""
        if meses >= 12:
            return 0.20  # 20% descuento anual
        elif meses >= 6:
            return 0.10  # 10% descuento semestral
        return 0.0
    
    # Método concreto
    def renovar_membresia(self, meses=1):
        """Renueva la membresía por N meses"""
        costo_base = self.calcular_costo_mensual() * meses
        descuento = self.__calcular_descuento(meses)
        costo_final = costo_base * (1 - descuento)
        
        pago = {
            "fecha": datetime.now().isoformat(),
            "meses": meses,
            "costo_base": costo_base,
            "descuento": descuento,
            "costo_final": costo_final
        }
        self.__historial_pagos.append(pago)
        return costo_final
    
    def to_dict(self):
        """Convierte la membresía a diccionario para JSON"""
        return {
            "numero_membresia": self.__numero_membresia,
            "titular": self.__titular,
            "fecha_inicio": self.__fecha_inicio,
            "estado": self.__estado,
            "tipo": self.__class__.__name__,
            "servicios_incluidos": self._servicios_incluidos,
            "historial_pagos": self.__historial_pagos
        }
    
    def __str__(self):
        return f"Membresía #{self.__numero_membresia} | {self.__titular} | {self.__estado.upper()}"


# HERENCIA: Clases derivadas de Membresía

class MembresiaBasica(Membresia):
    """Membresía básica con acceso limitado"""
    
    def __init__(self, numero_membresia, titular, fecha_inicio):
        super().__init__(numero_membresia, titular, fecha_inicio)
        self._servicios_incluidos = ["Acceso a máquinas", "Vestuarios"]
        self.acceso_maquinas = True
        self.horario_limitado = "6:00 AM - 2:00 PM"
    
    # POLIMORFISMO: Implementación específica
    def calcular_costo_mensual(self):
        return 30.0
    
    def obtener_horarios_permitidos(self):
        return self.horario_limitado
    
    def __str__(self):
        return f"{super().__str__()} | BÁSICA | ${self.calcular_costo_mensual()}/mes"


class MembresiaPremium(Membresia):
    """Membresía premium con todos los servicios"""
    
    def __init__(self, numero_membresia, titular, fecha_inicio):
        super().__init__(numero_membresia, titular, fecha_inicio)
        self._servicios_incluidos = [
            "Acceso a máquinas", "Clases grupales", "Spa", 
            "Lockers", "Nutricionista", "Toallas"
        ]
        self.clases_grupales = True
        self.spa = True
        self.lockers = True
        self.horario_completo = "5:00 AM - 11:00 PM"
    
    def calcular_costo_mensual(self):
        return 60.0
    
    def obtener_horarios_permitidos(self):
        return self.horario_completo
    
    def __str__(self):
        return f"{super().__str__()} | PREMIUM | ${self.calcular_costo_mensual()}/mes"


class MembresiaFamiliar(Membresia):
    """Membresía familiar con descuento por grupo"""
    
    def __init__(self, numero_membresia, titular, fecha_inicio, num_integrantes=2):
        super().__init__(numero_membresia, titular, fecha_inicio)
        self._servicios_incluidos = [
            "Acceso a máquinas", "Clases grupales", "Plan compartido"
        ]
        self.num_integrantes = num_integrantes
        self.descuento_grupo = 0.15  # 15% descuento
        self.plan_compartido = True
    
    def calcular_costo_mensual(self):
        costo_base = 40.0 * self.num_integrantes
        return costo_base * (1 - self.descuento_grupo)
    
    def obtener_horarios_permitidos(self):
        return "6:00 AM - 10:00 PM"
    
    def __str__(self):
        return f"{super().__str__()} | FAMILIAR ({self.num_integrantes} personas) | ${self.calcular_costo_mensual():.2f}/mes"


class MembresiaCorporativa(Membresia):
    """Membresía corporativa para empresas"""
    
    def __init__(self, numero_membresia, titular, fecha_inicio, empresa, num_empleados=1):
        super().__init__(numero_membresia, titular, fecha_inicio)
        self._servicios_incluidos = [
            "Acceso a máquinas", "Clases grupales", "Facturación empresarial"
        ]
        self.empresa = empresa
        self.num_empleados = num_empleados
        self.facturacion_empresa = True
    
    def calcular_costo_mensual(self):
        return 25.0 * self.num_empleados
    
    def obtener_horarios_permitidos(self):
        return "6:00 AM - 10:00 PM"
    
    def __str__(self):
        return f"{super().__str__()} | CORPORATIVA ({self.empresa}) | {self.num_empleados} empleados | ${self.calcular_costo_mensual():.2f}/mes"


# =============================================================================
# EJERCICIO 10.2: CLASES Y ENTRENAMIENTOS
# src/models/clase.py
# =============================================================================

class ClaseGrupal(ABC):
    """
    Clase abstracta base para clases grupales del gimnasio.
    Implementa ABSTRACCIÓN.
    """
    
    def __init__(self, nombre_clase, instructor, horario, duracion_min):
        # ENCAPSULAMIENTO: Atributos privados
        self.__nombre_clase = nombre_clase
        self.__instructor = instructor
        self.__horario = horario
        self.__duracion_min = duracion_min
        
        # Atributo protegido
        self._participantes_inscritos = []
        self._historial_asistencia = []
    
    @property
    def nombre_clase(self):
        return self.__nombre_clase
    
    @property
    def instructor(self):
        return self.__instructor
    
    @property
    def cupos_disponibles(self):
        return self.calcular_cupo_maximo() - len(self._participantes_inscritos)
    
    # Métodos abstractos (ABSTRACCIÓN)
    @abstractmethod
    def calcular_cupo_maximo(self):
        """Calcula el cupo máximo según el tipo de clase"""
        pass
    
    @abstractmethod
    def calcular_calorias_quemadas(self):
        """Estima calorías quemadas según tipo de clase"""
        pass
    
    # Método privado (ENCAPSULAMIENTO)
    def __validar_nivel_cliente(self, cliente, nivel_requerido):
        """Valida si el cliente cumple con el nivel requerido"""
        nivel_cliente = getattr(cliente, 'nivel', 'principiante')
        niveles = {'principiante': 1, 'intermedio': 2, 'avanzado': 3}
        return niveles.get(nivel_cliente, 1) >= niveles.get(nivel_requerido, 1)
    
    # Método concreto
    def inscribir_participante(self, cliente):
        """Inscribe un participante si hay cupo"""
        if len(self._participantes_inscritos) >= self.calcular_cupo_maximo():
            return False, "Clase llena"
        
        if cliente in self._participantes_inscritos:
            return False, "Ya está inscrito"
        
        self._participantes_inscritos.append(cliente)
        return True, "Inscripción exitosa"
    
    def registrar_asistencia(self, fecha):
        """Registra la asistencia de la clase"""
        self._historial_asistencia.append({
            "fecha": fecha,
            "asistentes": len(self._participantes_inscritos)
        })
    
    def to_dict(self):
        return {
            "nombre_clase": self.__nombre_clase,
            "instructor": self.__instructor,
            "horario": self.__horario,
            "duracion_min": self.__duracion_min,
            "tipo": self.__class__.__name__,
            "participantes": len(self._participantes_inscritos),
            "cupo_maximo": self.calcular_cupo_maximo()
        }
    
    def __str__(self):
        return f"{self.__nombre_clase} | {self.__instructor} | {self.__horario} | {len(self._participantes_inscritos)}/{self.calcular_cupo_maximo()}"


# HERENCIA: Clases derivadas

class ClaseYoga(ClaseGrupal):
    """Clase de Yoga con diferentes niveles"""
    
    def __init__(self, nombre_clase, instructor, horario, duracion_min, nivel="principiante", tipo_yoga="Hatha"):
        super().__init__(nombre_clase, instructor, horario, duracion_min)
        self.nivel = nivel
        self.tipo_yoga = tipo_yoga
        self.colchonetas_necesarias = True
    
    # POLIMORFISMO
    def calcular_cupo_maximo(self):
        return 20
    
    def calcular_calorias_quemadas(self):
        # Calorías por minuto según nivel
        calorias_minuto = {'principiante': 3, 'intermedio': 4, 'avanzado': 5}
        return calorias_minuto.get(self.nivel, 3) * self._ClaseGrupal__duracion_min
    
    def __str__(self):
        return f"YOGA {self.tipo_yoga} | {super().__str__()} | {self.nivel}"


class ClaseSpinning(ClaseGrupal):
    """Clase de Spinning de alta intensidad"""
    
    def __init__(self, nombre_clase, instructor, horario, duracion_min, intensidad="media"):
        super().__init__(nombre_clase, instructor, horario, duracion_min)
        self.bicicletas_disponibles = 15
        self.intensidad = intensidad
        self.musica = True
    
    def calcular_cupo_maximo(self):
        return self.bicicletas_disponibles
    
    def calcular_calorias_quemadas(self):
        intensidades = {'baja': 8, 'media': 10, 'alta': 12}
        return intensidades.get(self.intensidad, 10) * self._ClaseGrupal__duracion_min
    
    def __str__(self):
        return f"SPINNING | {super().__str__()} | Intensidad: {self.intensidad}"


class ClaseFuncional(ClaseGrupal):
    """Clase de entrenamiento funcional"""
    
    def __init__(self, nombre_clase, instructor, horario, duracion_min, nivel_dificultad="intermedio"):
        super().__init__(nombre_clase, instructor, horario, duracion_min)
        self.equipamiento = ["TRX", "Kettlebells", "Bandas elásticas"]
        self.nivel_dificultad = nivel_dificultad
        self.tipo_entrenamiento = "Circuito"
    
    def calcular_cupo_maximo(self):
        return 25
    
    def calcular_calorias_quemadas(self):
        dificultades = {'principiante': 7, 'intermedio': 9, 'avanzado': 11}
        return dificultades.get(self.nivel_dificultad, 9) * self._ClaseGrupal__duracion_min
    
    def __str__(self):
        return f"FUNCIONAL | {super().__str__()} | Nivel: {self.nivel_dificultad}"


class ClaseAerobicos(ClaseGrupal):
    """Clase de aeróbicos con coreografía"""
    
    def __init__(self, nombre_clase, instructor, horario, duracion_min, nivel_impacto="medio"):
        super().__init__(nombre_clase, instructor, horario, duracion_min)
        self.coreografia = True
        self.nivel_impacto = nivel_impacto
        self.musica = True
    
    def calcular_cupo_maximo(self):
        return 30
    
    def calcular_calorias_quemadas(self):
        impactos = {'bajo': 5, 'medio': 7, 'alto': 9}
        return impactos.get(self.nivel_impacto, 7) * self._ClaseGrupal__duracion_min
    
    def __str__(self):
        return f"AERÓBICOS | {super().__str__()} | Impacto: {self.nivel_impacto}"


# =============================================================================
# EJERCICIO 10.3: ENTRENADORES Y PERSONAL
# src/models/empleado.py
# =============================================================================

class EmpleadoGimnasio(ABC):
    """
    Clase abstracta base para empleados del gimnasio.
    Implementa ABSTRACCIÓN.
    """
    
    def __init__(self, nombre, codigo, especialidad, horario):
        # ENCAPSULAMIENTO
        self.__nombre = nombre
        self.__codigo = codigo
        self.__especialidad = especialidad
        self.__horario = horario
        self.__salario_base = 0.0
        self.__evaluaciones = []
        
        # Atributo protegido
        self._clientes_asignados = []
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def codigo(self):
        return self.__codigo
    
    # Métodos abstractos (ABSTRACCIÓN)
    @abstractmethod
    def calcular_salario(self):
        """Calcula el salario según el tipo de empleado"""
        pass
    
    @abstractmethod
    def generar_plan_trabajo(self):
        """Genera plan de trabajo específico"""
        pass
    
    # Método privado (ENCAPSULAMIENTO)
    def __calcular_comisiones(self):
        """Calcula comisiones según desempeño"""
        if len(self._clientes_asignados) > 10:
            return self.__salario_base * 0.10
        return 0.0
    
    # Método concreto
    def registrar_asistencia(self, fecha, presente=True):
        """Registra asistencia del empleado"""
        return {
            "fecha": fecha,
            "empleado": self.__nombre,
            "presente": presente
        }
    
    def to_dict(self):
        return {
            "nombre": self.__nombre,
            "codigo": self.__codigo,
            "especialidad": self.__especialidad,
            "horario": self.__horario,
            "tipo": self.__class__.__name__,
            "clientes_asignados": len(self._clientes_asignados),
            "salario": self.calcular_salario()
        }
    
    def __str__(self):
        return f"{self.__nombre} | {self.__codigo} | {self.__especialidad}"


# HERENCIA: Clases derivadas

class EntrenadorPersonal(EmpleadoGimnasio):
    """Entrenador personal con clientes individuales"""
    
    def __init__(self, nombre, codigo, especialidad, horario, certificaciones, tarifa_hora=25.0):
        super().__init__(nombre, codigo, especialidad, horario)
        self.certificaciones = certificaciones
        self.clientes_activos = []
        self.tarifa_hora = tarifa_hora
        self.horas_trabajadas = 0
    
    # POLIMORFISMO
    def calcular_salario(self):
        salario_base = self.tarifa_hora * self.horas_trabajadas
        comision = len(self.clientes_activos) * 50  # Bonificación por cliente
        return salario_base + comision
    
    def generar_plan_trabajo(self):
        return {
            "tipo": "Entrenamiento Personalizado",
            "clientes": len(self.clientes_activos),
            "horas_semanales": self.horas_trabajadas / 4,
            "especialidad": self._EmpleadoGimnasio__especialidad
        }
    
    def __str__(self):
        return f"ENTRENADOR PERSONAL | {super().__str__()} | {len(self.clientes_activos)} clientes"


class InstructorGrupal(EmpleadoGimnasio):
    """Instructor de clases grupales"""
    
    def __init__(self, nombre, codigo, especialidad, horario, clases_imparte):
        super().__init__(nombre, codigo, especialidad, horario)
        self.clases_imparte = clases_imparte
        self.horario_clases = []
        self.salario_fijo = 800.0
    
    def calcular_salario(self):
        pago_por_clase = 15.0
        total_clases = len(self.horario_clases) * 4  # Clases mensuales
        return self.salario_fijo + (pago_por_clase * total_clases)
    
    def generar_plan_trabajo(self):
        return {
            "tipo": "Clases Grupales",
            "clases_imparte": self.clases_imparte,
            "horarios": self.horario_clases,
            "clases_mes": len(self.horario_clases) * 4
        }
    
    def __str__(self):
        return f"INSTRUCTOR | {super().__str__()} | {len(self.clases_imparte)} clases"


class Nutricionista(EmpleadoGimnasio):
    """Nutricionista con consultas y planes alimenticios"""
    
    def __init__(self, nombre, codigo, especialidad, horario, consultas_dia=8):
        super().__init__(nombre, codigo, especialidad, horario)
        self.consultas_dia = consultas_dia
        self.planes_alimenticios = []
        self.tarifa_consulta = 40.0
    
    def calcular_salario(self):
        consultas_mensuales = self.consultas_dia * 20  # Días laborables
        return consultas_mensuales * self.tarifa_consulta
    
    def generar_plan_trabajo(self):
        return {
            "tipo": "Consultas Nutricionales",
            "consultas_dia": self.consultas_dia,
            "planes_activos": len(self.planes_alimenticios),
            "consultas_mes": self.consultas_dia * 20
        }
    
    def __str__(self):
        return f"NUTRICIONISTA | {super().__str__()} | {self.consultas_dia} consultas/día"


class Administrativo(EmpleadoGimnasio):
    """Personal administrativo"""
    
    def __init__(self, nombre, codigo, area, horario, turno, salario_fijo=1200.0):
        super().__init__(nombre, codigo, area, horario)
        self.area = area
        self.turno = turno
        self.salario_fijo = salario_fijo
    
    def calcular_salario(self):
        return self.salario_fijo
    
    def generar_plan_trabajo(self):
        return {
            "tipo": "Administrativo",
            "area": self.area,
            "turno": self.turno,
            "horario": self._EmpleadoGimnasio__horario
        }
    
    def __str__(self):
        return f"ADMINISTRATIVO | {super().__str__()} | {self.area} | {self.turno}"


# =============================================================================
# EJERCICIO 10.4: EQUIPAMIENTO Y MANTENIMIENTO
# src/models/equipo.py
# =============================================================================

class Equipo(ABC):
    """
    Clase abstracta base para equipamiento del gimnasio.
    Implementa ABSTRACCIÓN.
    """
    
    def __init__(self, codigo, nombre, fecha_adquisicion, valor):
        # ENCAPSULAMIENTO
        self.__codigo = codigo
        self.__nombre = nombre
        self.__fecha_adquisicion = fecha_adquisicion
        self.__valor = valor
        self.__valor_actual = valor
        
        # Atributo protegido
        self._historial_mantenimiento = []
    
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def valor_actual(self):
        return self.__valor_actual
    
    # Métodos abstractos (ABSTRACCIÓN)
    @abstractmethod
    def calcular_depreciacion(self):
        """Calcula la depreciación anual del equipo"""
        pass
    
    @abstractmethod
    def frecuencia_mantenimiento_dias(self):
        """Retorna días entre mantenimientos"""
        pass
    
    # Método privado (ENCAPSULAMIENTO)
    def __calcular_vida_util_restante(self):
        """Calcula años de vida útil restantes"""
        años_transcurridos = (datetime.now() - datetime.fromisoformat(self.__fecha_adquisicion)).days / 365
        vida_util_total = 10  # años
        return max(0, vida_util_total - años_transcurridos)
    
    # Método concreto
    def registrar_mantenimiento(self, fecha, tipo="preventivo", costo=0.0):
        """Registra un mantenimiento realizado"""
        mantenimiento = {
            "fecha": fecha,
            "tipo": tipo,
            "costo": costo,
            "realizado_por": "Técnico"
        }
        self._historial_mantenimiento.append(mantenimiento)
        return mantenimiento
    
    def actualizar_valor(self):
        """Actualiza el valor actual con depreciación"""
        depreciacion_anual = self.calcular_depreciacion()
        años = (datetime.now() - datetime.fromisoformat(self.__fecha_adquisicion)).days / 365
        self.__valor_actual = max(0, self.__valor * (1 - depreciacion_anual * años))
        return self.__valor_actual
    
    def to_dict(self):
        return {
            "codigo": self.__codigo,
            "nombre": self.__nombre,
            "fecha_adquisicion": self.__fecha_adquisicion,
            "valor_original": self.__valor,
            "valor_actual": self.__valor_actual,
            "tipo": self.__class__.__name__,
            "mantenimientos": len(self._historial_mantenimiento)
        }
    
    def __str__(self):
        return f"{self.__codigo} | {self.__nombre} | ${self.__valor_actual:.2f}"


# HERENCIA: Clases derivadas

class MaquinaCardio(Equipo):
    """Máquinas cardiovasculares"""
    
    def __init__(self, codigo, nombre, fecha_adquisicion, valor, tipo_cardio="cinta"):
        super().__init__(codigo, nombre, fecha_adquisicion, valor)
        self.tipo = tipo_cardio  # cinta, eliptica, bici
        self.horas_uso = 0
        self.calibracion = datetime.now().isoformat()
    
    # POLIMORFISMO
    def calcular_depreciacion(self):
        return 0.15  # 15% anual (alta depreciación)
    
    def frecuencia_mantenimiento_dias(self):
        return 30  # Mantenimiento mensual
    
    def __str__(self):
        return f"CARDIO ({self.tipo}) | {super().__str__()} | {self.horas_uso}h uso"


class Pesa(Equipo):
    """Pesas y mancuernas"""
    
    def __init__(self, codigo, nombre, fecha_adquisicion, valor, peso_kg, tipo_material="hierro"):
        super().__init__(codigo, nombre, fecha_adquisicion, valor)
        self.peso_kg = peso_kg
        self.tipo_material = tipo_material
        self.set_completo = True
    
    def calcular_depreciacion(self):
        return 0.05  # 5% anual (baja depreciación)
    
    def frecuencia_mantenimiento_dias(self):
        return 180  # Mantenimiento semestral
    
    def __str__(self):
        return f"PESA {self.peso_kg}kg | {super().__str__()} | {self.tipo_material}"


class EquipoFuncional(Equipo):
    """Equipos de entrenamiento funcional"""
    
    def __init__(self, codigo, nombre, fecha_adquisicion, valor, tipo_funcional="TRX"):
        super().__init__(codigo, nombre, fecha_adquisicion, valor)
        self.tipo = tipo_funcional
        self.versatilidad = "Alta"
        self.espacio_requerido = "Medio"
    
    def calcular_depreciacion(self):
        return 0.10  # 10% anual (depreciación media)
    
    def frecuencia_mantenimiento_dias(self):
        return 60  # Mantenimiento bimensual
    
    def __str__(self):
        return f"FUNCIONAL ({self.tipo}) | {super().__str__()}"


class Accesorio(Equipo):
    """Accesorios diversos del gimnasio"""
    
    def __init__(self, codigo, nombre, fecha_adquisicion, valor, tipo_accesorio, cantidad=1):
        super().__init__(codigo, nombre, fecha_adquisicion, valor)
        self.tipo = tipo_accesorio
        self.cantidad = cantidad
        self.reemplazable = True
    
    def calcular_depreciacion(self):
        return 0.25  # 25% anual (muy alta depreciación)
    
    def frecuencia_mantenimiento_dias(self):
        return 15  # Revisión quincenal
    
    def __str__(self):
        return f"ACCESORIO ({self.tipo}) | {super().__str__()} | x{self.cantidad}"


# =============================================================================
# ARCHIVO DE PRUEBA COMPLETO
# test_gym_system.py
# =============================================================================

def test_sistema_completo():
    """
    Prueba completa del sistema de gimnasio
    Demuestra los 4 pilares de POO en acción
    """
    
    print("=" * 80)
    print("PRUEBA COMPLETA DEL SISTEMA DE GIMNASIO")
    print("=" * 80)
    
    # ==========================
    # TEST 10.1: MEMBRESÍAS
    # ==========================
    print("\n" + "=" * 80)
    print("EJERCICIO 10.1: PLANES Y MEMBRESÍAS")
    print("=" * 80)
    
    # Crear 3 membresías de cada tipo
    membresias = [
        MembresiaBasica(1001, "Juan Pérez", "2024-01-15"),
        MembresiaBasica(1002, "María García", "2024-02-01"),
        MembresiaBasica(1003, "Carlos López", "2024-03-10"),
        
        MembresiaPremium(2001, "Ana Martínez", "2024-01-20"),
        MembresiaPremium(2002, "Luis Rodríguez", "2024-02-15"),
        MembresiaPremium(2003, "Sofia Hernández", "2024-03-05"),
        
        MembresiaFamiliar(3001, "Familia Gómez", "2024-01-10", 4),
        MembresiaFamiliar(3002, "Familia Torres", "2024-02-20", 3),
        MembresiaFamiliar(3003, "Familia Ramírez", "2024-03-15", 5),
        
        MembresiaCorporativa(4001, "Tech Corp", "2024-01-05", "TechCorp SA", 15),
        MembresiaCorporativa(4002, "FinanzasPlus", "2024-02-10", "FinanzasPlus Ltd", 20),
        MembresiaCorporativa(4003, "StartupHub", "2024-03-01", "StartupHub Inc", 10)
    ]
    
    # Mostrar todas las membresías (POLIMORFISMO en acción)
    print("\n📋 LISTADO DE MEMBRESÍAS:")
    print("-" * 80)
    for membresia in membresias:
        print(membresia)
        print(f"   Horarios: {membresia.obtener_horarios_permitidos()}")
        print(f"   Servicios: {', '.join(membresia._servicios_incluidos)}")
        print()
    
    # Calcular ingresos mensuales proyectados
    print("\n💰 INGRESOS MENSUALES PROYECTADOS:")
    print("-" * 80)
    ingresos_por_tipo = {}
    total_ingresos = 0
    
    for membresia in membresias:
        tipo = membresia.__class__.__name__
        costo = membresia.calcular_costo_mensual()
        ingresos_por_tipo[tipo] = ingresos_por_tipo.get(tipo, 0) + costo
        total_ingresos += costo
    
    for tipo, ingreso in ingresos_por_tipo.items():
        print(f"{tipo:25s}: ${ingreso:10.2f}")
    
    print("-" * 80)
    print(f"{'TOTAL INGRESOS':25s}: ${total_ingresos:10.2f}")
    
    # Generar reporte de servicios más usados
    print("\n📊 SERVICIOS MÁS UTILIZADOS:")
    print("-" * 80)
    servicios_count = {}
    for membresia in membresias:
        for servicio in membresia._servicios_incluidos:
            servicios_count[servicio] = servicios_count.get(servicio, 0) + 1
    
    for servicio, count in sorted(servicios_count.items(), key=lambda x: x[1], reverse=True):
        print(f"{servicio:30s}: {count:3d} membresías")
    
    # ==========================
    # TEST 10.2: CLASES GRUPALES
    # ==========================
    print("\n\n" + "=" * 80)
    print("EJERCICIO 10.2: CLASES Y ENTRENAMIENTOS")
    print("=" * 80)
    
    # Crear 2 clases de cada tipo
    clases = [
        ClaseYoga("Yoga Matutino", "Instructor Zen", "07:00", 60, "principiante", "Hatha"),
        ClaseYoga("Yoga Avanzado", "Instructor Zen", "18:00", 75, "avanzado", "Vinyasa"),
        
        ClaseSpinning("Spinning Intenso", "Coach Energy", "06:00", 45, "alta"),
        ClaseSpinning("Spinning Moderado", "Coach Energy", "19:00", 45, "media"),
        
        ClaseFuncional("Funcional Boot Camp", "Trainer Pro", "08:00", 50, "avanzado"),
        ClaseFuncional("Funcional Inicio", "Trainer Pro", "17:00", 45, "principiante"),
        
        ClaseAerobicos("Aeróbicos Dance", "Coach Ritmo", "09:00", 60, "medio"),
        ClaseAerobicos("Aeróbicos HIIT", "Coach Ritmo", "20:00", 45, "alto")
    ]
    
    # Crear horario semanal
    print("\n📅 HORARIO SEMANAL DE CLASES:")
    print("-" * 80)
    dias_semana = ["Lunes", "Miércoles", "Viernes"]
    
    for dia in dias_semana:
        print(f"\n{dia}:")
        for clase in clases:
            print(f"  {clase}")
            print(f"     Cupo: {clase.cupos_disponibles}/{clase.calcular_cupo_maximo()}")
            print(f"     Calorías estimadas: {clase.calcular_calorias_quemadas()} kcal")
    
    # Inscribir clientes simulados
    print("\n\n👥 INSCRIPCIÓN DE CLIENTES:")
    print("-" * 80)
    clientes_simulados = [f"Cliente{i}" for i in range(1, 26)]
    
    for i, clase in enumerate(clases):
        # Inscribir diferentes cantidades según la clase
        num_inscritos = min(len(clientes_simulados), clase.calcular_cupo_maximo() - 2)
        for cliente in clientes_simulados[:num_inscritos]:
            clase.inscribir_participante(cliente)
        print(f"{clase.nombre_clase:25s}: {len(clase._participantes_inscritos)}/{clase.calcular_cupo_maximo()} inscritos")
    
    # Generar reporte de ocupación
    print("\n\n📊 REPORTE DE OCUPACIÓN:")
    print("-" * 80)
    ocupacion_por_tipo = {}
    total_cupos = 0
    cupos_ocupados = 0
    
    for clase in clases:
        tipo = clase.__class__.__name__
        cupo_max = clase.calcular_cupo_maximo()
        ocupados = len(clase._participantes_inscritos)
        
        if tipo not in ocupacion_por_tipo:
            ocupacion_por_tipo[tipo] = {"max": 0, "ocupados": 0}
        
        ocupacion_por_tipo[tipo]["max"] += cupo_max
        ocupacion_por_tipo[tipo]["ocupados"] += ocupados
        total_cupos += cupo_max
        cupos_ocupados += ocupados
    
    for tipo, datos in ocupacion_por_tipo.items():
        porcentaje = (datos["ocupados"] / datos["max"]) * 100
        print(f"{tipo:20s}: {datos['ocupados']:3d}/{datos['max']:3d} ({porcentaje:.1f}% ocupación)")
    
    porcentaje_total = (cupos_ocupados / total_cupos) * 100
    print("-" * 80)
    print(f"{'TOTAL':20s}: {cupos_ocupados:3d}/{total_cupos:3d} ({porcentaje_total:.1f}% ocupación)")
    
    # ==========================
    # TEST 10.3: EMPLEADOS
    # ==========================
    print("\n\n" + "=" * 80)
    print("EJERCICIO 10.3: ENTRENADORES Y PERSONAL")
    print("=" * 80)
    
    # Crear equipo completo
    empleados = [
        EntrenadorPersonal("Roberto Fitness", "E001", "Musculación", "9:00-18:00", ["NSCA-CPT", "CrossFit L1"], 30.0),
        EntrenadorPersonal("Laura Strong", "E002", "Fitness General", "8:00-17:00", ["ACE-CPT"], 25.0),
        
        InstructorGrupal("Carlos Yoga", "I001", "Yoga", "7:00-13:00", ["Yoga", "Pilates"]),
        InstructorGrupal("Diana Spin", "I002", "Spinning", "14:00-21:00", ["Spinning", "Aeróbicos"]),
        
        Nutricionista("Dra. María Salud", "N001", "Nutrición Deportiva", "9:00-18:00", 8),
        
        Administrativo("Pedro Admin", "A001", "Recepción", "6:00-14:00", "Mañana", 1200),
        Administrativo("Carmen Apoyo", "A002", "Administración", "14:00-22:00", "Tarde", 1300)
    ]
    
    # Asignar clientes y clases
    empleados[0].clientes_activos = [f"Cliente{i}" for i in range(1, 9)]
    empleados[0].horas_trabajadas = 160
    
    empleados[1].clientes_activos = [f"Cliente{i}" for i in range(9, 16)]
    empleados[1].horas_trabajadas = 140
    
    empleados[2].horario_clases = ["Lun 7:00", "Mie 7:00", "Vie 7:00"]
    empleados[3].horario_clases = ["Lun 19:00", "Mar 19:00", "Jue 19:00", "Vie 19:00"]
    
    empleados[4].planes_alimenticios = [f"Plan{i}" for i in range(1, 25)]
    
    # Mostrar equipo (POLIMORFISMO en acción)
    print("\n👥 EQUIPO DEL GIMNASIO:")
    print("-" * 80)
    for empleado in empleados:
        print(f"\n{empleado}")
        plan = empleado.generar_plan_trabajo()
        print(f"   Tipo: {plan['tipo']}")
        for key, value in plan.items():
            if key != 'tipo':
                print(f"   {key}: {value}")
    
    # Calcular nómina mensual
    print("\n\n💰 NÓMINA MENSUAL:")
    print("-" * 80)
    nomina_por_tipo = {}
    total_nomina = 0
    
    for empleado in empleados:
        tipo = empleado.__class__.__name__
        salario = empleado.calcular_salario()
        nomina_por_tipo[tipo] = nomina_por_tipo.get(tipo, 0) + salario
        total_nomina += salario
        print(f"{empleado.nombre:25s} ({tipo:20s}): ${salario:10.2f}")
    
    print("\n" + "-" * 80)
    print("RESUMEN POR TIPO DE EMPLEADO:")
    for tipo, total in nomina_por_tipo.items():
        print(f"{tipo:25s}: ${total:10.2f}")
    
    print("-" * 80)
    print(f"{'TOTAL NÓMINA':25s}: ${total_nomina:10.2f}")
    
    # ==========================
    # TEST 10.4: EQUIPAMIENTO
    # ==========================
    print("\n\n" + "=" * 80)
    print("EJERCICIO 10.4: EQUIPAMIENTO Y MANTENIMIENTO")
    print("=" * 80)
    
    # Crear inventario completo
    equipos = [
        MaquinaCardio("MC001", "Cinta Profesional", "2023-01-15", 3000, "cinta"),
        MaquinaCardio("MC002", "Elíptica Advanced", "2023-02-20", 2500, "eliptica"),
        MaquinaCardio("MC003", "Bicicleta Estática", "2023-03-10", 1800, "bici"),
        MaquinaCardio("MC004", "Cinta Running", "2024-01-15", 3200, "cinta"),
        
        Pesa("P001", "Mancuernas Set", "2022-06-01", 800, 20, "hierro"),
        Pesa("P002", "Barra Olímpica", "2022-06-01", 500, 20, "acero"),
        Pesa("P003", "Discos Olímpicos", "2022-06-01", 1200, 25, "hierro"),
        
        EquipoFuncional("EF001", "TRX Pro", "2023-05-10", 400, "TRX"),
        EquipoFuncional("EF002", "Kettlebells Set", "2023-05-10", 600, "Kettlebells"),
        EquipoFuncional("EF003", "Battle Ropes", "2023-06-15", 200, "Cuerdas"),
        
        Accesorio("AC001", "Colchonetas Yoga", "2024-01-01", 30, "colchoneta", 25),
        Accesorio("AC002", "Bandas Elásticas", "2024-01-01", 15, "banda", 40),
        Accesorio("AC003", "Toallas", "2024-02-01", 10, "toalla", 100)
    ]
    
    # Actualizar valores con depreciación
    for equipo in equipos:
        equipo.actualizar_valor()
    
    # Mostrar inventario
    print("\n📦 INVENTARIO DE EQUIPOS:")
    print("-" * 80)
    for equipo in equipos:
        print(f"{equipo}")
        print(f"   Valor original: ${equipo.to_dict()['valor_original']:.2f}")
        print(f"   Depreciación anual: {equipo.calcular_depreciacion()*100:.0f}%")
        print(f"   Mantenimiento cada: {equipo.frecuencia_mantenimiento_dias()} días")
        print()
    
    # Programar mantenimientos preventivos
    print("\n🔧 CALENDARIO DE MANTENIMIENTOS PREVENTIVOS:")
    print("-" * 80)
    mantenimientos_programados = []
    
    for equipo in equipos:
        tipo = equipo.__class__.__name__
        frecuencia = equipo.frecuencia_mantenimiento_dias()
        mantenimientos_programados.append({
            "equipo": equipo.nombre,
            "codigo": equipo.codigo,
            "tipo": tipo,
            "frecuencia": frecuencia,
            "proximo": f"Cada {frecuencia} días"
        })
    
    # Agrupar por frecuencia
    por_frecuencia = {}
    for mant in mantenimientos_programados:
        freq = mant["frecuencia"]
        if freq not in por_frecuencia:
            por_frecuencia[freq] = []
        por_frecuencia[freq].append(mant)
    
    for frecuencia in sorted(por_frecuencia.keys()):
        print(f"\nMantenimiento cada {frecuencia} días:")
        for mant in por_frecuencia[frecuencia]:
            print(f"  - {mant['codigo']:10s} {mant['equipo']:30s} ({mant['tipo']})")
    
    # Calcular valor actual de activos
    print("\n\n💎 VALOR ACTUAL DE ACTIVOS:")
    print("-" * 80)
    valor_por_tipo = {}
    valor_original_total = 0
    valor_actual_total = 0
    
    for equipo in equipos:
        tipo = equipo.__class__.__name__
        datos = equipo.to_dict()
        valor_original = datos['valor_original']
        valor_actual = datos['valor_actual']
        
        if tipo not in valor_por_tipo:
            valor_por_tipo[tipo] = {"original": 0, "actual": 0}
        
        valor_por_tipo[tipo]["original"] += valor_original
        valor_por_tipo[tipo]["actual"] += valor_actual
        valor_original_total += valor_original
        valor_actual_total += valor_actual
    
    for tipo, valores in valor_por_tipo.items():
        depreciacion_tipo = ((valores["original"] - valores["actual"]) / valores["original"]) * 100
        print(f"{tipo:20s}:")
        print(f"  Valor original: ${valores['original']:10.2f}")
        print(f"  Valor actual:   ${valores['actual']:10.2f}")
        print(f"  Depreciación:   {depreciacion_tipo:6.1f}%")
        print()
    
    depreciacion_total = ((valor_original_total - valor_actual_total) / valor_original_total) * 100
    print("-" * 80)
    print(f"{'TOTAL ACTIVOS':20s}:")
    print(f"  Valor original: ${valor_original_total:10.2f}")
    print(f"  Valor actual:   ${valor_actual_total:10.2f}")
    print(f"  Depreciación:   {depreciacion_total:6.1f}%")
    
    # ==========================
    # RESUMEN FINAL
    # ==========================
    print("\n\n" + "=" * 80)
    print("RESUMEN EJECUTIVO DEL SISTEMA DE GIMNASIO")
    print("=" * 80)
    
    print(f"\n📊 MEMBRESÍAS:")
    print(f"  Total membresías activas: {len(membresias)}")
    print(f"  Ingresos mensuales: ${total_ingresos:.2f}")
    
    print(f"\n📅 CLASES:")
    print(f"  Total clases ofrecidas: {len(clases)}")
    print(f"  Ocupación promedio: {porcentaje_total:.1f}%")
    
    print(f"\n👥 PERSONAL:")
    print(f"  Total empleados: {len(empleados)}")
    print(f"  Nómina mensual: ${total_nomina:.2f}")
    
    print(f"\n💎 ACTIVOS:")
    print(f"  Total equipos: {len(equipos)}")
    print(f"  Valor actual: ${valor_actual_total:.2f}")
    
    print(f"\n💰 RESUMEN FINANCIERO:")
    ingresos = total_ingresos
    egresos = total_nomina + 500  # + costos operativos estimados
    utilidad = ingresos - egresos
    margen = (utilidad / ingresos) * 100 if ingresos > 0 else 0
    
    print(f"  Ingresos:  ${ingresos:10.2f}")
    print(f"  Egresos:   ${egresos:10.2f}")
    print(f"  Utilidad:  ${utilidad:10.2f}")
    print(f"  Margen:    {margen:7.1f}%")
    
    print("\n" + "=" * 80)
    print("DEMOSTRACIÓN COMPLETA DE LOS 4 PILARES DE POO:")
    print("=" * 80)
    print("✅ ABSTRACCIÓN:      Clases abstractas base definen contratos")
    print("✅ ENCAPSULAMIENTO:  Atributos privados y protegidos, getters/setters")
    print("✅ HERENCIA:         Múltiples clases derivadas especializadas")
    print("✅ POLIMORFISMO:     Métodos sobrescritos con comportamientos únicos")
    print("=" * 80)


if __name__ == "__main__":
    test_sistema_completo()