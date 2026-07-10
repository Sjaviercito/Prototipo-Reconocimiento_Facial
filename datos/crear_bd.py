import sqlite3
import os
from config import BD_PATH, BD_DIR

os.makedirs(BD_DIR, exist_ok=True)

conexion = sqlite3.connect(BD_PATH)
cursor = conexion.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.executescript("""
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT NOT NULL,
    rol_usuario TEXT NOT NULL,
    username_usuario TEXT NOT NULL,
    correo_usuario TEXT NOT NULL,
    pin_hash_usuario TEXT,
    contrasena_usuario TEXT NOT NULL,
    rostro_embedding_usuario BLOB
);
CREATE TABLE IF NOT EXISTS autorizador (
    id_autorizador INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_autorizador TEXT NOT NULL,
    puesto_autorizador TEXT NOT NULL,
    departamento_autorizador TEXT NOT NULL,
    correo_autorizador TEXT NOT NULL,
    telefono_autorizador TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS persona (
    id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_persona TEXT NOT NULL,
    departamento_proveedor_persona TEXT NOT NULL,
    tipo_persona TEXT NOT NULL,
    id_autorizador INTEGER,
    rostro_embedding_persona BLOB NOT NULL,
    correo_persona TEXT NOT NULL,
    firma_persona TEXT NOT NULL,
    ine_persona TEXT NOT NULL,
    telefono_persona TEXT NOT NULL,
    FOREIGN KEY (id_autorizador) REFERENCES autorizador(id_autorizador)

);
CREATE TABLE IF NOT EXISTS auditoria (
    id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    fecha_auditoria TEXT NOT NULL,
    accion_auditoria TEXT NOT NULL,
    tabla_afectada_auditoria TEXT NOT NULL,
    id_registro_afectado_auditoria INTEGER NOT NULL,
    hora_auditoria TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
CREATE TABLE IF NOT EXISTS visita (
    id_visita INTEGER PRIMARY KEY AUTOINCREMENT,
    id_persona INTEGER NOT NULL,
    id_usuario_entrada INTEGER NOT NULL,
    id_usuario_salida INTEGER,
    id_autorizador INTEGER,
    fecha_visita TEXT NOT NULL,
    hora_entrada_visita TEXT NOT NULL,
    hora_salida_visita TEXT,
    fotografia_entrada_visita BLOB NOT NULL,
    fotografia_salida_visita BLOB,
    tipo_entrada_visita TEXT NOT NULL,
    autorizador_nombre_copiado TEXT NOT NULL,
    FOREIGN KEY (id_usuario_entrada) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_usuario_salida) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_autorizador) REFERENCES autorizador(id_autorizador),
    FOREIGN KEY (id_persona) REFERENCES persona(id_persona)
);
CREATE TABLE IF NOT EXISTS reglamento(
    id_reglamento INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_subida_reglamento TEXT NOT NULL,
    ruta_pdf_reglamento TEXT NOT NULL,
    nombre_version_reglamento TEXT NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
CREATE TABLE IF NOT EXISTS firma(
    id_firma INTEGER PRIMARY KEY AUTOINCREMENT,
    id_persona INTEGER NOT NULL,
    id_reglamento INTEGER NOT NULL,
    fecha_firma TEXT NOT NULL,
    hora_firma TEXT NOT NULL,
    tipo_firma TEXT NOT NULL,
    ruta_firma TEXT,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_persona) REFERENCES persona(id_persona),
    FOREIGN KEY (id_reglamento) REFERENCES reglamento(id_reglamento)
);
CREATE TABLE IF NOT EXISTS correo_pendiente(
    id_correo_pendiente INTEGER PRIMARY KEY AUTOINCREMENT,
    id_persona INTEGER NOT NULL,
    id_reglamento INTEGER NOT NULL,
    fecha_fallo_correo_pendiente TEXT NOT NULL,
    hora_fallo_correo_pendiente TEXT NOT NULL,
    error_correo_pendiente TEXT NOT NULL,
    intentos_correo_pendiente INTEGER NOT NULL,
    FOREIGN KEY (id_persona) REFERENCES persona(id_persona),
    FOREIGN KEY (id_reglamento) REFERENCES reglamento(id_reglamento)  

);
    """)










conexion.commit()
conexion.close()

print("Base de datos creada correctamente.")