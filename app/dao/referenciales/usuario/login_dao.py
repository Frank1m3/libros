# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion
from werkzeug.security import generate_password_hash


class LoginDao:

    def buscarUsuario(self, usu_nick: str):
        buscar_usuario_sql = """
        SELECT
            u.usu_id,
            TRIM(u.usu_nick),
            u.usu_clave,
            u.usu_nro_intentos,
            u.fun_id,
            u.gru_id,
            u.usu_estado,
            CONCAT(COALESCE(p.nombres, ''), ' ', COALESCE(p.apellidos, '')) AS nombre_persona,
            g.gru_des,
            u.usu_email
        FROM
            usuarios u
        LEFT JOIN
            personas p ON p.id_persona = u.fun_id
        LEFT JOIN
            grupos g ON g.gru_id = u.gru_id
        WHERE
            u.usu_nick = %s AND u.usu_estado IS TRUE
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(buscar_usuario_sql, (usu_nick,))
            usuario_encontrado = cur.fetchone()
            if usuario_encontrado:
                return {
                    "usu_id": usuario_encontrado[0],
                    "usu_nick": usuario_encontrado[1],
                    "usu_clave": usuario_encontrado[2],
                    "usu_nro_intentos": usuario_encontrado[3],
                    "fun_id": usuario_encontrado[4],
                    "gru_id": usuario_encontrado[5],
                    "usu_estado": usuario_encontrado[6],
                    "nombre_persona": usuario_encontrado[7].strip(),
                    "grupo": usuario_encontrado[8],
                    "usu_email": usuario_encontrado[9]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener usuario: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def crearUsuario(self, usu_nick, usu_clave, usu_email, gru_id, fun_id=None):
        """
        Crea un nuevo usuario. Si es un cliente, fun_id puede ser None.
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            hash_clave = generate_password_hash(usu_clave)

            if fun_id:
                crear_usuario_sql = """
                    INSERT INTO usuarios (
                        usu_nick, usu_clave, usu_nro_intentos,
                        fun_id, gru_id, usu_estado, usu_email
                    ) VALUES (%s, %s, 0, %s, %s, TRUE, %s)
                    RETURNING usu_id
                """
                cur.execute(crear_usuario_sql, (usu_nick, hash_clave, fun_id, gru_id, usu_email))
            else:
                crear_usuario_sql = """
                    INSERT INTO usuarios (
                        usu_nick, usu_clave, usu_nro_intentos,
                        gru_id, usu_estado, usu_email
                    ) VALUES (%s, %s, 0, %s, TRUE, %s)
                    RETURNING usu_id
                """
                cur.execute(crear_usuario_sql, (usu_nick, hash_clave, gru_id, usu_email))

            usu_id = cur.fetchone()[0]
            con.commit()
            return usu_id
        except Exception as e:
            app.logger.error(f"Error al registrar nuevo usuario: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def existeNick(self, usu_nick):
        sql = "SELECT 1 FROM usuarios WHERE usu_nick = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (usu_nick,))
            return cur.fetchone() is not None
        except Exception as e:
            app.logger.error(f"Error al verificar nick existente: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
