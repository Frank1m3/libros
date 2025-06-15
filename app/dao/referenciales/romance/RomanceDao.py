from flask import current_app as app
from app.conexion.Conexion import Conexion

class RomanceDao:
    def get_por_id(self, id_libro):
        sql = """
            SELECT id_libro, titulo, descripcion, precio, imagen, autor
            FROM libros_romance
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
                    "imagen": l[4],
                    "autor": l[5]
                }
            return None
        except Exception as e:
            print(f"Error al obtener libro romance por ID: {e}")
            return None
        finally:
            cur.close()
            con.close()

    def getTodos(self):
        sql = """
            SELECT id_libro, titulo, descripcion, precio, imagen, autor
            FROM libros_romance
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            libros = []
            for l in rows:
                libros.append({
                    "id": l[0],
                    "titulo": l[1],
                    "descripcion": l[2],
                    "precio": float(l[3]),
                    "imagen": l[4],
                    "autor": l[5]
                })
            return libros
        except Exception as e:
            print(f"Error al obtener todos los libros romance: {e}")
            return []
        finally:
            cur.close()
            con.close()
