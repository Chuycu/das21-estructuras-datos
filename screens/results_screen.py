import customtkinter as ctk
from components.result_card import ResultCard
from colors import COLORES


class ResultsScreen(ctk.CTkFrame):
    def __init__(self, parent, resultados, total: int, on_restart):
        super().__init__(parent, fg_color=COLORES["fondo"], corner_radius=0)
        self.on_restart = on_restart
        self._build(resultados, total)

    def _build(self, resultados, total: int):
        hdr = ctk.CTkFrame(self, fg_color=COLORES["superficie"],
                           corner_radius=0, border_width=1, border_color=COLORES["borde"])
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="Resultados DASS-21", font=ctk.CTkFont("Helvetica", 17, "bold"),
                     text_color=COLORES["texto"]).pack(side="left", padx=20, pady=10)

        scroll = ctk.CTkScrollableFrame(self, fg_color=COLORES["fondo"], corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=24, pady=12)

        self._tarjeta_total(scroll, total)

        for res in resultados:
            ResultCard(scroll, res).pack(fill="x")

        ctk.CTkLabel(scroll,
                     text="⚠ Esta herramienta es orientativa y no constituye un diagnóstico clínico. "
                          "Si experimenta dificultades significativas, consulte a un profesional de salud mental.",
                     font=ctk.CTkFont("Helvetica", 9),
                     fg_color=COLORES["normal_light"], text_color=COLORES["normal"],
                     wraplength=680, justify="left", corner_radius=6).pack(fill="x", pady=8)

        ctk.CTkButton(scroll, text="← Volver al inicio", command=self.on_restart,
                      font=ctk.CTkFont("Helvetica", 11),
                      fg_color=COLORES["superficie"], text_color=COLORES["texto"],
                      hover_color=COLORES["fondo"], border_width=1,
                      border_color=COLORES["borde"], corner_radius=8,
                      width=180, height=38).pack(anchor="w", pady=4)

    def _tarjeta_total(self, parent, total: int):
        card = ctk.CTkFrame(parent, fg_color=COLORES["superficie"],
                            corner_radius=10, border_width=1, border_color=COLORES["borde"])
        card.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(card, text="Puntuación total (síntomas emocionales)",
                     font=ctk.CTkFont("Helvetica", 11),
                     text_color=COLORES["texto_sec"]).pack(side="left", padx=16, pady=12)

        ctk.CTkLabel(card, text=str(total), font=ctk.CTkFont("Helvetica", 22, "bold"),
                     text_color=COLORES["texto"]).pack(side="right", padx=16)
