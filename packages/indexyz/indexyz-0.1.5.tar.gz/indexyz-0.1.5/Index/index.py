import sys
import os
import time
from itertools import chain
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
