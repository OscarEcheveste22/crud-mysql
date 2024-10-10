import pymysql
from flask import Flask

app = Flask(__name__)
# Conexión a la base de datos MySQL
@app.route('/estudiantes')

def conectar():
    return pymysql.connect(
        host='157.245.141.164',  # Cambia esto si tu DB está en otro lugar
        user='root',
        password='root',
        db='estudiantes'
    )

# CREATE
def crear_alumno(no_control, nombre, ap_paterno, ap_materno, semestre):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO alumnos (no_control, nombre, ap_paterno, ap_materno, semestre) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (no_control, nombre, ap_paterno, ap_materno, semestre))
        conexion.commit()
    finally:
        conexion.close()

# READ
def leer_alumnos():
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM alumnos"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for alumno in resultado:
                print(alumno)
    finally:
        conexion.close()

# UPDATE
def actualizar_alumno(no_control, nombre=None, ap_paterno=None, ap_materno=None, semestre=None):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = "UPDATE alumnos SET "
            valores = []
            if nombre:
                sql += "nombre=%s, "
                valores.append(nombre)
            if ap_paterno:
                sql += "ap_paterno=%s, "
                valores.append(ap_paterno)
            if ap_materno:
                sql += "ap_materno=%s, "
                valores.append(ap_materno)
            if semestre:
                sql += "semestre=%s "
                valores.append(semestre)
            sql = sql.rstrip(', ')  # Eliminar la última coma
            sql += " WHERE no_control=%s"
            valores.append(no_control)
            cursor.execute(sql, tuple(valores))
        conexion.commit()
    finally:
        conexion.close()

# DELETE
def eliminar_alumno(no_control):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM alumnos WHERE no_control=%s"
            cursor.execute(sql, (no_control,))
        conexion.commit()
    finally:
        conexion.close()

# Menú para usar el CRUD
def menu():
    while True:
        print("\n--- Menú CRUD ---")
        print("1. Crear alumno")
        print("2. Leer alumnos")
        print("3. Actualizar alumno")
        print("4. Eliminar alumno")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            no_control = int(input("Número de control: "))
            nombre = input("Nombre: ")
            ap_paterno = input("Apellido Paterno: ")
            ap_materno = input("Apellido Materno: ")
            semestre = int(input("Semestre: "))
            crear_alumno(no_control, nombre, ap_paterno, ap_materno, semestre)
            print("Alumno creado.")
        elif opcion == '2':
            leer_alumnos()
        elif opcion == '3':
            no_control = int(input("Número de control del alumno a actualizar: "))
            nombre = input("Nuevo nombre (deja en blanco si no deseas cambiarlo): ")
            ap_paterno = input("Nuevo apellido paterno (deja en blanco si no deseas cambiarlo): ")
            ap_materno = input("Nuevo apellido materno (deja en blanco si no deseas cambiarlo): ")
            semestre = input("Nuevo semestre (deja en blanco si no deseas cambiarlo): ")
            actualizar_alumno(no_control, nombre or None, ap_paterno or None, ap_materno or None, int(semestre) if semestre else None)
            print("Alumno actualizado.")
        elif opcion == '4':
            no_control = int(input("Número de control del alumno a eliminar: "))
            eliminar_alumno(no_control)
            print("Alumno eliminado.")
        elif opcion == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

# Ejecutar el menú
if __name__ == '__main__':
    menu()
