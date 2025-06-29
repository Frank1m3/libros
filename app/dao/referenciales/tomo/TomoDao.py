from flask import current_app as app
from app.conexion.Conexion import Conexion

class TomoDao:

    def getTomos(self):
        sql = "SELECT id, numero, descripcion FROM tomos"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            return [{'id': t[0], 'numero': t[1], 'descripcion': t[2]} for t in cur.fetchall()]
        except Exception as e:
            app.logger.error(f"Error al obtener tomos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getTomoById(self, id):
        sql = "SELECT id, numero, descripcion FROM tomos WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            t = cur.fetchone()
            return {'id': t[0], 'numero': t[1], 'descripcion': t[2]} if t else None
        except Exception as e:
            app.logger.error(f"Error al obtener tomo por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarTomo(self, numero, descripcion):
        sql = "INSERT INTO tomos(numero, descripcion) VALUES (%s, %s) RETURNING id"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (numero, descripcion))
            nuevo_id = cur.fetchone()[0]
            con.commit()
            return nuevo_id
        except Exception as e:
            app.logger.error(f"Error al insertar tomo: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def updateTomo(self, id, numero, descripcion):
        sql = "UPDATE tomos SET numero = %s, descripcion = %s WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (numero, descripcion, id))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar tomo: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteTomo(self, id):
        sql = "DELETE FROM tomos WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar tomo: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
