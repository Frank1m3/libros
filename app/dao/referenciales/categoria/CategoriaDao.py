from flask import current_app as app
from app.conexion.Conexion import Conexion

class CategoriaDao:

    def getCategorias(self):
        sql = "SELECT id, nombre FROM categorias"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            categorias = cur.fetchall()
            return [{'id': c[0], 'nombre': c[1]} for c in categorias]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las categorías: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getCategoriaById(self, id):
        sql = "SELECT id, nombre FROM categorias WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            categoria = cur.fetchone()
            if categoria:
                return {'id': categoria[0], 'nombre': categoria[1]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener categoría por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarCategoria(self, nombre):
        sql = "INSERT INTO categorias(nombre) VALUES (%s) RETURNING id"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (nombre,))
            categoria_id = cur.fetchone()[0]
            con.commit()
            return categoria_id
        except Exception as e:
            app.logger.error(f"Error al insertar categoría: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def updateCategoria(self, id, nombre):
        sql = "UPDATE categorias SET nombre = %s WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (nombre, id))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar categoría: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteCategoria(self, id):
        sql = "DELETE FROM categorias WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar categoría: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
