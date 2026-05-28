from tkinter import messagebox, simpledialog
import customtkinter as ctk
from models import Usuario, ListaDobleUsuarios
from components.header import Header
from colors import COLORES


class UserManagementScreen(ctk.CTkFrame):
    def __init__(self, parent, lista_usuarios: ListaDobleUsuarios,
                 on_user_selected, on_new_test,
                 on_continue_test=None, on_view_result=None):
        super().__init__(parent, fg_color=COLORES["fondo"], corner_radius=0)
        self.lista = lista_usuarios
        self.on_user_selected = on_user_selected
        self.on_new_test = on_new_test
        self.on_continue_test = on_continue_test or on_new_test
        self.on_view_result = on_view_result
        self.usuario_actual: Usuario = None
        primeros = lista_usuarios.listar_todos()
        if primeros:
            self.usuario_actual = primeros[0]
        self._build_ui()

    def _build_ui(self):
        Header(self, title="DASS-21", subtitle="Gestión de Usuarios").pack(fill="x", pady=(0, 8))

        top_bar = ctk.CTkFrame(self, fg_color=COLORES["fondo"], corner_radius=0)
        top_bar.pack(fill="x", padx=24, pady=(0, 8))

        ctk.CTkButton(top_bar, text="+ Nuevo Usuario",
                      command=self._crear_nuevo_usuario,
                      font=ctk.CTkFont("Helvetica", 11, "bold"),
                      fg_color=COLORES["acento"], hover_color="#0C447C",
                      text_color="white", corner_radius=8,
                      width=160, height=38).pack(side="left")

        nav_frame = ctk.CTkFrame(self, fg_color=COLORES["fondo"], corner_radius=0)
        nav_frame.pack(fill="x", padx=24, pady=(0, 12))

        ctk.CTkButton(nav_frame, text="← Anterior",
                      command=self._ir_anterior,
                      font=ctk.CTkFont("Helvetica", 10),
                      fg_color=COLORES["superficie"], text_color=COLORES["texto"],
                      hover_color=COLORES["fondo"], border_width=1,
                      border_color=COLORES["borde"], corner_radius=8,
                      width=110, height=34).pack(side="left")

        self.lbl_nav = ctk.CTkLabel(nav_frame, text="Ningún usuario",
                                    font=ctk.CTkFont("Helvetica", 11, "bold"),
                                    text_color=COLORES["texto"])
        self.lbl_nav.pack(side="left", expand=True)

        ctk.CTkButton(nav_frame, text="Siguiente →",
                      command=self._ir_siguiente,
                      font=ctk.CTkFont("Helvetica", 10),
                      fg_color=COLORES["superficie"], text_color=COLORES["texto"],
                      hover_color=COLORES["fondo"], border_width=1,
                      border_color=COLORES["borde"], corner_radius=8,
                      width=110, height=34).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=COLORES["fondo"], corner_radius=0)
        self.scroll.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        self._refresh()

    def _refresh(self):
        self._update_nav_label()
        self._render_content()

    def _update_nav_label(self):
        usuarios = self.lista.listar_todos()
        total = len(usuarios)
        if not self.usuario_actual or total == 0:
            self.lbl_nav.configure(text="Ningún usuario")
            return
        try:
            pos = next(i + 1 for i, u in enumerate(usuarios) if u.id == self.usuario_actual.id)
        except StopIteration:
            pos = "?"
        self.lbl_nav.configure(text=f"{self.usuario_actual.nombre}  ({pos}/{total})")

    def _render_content(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        if not self.usuario_actual:
            usuarios = self.lista.listar_todos()
            msg = ("No hay usuarios registrados.\nCrea uno con el botón superior."
                   if not usuarios else "Usa ← → para navegar entre usuarios.")
            ctk.CTkLabel(self.scroll, text=msg, font=ctk.CTkFont("Helvetica", 12),
                         text_color=COLORES["texto_sec"], justify="center").pack(pady=60)
            return

        u = self.usuario_actual

        ctk.CTkLabel(self.scroll, text=u.nombre,
                     font=ctk.CTkFont("Helvetica", 20, "bold"),
                     text_color=COLORES["texto"], anchor="w").pack(fill="x", pady=(8, 2))

        info_parts = []
        if u.edad:
            info_parts.append(f"{u.edad} años")
        if u.genero:
            info_parts.append(u.genero)
        info_parts.append(f"Registrado: {u.fecha_registro[:10]}")
        ctk.CTkLabel(self.scroll, text="  ·  ".join(info_parts),
                     font=ctk.CTkFont("Helvetica", 10),
                     text_color=COLORES["texto_sec"], anchor="w").pack(fill="x", pady=(0, 10))

        ctk.CTkFrame(self.scroll, fg_color=COLORES["borde"], height=1,
                     corner_radius=0).pack(fill="x", pady=(0, 16))

        if u.tiene_test_en_progreso():
            prog_card = ctk.CTkFrame(self.scroll, fg_color=COLORES["anx_light"],
                                     corner_radius=10, border_width=1,
                                     border_color=COLORES["anx"])
            prog_card.pack(fill="x", pady=(0, 12))

            ctk.CTkLabel(prog_card,
                         text=f"Test en progreso — {u.progreso_test()}/21 preguntas respondidas",
                         font=ctk.CTkFont("Helvetica", 11, "bold"),
                         text_color=COLORES["anx"]).pack(padx=14, pady=(10, 6), anchor="w")

            btn_row = ctk.CTkFrame(prog_card, fg_color=COLORES["anx_light"], corner_radius=0)
            btn_row.pack(fill="x", padx=14, pady=(0, 10))

            ctk.CTkButton(btn_row, text="Descartar",
                          command=lambda: self._descartar_test(u),
                          font=ctk.CTkFont("Helvetica", 9),
                          fg_color=COLORES["anx_light"], text_color=COLORES["str"],
                          hover_color=COLORES["str_light"], border_width=1,
                          border_color=COLORES["str"], corner_radius=8,
                          width=100, height=34).pack(side="left")

            ctk.CTkButton(btn_row, text="Continuar test →",
                          command=lambda: self.on_continue_test(u),
                          font=ctk.CTkFont("Helvetica", 10, "bold"),
                          fg_color=COLORES["acento"], hover_color="#0C447C",
                          text_color="white", corner_radius=8,
                          width=150, height=34).pack(side="left", padx=(8, 0))
        else:
            ctk.CTkButton(self.scroll, text="+ Iniciar nuevo test",
                          command=lambda: self.on_new_test(u),
                          font=ctk.CTkFont("Helvetica", 11, "bold"),
                          fg_color=COLORES["acento"], hover_color="#0C447C",
                          text_color="white", corner_radius=8,
                          width=180, height=40).pack(anchor="w", pady=(0, 16))

        tests = u.tests_realizados
        n = len(tests)

        ctk.CTkLabel(self.scroll,
                     text=f"Historial de tests ({n} {'completado' if n == 1 else 'completados'})",
                     font=ctk.CTkFont("Helvetica", 12, "bold"),
                     text_color=COLORES["texto"], anchor="w").pack(fill="x", pady=(0, 8))

        if not tests:
            ctk.CTkLabel(self.scroll, text="Sin tests completados aún.",
                         font=ctk.CTkFont("Helvetica", 11),
                         text_color=COLORES["texto_sec"], anchor="w").pack(anchor="w", pady=(0, 20))
            return

        for i, test in enumerate(reversed(tests)):
            self._build_test_card(test, n - i, u)

    def _build_test_card(self, test: dict, numero: int, usuario: Usuario):
        card = ctk.CTkFrame(self.scroll, fg_color=COLORES["superficie"],
                            corner_radius=10, border_width=1, border_color=COLORES["borde"])
        card.pack(fill="x", pady=(0, 10))

        header_row = ctk.CTkFrame(card, fg_color=COLORES["superficie"], corner_radius=0)
        header_row.pack(fill="x", padx=14, pady=(10, 4))

        ctk.CTkLabel(header_row, text=f"Test #{numero}",
                     font=ctk.CTkFont("Helvetica", 11, "bold"),
                     text_color=COLORES["texto"]).pack(side="left")

        ctk.CTkLabel(header_row, text=test.get("fecha", ""),
                     font=ctk.CTkFont("Helvetica", 10),
                     text_color=COLORES["texto_sec"]).pack(side="right")

        ctk.CTkLabel(card, text=f"Puntaje total: {test.get('puntaje_total', '—')}",
                     font=ctk.CTkFont("Helvetica", 10),
                     text_color=COLORES["texto_sec"], anchor="w").pack(fill="x", padx=14, pady=(0, 6))

        scores_row = ctk.CTkFrame(card, fg_color=COLORES["superficie"], corner_radius=0)
        scores_row.pack(fill="x", padx=14, pady=(0, 10))

        dims = [
            ("Depresión", test.get("depresion", 0), COLORES["dep"], COLORES["dep_light"]),
            ("Ansiedad",  test.get("ansiedad",  0), COLORES["anx"], COLORES["anx_light"]),
            ("Estrés",    test.get("estres",    0), COLORES["str"], COLORES["str_light"]),
        ]
        for label, score, color, bg_light in dims:
            chip = ctk.CTkFrame(scores_row, fg_color=bg_light,
                                corner_radius=6, border_width=1, border_color=color)
            chip.pack(side="left", padx=(0, 8))
            ctk.CTkLabel(chip, text=f"{label}: {score}",
                         font=ctk.CTkFont("Helvetica", 9, "bold"),
                         text_color=color).pack(padx=10, pady=4)

        if numero == len(usuario.tests_realizados):
            ctk.CTkButton(card, text="Ver resultado completo",
                          command=lambda: self._ver_resultado(usuario),
                          font=ctk.CTkFont("Helvetica", 9),
                          fg_color=COLORES["superficie"], text_color=COLORES["acento"],
                          hover_color=COLORES["acento_light"], border_width=1,
                          border_color=COLORES["acento"], corner_radius=8,
                          width=160, height=30).pack(anchor="e", padx=14, pady=(0, 10))

    def _ver_resultado(self, usuario: Usuario):
        if self.on_view_result:
            self.on_view_result(usuario)

    def _descartar_test(self, usuario: Usuario):
        if messagebox.askyesno("Descartar test",
                               f"¿Descartar el test en progreso de {usuario.nombre}?"):
            usuario.finalizar_test()
            self._refresh()

    def _crear_nuevo_usuario(self):
        nombre = simpledialog.askstring("Nuevo Usuario", "Nombre completo:", parent=self)
        if not nombre or nombre.strip() == "":
            return
        edad = simpledialog.askinteger("Nuevo Usuario", "Edad (opcional, cancelar para omitir):",
                                       parent=self, minvalue=1, maxvalue=120)
        genero = simpledialog.askstring("Nuevo Usuario",
                                        "Género (opcional, cancelar para omitir):",
                                        parent=self)
        nuevo = Usuario(
            nombre=nombre.strip(),
            edad=edad,
            genero=genero.strip() if genero and genero.strip() else None,
        )
        self.lista.agregar(nuevo)
        self._seleccionar_usuario(nuevo)

    def _seleccionar_usuario(self, usuario: Usuario):
        self.usuario_actual = usuario
        self.on_user_selected(usuario)
        self._refresh()

    def _ir_anterior(self):
        usuarios = self.lista.listar_todos()
        if not usuarios:
            return
        if not self.usuario_actual:
            self._seleccionar_usuario(usuarios[-1])
            return
        anterior = self.lista.obtener_anterior(self.usuario_actual.id)
        if anterior:
            self._seleccionar_usuario(anterior)
        else:
            messagebox.showinfo("Inicio", "Ya estás en el primer usuario.")

    def _ir_siguiente(self):
        usuarios = self.lista.listar_todos()
        if not usuarios:
            return
        if not self.usuario_actual:
            self._seleccionar_usuario(usuarios[0])
            return
        siguiente = self.lista.obtener_siguiente(self.usuario_actual.id)
        if siguiente:
            self._seleccionar_usuario(siguiente)
        else:
            messagebox.showinfo("Fin", "Ya estás en el último usuario.")
