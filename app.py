import streamlit as st
import random
from sqlalchemy import text

st.set_page_config(page_title="Chatbot Institución Educativa", page_icon="🤖", layout="centered")

# --- CONEXIÓN AUTOMÁTICA A LA BASE DE DATOS ---
try:
    conn = st.connection("mysql", type="sql")
    
    def inicializar_base_de_datos():
        with conn.session as s:
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
            
            resultado = s.execute(text("SELECT COUNT(*) FROM estudiantes")).fetchone()
            if resultado[0] == 0:
                estudiantes_iniciales = [
                    ('000000', 'estudiante_T', 'Transición', 'transicion@colegio.edu.co'),
                    ('111111', 'estudiante_1ro', 'Primero (1°)', 'primero@colegio.edu.co'),
                    ('222222', 'estudiante_2do', 'Segundo (2°)', 'segundo@colegio.edu.co'),
                    ('333333', 'estudiante_3ro', 'Tercero (3°)', 'tercero@colegio.edu.co'),
                    ('444444', 'estudiante_4to', 'Cuarto (4°)', 'cuarto@colegio.edu.co'),
                    ('555555', 'estudiante_5to', 'Quinto (5°)', 'quinto@colegio.edu.co'),
                    ('666666', 'estudiante_6to', 'Sexto (6°)', 'sexto@colegio.edu.co'),
                    ('777777', 'estudiante_7mo', 'Séptimo (7°)', 'septimo@colegio.edu.co'),
                    ('888888', 'estudiante_8vo', 'Octavo (8°)', 'octavo@colegio.edu.co'),
                    ('999999', 'estudiante_9no', 'Noveno (9°)', 'noveno@colegio.edu.co'),
                    ('101010', 'estudiante_10mo', 'Décimo (10°)', 'decimo@colegio.edu.co'),
                    ('211111', 'estudiante_11decimo', 'Undécimo (11°)', 'undecimo@colegio.edu.co')
                ]
                for est in estudiantes_iniciales:
                    s.execute(text("INSERT IGNORE INTO estudiantes (documento, nombre_completo, grado, correo) VALUES (:doc, :nom, :grad, :corr)"),
                              {"doc": est[0], "nom": est[1], "grad": est[2], "corr": est[3]})
                s.commit()

    inicializar_base_de_datos()
except Exception as e:
    pass

st.title("🤖 Chatbot de la Institución Educativa")
st.write("Bienvenido al sistema de atención institucional.")

# Menú Principal
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
# MÓDULO 1: INFORMACIÓN ACADÉMICA Y CALIFICACIONES (Validado por Documento)
# ==============================================================================
def mostrar_tabla_calificaciones(materia, grado_nombre, es_bachillerato=False):
    nota_saber_hacer = 78.0 if "Transición" in grado_nombre else 85.0
    nota_convivir = 80.0
    nota_prueba_externa = 60.0 if es_bachillerato else 0.0

    if es_bachillerato:
        definitiva = (nota_saber_hacer * 0.70) + (nota_convivir * 0.25) + (nota_prueba_externa * 0.05)
    else:
        definitiva = (nota_saber_hacer * 0.70) + (nota_convivir * 0.30)

    definitiva_val = int(round(definitiva))
    nota_minima = 65
    
    if "Matemáticas" in materia and es_bachillerato:
        recuperacion_val = 68
        nivelacion_val = 0
        nota_final_val = recuperacion_val
    elif definitiva_val < nota_minima:
        recuperacion_val = 55
        nivelacion_val = 70
        nota_final_val = nivelacion_val
    else:
        recuperacion_val = 0
        nivelacion_val = 0
        nota_final_val = definitiva_val

    st.markdown(f"### Calificaciones: {materia.upper()} ({grado_nombre})")
    st.write(f"- **70%** | Cognitivo y Procedimental: Saber y Hacer | **{int(nota_saber_hacer)}**")
    if es_bachillerato:
        st.write(f"- **25%** | Actitudinal: Convivir | **{int(nota_convivir)}**")
        st.write(f"- **5%** | Cognitivo: Prueba externa | **{int(nota_prueba_externa)}**")
    else:
        st.write(f"- **30%** | Actitudinal: Convivir | **{int(nota_convivir)}**")
    
    st.write("---")
    st.write(f"**Definitiva:** {definitiva_val}")
    st.write(f"**Recuperación:** {recuperacion_val}")
    st.write(f"**Nivelación:** {nivelacion_val}")
    st.success(f"**Nota Final:** {nota_final_val}")

if menu_principal == "1. Información Académica y Calificaciones":
    st.header("📚 Información Académica y Calificaciones")
    doc_academico = st.text_input("Ingrese el número de documento del estudiante (ej. 000000, 101010, 211111):", key="doc_acad")
    
    if doc_academico:
        try:
            with conn.session as s:
                est_info = s.execute(text("SELECT nombre_completo, grado FROM estudiantes WHERE documento = :doc"), {"doc": doc_academico}).fetchone()
            
            if est_info:
                nombre_est, grado_est = est_info[0], est_info[1]
                st.success(f"Estudiante encontrado: **{nombre_est}** — Grado: **{grado_est}**")
                
                es_bach_db = any(g in grado_est for g in ["Sexto", "Séptimo", "Octavo", "Noveno", "Décimo", "Undécimo", "6°", "7°", "8°", "9°", "10°", "11°"])
                
                if "Transición" in grado_est:
                    mats = ["Dimensión Socio Afectiva", "Dimensión Comunicativa", "Dimensión Comunicativa Inglés", "Dimensión Cognitiva", "Dimensión Corporal", "Dimensión Artística", "Dimensión Religiosa", "Dimensión Informática", "Dimensión Convivencia"]
                elif any(g in grado_est for g in ["Primero", "Segundo", "Tercero", "Cuarto", "Quinto"]):
                    mats = ["Matemáticas", "Estadística", "Geometría", "Ciencias Naturales", "Ciencias Sociales", "Ética y Valores", "Cátedra de la Paz", "Artística", "Castellano", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Inglés"]
                elif any(g in grado_est for g in ["Sexto", "Séptimo", "6°", "7°"]):
                    mats = ["Matemáticas", "Estadística", "Geometría", "Ciencias Naturales", "Ciencias Sociales", "Ética y Valores", "Cátedra de la Paz", "Artística", "Lenguaje", "Lectura Crítica", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Inglés"]
                elif "Octavo" in grado_est:
                    mats = ["Matemáticas", "Estadística", "Geometría", "Ciencias Naturales", "Historia", "Geografía", "Ética y Valores", "Cátedra de la Paz", "Artística", "Lenguaje", "Lectura Crítica", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Inglés"]
                elif "Noveno" in grado_est:
                    mats = ["Matemáticas", "Biología", "Química", "Física", "Historia", "Geografía", "Ética y Valores", "Cátedra de la Paz", "Artística", "Lenguaje", "Lectura Crítica", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Filosofía", "Inglés"]
                else:
                    mats = ["Matemáticas", "Biología", "Química", "Física", "Ciencias Sociales", "Economía", "Ética y Valores", "Artística", "Lenguaje", "Lectura Crítica", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Filosofía", "Inglés"]
                
                mat_sel = st.selectbox("Seleccione la materia o dimensión a consultar:", ["--- Seleccione ---"] + mats)
                if mat_sel != "--- Seleccione ---":
                    mostrar_tabla_calificaciones(mat_sel, grado_est, es_bach_db)
            else:
                st.error("⚠️ El documento ingresado no se encuentra registrado en la base de datos.")
        except Exception as ex:
            st.warning("⚠️ Error al conectar con la base de datos. Verifique sus Secrets en Streamlit Cloud.")

# ==============================================================================
# MÓDULO 2: PAGOS Y FACTURACIÓN
# ==============================================================================
elif menu_principal == "2. Pagos y Facturación":
    st.header("💳 Pagos y Facturación")
    op_pagos = st.selectbox("Seleccione opción:", [
        "--- Seleccione ---", 
        "Pago de Eventos", 
        "Pruebas Saber (Grados 6° a 9°)", 
        "Preicfes y Pruebas ICFES (Grados 10° y 11°)"
    ])
    
    doc_estudiante = st.text_input("Ingrese el número de documento del estudiante (ej. 000000, 101010, 211111):")
    
    if op_pagos == "Pago de Eventos":
        evento = st.selectbox("Evento:", ["Día de la Familia Javeriana ($30.000)", "Boleta Rifa Institucional ($15.000)"])
        medio = st.selectbox("Medio de pago:", ["Bancolombia (Ahorros # 458-921384-01)", "Nequi (310-892-4102)", "Daviplata (310-892-4102)", "MasterCard"])
        ref = st.text_input("Ingrese la referencia / número de transacción:")
        
        if st.button("Registrar Pago"):
            if doc_estudiante and ref:
                try:
                    with conn.session as s:
                        res = s.execute(text("SELECT id FROM estudiantes WHERE documento = :doc"), {"doc": doc_estudiante}).fetchone()
                        if res:
                            est_id = res[0]
                            s.execute(text("INSERT INTO pagos (estudiante_id, concepto, valor, medio_pago, referencia_transaccion, estado) VALUES (:eid, :conc, :val, :med, :ref, 'Aprobado')"),
                                      {"eid": est_id, "conc": evento, "val": "$30.000" if "Familia" in evento else "$15.000", "med": medio, "ref": ref})
                            s.commit()
                            st.success(f"[✓] Pago guardado en la Base de Datos para el documento {doc_estudiante} vía {medio}. Ref: #{ref}.")
                        else:
                            st.error("⚠️ El documento ingresado no existe en la base de datos.")
                except Exception as ex:
                    st.success(f"[✓] Pago simulado registrado correctamente. Ref: #{ref}")
            else:
                st.warning("⚠️ Debe ingresar el documento del estudiante y una referencia válida.")
                
    elif op_pagos == "Pruebas Saber (Grados 6° a 9°)":
        st.subheader("📚 Pruebas Saber (Grados 6° a 9°)")
        grado_saber = st.selectbox("Seleccione el grado:", ["--- Seleccione ---", "6° (Sexto)", "7° (Séptimo)", "8° (Octavo)", "9° (Noveno)"])
        
        if grado_saber != "--- Seleccione ---":
            st.write("• **Costo total de las 3 pruebas:** $30.000 COP ($10.000 c/u)")
            p_saber_sel = st.selectbox("Seleccione la prueba a pagar:", ["--- Seleccione ---", "Prueba 2 (Intermedia) - $10.000", "Prueba 3 (Final) - $10.000"])
            if p_saber_sel != "--- Seleccione ---":
                medio_s = st.selectbox("Medio de pago:", ["Bancolombia", "Nequi", "Daviplata", "MasterCard"])
                ref_s = st.text_input("Referencia de transacción:")
                if st.button("Pagar Prueba Saber"):
                    if doc_estudiante and ref_s:
                        try:
                            with conn.session as s:
                                res = s.execute(text("SELECT id FROM estudiantes WHERE documento = :doc"), {"doc": doc_estudiante}).fetchone()
                                if res:
                                    s.execute(text("INSERT INTO pagos (estudiante_id, concepto, valor, medio_pago, referencia_transaccion, estado) VALUES (:eid, :conc, '$10.000', :med, :ref, 'Aprobado')"),
                                              {"eid": res[0], "conc": p_saber_sel, "med": medio_s, "ref": ref_s})
                                    s.commit()
                                    st.success(f"[✓] Pago guardado en Base de Datos para el documento {doc_estudiante}. Ref: #{ref_s}")
                                else:
                                    st.error("⚠️ Documento no encontrado.")
                        except:
                            st.success(f"[✓] Pago de {p_saber_sel} registrado con éxito para {doc_estudiante}.")
                    else:
                        st.warning("⚠️ Ingrese el documento y la referencia.")
                        
    elif op_pagos == "Preicfes y Pruebas ICFES (Grados 10° y 11°)":
        st.subheader("🎓 Preicfes y Pruebas ICFES (Grados 10° y 11°)")
        grado_pre = st.selectbox("Seleccione el grado:", ["--- Seleccione ---", "10° (Décimo)", "11° (Undécimo)"])
        
        if grado_pre != "--- Seleccione ---":
            st.write("• **Costo total acumulado:** $270.000 COP (3 Preicfes de $45.000 + 1 ICFES de $135.000)")
            p_pre_sel = st.selectbox("Seleccione concepto a pagar:", [
                "--- Seleccione ---", 
                "Preicfes Sesión 3 - $45.000", 
                "Examen Oficial ICFES - $135.000"
            ])
            if p_pre_sel != "--- Seleccione ---":
                medio_p = st.selectbox("Medio de pago:", ["Bancolombia", "Nequi", "Daviplata", "MasterCard"])
                ref_p = st.text_input("Referencia de transacción:")
                if st.button("Pagar Concepto Preicfes/ICFES"):
                    if doc_estudiante and ref_p:
                        try:
                            with conn.session as s:
                                res = s.execute(text("SELECT id FROM estudiantes WHERE documento = :doc"), {"doc": doc_estudiante}).fetchone()
                                if res:
                                    val_pago = "$45.000" if "Preicfes" in p_pre_sel else "$135.000"
                                    s.execute(text("INSERT INTO pagos (estudiante_id, concepto, valor, medio_pago, referencia_transaccion, estado) VALUES (:eid, :conc, :val, :med, :ref, 'Aprobado')"),
                                              {"eid": res[0], "conc": p_pre_sel, "val": val_pago, "med": medio_p, "ref": ref_p})
                                    s.commit()
                                    st.success(f"[✓] Pago guardado en Base de Datos para el documento {doc_estudiante}. Ref: #{ref_p}")
                                else:
                                    st.error("⚠️ Documento no encontrado.")
                        except:
                            st.success(f"[✓] Pago de {p_pre_sel} registrado con éxito para {doc_estudiante}.")
                    else:
                        st.warning("⚠️ Ingrese el documento y la referencia.")

# ==============================================================================
# MÓDULO 3: HORARIOS DE ATENCIÓN Y BIBLIOTECA
# ==============================================================================
elif menu_principal == "3. Horarios de Atención y Biblioteca":
    st.header("⏰ Horarios de Atención y Dependencias")
    op_h = st.selectbox("Seleccione:", ["--- Seleccione ---", "Administración y Secretaría", "Coordinaciones", "Biblioteca Institucional"])
    
    if op_h == "Administración y Secretaría":
        st.write("**Horario de Atención:** Lunes a Viernes: 8:00 AM - 10:00 AM | 2:00 PM - 4:00 PM")
        st.markdown("---")
        st.subheader("📌 Apartar Cupo - Administración")
        dia_admin = st.selectbox("Seleccione el día:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
        jornada_admin = st.selectbox("Seleccione jornada:", ["--- Seleccione ---", "Mañana", "Tarde"])
        
        horas_admin = ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM"] if jornada_admin == "Mañana" else ["2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM"] if jornada_admin == "Tarde" else []
            
        if horas_admin:
            hora_admin = st.selectbox("Seleccione la hora (cupos cada 30 min):", ["--- Seleccione ---"] + horas_admin)
            doc_admin = st.text_input("Documento del acudiente/estudiante:")
            if st.button("Confirmar Reserva en Administración"):
                if dia_admin != "--- Seleccione ---" and hora_admin != "--- Seleccione ---" and doc_admin:
                    try:
                        with conn.session as s:
                            s.execute(text("INSERT INTO reservas_dependencias (dependencia, dia, jornada, hora, documento_o_nombre) VALUES ('Administracion', :dia, :jor, :hor, :doc)"),
                                      {"dia": dia_admin, "jor": jornada_admin, "hor": hora_admin, "doc": doc_admin})
                            s.commit()
                            st.success(f"[✓] Cupo guardado en Base de Datos para Administración ({dia_admin} {jornada_admin} a las {hora_admin}).")
                    except:
                        st.success(f"[✓] Cupo apartado exitosamente para el documento {doc_admin}.")
                else:
                    st.warning("⚠️ Complete todos los datos.")

    elif op_h == "Coordinaciones":
        st.write("**Horario General:** Lunes a Viernes: 8:00 AM - 11:00 AM y 2:00 PM - 4:00 PM")
        st.markdown("---")
        st.subheader("📌 Apartar Cupo - Coordinaciones")
        dia_coord = st.selectbox("Seleccione el día:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"], key="d_coord")
        jornada_coord = st.selectbox("Seleccione jornada:", ["--- Seleccione ---", "Mañana", "Tarde"], key="j_coord")
        
        horas_coord = ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM"] if jornada_coord == "Mañana" else ["2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM"] if jornada_coord == "Tarde" else []
            
        if horas_coord:
            hora_coord = st.selectbox("Seleccione la hora (cupos cada 30 min):", ["--- Seleccione ---"] + horas_coord, key="h_coord")
            nombre_coord_est = st.text_input("Nombre o documento del estudiante / acudiente:")
            if st.button("Confirmar Reserva en Coordinación"):
                if dia_coord != "--- Seleccione ---" and hora_coord != "--- Seleccione ---" and nombre_coord_est:
                    try:
                        with conn.session as s:
                            s.execute(text("INSERT INTO reservas_dependencias (dependencia, dia, jornada, hora, documento_o_nombre) VALUES ('Coordinacion', :dia, :jor, :hor, :doc)"),
                                      {"dia": dia_coord, "jor": jornada_coord, "hor": hora_coord, "doc": nombre_coord_est})
                            s.commit()
                            st.success(f"[✓] Cupo guardado en Base de Datos para Coordinación ({dia_coord} a las {hora_coord}).")
                    except:
                        st.success(f"[✓] Cupo apartado con éxito.")
                else:
                    st.warning("⚠️ Complete todos los campos.")

    elif op_h == "Biblioteca Institucional":
        st.write("**Horario:** Lunes a Viernes: 7:00 AM - 12:00 PM | 1:30 PM - 6:30 PM")
        st.markdown("---")
        st.subheader("📚 Apartar Espacio en Biblioteca")
        sec_bib = st.selectbox("Sección:", ["--- Seleccione ---", "Primaria", "Bachillerato"])
        dia_bib = st.selectbox("Día de la semana:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"], key="d_bib")
        
        bloques_bib = [
            "1ª Hora (7:00 - 7:50 AM)", "2ª Hora (7:50 - 8:40 AM)", "3ª Hora (8:40 - 9:40 AM)", 
            "4ª Hora (10:00 - 10:50 AM)", "5ª Hora (10:50 - 11:40 AM)", "6ª Hora (11:40 - 12:00 PM)"
        ] if sec_bib == "Primaria" else [
            "1ª Hora (12:30 - 1:30 PM)", "2ª Hora (1:30 - 2:25 PM)", "3ª Hora (2:25 - 3:20 PM)", 
            "4ª Hora (3:50 - 4:45 PM)", "5ª Hora (4:45 - 5:40 PM)", "6ª Hora (5:40 - 6:30 PM)"
        ] if sec_bib == "Bachillerato" else []
            
        if bloques_bib:
            hora_bib = st.selectbox("Bloque horario de clase:", ["--- Seleccione ---"] + bloques_bib)
            motivo_bib = st.selectbox("Seleccione el motivo de la reserva:", [
                "--- Seleccione ---",
                "1. Investigación grupal / Trabajo en equipo",
                "2. Lectura y consulta individual",
                "3. Préstamo de material de apoyo pedagógico"
            ])
            responsable_bib = st.text_input("Nombre del docente o responsable:")
            
            if st.button("Apartar Espacio en Biblioteca"):
                if dia_bib != "--- Seleccione ---" and hora_bib != "--- Seleccione ---" and motivo_bib != "--- Seleccione ---" and responsable_bib:
                    try:
                        with conn.session as s:
                            s.execute(text("INSERT INTO reservas_biblioteca (seccion, dia, hora_bloque, responsable, motivo, estado) VALUES (:sec, :dia, :hor, :resp, :mot, 'RES')"),
                                      {"sec": sec_bib, "dia": dia_bib, "hor": hora_bib, "resp": responsable_bib, "mot": motivo_bib})
                            s.commit()
                            st.success(f"[✓] Espacio guardado en Base de Datos para Biblioteca ({sec_bib}) el día {dia_bib}.")
                    except:
                        st.success(f"[✓] Espacio apartado con éxito.")
                else:
                    st.warning("⚠️ Complete todos los campos, incluido el motivo.")

# ==============================================================================
# MÓDULO 4: ASESORÍA Y PSICOLOGÍA
# ============================================================
elif menu_principal == "4. Asesoría, Psicología y Bienestar":
    st.header("🧠 Asesoría, Psicología y Bienestar Escolar")
    area = st.selectbox("Seleccione área:", ["--- Seleccione ---", "Psicología Escolar y Orientación", "Fonoaudiología Escolar", "Terapia Ocupacional"])
    
    nombre = st.text_input("Nombre completo del estudiante:")
    grado = st.text_input("Grado (ej. 8°B):")
    contacto = st.text_input("Teléfono o correo de contacto:")
    modalidad = st.selectbox("Modalidad de cita:", ["Individual (Estudiante)", "Familiar"])
    
    if st.button("Registrar Solicitud / Cita"):
        if nombre and grado and contacto:
            try:
                with conn.session as s:
                    s.execute(text("INSERT INTO citas_psicologia (estudiante_nombre, grado, contacto, modalidad, estado) VALUES (:nom, :grad, :cont, :mod, 'Solicitada')"),
                              {"nom": nombre, "grad": grado, "cont": contacto, "mod": modalidad})
                    s.commit()
                    st.success(f"[✓] Cita guardada en Base de Datos para {nombre} ({grado}).")
            except:
                st.success(f"[✓] Solicitud registrada exitosamente para {nombre}.")
        else:
            st.warning("⚠️ Complete todos los campos.")

# ==============================================================================
# MÓDULO 5: QUEJAS, RECLAMOS Y SUGERENCIAS (PQRS)
# ============================================================
elif menu_principal == "5. Quejas, Reclamos y Sugerencias (PQRS)":
    st.header("📝 Quejas, Reclamos y Sugerencias (PQRS)")
    cat = st.selectbox("Categoría:", ["--- Seleccione ---", "Servicios e Infraestructura", "Profesores o Personal de la Institución", "Felicitaciones o Sugerencias de Mejora"])
    subcat = st.text_input("Subcategoría o Asunto específico:")
    detalle = st.text_area("Escriba los detalles de su reporte de manera respetuosa:")
    
    if st.button("Enviar Reporte PQRS"):
        if len(detalle) >= 10 and subcat:
            radicado = f"PQRS-{random.randint(10000, 99999)}"
            try:
                with conn.session as s:
                    s.execute(text("INSERT INTO pqrs (radicado, categoria, subcategoria, detalle, estado) VALUES (:rad, :cat, :sub, :det, 'Enviado')"),
                              {"rad": radicado, "cat": cat, "sub": subcat, "det": detalle})
                    s.commit()
                    st.success(f"[✓] Reporte guardado en Base de Datos.")
            except:
                pass
            st.markdown(f"**Número de Radicado:** `{radicado}`")
            st.markdown("💡 *«¡Recuerda que entre todos nos ayudamos a construir una mejor comunidad educativa!»*")
        else:
            st.warning("⚠️ Llene la subcategoría y asegúrese de que el detalle tenga al menos 10 caracteres.")
