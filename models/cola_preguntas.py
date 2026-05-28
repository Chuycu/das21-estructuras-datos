from typing import Optional


class NodoCola:
    def __init__(self, indice: int, texto: str):
        self.indice = indice
        self.texto = texto
        self.siguiente: Optional[NodoCola] = None


class ColaPreguntas:
    
    def __init__(self, preguntas: list[str]):
        self.frente: Optional[NodoCola] = None
        self.final: Optional[NodoCola] = None
        self.tamanio = 0
        for i, texto in enumerate(preguntas):
            self.encolar(i, texto)

    def encolar(self, indice: int, texto: str):
        nodo = NodoCola(indice, texto)
        if self.final:
            self.final.siguiente = nodo
        else:
            self.frente = nodo
        self.final = nodo
        self.tamanio += 1

    def desencolar(self) -> Optional[tuple[int, str]]:
        if not self.frente:
            return None
        nodo = self.frente
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        self.tamanio -= 1
        return nodo.indice, nodo.texto

    def esta_vacia(self) -> bool:
        return self.frente is None

    def total_restante(self) -> int:
        return self.tamanio
