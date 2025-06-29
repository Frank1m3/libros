from flask import current_app as app
from app.conexion.Conexion import Conexion

class MedidaDao:

    def getMedidas(self):
        sql = "SELECT id, alto, ancho, profundidad FROM medidas"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            medidas = cur.fetchall()
            # Retornamos una lista de diccionarios con los datos de cada medida
            return [
                {
                    'id': medida[0],
                    'alto': float(medida[1]) if medida[1] is not None else None,
                    'ancho': float(medida[2]) if medida[2] is not None else None,
                    'profundidad': float(medida[3]) if medida[3] is not None else None,
                }
                for medida in medidas
            ]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las medidas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getMedidaById(self, id):
        sql = "SELECT id, alto, ancho, profundidad FROM medidas WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            medida = cur.fetchone()
            if medida:
                return {
                    'id': medida[0],
                    'alto': float(medida[1]) if medida[1] is not None else None,
                    'ancho': float(medida[2]) if medida[2] is not None else None,
                    'profundidad': float(medida[3]) if medida[3] is not None else None,
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener medida por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarMedida(self, alto, ancho, profundidad):
        sql = "INSERT INTO medidas(alto, ancho, profundidad) VALUES (%s, %s, %s) RETURNING id"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (alto, ancho, profundidad))
            medida_id = cur.fetchone()[0]
            con.commit()
            return medida_id
        except Exception as e:
            app.logger.error(f"Error al insertar medida: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def updateMedida(self, id, alto, ancho, profundidad):
        sql = "UPDATE medidas SET alto = %s, ancho = %s, profundidad = %s WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (alto, ancho, profundidad, id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar medida: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteMedida(self, id):
        sql = "DELETE FROM medidas WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar medida: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
