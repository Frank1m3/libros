from flask import current_app as app
from app.conexion.Conexion import Conexion
import psycopg2
from psycopg2.extras import RealDictCursor


class InfantilDao:
    CATEGORIA_ID = 2  # ID correspondiente a la categoría Infantil

    def get_todos(self):
        """
        Devuelve una lista de libros infantiles con todos los datos relacionados.
        """
        sql = """
            SELECT 
                l.id, l.titulo, l.descripcion, l.isbn, l.precio, l.stock,l.paginas,
                a.nombre AS autor,
                e.nombre AS editorial,
                i.nombre AS idioma,
                m.ancho, m.alto, m.profundidad,
                ed.numero AS edicion,
                t.numero AS tomo,
                t.descripcion AS descripcion_tomo
            FROM libros l
            LEFT JOIN autores a ON l.autor_id = a.id
            LEFT JOIN editoriales e ON l.editorial_id = e.id
            LEFT JOIN idiomas i ON l.idioma_id = i.id
            LEFT JOIN medidas m ON l.medida_id = m.id
            LEFT JOIN ediciones ed ON l.edicion_id = ed.id
            LEFT JOIN tomos t ON l.tomo_id = t.id
            WHERE l.categoria_id = %s
            ORDER BY l.titulo
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(sql, (self.CATEGORIA_ID,))
            return cur.fetchall()
        except Exception as e:
            app.logger.error(f"[InfantilDao.get_todos] Error: {e}")
            return []
        finally:
            cur.close()
            con.close()

    def get_por_id(self, id_libro):
        """
        Devuelve un libro infantil específico por ID con todos sus datos relacionados.
        """
        sql = """
            SELECT 
                l.id, l.titulo, l.descripcion, l.isbn, l.precio, l.stock,l.paginas,
                a.nombre AS autor,
                e.nombre AS editorial,
                i.nombre AS idioma,
                m.ancho, m.alto, m.profundidad,
                ed.numero AS edicion,
                t.numero AS tomo,
                t.descripcion AS descripcion_tomo
            FROM libros l
            LEFT JOIN autores a ON l.autor_id = a.id
            LEFT JOIN editoriales e ON l.editorial_id = e.id
            LEFT JOIN idiomas i ON l.idioma_id = i.id
            LEFT JOIN medidas m ON l.medida_id = m.id
            LEFT JOIN ediciones ed ON l.edicion_id = ed.id
            LEFT JOIN tomos t ON l.tomo_id = t.id
            WHERE l.id = %s AND l.categoria_id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(sql, (id_libro, self.CATEGORIA_ID))
            return cur.fetchone()
        except Exception as e:
            app.logger.error(f"[InfantilDao.get_por_id] Error: {e}")
            return None
        finally:
            cur.close()
            con.close()

    def obtener_imagen(self, id_libro):
        """
        Devuelve la imagen binaria del libro infantil.
        """
        sql = "SELECT id, imagen FROM libros WHERE id = %s AND categoria_id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_libro, self.CATEGORIA_ID))
            return cur.fetchone()
        except Exception as e:
            app.logger.error(f"[InfantilDao.obtener_imagen] Error: {e}")
            return None
        finally:
            cur.close()
            con.close()
    def buscar_por_titulo(self, texto):
       
        sql = """
            SELECT 
                l.id, l.titulo, a.nombre AS autor
            FROM libros l
            LEFT JOIN autores a ON l.autor_id = a.id
            WHERE l.categoria_id = %s AND LOWER(l.titulo) LIKE %s
            ORDER BY l.titulo
            LIMIT 10
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(sql, (self.CATEGORIA_ID, f"%{texto.lower()}%"))
            return cur.fetchall()
        except Exception as e:
            app.logger.error(f"[InfantilDao.buscar_por_titulo] Error: {e}")
            return []
        finally:
            cur.close()
            con.close()
