from flask import Blueprint, render_template, Response, url_for, abort, jsonify, request, current_app as app
from app.conexion.Conexion import Conexion
import psycopg2
from psycopg2.extras import RealDictCursor

# Definición del blueprint
infantilapi = Blueprint('infantilapi', __name__, template_folder='templates')

class InfantilDao:
    CATEGORIA_ID = 2  # ID correspondiente a la categoría Infantil

    def get_todos(self):
        sql = """
            SELECT 
                l.id, l.titulo, l.descripcion, l.isbn, l.precio, l.stock, l.paginas,
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
        sql = """
            SELECT 
                l.id, l.titulo, l.descripcion, l.isbn, l.precio, l.stock, l.paginas,
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

# Ruta para búsqueda AJAX dentro del blueprint
@infantilapi.route('/infantil/buscar-libros')
def buscar_libros():
    query = request.args.get('q', '').strip()
    dao = InfantilDao()
    resultados = []

    if query:
        libros = dao.buscar_por_titulo(query)
        for libro in libros:
            resultados.append({
                'id': libro['id'],
                'titulo': libro['titulo'],
                'autor': libro.get('autor', 'Desconocido')
            })

    return jsonify(resultados)
