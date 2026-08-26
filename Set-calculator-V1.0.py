import customtkinter as ctk
import tkinter as tk
import json
import os
import random
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# Configuración inicial de la paleta y tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class SetCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Teoría de Conjuntos")
        self.geometry("1100x700")
        self.configure(fg_color="#FFFFFF")

        # Variables de estado
        self.users_file = "usuarios.json"
        self.current_user = None
        self.users_data = self.load_users()
        
        self.U = set()
        self.A = set()
        self.B = set()
        self.C = set()
        self.D = set()
        
        self.expression = ""
        
        self.setup_ui()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users_data, f)

    def setup_ui(self):
        # Contenedor principal
        self.main_container = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.main_container.pack(fill="both", expand=True)

        # Botón para abrir el Login (Izquierda)
        self.btn_toggle_login = ctk.CTkButton(
            self.main_container, text="☰ Login", width=80, 
            fg_color="#00509E", hover_color="#003f7a", command=self.toggle_sidebar
        )
        self.btn_toggle_login.place(x=10, y=10)

        # Panel Lateral de Login (Oculto por defecto) - Ancho ampliado a 400
        self.sidebar = ctk.CTkFrame(self, width=400, corner_radius=0, fg_color="#F0F8FF")
        
        self.lbl_user_status = ctk.CTkLabel(self.sidebar, text="No has iniciado sesión", font=("Arial", 16, "bold"), text_color="#00509E")
        self.lbl_user_status.pack(pady=20)

        self.sidebar_content = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_content.pack(fill="both", expand=True)

        self.view_register = ctk.CTkFrame(self.sidebar_content, fg_color="transparent")
        self.view_login = ctk.CTkFrame(self.sidebar_content, fg_color="transparent")
        self.view_delete = ctk.CTkFrame(self.sidebar_content, fg_color="transparent")

        # --- Register View ---
        ctk.CTkLabel(self.view_register, text="Registrar Nuevo Usuario", font=("Arial", 14, "bold"), text_color="#00509E").pack(pady=10)
        self.reg_username = ctk.CTkEntry(self.view_register, placeholder_text="Nombre de Usuario", fg_color="#FFFFFF", text_color="#000000")
        self.reg_username.pack(pady=10, padx=20, fill="x")
        self.reg_pin = ctk.CTkEntry(self.view_register, placeholder_text="PIN (4 dígitos)", show="*", fg_color="#FFFFFF", text_color="#000000")
        self.reg_pin.pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.view_register, text="Agregar Usuario", fg_color="#3A86FF", hover_color="#2a62bc", command=self.do_register).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.view_register, text="Ir a Acceder a Usuario", fg_color="#6c757d", command=lambda: self.show_view(self.view_login)).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.view_register, text="Ir a Borrar Usuario", fg_color="#FF4D4D", command=lambda: self.show_view(self.view_delete)).pack(pady=10, padx=20, fill="x")

        # --- Login View ---
        ctk.CTkLabel(self.view_login, text="Acceder a Usuario", font=("Arial", 14, "bold"), text_color="#00509E").pack(pady=10)
        self.login_user_combo = ctk.CTkComboBox(self.view_login, values=["Sin usuarios"])
        self.login_user_combo.pack(pady=10, padx=20, fill="x")
        self.login_pin = ctk.CTkEntry(self.view_login, placeholder_text="PIN (4 dígitos)", show="*", fg_color="#FFFFFF", text_color="#000000")
        self.login_pin.pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.view_login, text="Acceder", fg_color="#3A86FF", hover_color="#2a62bc", command=self.do_login).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.view_login, text="Ir a Registrar Usuario", fg_color="#6c757d", command=lambda: self.show_view(self.view_register)).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.view_login, text="Ir a Borrar Usuario", fg_color="#FF4D4D", command=lambda: self.show_view(self.view_delete)).pack(pady=10, padx=20, fill="x")

        # --- Delete View ---
        ctk.CTkLabel(self.view_delete, text="Borrar Usuario", font=("Arial", 14, "bold"), text_color="#FF4D4D").pack(pady=10)
        self.delete_user_combo = ctk.CTkComboBox(self.view_delete, values=["Sin usuarios"])
        self.delete_user_combo.pack(pady=10, padx=20, fill="x")
        self.delete_pin = ctk.CTkEntry(self.view_delete, placeholder_text="PIN del usuario", show="*", fg_color="#FFFFFF", text_color="#000000")
        self.delete_pin.pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.view_delete, text="Borrar Usuario", fg_color="#FF4D4D", hover_color="#cc0000", command=self.do_delete).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.view_delete, text="Ir a Registrar Usuario", fg_color="#6c757d", command=lambda: self.show_view(self.view_register)).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(self.view_delete, text="Ir a Acceder a Usuario", fg_color="#6c757d", command=lambda: self.show_view(self.view_login)).pack(pady=10, padx=20, fill="x")

        self.btn_close_sidebar = ctk.CTkButton(self.sidebar, text="Cerrar", fg_color="#00509E", hover_color="#003f7a", command=self.toggle_sidebar)
        self.btn_close_sidebar.pack(side="bottom", pady=20, padx=20, fill="x")

        # Mostrar por defecto la vista de registro
        self.show_view(self.view_register)

        # Área Central de Trabajo
        self.work_area = ctk.CTkFrame(self.main_container, fg_color="#FFFFFF")
        self.work_area.pack(side="right", fill="both", expand=True, padx=(100, 20), pady=20)

        # --- SECCIÓN: Generación de Conjuntos ---
        self.frame_gen = ctk.CTkFrame(self.work_area, fg_color="#E6F2FF")
        self.frame_gen.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(self.frame_gen, text="Generación de Conjuntos", font=("Arial", 16, "bold"), text_color="#00509E").pack(pady=5)
        
        self.type_var = ctk.StringVar(value="Mixto")
        self.opt_numbers = ctk.CTkRadioButton(self.frame_gen, text="Números", variable=self.type_var, value="Números", text_color="#000000")
        self.opt_words = ctk.CTkRadioButton(self.frame_gen, text="Palabras", variable=self.type_var, value="Palabras", text_color="#000000")
        self.opt_mixed = ctk.CTkRadioButton(self.frame_gen, text="Mixto", variable=self.type_var, value="Mixto", text_color="#000000")
        
        self.opt_numbers.pack(side="left", padx=20, pady=10)
        self.opt_words.pack(side="left", padx=20, pady=10)
        self.opt_mixed.pack(side="left", padx=20, pady=10)

        self.btn_generate = ctk.CTkButton(self.frame_gen, text="Generar Todo", fg_color="#00509E", hover_color="#003f7a", command=self.generate_sets)
        self.btn_generate.pack(side="right", padx=20, pady=10)

        # Entradas de Conjuntos
        self.frame_sets_input = ctk.CTkFrame(self.work_area, fg_color="#FFFFFF")
        self.frame_sets_input.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(self.frame_sets_input, text="Información: La cantidad mínima de elementos es 0 (vacío) y la máxima es el límite de procesamiento.", font=("Arial", 11, "italic"), text_color="#666666").pack(anchor="w", padx=5, pady=2)

        self.entries = {}
        for name in ["U", "A", "B", "C", "D"]:
            row = ctk.CTkFrame(self.frame_sets_input, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{name} =", font=("Consolas", 14, "bold"), text_color="#00509E", width=30).pack(side="left")
            entry = ctk.CTkEntry(row, placeholder_text=f"Elementos separados por comas", fg_color="#F0F8FF", text_color="#000000")
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.entries[name] = entry

        # --- SECCIÓN: Calculadora ---
        self.frame_calc = ctk.CTkFrame(self.work_area, fg_color="#E6F2FF")
        self.frame_calc.pack(fill="x", pady=10, padx=10)

        self.lbl_expr = ctk.CTkLabel(self.frame_calc, text="Expresión: ", font=("Arial", 18, "bold"), text_color="#00509E")
        self.lbl_expr.pack(pady=10)

        # Botones de Operandos y Operadores
        grid_frame = ctk.CTkFrame(self.frame_calc, fg_color="transparent")
        grid_frame.pack(pady=5)

        buttons = [
            'A', 'B', 'C', 'D', 'U',
            '∪', '∩', '-', 'Δ', '^c',
            '(', ')'
        ]
        
        row, col = 0, 0
        for btn in buttons:
            action = lambda x=btn: self.add_to_expression(x)
            ctk.CTkButton(grid_frame, text=btn, width=50, fg_color="#3A86FF", hover_color="#2a62bc", command=action).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 5:
                col = 0
                row += 1

        action_frame = ctk.CTkFrame(self.frame_calc, fg_color="transparent")
        action_frame.pack(pady=10)

        ctk.CTkButton(action_frame, text="Borrar", fg_color="#FF4D4D", hover_color="#cc0000", command=self.clear_expression).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Validar y Calcular", fg_color="#00509E", hover_color="#003f7a", command=self.calculate).pack(side="left", padx=10)

        # --- SECCIÓN: Resultados y Diagrama ---
        self.frame_results = ctk.CTkFrame(self.work_area, fg_color="#FFFFFF")
        self.frame_results.pack(fill="both", expand=True, pady=10, padx=10)

        self.txt_validation = ctk.CTkTextbox(self.frame_results, height=80, fg_color="#F0F8FF", text_color="#000000")
        self.txt_validation.pack(fill="x", pady=5)
        self.txt_validation.insert("0.0", "Las validaciones aparecerán aquí al calcular...")
        self.txt_validation.configure(state="disabled")

        self.lbl_result = ctk.CTkLabel(self.frame_results, text="Resultado: ", font=("Arial", 14, "bold"), text_color="#000000", wraplength=800)
        self.lbl_result.pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.fig.patch.set_facecolor('#FFFFFF')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_results)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- FUNCIONES DE UI ---
    def toggle_sidebar(self):
        if self.sidebar.winfo_ismapped():
            self.sidebar.place_forget()
        else:
            self.update_user_combos()
            self.sidebar.place(x=0, y=0, relheight=1)
            self.sidebar.lift()

    def update_user_combos(self):
        users = list(self.users_data.keys())
        if not users:
            users = ["Sin usuarios"]
        self.login_user_combo.configure(values=users)
        self.delete_user_combo.configure(values=users)
        if self.users_data:
            self.login_user_combo.set(users[0])
            self.delete_user_combo.set(users[0])
        else:
            self.login_user_combo.set("Sin usuarios")
            self.delete_user_combo.set("Sin usuarios")

    def show_view(self, view):
        for v in (self.view_register, self.view_login, self.view_delete):
            v.pack_forget()
        view.pack(fill="both", expand=True)



    # --- FUNCIONES DE USUARIO ---
    def do_register(self):
        username = self.reg_username.get().strip()
        pin = self.reg_pin.get().strip()

        if not username or not pin:
            messagebox.showerror("Error", "Debes ingresar usuario y PIN.")
            return

        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "El PIN debe ser estrictamente de 4 dígitos numéricos. Por favor, inténtalo nuevamente.")
            return

        if username in self.users_data:
            messagebox.showerror("Error", "El usuario ya existe.")
            return

        self.users_data[username] = pin
        self.save_users()
        self.current_user = username
        self.lbl_user_status.configure(text=f"Sesión: {username}", text_color="#00509E")
        messagebox.showinfo("Éxito", f"Usuario {username} creado y logueado.")
        self.update_user_combos()
        self.toggle_sidebar()
        
        # Limpiar campos
        self.reg_username.delete(0, 'end')
        self.reg_pin.delete(0, 'end')

    def do_login(self):
        username = self.login_user_combo.get()
        pin = self.login_pin.get().strip()

        if username == "Sin usuarios" or username not in self.users_data:
            messagebox.showerror("Error", "Selecciona un usuario válido.")
            return

        if not pin:
            messagebox.showerror("Error", "Debes ingresar el PIN.")
            return

        if self.users_data[username] == pin:
            self.current_user = username
            self.lbl_user_status.configure(text=f"Sesión: {username}", text_color="#00509E")
            messagebox.showinfo("Éxito", f"Has iniciado sesión como {username}")
            self.toggle_sidebar()
            
            # Limpiar campos
            self.login_pin.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Contraseña incorrecta. Por favor, inténtalo de nuevo.")

    def do_delete(self):
        username = self.delete_user_combo.get()
        pin = self.delete_pin.get().strip()

        if username == "Sin usuarios" or username not in self.users_data:
            messagebox.showerror("Error", "Selecciona un usuario válido.")
            return

        if not pin:
            messagebox.showerror("Error", "Debes ingresar el PIN.")
            return

        if self.users_data[username] == pin:
            del self.users_data[username]
            self.save_users()
            messagebox.showinfo("Éxito", f"Usuario {username} eliminado correctamente.")
            self.update_user_combos()
            if self.current_user == username:
                self.current_user = None
                self.lbl_user_status.configure(text="No has iniciado sesión")
            
            # Limpiar campos
            self.delete_pin.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Contraseña incorrecta. Por favor, inténtalo de nuevo.")

    # --- FUNCIONES LÓGICAS DE CONJUNTOS ---
    def generate_sets(self):
        words_pool = ["Árbol", "Avión", "Lápiz", "Ratón", "Cielo", "Música", "CAFÉ", "PERRO", "Gato", "Luz"]
        
        def get_random_elements():
            tipo = self.type_var.get()
            elements = set()
            count = random.randint(10, 20)
            for _ in range(count):
                if tipo == "Números":
                    elements.add(str(random.randint(1, 30)))
                elif tipo == "Palabras":
                    elements.add(random.choice(words_pool))
                else:
                    elements.add(str(random.randint(1, 30)) if random.choice([True, False]) else random.choice(words_pool))
            return elements

        self.U = get_random_elements()
        u_list = list(self.U)
        
        # Generar subconjuntos asegurando que pertenecen a U
        self.A = set(random.sample(u_list, random.randint(0, len(u_list))))
        self.B = set(random.sample(u_list, random.randint(0, len(u_list))))
        self.C = set(random.sample(u_list, random.randint(0, len(u_list))))
        self.D = set(random.sample(u_list, random.randint(0, len(u_list))))

        for name, subset in [("U", self.U), ("A", self.A), ("B", self.B), ("C", self.C), ("D", self.D)]:
            self.entries[name].delete(0, 'end')
            self.entries[name].insert(0, ", ".join(sorted(list(subset))))
        self.clear_expression()
        self.ax.clear()
        self.canvas.draw()

    def add_to_expression(self, val):
        self.expression += val
        self.lbl_expr.configure(text=f"Expresión: {self.expression}")

    def clear_expression(self):
        self.expression = ""
        self.lbl_expr.configure(text="Expresión: ")
        self.lbl_result.configure(text="Resultado: ")

    def read_sets_from_ui(self):
        def parse_set(s):
            if not s.strip(): return set()
            return {x.strip() for x in s.split(",") if x.strip()}
        
        self.U = parse_set(self.entries["U"].get())
        self.A = parse_set(self.entries["A"].get())
        self.B = parse_set(self.entries["B"].get())
        self.C = parse_set(self.entries["C"].get())
        self.D = parse_set(self.entries["D"].get())

    def validate_strict_rules(self):
        self.txt_validation.configure(state="normal")
        self.txt_validation.delete("0.0", "end")
        
        log = "Validando reglas de Teoría de Conjuntos...\n"
        subsets = {'A': self.A, 'B': self.B, 'C': self.C, 'D': self.D}
        all_valid = True
        
        for name, subset in subsets.items():
            if not subset.issubset(self.U):
                invalid_elements = subset - self.U
                log += f"[ERROR] {name} contiene elementos que no están en U: {invalid_elements}\n"
                all_valid = False
            else:
                log += f"[OK] {name} es un subconjunto válido de U.\n"
                
        if all_valid:
            log += "[ÉXITO] Todos los conjuntos respetan la pertenencia al Conjunto Universal.\n"
        else:
            log += "\n[!] Validación fallida. Revisa los elementos."
            
        self.txt_validation.insert("0.0", log)
        self.txt_validation.configure(state="disabled")
        return all_valid

    def calculate(self):
        self.read_sets_from_ui()
            
        if not self.validate_strict_rules():
            return

        expr = self.expression
        if not expr:
            self.update_venn_diagram()
            return

        # Parseo seguro de la expresión matemática a operadores de Python
        # Reemplazar complemento (X^c) por (U - X)
        expr = re.sub(r'([A-DU])\^c', r'(U - \1)', expr)
        
        # Reemplazar operadores
        expr = expr.replace('∪', '|').replace('∩', '&').replace('Δ', '^')
        
        # Diccionario seguro para eval()
        context = {
            'A': self.A, 'B': self.B, 'C': self.C, 'D': self.D, 'U': self.U
        }

        try:
            result = eval(expr, {"__builtins__": None}, context)
            if not isinstance(result, set):
                raise ValueError("La expresión no resultó en un conjunto.")
            
            if len(result) == 0:
                tipo = "Vacío"
            elif len(result) == 1:
                tipo = "Unitario"
            else:
                tipo = "Finito"
                
            res_str = "{" + ", ".join(sorted(list(result))) + "}" if result else "{}"
            self.lbl_result.configure(text=f"{self.expression} = {res_str}   |   Tipo de conjunto resultante: {tipo}")
            self.update_venn_diagram()
            
        except Exception as e:
            messagebox.showerror("Error de Sintaxis", "La expresión introducida no es válida o está incompleta.")

    def update_venn_diagram(self):
        self.ax.clear()
        self.ax.axis('off')
        
        # Para representar de forma matemáticamente exacta cualquier operación hasta de 4 conjuntos 
        # (incluyendo intersecciones complejas), usamos una malla de booleanos (grid evaluation).
        x = np.linspace(-2.5, 2.5, 300)
        y = np.linspace(-2.5, 2.5, 300)
        X, Y = np.meshgrid(x, y)

        # Definición geométrica de 4 conjuntos (Círculos superpuestos)
        A_mask = (X + 0.8)**2 + (Y - 0.5)**2 <= 1.2**2
        B_mask = (X - 0.8)**2 + (Y - 0.5)**2 <= 1.2**2
        C_mask = (X + 0)**2 + (Y + 1)**2 <= 1.2**2
        D_mask = (X + 0)**2 + (Y - 1)**2 <= 1.2**2
        U_mask = np.ones_like(X, dtype=bool)

        expr = self.expression
        expr = re.sub(r'([A-DU])\^c', r'(U_mask & ~\1_mask)', expr)
        expr = expr.replace('∪', '|').replace('∩', '&').replace('Δ', '^').replace('-', '& ~')
        
        # Reemplazar nombres por variables de máscara
        expr = expr.replace('A', 'A_mask').replace('B', 'B_mask').replace('C', 'C_mask').replace('D', 'D_mask').replace('U', 'U_mask')

        try:
            # Evaluar la máscara resultante
            result_mask = eval(expr)
            
            # Dibujar el área resultante sombreada
            self.ax.contourf(X, Y, result_mask, levels=[0.5, 1.5], colors=['#3A86FF'], alpha=0.5)
            
            # Dibujar los contornos de los conjuntos
            self.ax.contour(X, Y, A_mask, levels=[0.5], colors='red', linewidths=1.5)
            self.ax.text(-1.5, 1.5, 'A', color='red', fontsize=12, fontweight='bold')
            
            self.ax.contour(X, Y, B_mask, levels=[0.5], colors='green', linewidths=1.5)
            self.ax.text(1.5, 1.5, 'B', color='green', fontsize=12, fontweight='bold')
            
            self.ax.contour(X, Y, C_mask, levels=[0.5], colors='purple', linewidths=1.5)
            self.ax.text(-1.5, -1.5, 'C', color='purple', fontsize=12, fontweight='bold')
            
            self.ax.contour(X, Y, D_mask, levels=[0.5], colors='orange', linewidths=1.5)
            self.ax.text(1.5, -1.5, 'D', color='orange', fontsize=12, fontweight='bold')

            self.canvas.draw()
            
        except Exception as e:
            pass # Errores ya manejados en calculate()

if __name__ == "__main__":
    app = SetCalculatorApp()
    app.mainloop()
