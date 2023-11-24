#--------------------------------------------------------------------
import mysql.connector
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time
import jinja2



#--------------------------------------------------------------------
app = Flask(__name__, static_url_path='/static')


CORS(app) # Esto habilitará CORS para todas las rutas
#--------------------------------------------------------------------


class Usuario:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
            )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
#-------------------------------------------------------------
# Si no existe crea la tabla usuarios
        # self.cursor = self.conn.cursor(dictionary=True)
        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS `{database}`.`usuarios` (
        #             `id_usuario` INT NOT NULL AUTO_INCREMENT,
        #             `nombre_completo` VARCHAR(30) NOT NULL,
        #             `apellido` VARCHAR(30) NOT NULL,
        #             `correo_electronico` VARCHAR(30) NOT NULL,
        #             `contraseña` VARCHAR(11) NOT NULL,
        #             PRIMARY KEY (`id_usuario`),
        #             UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);''')
        # self.conn.commit()
        # self.cursor.close()

        # self.cursor = self.conn.cursor(dictionary=True)


    def mostrar_usuario(self, id_usuario):
        sql = f"SELECT * FROM usuarios where id_usuario = {id_usuario}"
        self.cursor.execute(sql)
        usuario = self.cursor.fetchone()
        self.conn.commit()
        if usuario:
            return usuario
        else:
            return False

    def registrarse(self, nombre, apellido, email, contraseña):
        self.cursor.execute(f"SELECT * FROM usuarios WHERE correo_electrónico = '{email}'")
        usuario_existe = self.cursor.fetchone()
        if usuario_existe:
            return False

        sql = "INSERT INTO usuarios (nombre_completo,apellido,correo_electrónico,contraseña) VALUES (%s, %s, %s, %s)"
        valores = (nombre,apellido,email,contraseña)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True
    


def validar_usuario_login(self, email, contraseña):
    self.cursor.execute(f"SELECT * FROM usuarios WHERE correo_electrónico = '{email}'")
    usuario_existe = self.cursor.fetchone()
    if not usuario_existe:
        return False
    else:
        if usuario_existe['contraseña'] == contraseña:
            session['usuario'] = usuario_existe
            return True
        else: 
            return False
        
#----------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/actividades", methods=["GET"])
def actividades():
    return render_template("actividades.html")

@app.route("/nosotros", methods=["GET"])
def nosotros():
    return render_template("nosotros.html")

@app.route("/contacto", methods=["GET"])
def contacto():
    return render_template("contacto.html")

@app.route("/registrarse", methods=["GET"])
def registrarse():
    return render_template("registrarse.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

usuario = Usuario(host='localhost', user='root', password='', database='olympia')


#----------------PRUEBAS---------------------------------------------4

#print(usuario.mostrar_usuario(1))
print(usuario.registrarse("miguel", "vincent", "mmppppp@h.com", 1234566666))






# #--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
# #--------------------------------------------------------------------