from flask import current_app as app
from app.conexion.Conexion import Conexion

class IdiomaDao:

    def getIdiomas(self):
        sql = "SELECT id, nombre FROM idiomas"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            idiomas = cur.fetchall()
            return [{'id': idioma[0], 'nombre': idioma[1]} for idioma in idiomas]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los idiomas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getIdiomaById(self, id):
        sql = "SELECT id, nombre FROM idiomas WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            idioma = cur.fetchone()
            if idioma:
                return {'id': idioma[0], 'nombre': idioma[1]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener idioma por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarIdioma(self, nombre):
        sql = "INSERT INTO idiomas(nombre) VALUES (%s) RETURNING id"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (nombre,))
            idioma_id = cur.fetchone()[0]
            con.commit()
            return idioma_id
        except Exception as e:
            app.logger.error(f"Error al insertar idioma: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def updateIdioma(self, id, nombre):
        sql = "UPDATE idiomas SET nombre = %s WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (nombre, id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar idioma: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteIdioma(self, id):
        sql = "DELETE FROM idiomas WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar idioma: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
