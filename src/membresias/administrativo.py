
from .base import EmpleadoGimnasio

class Administrativo(EmpleadoGimnasio):
    def __init__(self,nombre,cod,esp,turno,sal):
        super().__init__(nombre,cod,esp,turno)
        self.sal=sal

    def calcular_salario(self):
        return self.sal

    def generar_plan_trabajo(self):
        return "Gestión administrativa"
