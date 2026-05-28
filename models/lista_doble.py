# models/lista_doble.py
from typing import Optional
from .usuario import Usuario


class Nodo:
    def __init__(self, usuario: Usuario):
        self.usuario = usuario
        self.siguiente: Optional[Nodo] = None
        self.anterior: Optional[Nodo] = None


class ListaDobleUsuarios:
    def __init__(self):
        self.cabeza: Optional[Nodo] = None
        self.cola: Optional[Nodo] = None
        self.contador = 0

    def agregar(self, usuario: Usuario):
        nuevo_nodo = Nodo(usuario)
        self.contador += 1
        usuario.id = self.contador

        if not self.cabeza:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo

    def listar_todos(self) -> list[Usuario]:
        """Devuelve una lista con todos los usuarios"""
        usuarios = []
        actual = self.cabeza
        while actual is not None:          # ← Corrección importante
            usuarios.append(actual.usuario)
            actual = actual.siguiente
        return usuarios

    def buscar_por_id(self, id_usuario: int) -> Optional[Usuario]:
        actual = self.cabeza
        while actual is not None:
            if actual.usuario.id == id_usuario:
                return actual.usuario
            actual = actual.siguiente
        return None

    def obtener_siguiente(self, id_actual: int) -> Optional[Usuario]:
        actual = self.cabeza
        while actual is not None:
            if actual.usuario.id == id_actual:
                if actual.siguiente:
                    return actual.siguiente.usuario
                return None
            actual = actual.siguiente
        return None

    def obtener_anterior(self, id_actual: int) -> Optional[Usuario]:
        actual = self.cabeza
        while actual is not None:
            if actual.usuario.id == id_actual:
                if actual.anterior:
                    return actual.anterior.usuario
                return None
            actual = actual.siguiente
        return None

    def eliminar(self, id_usuario: int) -> bool:
        actual = self.cabeza
        while actual is not None:
            if actual.usuario.id == id_usuario:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente

                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior
                return True
            actual = actual.siguiente
        return False