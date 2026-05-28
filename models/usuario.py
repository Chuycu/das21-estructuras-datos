# models/usuario.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Usuario:
    nombre: str
    edad: Optional[int] = None
    genero: Optional[str] = None
    fecha_registro: str = None
    id: int = 0
    tests_realizados: List[dict] = field(default_factory=list)
    test_en_progreso: Optional[list] = field(default=None)

    def __post_init__(self):
        if self.fecha_registro is None:
            self.fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def agregar_test(self, respuestas: list[int], resultados, total: int):
        test = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "respuestas": respuestas,
            "puntaje_total": total,
            "depresion": resultados[0].puntaje,
            "ansiedad": resultados[1].puntaje,
            "estres": resultados[2].puntaje,
        }
        self.tests_realizados.append(test)

    def iniciar_test(self):
        self.test_en_progreso = [-1] * 21

    def guardar_progreso(self, respuestas: list[int]):
        self.test_en_progreso = respuestas[:]

    def finalizar_test(self):
        self.test_en_progreso = None

    def tiene_test_en_progreso(self) -> bool:
        return self.test_en_progreso is not None

    def progreso_test(self) -> int:
        if not self.test_en_progreso:
            return 0
        return sum(1 for r in self.test_en_progreso if r >= 0)

    def cantidad_tests(self) -> int:
        return len(self.tests_realizados)