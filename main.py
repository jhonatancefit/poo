from datetime import date

# === MEMBRESÍAS ===
from src.membresias.basica import MembresiaBasica
from src.membresias.premium import MembresiaPremium
from src.membresias.familiar import MembresiaFamiliar
from src.membresias.corporativa import MembresiaCorporativa

# === CLASES GRUPALES ===
from src.clases.yoga import ClaseYoga
from src.clases.spinning import ClaseSpinning
from src.clases.funcional import ClaseFuncional
from src.clases.aerobicos import ClaseAerobicos

# === EMPLEADOS ===
from src.empleados.entrenador import EntrenadorPersonal
from src.empleados.instructor import InstructorGrupal
from src.empleados.nutricionista import Nutricionista
from src.empleados.administrativo import Administrativo

# === EQUIPOS ===
from src.equipos.cardio import MaquinaCardio
from src.equipos.pesa import Pesa
from src.equipos.funcional import EquipoFuncional
from src.equipos.accesorio import Accesorio


print("\n=== SISTEMA DE GIMNASIO — PRUEBAS ===\n")

# -------------------------------------------------------------------
# 1. MEMBRESÍAS
# -------------------------------------------------------------------
print("---- MEMBRESÍAS ----")

m1 = MembresiaBasica(1, "Ana", date.today())
m2 = MembresiaPremium(2, "Luis", date.today())
m3 = MembresiaFamiliar(3, "Familia Gómez", date.today(), 3)
m4 = MembresiaCorporativa(4, "CorpX", date.today(), "CorpX", 12)

membresias = [m1, m2, m3, m4]

for m in membresias:
    print(f"{m} -> Costo: ${m.calcular_costo_mensual():.2f}, Horarios: {m.obtener_horarios_permitidos()}")

# -------------------------------------------------------------------
# 2. CLASES GRUPALES
# -------------------------------------------------------------------
print("\n---- CLASES GRUPALES ----")

c1 = ClaseYoga("Yoga Mañana", "Laura", "Lunes 7am", 60)
c2 = ClaseSpinning("Spinning Pro", "Marco", "Martes 6pm", 45, 12)
c3 = ClaseFuncional("Funcional Total", "Diego", "Jueves 8am", 50)
c4 = ClaseAerobicos("AeroDance", "Lina", "Sábado 9am", 50)

clases = [c1, c2, c3, c4]

# Inscribir participantes
for i, clase in enumerate(clases):
    clase.inscribir_participante(100 + i)
    clase.inscribir_participante(200 + i)
    print(f"{clase._nombre} -> Ocupación: {clase.obtener_ocupacion()} / {clase.calcular_cupo_maximo()}")

# -------------------------------------------------------------------
# 3. EMPLEADOS
# -------------------------------------------------------------------
print("\n---- EMPLEADOS ----")

e1 = EntrenadorPersonal("Javier", "E01", "Fuerza", 40)
e2 = InstructorGrupal("Mariana", "E02", "Yoga", ["Yoga A", "Yoga B"])
e3 = Nutricionista("Sara", "E03", "Nutrición", 4, 50)
e4 = Administrativo("Pedro", "E04", "Admin", "mañana", 1200)

empleados = [e1, e2, e3, e4]

for emp in empleados:
    print(f"{emp._nombre} -> Salario mensual: ${emp.calcular_salario():.2f}")

# -------------------------------------------------------------------
# 4. EQUIPOS
# -------------------------------------------------------------------
print("\n---- EQUIPOS ----")

eq1 = MaquinaCardio("C01", "Caminadora", date(2022, 1, 1), 5000, 1000)
eq2 = Pesa("P01", "Set de Pesas", date(2021, 5, 1), 1500)
eq3 = EquipoFuncional("F01", "Rack Crossfit", date(2020, 6, 1), 7000)
eq4 = Accesorio("A01", "Bandas Elásticas", date(2023, 1, 1), 200)

equipos = [eq1, eq2, eq3, eq4]

for eq in equipos:
    print(f"{eq._nombre} -> Depreciación anual: ${eq.calcular_depreciacion():.2f}")

print("\n=== FIN DE PRUEBAS ===\n")