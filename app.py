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

class Database:
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



class Usuario:
    def __init__(self,database):
        self.db = database
    def __str__(self):
        return "database connection: host='127.0.0.1', user='root', password= '1234', database='olympiae' "
    def mostrar_usuario(self, id_usuario):
        try: 
            sql = f"SELECT nombre_completo, apellido, correo_electronico, tipo_usuario FROM usuarios where id_usuario = {id_usuario}"
            self.db.cursor.execute(sql)
            usuario = self.db.cursor.fetchone()
            print("usuario"+str(usuario))
            self.db.conn.commit()
            if usuario:
                try:
                    sql = (f"SELECT C.nombre_curso AS NombreCurso, "
                        f"DH.dias_y_horarios AS DiaYHorario FROM usuario_cursos UC JOIN usuarios U ON "
                        f"UC.fk_id_usuario = U.id_usuario JOIN cursos_dias_horarios CDH ON UC.fk_id_cursos_dias_horarios = CDH.id_cursos_dias_horarios "
                        f"JOIN cursos C ON CDH.fk_id_cursos = C.id_cursos JOIN dias_y_horarios DH ON CDH.fk_id_dias_y_horarios = DH.id_dias_y_horarios "
                        f"WHERE U.id_usuario = {id_usuario}")

                    self.db.cursor.execute(sql)
                    cursos = self.db.cursor.fetchall()
                    self.db.conn.commit()
                    info_usuario = {'id_usuario': id_usuario,'data_usuario': usuario, 'inscripciones': cursos}
                    print(info_usuario)
                    return info_usuario
                except mysql.connector.Error as err:
                    print(f"Error al mostrar los cursos del usuario: {err}")
                    return "Error al mostrar los cursos del usuario"
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Error al mostrar usuario: {err}")
            return "Error al mostrar usuario"
    
    def mostrar_cursos(self):
        try: 
            if usuario:
                sql =   '''
                    SELECT C.id_cursos AS IdCurso, C.nombre_curso AS NombreCurso, GROUP_CONCAT(DH.dias_y_horarios) AS Horarios
                    FROM cursos AS C
                    JOIN cursos_dias_horarios AS CDH ON C.id_cursos = CDH.fk_id_cursos
                    JOIN dias_y_horarios AS DH ON CDH.fk_id_dias_y_horarios = DH.id_dias_y_horarios
                    GROUP BY C.id_cursos, C.nombre_curso
                    '''
                self.db.cursor.execute(sql)
                cursos_horarios = self.db.cursor.fetchall()
                print (cursos_horarios)
                return cursos_horarios
        except mysql.connector.Error as err:
            print(f"Error al mostrar los cursos: {err}")
            return "Error al mostrar cursos"

    def registrarse(self, nombre, apellido, email, contraseña, tipo_usuario):
        self.db.cursor.execute(f"SELECT * FROM usuarios WHERE correo_electronico = '{email}'")
        usuario_existe = self.db.cursor.fetchone()
        if usuario_existe:
            return 'Usuario ya registrado'
        contraseña_segura = generate_password_hash(contraseña).decode('utf-8')

        sql = "INSERT INTO usuarios (nombre_completo,apellido,correo_electronico,contraseña, tipo_usuario) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre,apellido,email,contraseña_segura, tipo_usuario)
        
        try:
            self.db.cursor.execute(sql, valores)
            self.db.conn.commit()
            return "Usuario registrado con exito"
        except mysql.connector.Error as err:
            print(f"Error al registrar usuario: {err}")
            return "Error al registrar usuario"
        
    def guardar_reserva(self, id_usuario, id_curso, horario):
        #print(horario)
        
        #Sacamos el id de la tabla dias_y_horarios buscando por "horario"
        self.db.cursor.execute(f"SELECT id_dias_y_horarios FROM dias_y_horarios WHERE dias_y_horarios = '{horario}'")
        id_dias_y_horarios = self.db.cursor.fetchone()
        id_dias_y_horarios = id_dias_y_horarios['id_dias_y_horarios']
        #print (id_dias_y_horarios)
        
        #Ahora con el id de la tabla dias_y_horarios y el id_curso, sacamos el id de la tabla cursos_dias_y_horarios
        self.db.cursor.execute(f"SELECT id_cursos_dias_horarios FROM cursos_dias_horarios WHERE fk_id_cursos = '{id_curso}' AND fk_id_dias_y_horarios = '{id_dias_y_horarios}'")
        id_cursos_dias_horarios = self.db.cursor.fetchone()
        id_cursos_dias_horarios = id_cursos_dias_horarios['id_cursos_dias_horarios']
        print(id_cursos_dias_horarios)
        
        #En la tabla usuario_cursos, asociamos los id_usuario con el id_cursos_dias_horarios obtenido  
        sql = "INSERT INTO usuario_cursos (fk_id_usuario, fk_id_cursos_dias_horarios) VALUES (%s, %s)"
        valores = (id_usuario, id_cursos_dias_horarios)
        
        try:
            self.db.cursor.execute(sql, valores)
            self.db.conn.commit()
            return "Curso reservado con exito"
        except mysql.connector.Error as err:
            print(f"Error al reservar curso: {err}")
            return "Error al reservar curso"

    def cancelar_reserva(self, id_usuario, id_curso, horario):
        print(horario)
        
        #Sacamos el id de la tabla dias_y_horarios buscando por "horario"
        self.db.cursor.execute(f"SELECT id_dias_y_horarios FROM dias_y_horarios WHERE dias_y_horarios = '{horario}'")
        id_dias_y_horarios = self.db.cursor.fetchone()
        id_dias_y_horarios = id_dias_y_horarios['id_dias_y_horarios']
        print (id_dias_y_horarios)
        
        #Ahora con el id de la tabla dias_y_horarios y el id_curso, sacamos el id de la tabla cursos_dias_y_horarios
        self.db.cursor.execute(f"SELECT id_cursos_dias_horarios FROM cursos_dias_horarios WHERE fk_id_cursos = '{id_curso}' AND fk_id_dias_y_horarios = '{id_dias_y_horarios}'")
        id_cursos_dias_horarios = self.db.cursor.fetchone()
        id_cursos_dias_horarios = id_cursos_dias_horarios['id_cursos_dias_horarios']
        print(id_cursos_dias_horarios)
        
        #En la tabla usuario_cursos, asociamos los id_usuario con el id_cursos_dias_horarios obtenido  
        sql = "DELETE FROM usuario_cursos WHERE fk_id_usuario = %s AND fk_id_cursos_dias_horarios = %s"
        valores = (id_usuario, id_cursos_dias_horarios)
        
        try:
            self.db.cursor.execute(sql, valores)
            self.db.conn.commit()
            return "Curso reservado con exito"
        except mysql.connector.Error as err:
            print(f"Error al reservar curso: {err}")
            return "Error al reservar curso"


# Create an instance of the Database class
database = Database(host='localhost', user='root', password='1234', database='olympiae')

# Create an instance of the Usuario class with the database instance
usuario = Usuario(database)
print(usuario)


                
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
            usuario.db.cursor.execute(f"SELECT * FROM usuarios WHERE correo_electronico = '{email}'")
            usuario_existe = usuario.db.cursor.fetchone() 
            if not usuario_existe:
                return render_template('registrarse.html', mensaje="Registrate para poder ingresar")
                
            else:
                if check_password_hash( usuario_existe['contraseña'] , contraseña):
                    session['id_usuario'] = usuario_existe['id_usuario']
                    return redirect(url_for('info_usuario'))
                else: 
                    return render_template('login.html', errores='Las contraseña no es valida')
        except mysql.connector.Error as err:
            print(f"Error en el login: {err}")
            return "Error en login"   
    else:
        return render_template("login.html")
    
@app.route("/usuario", methods=["GET"] )
def info_usuario():
    if 'id_usuario' in session:
        id_usuario = int(session['id_usuario'])
        datos_usuario = usuario.mostrar_usuario(id_usuario)
        cursos_horarios = usuario.mostrar_cursos()
        print (cursos_horarios)
        #info_usuario = {'id_usuario': id_usuario,'data_usuario': usuario, 'inscripciones': cursos}
        return render_template("usuario.html", usuario=datos_usuario, cursos = cursos_horarios)
    else:
        return redirect(url_for('login'))

@app.route("/reservar_lugar", methods=["POST"])
def reserva_lugar():
    if 'id_usuario' in session:
        curso = request.form.get('curso')  # Para datos en formato x-www-form-urlencoded
        horario = request.form.get('horario')  # Para datos en formato x-www-form-urlencoded
        id_usuario = request.form.get('idusuario')
        id_curso = request.form.get('idcurso')
        print(f"Curso recibido: {curso}")
        print(f"ID Curso recibido: {id_curso}")
        print(f"Horario recibido: {horario}")
        print(f"ID usuario reserva: {id_usuario}")
        
        usuario.guardar_reserva(id_usuario,id_curso,horario)
    

        return jsonify({'mensaje': 'Reserva exitosa'})

@app.route("/cancelar_reserva", methods=["DELETE"])
def cancelar_reserva():
    if 'id_usuario' in session:
        #id_usuario = int(session['id_usuario'])
        curso = request.form.get('curso')  # Para datos en formato x-www-form-urlencoded
        horario = request.form.get('horario')  # Para datos en formato x-www-form-urlencoded
        id_usuario = request.form.get('idusuario')
        id_curso = request.form.get('idcurso')
        print(f"Curso cancelado: {curso}")
        print(f"ID Curso cancelado: {id_curso}")
        print(f"Horario: {horario}")
        print(f"ID usuario: {id_usuario}")

        usuario.cancelar_reserva(id_usuario,id_curso,horario)

        return jsonify({'mensaje': 'Cancelacion exitosa'})

@app.route("/logout", methods=["GET"] )
def logout():
    session.pop('usuario', None)
    return   redirect(url_for('index'))



#----------------PRUEBAS---------------------------------------------


#print(usuario.mostrar_usuario(2))
#print(usuario.registrarse("miguel", "vincent", "mmppppp@h.com", 1234566666, 1))


# # #--------------------------------------------------------------------
if __name__ == "__main__":
   app.run(debug=True)
# # #--------------------------------------------------------------------