
from .base import EmpleadoGimnasio

class InstructorGrupal(EmpleadoGimnasio):
    def __init__(self,nombre,cod,esp,clases):
        super().__init__(nombre,cod,esp,0)
        self.clases=clases

    def calcular_salario(self):
        return 1200 + len(self.clases)*50

    def generar_plan_trabajo(self):
        return "Plan de clases grupales"
