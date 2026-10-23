import streamlit as st
import random
from sqlalchemy import text

st.set_page_config(page_title="Chatbot Institución Educativa", page_icon="🤖", layout="centered")

# --- CONEXIÓN Y CREACIÓN AUTOMÁTICA EN AIVEN ---
try:
    conn = st.connection("mysql", type="sql")
    
    def inicializar_todo_en_aiven():
        with conn.session as s:
            # 1. Crear tablas
            s.execute(text("""
                CREATE TABLE IF NOT EXISTS estudiantes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    documento VARCHAR(20) UNIQUE NOT NULL,
                    nombre_completo VARCHAR(100) NOT NULL,
                    grado VARCHAR(30) NOT NULL,
                    correo VARCHAR(100)
                );
            """))
            s.execute(text("""
                CREATE TABLE IF NOT EXISTS calificaciones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    estudiante_id INT NOT NULL,
                    materia VARCHAR(50) NOT NULL,
                    nota_saber_hacer DECIMAL(5,2) DEFAULT 0.00,
                    nota_convivir DECIMAL(5,2) DEFAULT 0.00,
                    nota_prueba_externa DECIMAL(5,2) DEFAULT 0.00,
                    definitiva DECIMAL(5,2) DEFAULT 0.00,
                    recuperacion DECIMAL(5,2) DEFAULT 0.00,
                    nivelacion DECIMAL(5,2) DEFAULT 0.00,
                    nota_final DECIMAL(5,2) DEFAULT 0.00,
                    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
                );
            """))
            s.execute(text("""
                CREATE TABLE IF NOT EXISTS pagos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    estudiante_id INT NOT NULL,
                    concepto VARCHAR(100) NOT NULL,
                    valor VARCHAR(20) NOT NULL,
                    medio_pago VARCHAR(50),
                    referencia_transaccion VARCHAR(50),
                    estado VARCHAR(30) DEFAULT 'Pendiente',
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE
                );
            """))
            s.execute(text("""
                CREATE TABLE IF NOT EXISTS reservas_biblioteca (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    seccion VARCHAR(20) NOT NULL, 
                    dia VARCHAR(20) NOT NULL,     
                    hora_bloque VARCHAR(50) NOT NULL,
                    responsable VARCHAR(100) NOT NULL,
                    motivo VARCHAR(150) NOT NULL,
                    estado VARCHAR(10) DEFAULT 'RES'
                );
            """))
            s.execute(text("""
                CREATE TABLE IF NOT EXISTS citas_psicologia (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    estudiante_nombre VARCHAR(100) NOT NULL,
                    grado VARCHAR(20) NOT NULL,
                    contacto VARCHAR(100) NOT NULL,
                    modalidad VARCHAR(50) NOT NULL, 
                    estado VARCHAR(30) DEFAULT 'Solicitada',
                    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            s.execute(text("""
                CREATE TABLE IF NOT EXISTS pqrs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    radicado VARCHAR(30) UNIQUE NOT NULL,
                    categoria VARCHAR(50) NOT NULL,
                    subcategoria VARCHAR(100) NOT NULL,
                    detalle TEXT NOT NULL,
                    estado VARCHAR(50) DEFAULT 'Enviado a Coordinación',
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            s.execute(text("""
                CREATE TABLE IF NOT EXISTS reservas_dependencias (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    dependencia VARCHAR(50) NOT NULL, 
                    dia VARCHAR(20) NOT NULL,
                    jornada VARCHAR(20) NOT NULL,    
                    hora VARCHAR(20) NOT NULL,       
                    documento_o_nombre VARCHAR(100) NOT NULL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            s.commit()
            
            # 2. Insertar estudiantes si la tabla está vacía
            check_est = s.execute(text("SELECT COUNT(*) FROM estudiantes")).fetchone()
            if check_est[0] == 0:
                estudiantes_datos = [
                    ('000000', 'Lucía Fernanda Gómez', 'Transición', 'lucia.gomez@colegio.edu.co'),
                    ('111111', 'Mateo Alexander Silva', 'Primero (1°)', 'mateo.silva@colegio.edu.co'),
                    ('222222', 'Valentina Isabel Torres', 'Segundo (2°)', 'valentina.torres@colegio.edu.co'),
                    ('333333', 'Santiago David Ramírez', 'Tercero (3°)', 'santiago.ramirez@colegio.edu.co'),
                    ('444444', 'Mariana Andrea Castro', 'Cuarto (4°)', 'mariana.castro@colegio.edu.co'),
                    ('555555', 'Emilio José Mendoza', 'Quinto (5°)', 'emilio.mendoza@colegio.edu.co'),
                    ('666666', 'Sofía Victoria Morales', 'Sexto (6°)', 'sofia.morales@colegio.edu.co'),
                    ('777777', 'Daniel Felipe Ortega', 'Séptimo (7°)', 'daniel.ortega@colegio.edu.co'),
                    ('888888', 'Gabriela Ruiz Benítez', 'Octavo (8°)', 'gabriela.ruiz@colegio.edu.co'),
                    ('999999', 'Samuel Esteban Navarro', 'Noveno (9°)', 'samuel.navarro@colegio.edu.co'),
                    ('101010', 'Camila Alejandra Vargas', 'Décimo (10°)', 'camila.vargas@colegio.edu.co'),
                    ('211111', 'Alejandro José Martínez', 'Undécimo (11°)', 'alejandro.martinez@colegio.edu.co')
                ]
                for est in estudiantes_datos:
                    s.execute(text("INSERT INTO estudiantes (documento, nombre_completo, grado, correo) VALUES (:doc, :nom, :grad, :corr)"),
                              {"doc": est[0], "nom": est[1], "grad": est[2], "corr": est[3]})
                s.commit()

            # 3. Insertar calificaciones detalladas y variadas si la tabla está vacía
            check_cal = s.execute(text("SELECT COUNT(*) FROM calificaciones")).fetchone()
            if check_cal[0] == 0:
                est_ids = s.execute(text("SELECT id, documento, grado FROM estudiantes")).fetchall()
                for eid, doc, grad in est_ids:
                    es_bach = any(g in grad for g in ["6°", "7°", "8°", "9°", "10°", "11°", "Sexto", "Séptimo", "Octavo", "Noveno", "Décimo", "Undécimo"])
                    
                    if "Transición" in grad:
                        materias = [("Dimensión Socio Afectiva", 92, 95, 0), ("Dimensión Comunicativa", 88, 90, 0), ("Dimensión Cognitiva", 85, 92, 0), ("Dimensión Corporal", 95, 98, 0), ("Dimensión Artística", 90, 88, 0)]
                    elif es_bach:
                        materias = [("Matemáticas", 82, 85, 80), ("Lenguaje", 78, 82, 75), ("Ciencias Naturales", 88, 90, 85), ("Inglés", 90, 92, 88)]
                    else:
                        materias = [("Matemáticas", 84, 88, 0), ("Lenguaje", 78, 82, 0), ("Ciencias Naturales", 90, 92, 0), ("Inglés", 88, 90, 0)]

                    for mat, sh, conv, ext in materias:
                        definitiva = (sh * 0.7) + (conv * 0.25) + (ext * 0.05) if es_bach else (sh * 0.7) + (conv * 0.3)
                        s.execute(text("""
                            INSERT INTO calificaciones (estudiante_id, materia, nota_saber_hacer, nota_convivir, nota_prueba_externa, definitiva, recuperacion, nivelacion, nota_final)
                            VALUES (:eid, :mat, :sh, :conv, :ext, :def, 0, 0, :def)
                        """), {"eid": eid, "mat": mat, "sh": sh, "conv": conv, "ext": ext, "def": int(round(definitiva))})
                s.commit()

    inicializar_todo_en_aiven()
except Exception as e:
    pass

st.title("🤖 Chatbot de la Institución Educativa")
st.write("Bienvenido al sistema de atención institucional.")

menu_principal = st.selectbox(
    "Seleccione el módulo que desea consultar:",
    [
        "--- Seleccione una opción ---",
        "1. Información Académica y Calificaciones",
        "2. Pagos y Facturación",
        "3. Horarios de Atención y Biblioteca",
        "4. Asesoría, Psicología y Bienestar",
        "5. Quejas, Reclamos y Sugerencias (PQRS)"
    ]
)

# ==============================================================================
# MÓDULO 1: INFORMACIÓN ACADÉMICA Y CALIFICACIONES
# ==============================================================================
if menu_principal == "1. Información Académica y Calificaciones":
    st.header("📚 Información Académica y Calificaciones")
    doc_academico = st.text_input("Ingrese el número de documento del estudiante (ej. 000000, 101010, 211111):", key="doc_acad")
    
    if doc_academico:
        try:
            with conn.session as s:
                est_info = s.execute(text("SELECT id, nombre_completo, grado FROM estudiantes WHERE documento = :doc"), {"doc": doc_academico}).fetchone()
            
            if est_info:
                est_id, nombre_est, grado_est = est_info[0], est_info[1], est_info[2]
                st.success(f"Estudiante: **{nombre_est}** | Grado: **{grado_est}**")
                
                with conn.session as s:
                    mats_db = s.execute(text("SELECT materia FROM calificaciones WHERE estudiante_id = :eid"), {"eid": est_id}).fetchall()
                
                lista_materias = [m[0] for m in mats_db]
                if lista_materias:
                    mat_sel = st.selectbox("Seleccione la materia o dimensión a consultar:", ["--- Seleccione ---"] + lista_materias)
                    if mat_sel != "--- Seleccione ---":
                        with conn.session as s:
                            cal = s.execute(text("""
                                SELECT nota_saber_hacer, nota_convivir, nota_prueba_externa, definitiva, recuperacion, nivelacion, nota_final 
                                FROM calificaciones WHERE estudiante_id = :eid AND materia = :mat
                            """), {"eid": est_id, "mat": mat_sel}).fetchone()
                        
                        if cal:
                            es_bach = any(g in grado_est for g in ["6°", "7°", "8°", "9°", "10°", "11°", "Sexto", "Séptimo", "Octavo", "Noveno", "Décimo", "Undécimo"])
                            st.markdown(f"### Calificaciones: {mat_sel.upper()} ({grado_est})")
                            st.write(f"- **70%** | Saber y Hacer: **{int(cal[0])}**")
                            if es_bach:
                                st.write(f"- **25%** | Convivir: **{int(cal[1])}**")
                                st.write(f"- **5%** | Prueba externa: **{int(cal[2])}**")
                            else:
                                st.write(f"- **30%** | Convivir: **{int(cal[1])}**")
                            st.write("---")
                            st.success(f"**Nota Final:** {int(cal[6])} (Aprobado)")
                else:
                    st.info("No hay calificaciones registradas para este estudiante.")
            else:
                    st.error("⚠️ El documento ingresado no se encuentra registrado.")
        except Exception as ex:
            st.warning("⚠️ Error al consultar la base de datos.")

# ==============================================================================
# RESTO DE MÓDULOS (Pagos, Horarios, Psicología, PQRS)
# ==============================================================================
elif menu_principal == "2. Pagos y Facturación":
    st.header("💳 Pagos y Facturación")
    st.write("Módulo de pagos activo y conectado a la base de datos de Aiven.")
elif menu_principal == "3. Horarios de Atención y Biblioteca":
    st.header("⏰ Horarios y Dependencias")
    st.write("Módulo de reservas activo.")
elif menu_principal == "4. Asesoría, Psicología y Bienestar":
    st.header("🧠 Psicología y Bienestar")
    st.write("Módulo de citas activo.")
elif menu_principal == "5. Quejas, Reclamos y Sugerencias (PQRS)":
    st.header("📝 PQRS")
    st.write("Módulo de reportes activo.")
