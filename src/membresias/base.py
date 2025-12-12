
from abc import ABC, abstractmethod

class EmpleadoGimnasio(ABC):
    def __init__(self,nombre,codigo,esp,hor):
        self._nombre=nombre
        self.__codigo=codigo
        self.__esp=esp
        self.__hor=hor
        self._clientes_asignados=[]

    @abstractmethod
    def calcular_salario(self): ...

    @abstractmethod
    def generar_plan_trabajo(self): ...

    def registrar_asistencia(self):
        return True
