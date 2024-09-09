import random
import csv
import openpyxl
from datetime import datetime
from tabulate import tabulate

def main():
    print('Hola, ¿cómo estás?')
    print('Selecciona la opción que deseas realizar en este momento:')
    MenuPrincipal()

def cargar_datos(nombre_archivo):
    try:
        with open(f"{nombre_archivo}.csv", 'r', newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)
    except FileNotFoundError:
        return []

def guardar_datos(nombre_archivo, datos, campos):
    with open(f"{nombre_archivo}.csv", 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(datos)

# Cargar datos al inicio del programa
unidades_registradas = cargar_datos("unidades")
prestamos_registrados = cargar_datos("prestamos")
clientes_registrados = cargar_datos("clientes")

continuar = True

def MenuPrincipal():
    global continuar  # Permite modificar la variable 'continuar'
    while continuar:  # Se repite hasta que el usuario decida salir
        print('\n\t Menú Principal')
        print('\t1. Registro')
        print('\t2. Préstamo')
        print('\t3. Retorno')
        print('\t4. Reportes')
        print('\t5. Salir')

        opcion = input('\nOpción deseada: ')

        if opcion == '1':
            MenuRegistro()
        elif opcion == '2':
            MenuPrestamo()
        elif opcion == '3':
            MenuRetorno()
        elif opcion == '4':
            MenuReportes()
        elif opcion == '5':
            if ConfirmarSalida():
                print('\nGracias por usar el sistema. ¡Hasta luego!')
                continuar = False  # Finaliza el ciclo, saliendo del programa
            else:
                continue  # Vuelve al menú principal si no se confirma la salida
        else:
            print('\nOpción inválida. Por favor, selecciona una opción válida.')

def GuardarYSalir():
    guardar_datos("unidades", unidades_registradas, ["clave", "rodada"])
    guardar_datos("prestamos", prestamos_registrados, ["Folio", "Clave Unidad", "Clave Cliente", "Fecha Prestamo", "Días Prestamo", "Fecha Retorno"])
    guardar_datos("clientes", clientes_registrados, ["clave_cliente", "apellidos", "nombres", "telefono"])
    print('\nDatos guardados. Gracias por usar el sistema. ¡Hasta luego!')


def ConfirmarSalida():
    """Función para confirmar si el usuario realmente quiere salir."""
    while True:
        confirmacion = input("¿Estás seguro de que deseas salir? (s/n): ").strip().lower()
        if confirmacion == 's':
            return True
        elif confirmacion == 'n':
            return False
        else:
            print("Opción inválida. Por favor, ingresa 's' para sí o 'n' para no.")

def MenuRegistro():
    print('\nEn este momento estás en Registro, ¿qué deseas hacer?')
    print('\t1. Unidades')
    print('\t2. Clientes')
    print('\t3. Volver al Menú Principal')

    opcionRegistro = input('\nOpción deseada: ')

    if opcionRegistro == '1':
        MenuUnidad()
    elif opcionRegistro == '2':
        MenuCliente()
    elif opcionRegistro == '3':
        MenuPrincipal()
    else:
        print('\nOpción inválida. Por favor, selecciona una opción válida.')
        MenuRegistro()

def MenuUnidad():
    print('\n¿Que deseas realizar?')
    print('\t1. Agregar nueva unidad')
    print('\t2. Volver al Menú de Registro')

    opcionUnidad = input('\nOpción deseada: ')
    
    if opcionUnidad == '1':
        RegistrarUnidad()
        
    elif opcionUnidad == '2':
        MenuRegistro()
    else:
        print('\nOpción inválida. Por favor, selecciona una opción válida.')
        MenuUnidad()

def RegistrarUnidad():
    print("\nPara cancelar en cualquier momento, ingrese 'cancelar'.")
    
    # Generar clave única para la unidad
    clave = random.randint(1, 1000)
    
    # Solicitar la rodada de la bicicleta
    while True:
        rodada = input("\nIngrese la rodada de la bicicleta (20, 26 o 29): ")
        if rodada.lower() == 'cancelar':
            print("Operación cancelada.")
            return MenuUnidad()
        if rodada in ["20", "26", "29"]:
            print("Rodada valida.")
            break
        else:
            print("Rodada inválida. Por favor, ingrese 20, 26 o 29.")
    # Guardar los datos de la unidad
    unidad = {
    "clave": clave,
    "rodada": rodada
    }
    unidades_registradas.append(unidad)
        
    print("\nSe ha registrado la siguiente unidad:")
    print(f"Clave: {clave}")
    print(f"Rodada: {rodada}")
    print("\nRegistro de unidad completado.")
    MenuUnidad()


def MenuCliente():
    print('\n¿Qué deseas realizar?')
    print('\t1. Registrar nuevo cliente')
    print('\t2. Volver al Menú Principal')

    opcionCliente = input('\nOpción deseada: ')
    
    if opcionCliente == '1':
        RegistrarCliente()
    elif opcionCliente == '2':
        MenuPrincipal()
    else:
        print('\nOpción inválida. Por favor, selecciona una opción válida.')
        MenuCliente()

def RegistrarCliente():
    print("\nPara cancelar en cualquier momento, ingrese 'cancelar'.")

    clave_cliente = random.randint(1, 1000)

    # Validar apellidos
    while True:
        apellidos = input("Ingrese los apellidos del cliente (máximo 40 caracteres): ")
        if apellidos.lower() == 'cancelar':
            print("Operación cancelada.")
            return MenuCliente()
        if 1 <= len(apellidos) <= 40:
            break
        else:
            print("Apellidos inválidos. Deben contener entre 1 y 40 caracteres.")
    
    # Validar nombres
    while True:
        nombres = input("Ingrese los nombres del cliente (máximo 40 caracteres): ")
        if nombres.lower() == 'cancelar':
            print("Operación cancelada.")
            return MenuCliente()
        if 1 <= len(nombres) <= 40:
            break
        else:
            print("Nombres inválidos. Deben contener entre 1 y 40 caracteres.")
    
    # Validar teléfono
    while True:
        telefono = input("Ingrese el número de teléfono del cliente (10 dígitos): ")
        if telefono.lower() == 'cancelar':
            print("Operación cancelada.")
            return MenuCliente()
        if telefono.isdigit() and len(telefono) == 10:
            break
        else:
            print("Número de teléfono inválido. Debe contener exactamente 10 dígitos.")
    
    cliente = {
        "clave_cliente": clave_cliente,
        "apellidos": apellidos,
        "nombres": nombres,
        "telefono": telefono
    }
    clientes_registrados.append(cliente)
    
    print("\nCliente registrado con éxito:")
    print(tabulate([cliente.values()], headers=cliente.keys(), tablefmt="grid"))

    MenuCliente()


def MenuPrestamo():
    print('\n¿Que deseas realizar?')
    print('\t1. Registrar un nuevo préstamo')
    print('\t2. Ver préstamos registrados')
    print('\t3. Volver al Menú Principal')

    opcionPrestamo = input('\nOpción deseada: ')
    
    if opcionPrestamo == '1':
        RegistrarPrestamo()
    elif opcionPrestamo == '2':
        VerPrestamos()
    elif opcionPrestamo == '3':
        MenuPrincipal()
    else:
        print('\nOpción inválida. Por favor, selecciona una opción válida.')
        MenuPrestamo()

def RegistrarPrestamo():
    print("\nPara cancelar en cualquier momento, ingrese 'cancelar'.")

    folio = random.randint(1, 1000)
    
    # Validar clave de la unidad
    while True:
        clave_unidad = input("Ingrese la clave de la unidad (número entero mayor a cero): ")
        if clave_unidad.lower() == 'cancelar':
            print("Operación cancelada.")
            return MenuPrestamo()
        if clave_unidad.isdigit() and int(clave_unidad) > 0:
            clave_unidad = int(clave_unidad)
            if any(unidad['clave'] == clave_unidad for unidad in unidades_registradas):
                break
            else:
                print("Clave de unidad no encontrada. Por favor, ingrese una clave de unidad registrada.")
        else:
            print("Clave de unidad inválida. Debe ser un número entero mayor a cero.")
    
    # Validar clave del cliente
    while True:
        clave_cliente = input("Ingrese la clave del cliente (número entero mayor a cero): ")
        if clave_cliente.lower() == 'cancelar':
            print("Operación cancelada.")
            return MenuPrestamo()
        if clave_cliente.isdigit() and int(clave_cliente) > 0:
            clave_cliente = int(clave_cliente)
            if any(cliente['clave_cliente'] == clave_cliente for cliente in clientes_registrados):
                break
            else:
                print("Clave del cliente no encontrada. Por favor, ingrese una clave de cliente registrada.")
        else:
            print("Clave del cliente inválida. Debe ser un número entero mayor a cero.")
    
    # Validar fecha del préstamo
    fecha_actual = datetime.now().strftime("%m-%d-%Y")
    while True:
        fecha_prestamo = input(f"Ingrese la fecha del préstamo (por defecto {fecha_actual} o formato mm-dd-aaaa): ")
        if fecha_prestamo.lower() == 'cancelar':
            print("Operación cancelada.")
            return MenuPrestamo()
        if fecha_prestamo == "":
            fecha_prestamo = fecha_actual
            break
        else:
            try:
                fecha_prestamo_dt = datetime.strptime(fecha_prestamo, "%m-%d-%Y")
                if fecha_prestamo_dt.date() >= datetime.now().date():
                    fecha_prestamo = fecha_prestamo_dt.strftime("%m-%d-%Y")
                    break
                else:
                    print("Fecha inválida. La fecha no puede ser anterior a la fecha actual.")
            except ValueError:
                print("Fecha inválida. Debe estar en el formato mm-dd-aaaa.")
    
    # Validar cantidad de días del préstamo
    while True:
        dias_prestamo = input("Ingrese la cantidad de días del préstamo (entre 1 y 14 días): ")
        if dias_prestamo.lower() == 'cancelar':
            print("Operación cancelada.")
            return MenuPrestamo()
        if dias_prestamo.isdigit() and 1 <= int(dias_prestamo) <= 14:
            dias_prestamo = int(dias_prestamo)
            break
        else:
            print("Cantidad de días inválida. Debe ser un número entero entre 1 y 14 días.")
    
    fecha_retorno = ""

    prestamo = {
        "Folio": folio,
        "Clave Unidad": clave_unidad,
        "Clave Cliente": clave_cliente,
        "Fecha Prestamo": fecha_prestamo,
        "Días Prestamo": dias_prestamo,
        "Fecha Retorno": fecha_retorno
    }
    prestamos_registrados.append(prestamo)
    
    print("\nDatos del préstamo registrado:")
    print(tabulate([prestamo.values()], headers=prestamo.keys(), tablefmt="grid"))

    MenuPrestamo()


def VerPrestamos():
    print("\n\tListado de Préstamos Registrados")
    
    if not prestamos_registrados:
        print("No se han registrado préstamos.")
        return
    
    tabla = [[p["Folio"], p["Clave Unidad"], p["Clave Cliente"], p["Fecha Prestamo"], p["Días Prestamo"], p["Fecha Retorno"]] for p in prestamos_registrados]
    print(tabulate(tabla, headers=["Folio", "Clave Unidad", "Clave Cliente", "Fecha Prestamo", "Días Prestamo", "Fecha Retorno"], tablefmt="grid"))
    
    MenuPrestamo()
    

def MenuRetorno():
    print('\n\tMenú de Retorno')
    print('\t1. Ver préstamos pendientes de retorno')
    print('\t2. Registrar retorno')
    print('\t3. Volver al Menú Principal')

    opcionRetorno = input('\nOpción deseada: ')
    
    if opcionRetorno == '1':
        MostrarPrestamosPendientes()
    elif opcionRetorno == '2':
        RegistrarRetorno()
    elif opcionRetorno == '3':
        MenuPrincipal()
    else:
        print('\nOpción inválida. Por favor, selecciona una opción válida.')
        MenuRetorno()

def MostrarPrestamosPendientes():
    print("\n\tPréstamos Pendientes de Retorno")
    
    prestamos_pendientes = [p for p in prestamos_registrados if p["Fecha Retorno"] == ""]
    
    if not prestamos_pendientes:
        print("No hay préstamos pendientes de retorno.")
    else:
        tabla = [[p["Folio"], p["Clave Unidad"], p["Clave Cliente"], p["Fecha Prestamo"], p["Días Prestamo"]] for p in prestamos_pendientes]
        print(tabulate(tabla, headers=["Folio", "Clave Unidad", "Clave Cliente", "Fecha Prestamo", "Días Prestamo"], tablefmt="grid"))
    
    MenuRetorno()

def RegistrarRetorno():
    folio = input("Ingrese el folio del préstamo a retornar: ")
    
    prestamo = next((p for p in prestamos_registrados if str(p["Folio"]) == folio), None)
    
    if prestamo is None:
        print(f"No se encontró un préstamo con el folio {folio}.")
        MenuRetorno()
        return
    
    if prestamo["Fecha Retorno"] != "":
        print(f"El préstamo con folio {folio} ya ha sido retornado.")
        MenuRetorno()
        return
    
    fecha_actual = datetime.now().strftime("%m-%d-%Y")
    prestamo["Fecha Retorno"] = fecha_actual
    
    print(f"\nPréstamo con folio {folio} ha sido marcado como retornado en la fecha {fecha_actual}.")
    print("\nDatos actualizados del préstamo:")
    print(tabulate([prestamo.values()], headers=prestamo.keys(), tablefmt="grid"))
    
    MenuRetorno()

def ExportarReporte(datos, headers, nombre_archivo):
    while True:
        print("\n¿Desea exportar este reporte?")
        print("1. Exportar como CSV")
        print("2. Exportar como Excel")
        print("3. No exportar")
        
        opcion = input("\nOpción deseada: ")
        
        if opcion == "1":
            ExportarCSV(datos, headers, nombre_archivo)
            break
        elif opcion == "2":
            ExportarExcel(datos, headers, nombre_archivo)
            break
        elif opcion == "3":
            print("No se exportará el reporte.")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def ExportarCSV(datos, headers, nombre_archivo):
    nombre_archivo = f"{nombre_archivo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(nombre_archivo, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(datos)
    print(f"Reporte exportado como CSV: {nombre_archivo}")

def ExportarExcel(datos, headers, nombre_archivo):
    nombre_archivo = f"{nombre_archivo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(headers)
    for row in datos:
        ws.append(row)
    wb.save(nombre_archivo)
    print(f"Reporte exportado como Excel: {nombre_archivo}")

def MenuReportes():
    
    print('\n\tMenú de Reportes')
    print('\t1. Ver usuarios registrados')
    print('\t2. Ver préstamos no devueltos')
    print('\t3. Buscar préstamos por duración')
    print('\t4. Volver al Menú Principal')

    opcion = input('\nOpción deseada: ')

    if opcion == '1':
        VerUsuariosRegistrados()
    elif opcion == '2':
        VerPrestamosNoDevueltos()
    elif opcion == '3':
        BuscarPrestamosPorDuracion()
    elif opcion == '4':
        MenuPrincipal()
    else:
        print('\nOpción inválida. Por favor, selecciona una opción válida.')

def VerUsuariosRegistrados():
    print("\n\tListado de Usuarios Registrados")
    
    if not clientes_registrados:
        print("No hay usuarios registrados.")
        return
    
    headers = ["Clave Cliente", "Apellidos", "Nombres", "Teléfono"]
    datos = [[c["clave_cliente"], c["apellidos"], c["nombres"], c["telefono"]] for c in clientes_registrados]
    
    print(tabulate(datos, headers=headers, tablefmt="grid"))
    
    ExportarReporte(datos, headers, "usuarios_registrados")

def VerPrestamosNoDevueltos():
    print("\n\tListado de Préstamos No Devueltos")
    
    prestamos_no_devueltos = [p for p in prestamos_registrados if p["Fecha Retorno"] == ""]
    
    if not prestamos_no_devueltos:
        print("No hay préstamos pendientes de devolución.")
        return
    
    headers = ["Folio", "Clave Unidad", "Clave Cliente", "Fecha Prestamo", "Días Prestamo"]
    datos = [[p["Folio"], p["Clave Unidad"], p["Clave Cliente"], p["Fecha Prestamo"], p["Días Prestamo"]] for p in prestamos_no_devueltos]
    
    print(tabulate(datos, headers=headers, tablefmt="grid"))
    
    ExportarReporte(datos, headers, "prestamos_no_devueltos")

def BuscarPrestamosPorDuracion():
    while True:
        dias = input("\nIngrese la cantidad de días de préstamo a buscar: ")
        if dias.isdigit() and int(dias) > 0:
            dias = int(dias)
            break
        else:
            print("Por favor, ingrese un número entero positivo.")
    
    prestamos_encontrados = [p for p in prestamos_registrados if p["Días Prestamo"] == dias]
    
    if not prestamos_encontrados:
        print(f"No se encontraron préstamos con duración de {dias} días.")
        return
    
    print(f"\n\tListado de Préstamos con Duración de {dias} Días")
    headers = ["Folio", "Clave Unidad", "Clave Cliente", "Fecha Prestamo", "Días Prestamo", "Fecha Retorno"]
    datos = [[p["Folio"], p["Clave Unidad"], p["Clave Cliente"], p["Fecha Prestamo"], p["Días Prestamo"], p["Fecha Retorno"]] for p in prestamos_encontrados]
    
    print(tabulate(datos, headers=headers, tablefmt="grid"))
    
    ExportarReporte(datos, headers, f"prestamos_duracion_{dias}_dias")



if __name__ == "__main__":
    main()
