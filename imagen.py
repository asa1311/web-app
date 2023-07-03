from flask import Flask,flash,request,redirect,session
from werkzeug.utils import secure_filename
from db import get_db
import utils
import uuid
import os

class Imagen():
    def __init__(self, id = "", nombre = "", tamano = None, privacidad = "", ubicacion = "", usuario = None):
        self.id = id
        self.nombre = nombre
        self.privacidad = privacidad
        self.ubicacion = ubicacion
        self.usuario = usuario

    def setId(self, id):
        self.id = id
        
    def setNombre(self, nombre):
        self.nombre = nombre
        
    def setTamano(self, tamano):
        self.tamano = tamano
        
    def setPrivacidad(self, privacidad):
        self.privacidad = privacidad
        
    def setUbicacion(self, ubicacion):
        self.ubicacion = ubicacion
        
    def setUsuario(self, usuario):
        self.usuario = usuario
        
    def getId(self):
       return self.id
        
    def getNombre(self):
        return self.nombre
        
    def getTamano(self):
        return self.tamano
        
    def getPrivacidad(self):
        return self.privacidad
        
    def getUbicacion(self):
        return self.ubicacion
        
    def getUsuario(self):
        return self.usuario

    def uploadImage(self):
        result = {
            "status": "error",
            "message": "No se pudo cargar la imagen"
        }
        unique_filename = ""
        try:
            # check if the post request has the file part
            if 'inputFile' not in request.files:
                result["message"] =  'No se encontro el archivo'
                return result
            
            file = request.files['inputFile']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                result["message"] =  'No ha seleccionado un archivo'
                return result
            
            if file and utils.allowed_file(file.filename):
                filename, file_extension = os.path.splitext(file.filename)
                filename = secure_filename(filename)
                unique_filename = str(uuid.uuid4()) + file_extension
                file.save(os.path.join("./static/files", unique_filename))
                size = os.stat(os.path.join("./static/files", unique_filename)).st_size
                privacidad=request.form['Privacidad']
                ##privacidad = 0
                ##if "isPrivate" in request.form:
                   ## privacidad = 1
                    
                self.setNombre(filename)
                self.setPrivacidad(privacidad)
                self.setTamano(size)
                self.setUbicacion(unique_filename)
                self.setUsuario(session.get('id'))
                save = self.guardar()
                if save:
                    result["status"] = 'ok'
                    result["message"] = "Se cargo la imagen con éxito!"
                else:
                    os.remove(os.path.join("./static/files", unique_filename))
                    result["message"] = "No se pudo guardar la información de la imagen"
            else:
                result["message"] = "La extensión del archivo no es permitida"                
        except Exception as e:
            os.remove(os.path.join("./static/files", unique_filename))
            result["message"] = e
                    
        return result
    
    def guardar(self):
        resultado = False
        try:
            db=get_db()
            resultado = db.execute("INSERT INTO imagenes (nombre, tamaño, privacidad, ubicacion, id_usuario) values (?,?,?,?,?)",(self.getNombre() ,self.getTamano(),self.getPrivacidad(),self.getUbicacion(),self.getUsuario()))
            db.commit()               
        except Exception as e:
            resultado = False
            print(e)            
        return resultado
    
    def obtenerImagenGaleria(self):
        db=get_db()
        usuario= request.cookies.get('usuario')
        gallery=db.execute("SELECT * FROM usuario WHERE user = ? ",(usuario, )).fetchone()
        id=gallery[0]
        myuser=db.execute("SELECT id,ubicacion,privacidad,nombre FROM imagenes WHERE id_usuario = ?",(id,)).fetchall()
        return myuser
    
    def obtenerImagenesTodos(self):
        db=get_db()
        user=db.execute("SELECT id,ubicacion,privacidad,nombre FROM imagenes;").fetchall()
        return user
        
    def eliminarImagen(self,id,filename):
        db=get_db()
        borrar=db.execute("DELETE from imagenes where id=?",(id,))
        db.commit()
        if borrar:
            os.remove(os.path.join("./static/files", filename))
        return borrar

    def actualizarImagen(self,nombre,privacidad,id):
        db=get_db()
        actualizar=db.execute("UPDATE imagenes set nombre = ? , privacidad = ?  where id= ?",(nombre,privacidad,id))
        db.commit()
        return actualizar
    
    def buscarImagen(self,nombre):
        db=get_db()
        user=db.execute("SELECT id,ubicacion,privacidad,nombre FROM imagenes WHERE nombre LIKE ? AND privacidad = ?",("%"+nombre+"%","Publica",)).fetchall()
        return user


