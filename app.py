#--------------------------------------------------------------------
import mysql.connector
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time
import jinja2
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash




#--------------------------------------------------------------------
app = Flask(__name__, static_url_path='/static')
bcrypt = Bcrypt(app)
app.secret_key = 'secret_key_olympia'
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
        try: 
            sql = f"SELECT nombre_completo, apellido, correo_electronico, tipo_usuario FROM usuarios where id_usuario = {id_usuario}"
            self.cursor.execute(sql)
            usuario = self.cursor.fetchone()
            self.conn.commit()
            if usuario:
                try:
                    sql = (f"SELECT C.nombre_curso AS NombreCurso, "
                        f"DH.dias_y_horarios AS DiaYHorario FROM usuario_cursos UC JOIN usuarios U ON "
                        f"UC.fk_id_usuario = U.id_usuario JOIN cursos_dias_horarios CDH ON UC.fk_id_cursos_dias_horarios = CDH.id_cursos_dias_horarios "
                        f"JOIN cursos C ON CDH.fk_id_cursos = C.id_cursos JOIN dias_y_horarios DH ON CDH.fk_id_dias_y_horarios = DH.id_dias_y_horarios "
                        f"WHERE U.id_usuario = {id_usuario}")

                    self.cursor.execute(sql)
                    cursos = self.cursor.fetchall()
                    self.conn.commit()
                    info_usuario = {'data_usuario': usuario, 'inscripciones': cursos}
                    return info_usuario
                except mysql.connector.Error as err:
                    print(f"Error al mostrar los cursos del usuario: {err}")
                    return "Error al mostrar los cursos del usuario"
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Error al mostrar usuario: {err}")
            return "Error al mostrar usuario"

    def registrarse(self, nombre, apellido, email, contraseña, tipo_usuario):
        self.cursor.execute(f"SELECT * FROM usuarios WHERE correo_electronico = '{email}'")
        usuario_existe = self.cursor.fetchone()
        if usuario_existe:
            return 'Usuario ya registrado'
        contraseña_segura = generate_password_hash(contraseña).decode('utf-8')

        sql = "INSERT INTO usuarios (nombre_completo,apellido,correo_electronico,contraseña, tipo_usuario) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre,apellido,email,contraseña_segura, tipo_usuario)
        
        try:
            self.cursor.execute(sql, valores)
            self.conn.commit()
            return "Usuario registrado con exito"
        except mysql.connector.Error as err:
            print(f"Error al registrar usuario: {err}")
            return "Error al registrar usuario"
    




                
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

@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        contraseña = request.form['password1']

        resultado_registro = usuario.registrarse( nombre, apellido, email, contraseña,2)

        if resultado_registro == "Usuario registrado con exito":
            #return render_template('login.html')
            return redirect(url_for('login'))
        else: 
            print('no se pudo registrar el usuario')
            return render_template('registrarse.html', errores=resultado_registro)
        
    return render_template('registrarse.html')

@app.route("/login", methods=["POST", "GET"] )
def login():
    if request.method == "POST":
        email = request.form['email']
        contraseña = request.form['password1']
        try:
            usuario.cursor.execute(f"SELECT * FROM usuarios WHERE correo_electronico = '{email}'")
            usuario_existe = usuario.cursor.fetchone() 
            if not usuario_existe:
                return render_template('registrarse.html', mensaje="Registrate para poder ingresar")
                
            else:
                if check_password_hash( usuario_existe['contraseña'] , contraseña):
                    session['id_usuario'] = usuario_existe['id_usuario']
                    return redirect(url_for('usuario'))
                else: 
                    return render_template('login.html', errores='Las contraseña no es valida')
        except mysql.connector.Error as err:
            print(f"Error en el login: {err}")
            return "Error en login"   
    else:
        return render_template("login.html")
    
@app.route("/usuario", methods=["GET"] )
def usuario():
    if 'id_usuario' in session:
        id_usuario = int(session['id_usuario'])
        datos_usuario = usuario.mostrar_usuario(id_usuario)
        return render_template("usuario.html", usuario=datos_usuario)
    else:
        return redirect(url_for('login'))

@app.route("/logout", methods=["GET"] )
def logout():
    session.pop('usuario', None)
    return   redirect(url_for('index'))

usuario = Usuario(host='localhost', user='root', password='', database='olympiae')


#----------------PRUEBAS---------------------------------------------


#print(usuario.mostrar_usuario(2))
#print(usuario.registrarse("miguel", "vincent", "mmppppp@h.com", 1234566666))


# # #--------------------------------------------------------------------
#if __name__ == "__main__":
#   app.run(debug=True)
# # #--------------------------------------------------------------------