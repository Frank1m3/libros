from flask import current_app as app
from app.conexion.Conexion import Conexion

class ContactoDao:

    def insertar(self, nombre, apellido, correo, telefono, mensaje):
        """
        Inserta un nuevo registro de cliente en la base de datos.
        """
        sql = """
            INSERT INTO cliente (nombre, apellido, gmail, telefono, mensaje)
            VALUES (%s, %s, %s, %s, %s)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        try:
            with con.cursor() as cur:
                cur.execute(sql, (nombre, apellido, correo, telefono, mensaje))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"[ContactoDao.insertar] Error: {e}")
            return False
        finally:
            con.close()
