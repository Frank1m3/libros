from flask import current_app as app
from app.conexion.Conexion import Conexion
import psycopg2
from psycopg2.extras import RealDictCursor



class RegistrarDao:
    def __init__(self):
        self.conn = Conexion().getConexion()


    def insertar_libro(self, titulo, autor_id, descripcion, isbn, precio, stock,
                       paginas, categoria_id, editorial_id, idioma_id,
                       medida_id, edicion_id, tomo_id, imagen):
        with self.conn.cursor() as cur:
            query = """
                INSERT INTO libros (
                    titulo, autor_id, descripcion, isbn, precio, stock,
                    paginas, categoria_id, editorial_id, idioma_id,
                    medida_id, edicion_id, tomo_id, imagen
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (
                titulo, autor_id, descripcion, isbn, precio, stock,
                paginas, categoria_id, editorial_id, idioma_id,
                medida_id, edicion_id, tomo_id, psycopg2.Binary(imagen) if imagen else None
            ))
            self.conn.commit()

    def get_todos(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, titulo, descripcion, isbn, precio, stock, paginas
                FROM libros ORDER BY id DESC
            """)
            columnas = [desc[0] for desc in cur.description]
            return [dict(zip(columnas, fila)) for fila in cur.fetchall()]

    def obtener_libro_por_id(self, libro_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, titulo, descripcion, isbn, precio, stock, paginas
                FROM libros WHERE id = %s
            """, (libro_id,))
            fila = cur.fetchone()
            if fila:
                columnas = [desc[0] for desc in cur.description]
                return dict(zip(columnas, fila))
            return None

    def obtener_imagen(self, libro_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT imagen FROM libros WHERE id = %s", (libro_id,))
            fila = cur.fetchone()
            return fila[0] if fila and fila[0] else None

    def get_autores(self):
        return self._listar_referencial("autores")

    def get_categorias(self):
        return self._listar_referencial("categorias")

    def get_editoriales(self):
        return self._listar_referencial("editoriales")

    def get_idiomas(self):
        return self._listar_referencial("idiomas")

    def get_medidas(self):
        return self._listar_referencial("medidas")

    def get_ediciones(self):
        return self._listar_referencial("ediciones")

    def get_tomos(self):
        return self._listar_referencial("tomos")

    def _listar_referencial(self, tabla):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {tabla} ORDER BY id")
            columnas = [desc[0] for desc in cur.description]
            return [dict(zip(columnas, fila)) for fila in cur.fetchall()]

