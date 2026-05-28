from abc import ABC, abstractmethod
from dataclasses import dataclass


PREGUNTAS = [
    "Me ha costado mucho descargar la tensión.",
    "Me di cuenta que tenía la boca seca.",
    "No podía sentir ningún sentimiento positivo.",
    "Se me hizo difícil respirar.",
    "Se me hizo difícil tomar la iniciativa para hacer cosas.",
    "Reaccioné exageradamente en ciertas situaciones.",
    "Sentí que mis manos temblaban.",
    "He sentido que estaba gastando una gran cantidad de energía.",
    "Estaba preocupado por situaciones en las cuales podía tener pánico o en las que podría hacer el ridículo.",
    "He sentido que no había nada que me ilusionara.",
    "Me he sentido inquieto.",
    "Se me hizo difícil relajarme.",
    "Me sentí triste y deprimido.",
    "No toleré nada que no me permitiera continuar con lo que estaba haciendo.",
    "Sentí que estaba al punto de pánico.",
    "No me pude entusiasmar por nada.",
    "Sentí que valía muy poco como persona.",
    "He tendido a sentirme enfadado con facilidad.",
    "Sentí los latidos de mi corazón a pesar de no haber hecho ningún esfuerzo físico.",
    "Tuve miedo sin razón.",
    "Sentí que la vida no tenía ningún sentido.",
]

OPCIONES = [
    ("0", "No me ha ocurrido"),
    ("1", "Me ha ocurrido un poco / parte del tiempo"),
    ("2", "Me ha ocurrido bastante / buena parte del tiempo"),
    ("3", "Me ha ocurrido mucho / la mayor parte del tiempo"),
]


@dataclass
class Resultado:
    nombre: str
    puntaje: int
    nivel: str
    descripcion: str
    maximo: int = 21


class Dimension(ABC):
    nombre: str
    items: list[int]

    def calcular_puntaje(self, respuestas: list[int]) -> int:
        return sum(respuestas[i - 1] for i in self.items)

    @abstractmethod
    def interpretar(self, puntaje: int) -> tuple[str, str]:
        pass

    def evaluar(self, respuestas: list[int]) -> Resultado:
        puntaje = self.calcular_puntaje(respuestas)
        nivel, descripcion = self.interpretar(puntaje)
        return Resultado(self.nombre, puntaje, nivel, descripcion)


class Depresion(Dimension):
    nombre = "Depresión"
    items = [3, 5, 10, 13, 16, 17, 21]

    def interpretar(self, s: int) -> tuple[str, str]:
        if s < 5:  return "Normal",                "Sin sintomatología depresiva significativa."
        if s <= 6: return "Leve",                  "Presencia de síntomas leves de depresión."
        if s <= 10: return "Moderada",             "Presencia de síntomas moderados de depresión."
        if s <= 13: return "Severa",               "Presencia de síntomas severos de depresión."
        return             "Extremadamente severa","Presencia de síntomas extremadamente severos de depresión."


class Ansiedad(Dimension):
    nombre = "Ansiedad"
    items = [2, 4, 7, 9, 15, 19, 20]

    def interpretar(self, s: int) -> tuple[str, str]:
        if s < 4:  return "Normal",                "Sin sintomatología ansiosa significativa."
        if s == 4: return "Leve",                  "Presencia de síntomas leves de ansiedad."
        if s <= 7: return "Moderada",              "Presencia de síntomas moderados de ansiedad."
        if s <= 9: return "Severa",                "Presencia de síntomas severos de ansiedad."
        return             "Extremadamente severa","Presencia de síntomas extremadamente severos de ansiedad."


class Estres(Dimension):
    nombre = "Estrés"
    items = [1, 6, 8, 11, 12, 14, 18]

    def interpretar(self, s: int) -> tuple[str, str]:
        if s < 8:   return "Normal",                  "Sin sintomatología de estrés significativa."
        if s <= 9:  return "Leve",                    "Presencia de síntomas leves de estrés."
        if s <= 12: return "Moderado",                "Presencia de síntomas moderados de estrés."
        if s <= 16: return "Severo",                  "Presencia de síntomas severos de estrés."
        return              "Extremadamente severo",  "Presencia de síntomas extremadamente severos de estrés."


class DASS21:
    def __init__(self):
        self._dimensiones: list[Dimension] = [Depresion(), Ansiedad(), Estres()]

    def calcular(self, respuestas: list[int]) -> list[Resultado]:
        return [d.evaluar(respuestas) for d in self._dimensiones]


def calcular_resultados(respuestas: list[int]) -> list[Resultado]:
    return DASS21().calcular(respuestas)
