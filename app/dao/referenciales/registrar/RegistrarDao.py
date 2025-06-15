from flask import current_app as app
from app.conexion.Conexion import Conexion
import psycopg2
from psycopg2.extras import RealDictCursor

class RegistrarDao:

    def insertar_libro(self, titulo, descripcion, isbn, precio, stock, imagen_bytes,
                      categoria_id, autor_id, editorial_id, idioma_id,
                      medida_id, edicion_id, tomo_id, paginas):
        sql = """
            INSERT INTO libros (titulo, descripcion, isbn, precio, stock, imagen,
                                categoria_id, autor_id, editorial_id, idioma_id,
                                medida_id, edicion_id, tomo_id, paginas)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (titulo, descripcion, isbn, precio, stock, imagen_bytes,
                              categoria_id, autor_id, editorial_id, idioma_id,
                              medida_id, edicion_id, tomo_id, paginas))
            nuevo_id = cur.fetchone()[0]
            con.commit()
            return nuevo_id
        except Exception as e:
            app.logger.error(f"[RegistrarDao.insertar_libro] Error: {e}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def actualizar_libro_completo(self, libro_id, titulo, descripcion, isbn, precio, stock, paginas,
                                  imagen_bytes, categoria_id, autor_id, editorial_id,
                                  idioma_id, medida_id, edicion_id, tomo_id):
        if imagen_bytes:
            sql = """
                UPDATE libros SET
                    titulo = %s,
                    descripcion = %s,
                    isbn = %s,
                    precio = %s,
                    stock = %s,
                    paginas = %s,
                    imagen = %s,
                    categoria_id = %s,
                    autor_id = %s,
                    editorial_id = %s,
                    idioma_id = %s,
                    medida_id = %s,
                    edicion_id = %s,
                    tomo_id = %s
                WHERE id = %s
            """
            params = (titulo, descripcion, isbn, precio, stock, paginas,
                      imagen_bytes, categoria_id, autor_id, editorial_id,
                      idioma_id, medida_id, edicion_id, tomo_id, libro_id)
        else:
            sql = """
                UPDATE libros SET
                    titulo = %s,
                    descripcion = %s,
                    isbn = %s,
                    precio = %s,
                    stock = %s,
                    paginas = %s,
                    categoria_id = %s,
                    autor_id = %s,
                    editorial_id = %s,
                    idioma_id = %s,
                    medida_id = %s,
                    edicion_id = %s,
                    tomo_id = %s
                WHERE id = %s
            """
            params = (titulo, descripcion, isbn, precio, stock, paginas,
                      categoria_id, autor_id, editorial_id,
                      idioma_id, medida_id, edicion_id, tomo_id, libro_id)

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, params)
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"[RegistrarDao.actualizar_libro_completo] Error: {e}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def obtener_libro_por_id(self, libro_id):
        sql = """
            SELECT 
                l.id, l.titulo, l.descripcion, l.isbn, l.precio, l.stock, l.paginas, l.imagen,
                a.nombre AS autor,
                e.nombre AS editorial,
                i.nombre AS idioma,
                m.ancho, m.alto, m.profundidad,
                ed.numero AS edicion,
                t.numero AS tomo,
                t.descripcion AS descripcion_tomo,
                l.categoria_id, l.autor_id, l.editorial_id, l.idioma_id,
                l.medida_id, l.edicion_id, l.tomo_id
            FROM libros l
            LEFT JOIN autores a ON l.autor_id = a.id
            LEFT JOIN editoriales e ON l.editorial_id = e.id
            LEFT JOIN idiomas i ON l.idioma_id = i.id
            LEFT JOIN medidas m ON l.medida_id = m.id
            LEFT JOIN ediciones ed ON l.edicion_id = ed.id
            LEFT JOIN tomos t ON l.tomo_id = t.id
            WHERE l.id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(sql, (libro_id,))
            return cur.fetchone()
        except Exception as e:
            app.logger.error(f"[RegistrarDao.obtener_libro_por_id] Error: {e}")
            return None
        finally:
            cur.close()
            con.close()

    def obtener_imagen(self, libro_id):
        sql = "SELECT imagen FROM libros WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (libro_id,))
            row = cur.fetchone()
            if row:
                return row[0]
            return None
        except Exception as e:
            app.logger.error(f"[RegistrarDao.obtener_imagen] Error: {e}")
            return None
        finally:
            cur.close()
            con.close()

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
            ORDER BY l.titulo
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            app.logger.error(f"[RegistrarDao.get_todos] Error: {e}")
            return []
        finally:
            cur.close()
            con.close()

    # Métodos para listas referenciales
    def get_categorias(self):
        sql = "SELECT id, nombre FROM categorias ORDER BY nombre"
        return self._get_lista_referencial(sql, 'get_categorias')

    def get_autores(self):
        sql = "SELECT id, nombre FROM autores ORDER BY nombre"
        return self._get_lista_referencial(sql, 'get_autores')

    def get_editoriales(self):
        sql = "SELECT id, nombre FROM editoriales ORDER BY nombre"
        return self._get_lista_referencial(sql, 'get_editoriales')

    def get_idiomas(self):
        sql = "SELECT id, nombre FROM idiomas ORDER BY nombre"
        return self._get_lista_referencial(sql, 'get_idiomas')

    def get_medidas(self):
        sql = "SELECT id, ancho, alto, profundidad FROM medidas ORDER BY id"
        # Para medidas, devolver dicc con esas columnas
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            app.logger.error(f"[RegistrarDao.get_medidas] Error: {e}")
            return []
        finally:
            cur.close()
            con.close()

    def get_ediciones(self):
        sql = "SELECT id, numero FROM ediciones ORDER BY numero"
        return self._get_lista_referencial(sql, 'get_ediciones')

    def get_tomos(self):
        sql = "SELECT id, numero, descripcion FROM tomos ORDER BY numero"
        return self._get_lista_referencial(sql, 'get_tomos')

    # Método privado para evitar repetir código en consultas simples
    def _get_lista_referencial(self, sql, metodo_nombre):
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            filas = cur.fetchall()
            # Convertir a lista de dicts con columnas id y nombre (cuando aplica)
            if cur.description and len(cur.description) == 2:
                resultado = [{'id': row[0], 'nombre': row[1]} for row in filas]
            else:
                # Si no hay solo dos columnas (como en medidas o tomos), devolver filas sin procesar
                resultado = [dict(zip([desc[0] for desc in cur.description], row)) for row in filas]
            return resultado
        except Exception as e:
            app.logger.error(f"[RegistrarDao.{metodo_nombre}] Error: {e}")
            return []
        finally:
            cur.close()
            con.close()
