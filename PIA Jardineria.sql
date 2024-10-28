import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statistics

# Conexión a la base de datos
conn = sqlite3.connect('renta_bicicletas.db')
cursor = conn.cursor()

# Creación de tablas
def crear_tablas():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Unidades (
        clave INTEGER PRIMARY KEY AUTOINCREMENT,
        rodada INTEGER CHECK(rodada IN (20, 26, 29)),
        color TEXT CHECK(length(color) <= 15) NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clientes (
        clave INTEGER PRIMARY KEY AUTOINCREMENT,
        apellidos TEXT CHECK(length(apellidos) <= 40) NOT NULL,
        nombres TEXT CHECK(length(nombres) <= 40) NOT NULL,
        telefono TEXT CHECK(length(telefono) = 10 AND telefono GLOB '[0-9]*') NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prestamos (
        folio INTEGER PRIMARY KEY AUTOINCREMENT,
        unidad_clave INTEGER NOT NULL,
        cliente_clave INTEGER NOT NULL,
        fecha_prestamo DATE NOT NULL,
        dias_prestamo INTEGER CHECK(dias_prestamo BETWEEN 1 AND 14) NOT NULL,
        fecha_retorno DATE,
        FOREIGN KEY (unidad_clave) REFERENCES Unidades(clave),
        FOREIGN KEY (cliente_clave) REFERENCES Clientes(clave)
    )''')
    conn.commit()

# Función para exportar datos a CSV
def exportar_csv(datos, nombre_archivo):
    datos.to_csv(f'{nombre_archivo}.csv', index=False)
    print(f'Reporte exportado a {nombre_archivo}.csv')

# Función para exportar datos a Excel
def exportar_excel(datos, nombre_archivo):
    datos.to_excel(f'{nombre_archivo}.xlsx', index=False)
    print(f'Reporte exportado a {nombre_archivo}.xlsx')

# Función para mostrar el menú principal con ruta
def mostrar_menu(ruta):
    while True:
        print(f"{ruta} >")
        print("1. Registrar cliente")
        print("2. Registrar unidad")
        print("3. Registrar préstamo")
        print("4. Retornar unidad")
        print("5. Informes")
        print("6. Análisis")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_cliente(ruta + " > Registro de Cliente")
        elif opcion == '2':
            registrar_unidad(ruta + " > Registro de Unidad")
        elif opcion == '3':
            registrar_prestamo(ruta + " > Registro de Préstamo")
        elif opcion == '4':
            retornar_unidad(ruta + " > Retorno de Unidad")
        elif opcion == '5':
            mostrar_informes(ruta + " > Informes")
        elif opcion == '6':
            mostrar_analisis(ruta + " > Análisis")
        elif opcion == '7':
            confirmar_salida(ruta)
        else:
            print("Opción no válida, intente nuevamente.")

# Función para registrar cliente
def registrar_cliente(ruta):
    print(ruta)
    apellidos = input("Ingrese los apellidos del cliente (máximo 40 caracteres): ")
    nombres = input("Ingrese los nombres del cliente (máximo 40 caracteres): ")
    telefono = input("Ingrese el teléfono del cliente (10 dígitos): ")
    
    if len(apellidos) > 40 or len(nombres) > 40 or len(telefono) != 10 or not telefono.isdigit():
        print("Datos inválidos. Intente nuevamente.")
        return
    
    cursor.execute("INSERT INTO Clientes (apellidos, nombres, telefono) VALUES (?, ?, ?)", (apellidos, nombres, telefono))
    conn.commit()
    print("Cliente registrado exitosamente.")

# Función para registrar unidad
def registrar_unidad(ruta):
    print(ruta)
    rodada = input("Ingrese la rodada de la unidad (20, 26, 29): ")
    color = input("Ingrese el color de la unidad (máximo 15 caracteres): ")

    if rodada not in ['20', '26', '29'] or len(color) > 15:
        print("Datos inválidos. Intente nuevamente.")
        return

    cursor.execute("INSERT INTO Unidades (rodada, color) VALUES (?, ?)", (rodada, color))
    conn.commit()
    print("Unidad registrada exitosamente.")

# Función para registrar préstamo
def registrar_prestamo(ruta):
    print(ruta)
    unidades = pd.read_sql_query("SELECT clave, rodada, color FROM Unidades", conn)
    print(unidades)
    unidad_clave = input("Seleccione la clave de la unidad: ")

    clientes = pd.read_sql_query("SELECT clave, apellidos, nombres FROM Clientes", conn)
    print(clientes)
    cliente_clave = input("Seleccione la clave del cliente: ")

    dias_prestamo = input("Ingrese la cantidad de días del préstamo (1-14): ")

    fecha_prestamo = input("Ingrese la fecha del préstamo (mm-dd-aaaa, presione Enter para usar la fecha actual): ") or datetime.now().strftime("%m-%d-%Y")
    
    if not dias_prestamo.isdigit() or not 1 <= int(dias_prestamo) <= 14:
        print("Datos inválidos. Intente nuevamente.")
        return

    cursor.execute("INSERT INTO Prestamos (unidad_clave, cliente_clave, fecha_prestamo, dias_prestamo) VALUES (?, ?, ?, ?)", 
                   (unidad_clave, cliente_clave, fecha_prestamo, dias_prestamo))
    conn.commit()
    print("Préstamo registrado exitosamente.")

# Función para retornar unidad
def retornar_unidad(ruta):
    print(ruta)
    prestamos = pd.read_sql_query("SELECT * FROM Prestamos WHERE fecha_retorno IS NULL ORDER BY fecha_prestamo DESC", conn)
    print(prestamos)
    folio = input("Seleccione el folio del préstamo a retornar: ")
    fecha_retorno = datetime.now().strftime("%m-%d-%Y")
    
    cursor.execute("UPDATE Prestamos SET fecha_retorno = ? WHERE folio = ?", (fecha_retorno, folio))
    conn.commit()
    print("Unidad retornada exitosamente.")

# Función para mostrar informes
def mostrar_informes(ruta):
    print(ruta)
    print("1. Listado de clientes")
    print("2. Listado de unidades")
    print("3. Listado de unidades por rodada")
    print("4. Listado de unidades por color")
    print("5. Préstamos retrasados")
    print("6. Préstamos por retornar")
    print("7. Préstamos por período")
    opcion = input("Seleccione una opción: ")
    
    if opcion == '1':
        clientes = pd.read_sql_query("SELECT * FROM Clientes", conn)
        print(clientes)
        exportar(clientes, "clientes")
    elif opcion == '2':
        unidades = pd.read_sql_query("SELECT * FROM Unidades", conn)
        print(unidades)
        exportar(unidades, "unidades")
    elif opcion == '3':
        rodada = input("Ingrese la rodada (20, 26, 29): ")
        unidades_rodada = pd.read_sql_query("SELECT clave, color FROM Unidades WHERE rodada = ?", conn, params=(rodada,))
        print(unidades_rodada)
        exportar(unidades_rodada, f"unidades_rodada_{rodada}")
    # Agrega las otras opciones aquí...

# Función para realizar análisis
def mostrar_analisis(ruta):
    print(ruta)
    print("1. Duración de préstamos")
    print("2. Ranking de clientes")
    print("3. Preferencias de rentas")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        duracion_prestamos()
    elif opcion == '2':
        ranking_clientes()
    elif opcion == '3':
        mostrar_preferencias()

# Otras funciones de análisis y gráficos...
def duracion_prestamos():
    prestamos = pd.read_sql_query("SELECT dias_prestamo FROM Prestamos", conn)
    dias = prestamos['dias_prestamo'].tolist()
    print("Media:", statistics.mean(dias))
    print("Mediana:", statistics.median(dias))
    print("Moda:", statistics.mode(dias))
    print("Mínimo:", min(dias))
    print("Máximo:", max(dias))
    print("Desviación estándar:", statistics.stdev(dias))

def ranking_clientes():
    ranking = pd.read_sql_query("""
        SELECT Clientes.clave, Clientes.apellidos, Clientes.nombres, COUNT(Prestamos.cliente_clave) AS cantidad_prestamos
        FROM Prestamos
        JOIN Clientes ON Clientes.clave = Prestamos.cliente_clave
        GROUP BY Prestamos.cliente_clave
        ORDER BY cantidad_prestamos DESC
    """, conn)
    print(ranking)

def mostrar_preferencias():
    print("1. Por rodada")
    print("2. Por color")
    print("3. Por día de la semana")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        prestamos_rodada()
    elif opcion == '2':
        prestamos_color()
    elif opcion == '3':
        prestamos_dia_semana()

# Confirmar salida
def confirmar_salida(ruta):
    confirmacion = input("¿Está seguro de que desea salir? (S/N): ")
    if confirmacion.lower() == 's':
        conn.close()
        print("Gracias por usar el sistema.")
    else:
        mostrar_menu(ruta)

# Iniciar el sistema
if __name__ == "__main__":
    crear_tablas()
    mostrar_menu("Menú Principal")
