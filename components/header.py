import customtkinter as ctk
from colors import COLORES


class Header(ctk.CTkFrame):
    def __init__(self, parent, title="DASS-21", subtitle="Escala de Depresión, Ansiedad y Estrés"):
        super().__init__(parent, fg_color=COLORES["superficie"],
                         corner_radius=0, border_width=1, border_color=COLORES["borde"])

        ctk.CTkLabel(self, text=title, font=ctk.CTkFont("Helvetica", 17, "bold"),
                     text_color=COLORES["texto"]).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(self, text=subtitle, font=ctk.CTkFont("Helvetica", 11),
                     text_color=COLORES["texto_sec"]).pack(side="left")
