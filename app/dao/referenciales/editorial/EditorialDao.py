from flask import current_app as app
from app.conexion.Conexion import Conexion

class EditorialDao:

    def getEditoriales(self):
        sql = "SELECT id, nombre FROM editoriales"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            data = cur.fetchall()
            return [{'id': row[0], 'nombre': row[1]} for row in data]
        except Exception as e:
            app.logger.error(f"Error al obtener editoriales: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getEditorialById(self, id):
        sql = "SELECT id, nombre FROM editoriales WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            row = cur.fetchone()
            return {'id': row[0], 'nombre': row[1]} if row else None
        except Exception as e:
            app.logger.error(f"Error al obtener editorial: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarEditorial(self, nombre):
        sql = "INSERT INTO editoriales(nombre) VALUES (%s) RETURNING id"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (nombre,))
            editorial_id = cur.fetchone()[0]
            con.commit()
            return editorial_id
        except Exception as e:
            app.logger.error(f"Error al insertar editorial: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def updateEditorial(self, id, nombre):
        sql = "UPDATE editoriales SET nombre = %s WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (nombre, id))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar editorial: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteEditorial(self, id):
        sql = "DELETE FROM editoriales WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar editorial: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
