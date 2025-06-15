from flask import current_app as app
from app.conexion.Conexion import Conexion

class NovedadDao:
    def getTodos(self):
        sql = """
            SELECT id_libro, titulo, descripcion, precio, imagen
            FROM libros_novedad
            ORDER BY id_libro DESC
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(sql)
            resultados = cur.fetchall()
            libros = []

            for l in resultados:
                libros.append({
                    "id": l[0],
                    "titulo": l[1],
                    "descripcion": l[2],
                    "precio": float(l[3]),
                    "imagen": l[4]
                })

            return libros

        except Exception as e:
            app.logger.error(f"Error al obtener libros de novedad: {e}")
            return []

        finally:
            cur.close()
            con.close()

    def getPorId(self, id_libro):
        sql = """
            SELECT id_libro, titulo, descripcion, precio, imagen
            FROM libros_novedad
            WHERE id_libro = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(sql, (id_libro,))
            l = cur.fetchone()

            if l:
                return {
                    "id": l[0],
                    "titulo": l[1],
                    "descripcion": l[2],
                    "precio": float(l[3]),
                    "imagen": l[4]
                }
            return None

        except Exception as e:
            app.logger.error(f"Error al obtener libro por ID: {e}")
            return None

        finally:
            cur.close()
            con.close()

    def insertarLibro(self, titulo, descripcion, precio, imagen):
        sql = """
            INSERT INTO libros_novedad (titulo, descripcion, precio, imagen)
            VALUES (%s, %s, %s, %s)
            RETURNING id_libro
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(sql, (titulo, descripcion, precio, imagen))
            id_libro = cur.fetchone()[0]
            con.commit()
            return id_libro

        except Exception as e:
            app.logger.error(f"Error al insertar libro: {e}")
            con.rollback()
            return None

        finally:
            cur.close()
            con.close()

    def actualizarLibro(self, id_libro, titulo, descripcion, precio, imagen):
        sql = """
            UPDATE libros_novedad
            SET titulo = %s, descripcion = %s, precio = %s, imagen = %s
            WHERE id_libro = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(sql, (titulo, descripcion, precio, imagen, id_libro))
            con.commit()
            return cur.rowcount > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar libro: {e}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def eliminarLibro(self, id_libro):
        sql = """
            DELETE FROM libros_novedad
            WHERE id_libro = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(sql, (id_libro,))
            con.commit()
            return cur.rowcount > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar libro: {e}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
