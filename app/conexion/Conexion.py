import psycopg2
import psycopg2.extensions
import psycopg2.extras

class Conexion:
    """Metodo constructor"""
    def __init__(self):
        dbname = "veterinaria_bd"
        user = "postgres"
        password = "postgres"
        host = "127.0.0.1"
        port = 5432

        # Configura la conexión
        self.con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        # Asegura el uso correcto del tipo BYTEA
        psycopg2.extensions.register_adapter(bytes, psycopg2.Binary)

    """getConexion

        Retorna la instancia de la base de datos
    """
    def getConexion(self):
        return self.con
