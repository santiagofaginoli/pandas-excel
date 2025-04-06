import pandas as pd
import os
from datetime import datetime

archivo_excel = "clientes.xlsx"
clientes = []

# Paso 1: Cargar archivo existente si existe
if os.path.exists(archivo_excel):
    df_existente = pd.read_excel(archivo_excel)
    dnis_existentes = set(df_existente["dni"].astype(str))
else:
    df_existente = pd.DataFrame(columns=["nombre", "apellido", "dni", "fecha nacimiento", "antiguedad"])
    dnis_existentes = set()

# Paso 2: Ingreso manual de datos
while True:
    print("\nIngresá los datos del cliente:")

    # Validar nombre (solo letras y espacios)
    while True:
        nombre = input("Nombre: ").strip()
        if nombre.replace(" ", "").isalpha():
            break
        else:
            print("⚠️ El nombre solo debe contener letras.")

    # Validar apellido (solo letras y espacios)
    while True:
        apellido = input("Apellido: ").strip()
        if apellido.replace(" ", "").isalpha():
            break
        else:
            print("⚠️ El apellido solo debe contener letras.")

    # Validar DNI
    while True:
        try:
            dni = int(input("DNI (8 dígitos): "))
            if len(str(dni)) != 8:
                print("⚠️ El DNI debe tener exactamente 8 dígitos.")
                continue
            if str(dni) in dnis_existentes:
                print("⚠️ Ese DNI ya está registrado. No se agregará este cliente.")
                dni = None
                break
            break
        except ValueError:
            print("⚠️ Ingresá solo números.")

    if dni is None:
        continuar = input("¿Querés ingresar otro cliente? (s/n): ").lower()
        if continuar != 's':
            break
        else:
            continue

    # Validar fecha de nacimiento
    while True:
        fecha_nac = input("Fecha de nacimiento (DD-MM-YYYY): ")
        try:
            fecha_nac_valida = datetime.strptime(fecha_nac, "%d-%m-%Y")
            break
        except ValueError:
            print("⚠️ Fecha inválida. Usá el formato DD-MM-YYYY.")

    # Validar antigüedad
    while True:
        try:
            antiguedad = int(input("Antigüedad (en años): "))
            if antiguedad < 0:
                print("⚠️ La antigüedad no puede ser negativa.")
                continue
            break
        except ValueError:
            print("⚠️ Ingresá un número válido.")

    # Guardar cliente
    clientes.append((nombre, apellido, dni, fecha_nac, antiguedad))
    dnis_existentes.add(str(dni))  # aseguramos consistencia como string

    continuar = input("¿Querés ingresar otro cliente? (s/n): ").lower()
    if continuar != 's':
        break

# Paso 3: Combinar y guardar
if clientes:
    df_nuevos = pd.DataFrame(clientes, columns=["nombre", "apellido", "dni", "fecha nacimiento", "antiguedad"])
    df_final = pd.concat([df_existente, df_nuevos], ignore_index=True)
    df_final.to_excel(archivo_excel, index=False)
    print(f"\n✅ Se agregaron {len(clientes)} cliente(s) nuevo(s) al archivo '{archivo_excel}'.")
else:
    print("\nℹ️ No se agregaron clientes nuevos.")
