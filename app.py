#--------------------------------------------------------------------
import mysql.connector
from flask import Flask, request, jsonify, render_template, request, redirect, url_for, session
from flask import request
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time
import jinja2
#--------------------------------------------------------------------
from datetime import date
#--------------------------------------------------------------------


#--------------------------------------------------------------------
app = Flask(__name__, static_url_path='/static')


CORS(app) # Esto habilitará CORS para todas las rutas
#--------------------------------------------------------------------


class Usuario:
    """
    Esta clase proporciona métodos para administrar un catálogo de tareas
    almacenados en una base de datos MySQL.
    """
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
#-------------------------------------------------------------
# Si no existe crea la tabla usuarios
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `{database}`.`usuarios` (
                    `id_usuario` INT NOT NULL AUTO_INCREMENT,
                    `nombre` VARCHAR(50) NOT NULL,
                    `apellido` VARCHAR(50) NOT NULL,
                    `email` VARCHAR(200) NOT NULL,
                    `contraseña` VARCHAR(8) NOT NULL,
                    PRIMARY KEY (`id_usuario`),
                    UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);''')
        self.conn.commit()
        self.cursor.close()

        self.cursor = self.conn.cursor(dictionary=True)
#----------------------------------------------------------------
#Si no existe crea la tabla cursos
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE `{database}`.`cursos` (
                    `id_curso` INT NOT NULL AUTO_INCREMENT,
                    `nombre` VARCHAR(45) NOT NULL,
                    `descripcion` VARCHAR(500) NOT NULL,
                    `dias` VARCHAR(45) NOT NULL,
                    `horario` VARCHAR(45) NOT NULL,
                    PRIMARY KEY (`id_curso`));''')
        self.conn.commit()
        self.cursor.close()

        self.cursor = self.conn.cursor(dictionary=True)
#----------------------------------------------------------------
#Si no existe crea la tabla cursos_usuarios
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE `olympia`.`cursos_usuario` (
                    `idcursos_usuario` INT NOT NULL,
                    `fk_usuario` INT NOT NULL,
                    `fk_cursos` INT NOT NULL,
                    PRIMARY KEY (`idcursos_usuario`),
                    INDEX `fk_usuario_idx` (`fk_usuario` ASC) VISIBLE,
                    INDEX `fk_curso_idx` (`fk_cursos` ASC) VISIBLE,
                    CONSTRAINT `fk_usuario`
                        FOREIGN KEY (`fk_usuario`)
                        REFERENCES `olympia`.`usuarios` (`id_usuario`)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    CONSTRAINT `fk_curso`
                        FOREIGN KEY (`fk_cursos`)
                        REFERENCES `olympia`.`cursos` (`id_curso`)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE);''')
        self.conn.commit()
        self.cursor.close()

        self.cursor = self.conn.cursor(dictionary=True)


    def registrarse(self, nombre, apellido, email, contraseña):
        self.cursor.execute(f"SELECT * FROM usuarios WHERE email = {email}")
        usuario_existe = self.cursor.fetchone()
        if usuario_existe:
            return False

        sql = "INSERT INTO usuarios (nombre,apellido,email,contraseña) VALUES (%s, %s, %s, %s)"
        valores = (nombre,apellido,email,contraseña)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return True

  
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

@app.route("/registrase", methods=["GET"])      
def registrarse():
    return render_template("registrase.html")

#usuario = Usuario(host='localhost', user='root', password='', database='olympia')

#--------------------------------------------------------------------
#if __name__ == "__main__":
#    app.run(debug=True)
#--------------------------------------------------------------------