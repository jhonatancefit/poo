
from .base import EmpleadoGimnasio

class EntrenadorPersonal(EmpleadoGimnasio):
    def __init__(self,nombre,cod,esp,tarifa):
        super().__init__(nombre,cod,esp,0)
        self.tarifa=tarifa

    def calcular_salario(self):
        return self.tarifa*40

    def generar_plan_trabajo(self):
        return "Plan personalizado"
