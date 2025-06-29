from flask import current_app as app
from app.conexion.Conexion import Conexion

class AutorDao:

    def getAutores(self):
        sql = "SELECT id, nombre FROM autores"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            autores = cur.fetchall()
            return [{'id': autor[0], 'nombre': autor[1]} for autor in autores]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los autores: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getAutorById(self, id):
        sql = "SELECT id, nombre FROM autores WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            autor = cur.fetchone()
            if autor:
                return {'id': autor[0], 'nombre': autor[1]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener autor por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarAutor(self, nombre):
        sql = "INSERT INTO autores(nombre) VALUES (%s) RETURNING id"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (nombre,))
            autor_id = cur.fetchone()[0]
            con.commit()
            return autor_id
        except Exception as e:
            app.logger.error(f"Error al insertar autor: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def updateAutor(self, id, nombre):
        sql = "UPDATE autores SET nombre = %s WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (nombre, id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar autor: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteAutor(self, id):
        sql = "DELETE FROM autores WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar autor: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
