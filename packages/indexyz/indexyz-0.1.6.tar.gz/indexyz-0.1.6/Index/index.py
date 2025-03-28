import sys
import os
import time
from itertools import chain
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import tkinter as tk
import customtkinter as ctk

class Index:
    
    @staticmethod
    def initialize_credentials(empresa):
        try:
            base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")
            json_path = os.path.join(base_path, f"{empresa}.json")
            credentials = Credentials.from_service_account_file(json_path)
            return build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            print(f"Error al inicializar credenciales: {e}")
            return
    
    @staticmethod
    def get_data(service, archivo, hoja, rango=None):
        while True:
            try:
                rango_hoja = f"{hoja}!{rango}" if rango else f"{hoja}"
                data = service.spreadsheets().values().get(
                    spreadsheetId=archivo,
                    range=rango_hoja
                ).execute().get('values', [])
                if data:
                    max_cols = max(len(fila) for fila in data) if data else 0
                    data = [fila + [""] * (max_cols - len(fila)) for fila in data]
                    break
            except Exception as e:
                print(f"Error en get_data: {e}")
                return
        return data
    
    @staticmethod
    def update_data(service, archivo, hoja, rango, valores):
        while True:
            try:
                start_col, start_row = ''.join([c for c in rango.split(":")[0] if c.isalpha()]), ''.join([c for c in rango.split(":")[0] if c.isdigit()])
                end_col, end_row = ''.join([c for c in rango.split(":")[1] if c.isalpha()]), ''.join([c for c in rango.split(":")[1] if c.isdigit()])

                start_row = int(start_row) if start_row else None
                end_row = int(end_row) if end_row else None

                num_cols = ord(end_col) - ord(start_col) + 1
                if start_row and end_row:
                    num_rows = end_row - start_row + 1
                else:
                    num_rows = len(valores)

                for fila in valores:
                    if len(fila) != num_cols:
                        print(f"Error: El número de columnas no coincide con el rango {rango}.")
                        return

                if len(valores) != num_rows:
                    print(f"Error: El número de filas no coincide con el rango {rango}.")
                    return

                service.spreadsheets().values().update(
                    spreadsheetId=archivo,
                    range=f"{hoja}!{rango}",
                    valueInputOption="RAW",
                    body={"values": valores}
                ).execute()
                break

            except HttpError as http_err:
                print(f"Error HTTP en update_data: {http_err}")
                time.sleep(3)
            except Exception as e:
                print(f"Error inesperado en update_data: {e}")
                time.sleep(3)

    @staticmethod
    def update_data_locate(service, archivo, hojas, ubicaciones, valores):
        while True:
            try:
                if len(ubicaciones) != len(valores):
                    print(f"Error: El número de ubicaciones ({len(ubicaciones)}) no coincide con el número de valores ({len(valores)}).")
                    return
                data = [
                    {"range": f"{hoja}!{ubicaciones[i]}", "values": [[valores[i]]]}
                    for i, hoja in enumerate(hojas)
                ]
                body = {"valueInputOption": "RAW", "data": data}
                service.spreadsheets().values().batchUpdate(
                    spreadsheetId=archivo,
                    body=body
                ).execute()
                break
            except Exception as e:
                print(f"Error en update_data_locate: {e}")
                time.sleep(3)

    @staticmethod
    def get_index(data_cliente, columnas=None, filas=None):
        def letra_a_indice(letra):
            return sum((ord(c) - 64) * (26 ** i) for i, c in enumerate(reversed(letra))) - 1
        def procesar_columna(c):
            if "-" in c:
                a, b = c.split("-")
                a, b = letra_a_indice(a), letra_a_indice(b)
                return range(*sorted((a, b + 1), reverse=a > b))
            else:
                return [letra_a_indice(c)]
        if columnas is None and filas is None:
            return data_cliente
        indices = list(chain.from_iterable(procesar_columna(c) for c in columnas))
        if filas is None:
            return [[fila[i] for i in indices] for fila in data_cliente]
        elif isinstance(filas, int):
            return [[fila[i] for i in indices] for fila in [data_cliente[filas]]]
        else:
            return [[fila[i] for i in indices] for fila in [data_cliente[f] for f in filas]]

    @staticmethod
    def print_matriz(matriz):
        for fila in matriz:
            print("\t".join(map(str, fila)))

class VentanaUsuario:
    def __init__(self, botones_con_funciones):
        self.root = ctk.CTk()
        self.root.title("USER")
        self.root.configure(fg_color="black")
        self.ventanas_managers = []
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        self.agregar_menu(botones_con_funciones)

    def agregar_menu(self, botones_con_funciones):
        ventana_manager = VentanasManager(self.root)
        self.ventanas_managers.append(ventana_manager)
        variable = ctk.StringVar(value="")
        menu = ctk.CTkOptionMenu(self.root, values=list(botones_con_funciones.keys()), fg_color="gray20", text_color="white", variable=variable)
        menu.pack(side="top", padx=5, pady=5)
        menu.configure(command=lambda opcion: ventana_manager.abrir_ventana(opcion, *botones_con_funciones.get(opcion, ("", []))))

    def mostrar(self):
        self.root.mainloop()

    def cerrar_aplicacion(self):
        self.root.destroy()

class VentanasManager:
    def __init__(self, root):
        self.root = root
        self.ventanas_abiertas = {}

    def abrir_ventana(self, ventana_titulo, nombres_boton, funciones):
        if ventana_titulo in self.ventanas_abiertas:
            self.ventanas_abiertas[ventana_titulo].attributes("-topmost", True)
            return
        nueva_ventana = tk.Toplevel(self.root)
        nueva_ventana.title(ventana_titulo)
        nueva_ventana.config(bg="black")
        ventana_con_botones = VentanaConBotones(nueva_ventana, nombres_boton, funciones)
        ventana_con_botones.crear_botones_y_contenido(nombres_boton, funciones)
        nueva_ventana.geometry(f"{nueva_ventana.winfo_screenwidth()//2}x{nueva_ventana.winfo_screenheight()//2}")
        nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(ventana_titulo))
        nueva_ventana.attributes("-topmost", True)
        self.ventanas_abiertas[ventana_titulo] = nueva_ventana

    def cerrar_ventana(self, ventana_titulo):
        self.ventanas_abiertas.pop(ventana_titulo, None).destroy()

class VentanaConBotones:
    def __init__(self, ventana, nombres_boton, funciones):
        self.ventana = ventana
        self.frame_botones = ctk.CTkFrame(ventana)
        self.frame_botones.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)
        self.frame_contenedor = ctk.CTkFrame(self.ventana)
        self.frame_contenedor.pack(fill='both', expand=True, padx=10, pady=10)
        self.botones = {}
        self.frame_contenido = {}
        self.crear_botones_y_contenido(nombres_boton, funciones)

    def crear_botones_y_contenido(self, nombres_boton, funciones):
        for boton in self.botones.values():
            boton.destroy()

        for texto_boton, funcion in zip(nombres_boton, funciones):
            boton = ctk.CTkButton(self.frame_botones, text=texto_boton, command=lambda f=funcion, t=texto_boton: self.mostrar_contenido(f, t))
            boton.pack(side=tk.LEFT, padx=5, pady=5)
            self.botones[texto_boton] = boton
            if texto_boton not in self.frame_contenido:
                self.frame_contenido[texto_boton] = ctk.CTkFrame(self.frame_contenedor)
            self.frame_contenido[texto_boton].pack_forget()
            funcion(self.frame_contenido[texto_boton])
        if nombres_boton:
            primer_boton = self.botones.get(nombres_boton[0])
            if primer_boton:
                primer_boton.invoke()

    def mostrar_contenido(self, funcion, nombre_boton):
        for frame in self.frame_contenido.values():
            frame.pack_forget()
        frame_lista_cliente = self.frame_contenido.get(nombre_boton, None)
        if frame_lista_cliente:
            for widget in frame_lista_cliente.winfo_children():
                widget.destroy()
        self.frame_contenido[nombre_boton].pack(fill='both', expand=True)
        funcion(self.frame_contenido[nombre_boton])
