import tkinter as tk
import customtkinter as ctk
from components.header import Header
from colors import COLORES
from models import PREGUNTAS, OPCIONES, ColaPreguntas


class QuestionnaireScreen(ctk.CTkFrame):
    def __init__(self, parent, on_calculate, on_save_progress=None,
                 on_back=None, respuestas_iniciales=None):
        super().__init__(parent, fg_color=COLORES["fondo"], corner_radius=0)
        self.on_calculate = on_calculate
        self.on_save_progress = on_save_progress
        self.on_back = on_back

        iniciales = respuestas_iniciales or [-1] * 21
        self.respuestas: list[int] = iniciales[:]

        pendientes = [i for i, r in enumerate(self.respuestas) if r < 0]
        respondidas = [i for i, r in enumerate(self.respuestas) if r >= 0]
        orden = pendientes + respondidas
        self._cola = ColaPreguntas([PREGUNTAS[i] for i in orden])
        self._orden_indices = orden  
        self._pos = 0 
        self._var = tk.IntVar(value=-1)

        self._build_ui()
        self._mostrar_pregunta_actual()

    def _build_ui(self):
        Header(self).pack(fill="x")

        # Barra de progreso
        prog_frame = ctk.CTkFrame(self, fg_color=COLORES["fondo"], corner_radius=0)
        prog_frame.pack(fill="x", padx=24, pady=(14, 0))

        self.prog_lbl = ctk.CTkLabel(prog_frame, text="",
                                     font=ctk.CTkFont("Helvetica", 10),
                                     text_color=COLORES["texto_sec"])
        self.prog_lbl.pack(anchor="e")

        self.prog_bar = ctk.CTkProgressBar(prog_frame, height=8, corner_radius=4,
                                           fg_color=COLORES["borde"],
                                           progress_color=COLORES["acento"])
        self.prog_bar.set(0)
        self.prog_bar.pack(fill="x", pady=4)

        # Área central de la pregunta
        self.card = ctk.CTkFrame(self, fg_color=COLORES["superficie"],
                                 corner_radius=12, border_width=1,
                                 border_color=COLORES["borde"])
        self.card.pack(fill="both", expand=True, padx=24, pady=16)

        top = ctk.CTkFrame(self.card, fg_color=COLORES["superficie"], corner_radius=0)
        top.pack(fill="x", padx=20, pady=(20, 12))

        self.lbl_num = ctk.CTkLabel(top, text="",
                                    font=ctk.CTkFont("Helvetica", 11),
                                    text_color=COLORES["texto_sec"],
                                    anchor="w", width=60)
        self.lbl_num.pack(side="left", anchor="nw", pady=(2, 0))

        self.lbl_texto = ctk.CTkLabel(top, text="",
                                      font=ctk.CTkFont("Helvetica", 13),
                                      text_color=COLORES["texto"],
                                      wraplength=560, justify="left", anchor="w")
        self.lbl_texto.pack(side="left", fill="x", expand=True)

        ctk.CTkFrame(self.card, fg_color=COLORES["borde"],
                     height=1, corner_radius=0).pack(fill="x", padx=20)

        ops_frame = ctk.CTkFrame(self.card, fg_color=COLORES["superficie"], corner_radius=0)
        ops_frame.pack(fill="x", padx=20, pady=16)

        self._radio_btns = []
        for val, etiqueta in OPCIONES:
            rb = ctk.CTkRadioButton(
                ops_frame,
                text=f"  {val}  –  {etiqueta}",
                variable=self._var,
                value=int(val),
                font=ctk.CTkFont("Helvetica", 11),
                text_color=COLORES["texto"],
                fg_color=COLORES["acento"],
                hover_color=COLORES["acento_light"],
                command=self._on_seleccion,
            )
            rb.pack(anchor="w", pady=5)
            self._radio_btns.append(rb)

        nav = ctk.CTkFrame(self, fg_color=COLORES["fondo"], corner_radius=0)
        nav.pack(fill="x", padx=24, pady=(0, 16))

        self.btn_anterior = ctk.CTkButton(nav, text="← Anterior",
                                          command=self._anterior,
                                          font=ctk.CTkFont("Helvetica", 10),
                                          fg_color=COLORES["superficie"],
                                          text_color=COLORES["texto"],
                                          hover_color=COLORES["fondo"],
                                          border_width=1, border_color=COLORES["borde"],
                                          corner_radius=8, width=110, height=36)
        self.btn_anterior.pack(side="left")

        if self.on_back:
            ctk.CTkButton(nav, text="Salir",
                          command=self._guardar_y_salir,
                          font=ctk.CTkFont("Helvetica", 10),
                          fg_color=COLORES["superficie"], text_color=COLORES["texto_sec"],
                          hover_color=COLORES["fondo"], border_width=1,
                          border_color=COLORES["borde"], corner_radius=8,
                          width=80, height=36).pack(side="left", padx=(8, 0))

        self.btn_siguiente = ctk.CTkButton(nav, text="Siguiente →",
                                           command=self._siguiente,
                                           font=ctk.CTkFont("Helvetica", 11, "bold"),
                                           fg_color=COLORES["acento"], hover_color="#0C447C",
                                           text_color="white", corner_radius=8,
                                           width=140, height=36)
        self.btn_siguiente.pack(side="right")

        self.btn_calcular = ctk.CTkButton(nav, text="Ver resultados →",
                                          command=self._calcular,
                                          font=ctk.CTkFont("Helvetica", 11, "bold"),
                                          fg_color=COLORES["acento"], hover_color="#0C447C",
                                          text_color="white", corner_radius=8,
                                          width=160, height=36)

    def _mostrar_pregunta_actual(self):
        idx_real = self._orden_indices[self._pos]
        num_display = idx_real + 1
        total = len(self._orden_indices)

        self.lbl_num.configure(text=f"Pregunta\n{num_display} / 21")
        self.lbl_texto.configure(text=PREGUNTAS[idx_real])

        respondidas = sum(1 for r in self.respuestas if r >= 0)
        self.prog_bar.set(respondidas / 21)
        self.prog_lbl.configure(text=f"{respondidas} / 21 respondidas")

        val_actual = self.respuestas[idx_real]
        self._var.set(val_actual)

        # Highlight card si ya respondida
        self.card.configure(border_color=COLORES["acento"] if val_actual >= 0 else COLORES["borde"])

        # Botón anterior
        self.btn_anterior.configure(state="normal" if self._pos > 0 else "disabled")

        # Mostrar siguiente o calcular en última pregunta
        es_ultima = (self._pos == total - 1)
        todas_respondidas = all(r >= 0 for r in self.respuestas)

        if es_ultima and todas_respondidas:
            self.btn_siguiente.pack_forget()
            self.btn_calcular.pack(side="right")
        else:
            self.btn_calcular.pack_forget()
            self.btn_siguiente.pack(side="right")
            self.btn_siguiente.configure(
                state="normal" if self.respuestas[idx_real] >= 0 else "disabled"
            )

    def _on_seleccion(self):
        idx_real = self._orden_indices[self._pos]
        self.respuestas[idx_real] = self._var.get()
        self.card.configure(border_color=COLORES["acento"])

        if self.on_save_progress:
            self.on_save_progress(self.respuestas[:])

        self.after(300, self._siguiente)

    def _siguiente(self):
        idx_real = self._orden_indices[self._pos]
        if self.respuestas[idx_real] < 0:
            return
        if self._pos < len(self._orden_indices) - 1:
            self._pos += 1
        self._mostrar_pregunta_actual()

    def _anterior(self):
        if self._pos > 0:
            self._pos -= 1
            self._mostrar_pregunta_actual()

    def _guardar_y_salir(self):
        if self.on_save_progress:
            self.on_save_progress(self.respuestas[:])
        if self.on_back:
            self.on_back()

    def _calcular(self):
        self.on_calculate(self.respuestas[:])
