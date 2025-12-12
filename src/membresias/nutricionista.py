
from .base import EmpleadoGimnasio

class Nutricionista(EmpleadoGimnasio):
    def __init__(self,nombre,cod,esp,citas,tarifa):
        super().__init__(nombre,cod,esp,0)
        self.citas=citas
        self.tarifa=tarifa

    def calcular_salario(self):
        return self.citas*self.tarifa*4

    def generar_plan_trabajo(self):
        return "Plan nutricional mensual"
