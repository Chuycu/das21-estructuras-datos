import customtkinter as ctk
from colors import COLORES, NIVEL_COLORES
from models import Resultado


class ResultCard(ctk.CTkFrame):
    def __init__(self, parent, resultado: Resultado):
        super().__init__(parent, fg_color=COLORES["fondo"], corner_radius=0)

        color, light, barra = NIVEL_COLORES[resultado.nombre]

        card = ctk.CTkFrame(self, fg_color=light, corner_radius=10,
                            border_width=1, border_color=color)
        card.pack(fill="x", pady=6)

        top = ctk.CTkFrame(card, fg_color=light)
        top.pack(fill="x", padx=14, pady=(12, 4))

        ctk.CTkLabel(top, text=resultado.nombre, font=ctk.CTkFont("Helvetica", 12, "bold"),
                     text_color=color).pack(side="left")

        ctk.CTkLabel(top, text=f"{resultado.puntaje}  ·  {resultado.nivel}",
                     font=ctk.CTkFont("Helvetica", 12), text_color=color).pack(side="right")

        ctk.CTkLabel(card, text=resultado.descripcion, font=ctk.CTkFont("Helvetica", 10),
                     text_color=color, anchor="w").pack(fill="x", padx=14)

        bar_frame = ctk.CTkFrame(card, fg_color=light)
        bar_frame.pack(fill="x", padx=14, pady=(8, 12))

        pct = min(1.0, resultado.puntaje / resultado.maximo)
        pb = ctk.CTkProgressBar(bar_frame, height=8, corner_radius=4,
                                fg_color=COLORES["borde"], progress_color=barra)
        pb.set(pct)
        pb.pack(fill="x")
