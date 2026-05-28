import customtkinter as ctk
from tkinter import messagebox

from models import ListaDobleUsuarios, Usuario, calcular_resultados
from screens.questionnaire_screen import QuestionnaireScreen
from screens.results_screen import ResultsScreen
from screens.user_management_screen import UserManagementScreen
from colors import COLORES

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class DASS21App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DASS-21 · Konrad Lorenz")
        self.geometry("780x700")
        self.minsize(700, 550)
        self.configure(fg_color=COLORES["fondo"])
        self.resizable(True, True)

        self.usuarios = ListaDobleUsuarios()
        self.usuario_actual: Usuario = None
        self.current_screen = None

        self._crear_usuario_prueba()
        self.show_user_management()

    def _crear_usuario_prueba(self):
        if not self.usuarios.listar_todos():
            self.usuarios.agregar(Usuario(nombre="Carlos López", edad=28, genero="Masculino"))
            self.usuarios.agregar(Usuario(nombre="María González", edad=34, genero="Femenino"))
            self.usuarios.agregar(Usuario(nombre="Juan Pérez", edad=22))

    def show_user_management(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = UserManagementScreen(
            self,
            self.usuarios,
            on_user_selected=self.on_user_selected,
            on_new_test=self.start_new_test,
            on_continue_test=self.continue_test,
            on_view_result=self.view_last_result,
        )
        self.current_screen.pack(fill="both", expand=True)

    def on_user_selected(self, usuario: Usuario):
        self.usuario_actual = usuario

    def start_new_test(self, usuario: Usuario):
        self.usuario_actual = usuario
        usuario.iniciar_test()
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = QuestionnaireScreen(
            self,
            on_calculate=self.show_results,
            on_save_progress=usuario.guardar_progreso,
            on_back=self.show_user_management,
            respuestas_iniciales=usuario.test_en_progreso,
        )
        self.current_screen.pack(fill="both", expand=True)

    def continue_test(self, usuario: Usuario):
        self.usuario_actual = usuario
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = QuestionnaireScreen(
            self,
            on_calculate=self.show_results,
            on_save_progress=usuario.guardar_progreso,
            on_back=self.show_user_management,
            respuestas_iniciales=usuario.test_en_progreso,
        )
        self.current_screen.pack(fill="both", expand=True)

    def view_last_result(self, usuario: Usuario):
        if not usuario.tests_realizados:
            return
        last = usuario.tests_realizados[-1]
        resultados = calcular_resultados(last["respuestas"])
        total = last["puntaje_total"]
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = ResultsScreen(
            self, resultados, total, on_restart=self.show_user_management
        )
        self.current_screen.pack(fill="both", expand=True)

    def show_results(self, respuestas: list[int]):
        if any(r < 0 for r in respuestas):
            messagebox.showwarning("Faltan respuestas",
                                   "Por favor responda todas las preguntas antes de continuar.")
            return

        resultados = calcular_resultados(respuestas)
        total = sum(r.puntaje for r in resultados)

        if self.usuario_actual:
            self.usuario_actual.agregar_test(respuestas, resultados, total)
            self.usuario_actual.finalizar_test()

        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = ResultsScreen(self, resultados, total, on_restart=self.show_user_management)
        self.current_screen.pack(fill="both", expand=True)
