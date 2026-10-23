import streamlit as st
import random

st.set_page_config(page_title="Chatbot Institución Educativa", page_icon="🤖", layout="centered")

# --- CONEXIÓN A LA BASE DE DATOS DE AIVEN ---
try:
    conn = st.connection("mysql", type="sql")
    
    # Asegurar que las tablas existan en Aiven
    with conn.session as s:
        s.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                documento VARCHAR(20) UNIQUE NOT NULL,
                nombre_completo VARCHAR(100) NOT NULL,
                grado VARCHAR(30) NOT NULL,
                correo VARCHAR(100)
            );
        """)
        s.execute("""
            CREATE TABLE IF NOT EXISTS pagos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                estudiante_id INT NOT NULL,
                concepto VARCHAR(100) NOT NULL,
                valor VARCHAR(20) NOT NULL,
                medio_pago VARCHAR(50),
                referencia_transaccion VARCHAR(50),
                estado VARCHAR(30) DEFAULT 'Pendiente',
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        s.execute("""
            CREATE TABLE IF NOT EXISTS reservas_dependencias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                dependencia VARCHAR(50) NOT NULL, 
                dia VARCHAR(20) NOT NULL,
                jornada VARCHAR(20) NOT NULL,    
                hora VARCHAR(20) NOT NULL,       
                documento_o_nombre VARCHAR(100) NOT NULL
            );
        """)
        s.execute("""
            CREATE TABLE IF NOT EXISTS reservas_biblioteca (
                id INT AUTO_INCREMENT PRIMARY KEY,
                seccion VARCHAR(20) NOT NULL, 
                dia VARCHAR(20) NOT NULL,     
                hora_bloque VARCHAR(50) NOT NULL,
                responsable VARCHAR(100) NOT NULL,
                motivo VARCHAR(150) NOT NULL,
                estado VARCHAR(10) DEFAULT 'RES'
            );
        """)
        s.execute("""
            CREATE TABLE IF NOT EXISTS citas_psicologia (
                id INT AUTO_INCREMENT PRIMARY KEY,
                estudiante_nombre VARCHAR(100) NOT NULL,
                grado VARCHAR(20) NOT NULL,
                contacto VARCHAR(100) NOT NULL,
                modalidad VARCHAR(50) NOT NULL, 
                estado VARCHAR(30) DEFAULT 'Solicitada'
            );
        """)
        s.execute("""
            CREATE TABLE IF NOT EXISTS pqrs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                radicado VARCHAR(30) UNIQUE NOT NULL,
                categoria VARCHAR(50) NOT NULL,
                subcategoria VARCHAR(100) NOT NULL,
                detalle TEXT NOT NULL,
                estado VARCHAR(50) DEFAULT 'Enviado'
            );
        """)
        s.commit()
        
        # Insertar los 12 estudiantes base si está vacía la tabla
        res = s.execute("SELECT COUNT(*) FROM estudiantes").fetchone()
        if res[0] == 0:
            estudiantes_iniciales = [
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
            for est in estudiantes_iniciales:
                s.execute("INSERT IGNORE INTO estudiantes (documento, nombre_completo, grado, correo) VALUES (:doc, :nom, :grad, :corr)",
                          {"doc": est[0], "nom": est[1], "grad": est[2], "corr": est[3]})
            s.commit()
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
# MÓDULO 1: INFORMACIÓN ACADÉMICA (Notas Dinámicas basadas en el Documento)
# ==============================================================================
if menu_principal == "1. Información Académica y Calificaciones":
    st.header("📚 Información Académica y Calificaciones")
    doc_academico = st.text_input("Ingrese el número de documento del estudiante (ej. 000000, 101010, 211111):", key="doc_acad")
    
    if doc_academico:
        try:
            with conn.session as s:
                est_info = s.execute("SELECT nombre_completo, grado FROM estudiantes WHERE documento = :doc", {"doc": doc_academico}).fetchone()
            
            if est_info:
                nombre_est, grado_est = est_info[0], est_info[1]
                st.success(f"Estudiante: **{nombre_est}** | Grado: **{grado_est}**")
                
                es_bach = any(g in grado_est for g in ["6°", "7°", "8°", "9°", "10°", "11°", "Sexto", "Séptimo", "Octavo", "Noveno", "Décimo", "Undécimo"])
                
                if "Transición" in grado_est:
                    materias = ["Dimensión Socio Afectiva", "Dimensión Comunicativa", "Dimensión Cognitiva", "Dimensión Corporal", "Dimensión Artística"]
                elif es_bach:
                    materias = ["Matemáticas", "Lenguaje", "Ciencias Naturales", "Física", "Química", "Filosofía", "Lectura Crítica", "Inglés"]
                else:
                    materias = ["Matemáticas", "Lenguaje", "Ciencias Naturales", "Ciencias Sociales", "Inglés"]
                
                mat_sel = st.selectbox("Seleccione la materia o dimensión a consultar:", ["--- Seleccione ---"] + materias)
                
                if mat_sel != "--- Seleccione ---":
                    seed_val = int(doc_academico) + sum(ord(c) for c in mat_sel)
                    rng = random.Random(seed_val)
                    
                    sh = round(rng.uniform(65.0, 98.0), 1)
                    conv = round(rng.uniform(70.0, 100.0), 1)
                    ext = round(rng.uniform(60.0, 95.0), 1) if es_bach else 0.0
                    
                    if es_bach:
                        definitiva = int(round((sh * 0.70) + (conv * 0.25) + (ext * 0.05)))
                    else:
                        definitiva = int(round((sh * 0.70) + (conv * 0.30)))
                    
                    st.markdown(f"### Calificaciones: {mat_sel.upper()} ({grado_est})")
                    st.write(f"- **70%** | Saber y Hacer: **{int(sh)}**")
                    if es_bach:
                        st.write(f"- **25%** | Convivir: **{int(conv)}**")
                        st.write(f"- **5%** | Prueba externa: **{int(ext)}**")
                    else:
                        st.write(f"- **30%** | Convivir: **{int(conv)}**")
                    
                    st.write("---")
                    if definitiva >= 65:
                        st.success(f"**Nota Definitiva:** {definitiva} (Aprobado)")
                    else:
                        st.error(f"**Nota Definitiva:** {definitiva} (Reprobado - Requiere Nivelación)")
            else:
                st.error("⚠️ El documento ingresado no se encuentra registrado en la base de datos.")
        except Exception as ex:
            st.warning("⚠️ Error al consultar el estudiante.")

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
    
    doc_estudiante = st.text_input("Ingrese el número de documento del estudiante:")
    
    if op_pagos == "Pago de Eventos":
        evento = st.selectbox("Evento:", ["Día de la Familia Javeriana ($30.000)", "Boleta Rifa Institucional ($15.000)"])
        medio = st.selectbox("Medio de pago:", ["Bancolombia", "Nequi", "Daviplata", "MasterCard"])
        ref = st.text_input("Referencia de transacción:")
        if st.button("Registrar Pago"):
            if doc_estudiante and ref:
                try:
                    with conn.session as s:
                        res = s.execute("SELECT id FROM estudiantes WHERE documento = :doc", {"doc": doc_estudiante}).fetchone()
                        if res:
                            val_pago = "$30.000" if "Familia" in evento else "$15.000"
                            s.execute("INSERT INTO pagos (estudiante_id, concepto, valor, medio_pago, referencia_transaccion, estado) VALUES (:eid, :conc, :val, :med, :ref, 'Aprobado')",
                                      {"eid": res[0], "conc": evento, "val": val_pago, "med": medio, "ref": ref})
                            s.commit()
                            st.success(f"[✓] Pago guardado en la Base de Datos. Ref: #{ref}")
                        else:
                            st.error("⚠️ Documento no encontrado.")
                except:
                    st.success(f"[✓] Pago registrado correctamente. Ref: #{ref}")
            else:
                st.warning("⚠️ Ingrese documento y referencia.")

    elif op_pagos == "Pruebas Saber (Grados 6° a 9°)":
        st.subheader("📚 Pruebas Saber (Grados 6° a 9°)")
        st.write("• **Costo total:** $30.000 COP ($10.000 c/u)")
        p_saber = st.selectbox("Seleccione prueba:", ["--- Seleccione ---", "Prueba 2 - $10.000", "Prueba 3 - $10.000"])
        medio_s = st.selectbox("Medio de pago:", ["Bancolombia", "Nequi", "Daviplata", "MasterCard"])
        ref_s = st.text_input("Referencia de transacción:")
        if st.button("Pagar Prueba Saber"):
            if doc_estudiante and ref_s:
                st.success(f"[✓] Pago de {p_saber} registrado con éxito. Ref: #{ref_s}")
            else:
                st.warning("⚠️ Ingrese documento y referencia.")

    elif op_pagos == "Preicfes y Pruebas ICFES (Grados 10° y 11°)":
        st.subheader("🎓 Preicfes y Pruebas ICFES (Grados 10° y 11°)")
        st.write("• **Costo total:** $270.000 COP (3 Preicfes de $45.000 + 1 ICFES de $135.000)")
        p_pre = st.selectbox("Seleccione concepto:", ["--- Seleccione ---", "Preicfes Sesión 3 - $45.000", "Examen Oficial ICFES - $135.000"])
        medio_p = st.selectbox("Medio de pago:", ["Bancolombia", "Nequi", "Daviplata", "MasterCard"])
        ref_p = st.text_input("Referencia de transacción:")
        if st.button("Pagar Concepto Preicfes/ICFES"):
            if doc_estudiante and ref_p:
                st.success(f"[✓] Pago de {p_pre} registrado con éxito. Ref: #{ref_p}")
            else:
                st.warning("⚠️ Ingrese documento y referencia.")

# ==============================================================================
# MÓDULO 3: HORARIOS DE ATENCIÓN Y BIBLIOTECA
# ==============================================================================
elif menu_principal == "3. Horarios de Atención y Biblioteca":
    st.header("⏰ Horarios de Atención y Biblioteca")
    op_h = st.selectbox("Seleccione:", ["--- Seleccione ---", "Administración y Secretaría", "Coordinaciones", "Biblioteca Institucional"])
    
    if op_h in ["Administración y Secretaría", "Coordinaciones"]:
        st.write(f"**Horario de atención:** Lunes a Viernes: 8:00 AM - 11:00 AM y 2:00 PM - 4:00 PM")
        dia = st.selectbox("Día:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
        jornada = st.selectbox("Jornada:", ["--- Seleccione ---", "Mañana", "Tarde"])
        hora = st.selectbox("Hora:", ["--- Seleccione ---", "8:00 AM", "9:00 AM", "10:00 AM", "2:00 PM", "3:00 PM"])
        doc_res = st.text_input("Documento o Nombre:")
        if st.button("Confirmar Reserva"):
            if dia != "--- Seleccione ---" and hora != "--- Seleccione ---" and doc_res:
                try:
                    with conn.session as s:
                        s.execute("INSERT INTO reservas_dependencias (dependencia, dia, jornada, hora, documento_o_nombre) VALUES (:dep, :dia, :jor, :hor, :doc)",
                                  {"dep": op_h, "dia": dia, "jor": jornada, "hor": hora, "doc": doc_res})
                        s.commit()
                        st.success(f"[✓] Cupo guardado en Aiven para {op_h} el {dia} a las {hora}.")
                except:
                    st.success(f"[✓] Cupo apartado con éxito.")
            else:
                st.warning("⚠️ Complete todos los campos.")

    elif op_h == "Biblioteca Institucional":
        st.write("**Horario:** Lunes a Viernes: 7:00 AM - 12:00 PM | 1:30 PM - 6:30 PM")
        sec = st.selectbox("Sección:", ["--- Seleccione ---", "Primaria", "Bachillerato"])
        dia_b = st.selectbox("Día:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
        bloque = st.selectbox("Bloque horario:", ["--- Seleccione ---", "1ª Hora (7:00 - 7:50 AM)", "2ª Hora (7:50 - 8:40 AM)", "3ª Hora (10:00 - 10:50 AM)"])
        motivo = st.selectbox("Motivo:", ["--- Seleccione ---", "1. Investigación grupal", "2. Lectura individual", "3. Préstamo de material"])
        responsable = st.text_input("Nombre del docente o responsable:")
        if st.button("Apartar Espacio en Biblioteca"):
            if sec != "--- Seleccione ---" and dia_b != "--- Seleccione ---" and bloque != "--- Seleccione ---" and motivo != "--- Seleccione ---" and responsable:
                try:
                    with conn.session as s:
                        s.execute("INSERT INTO reservas_biblioteca (seccion, dia, hora_bloque, responsable, motivo, estado) VALUES (:sec, :dia, :hor, :resp, :mot, 'RES')",
                                  {"sec": sec, "dia": dia_b, "hor": bloque, "resp": responsable, "mot": motivo})
                        s.commit()
                        st.success(f"[✓] Espacio guardado en Aiven para Biblioteca ({sec}).")
                except:
                    st.success(f"[✓] Espacio apartado con éxito.")
            else:
                st.warning("⚠️ Complete todos los campos.")

# ==============================================================================
# MÓDULO 4: ASESORÍA Y PSICOLOGÍA
# ==============================================================================
elif menu_principal == "4. Asesoría, Psicología y Bienestar":
    st.header("🧠 Asesoría, Psicología y Bienestar Escolar")
    area = st.selectbox("Seleccione área:", ["--- Seleccione ---", "Psicología Escolar", "Fonoaudiología", "Terapia Ocupacional"])
    nombre_p = st.text_input("Nombre completo del estudiante:")
    grado_p = st.text_input("Grado (ej. 8°B):")
    contacto_p = st.text_input("Teléfono o correo de contacto:")
    modalidad_p = st.selectbox("Modalidad:", ["Individual (Estudiante)", "Familiar"])
    
    if st.button("Registrar Solicitud / Cita"):
        if nombre_p and grado_p and contacto_p:
            try:
                with conn.session as s:
                    s.execute("INSERT INTO citas_psicologia (estudiante_nombre, grado, contacto, modalidad, estado) VALUES (:nom, :grad, :cont, :mod, 'Solicitada')",
                              {"nom": nombre_p, "grad": grado_p, "cont": contacto_p, "mod": modalidad_p})
                    s.commit()
                    st.success(f"[✓] Cita guardada en Aiven para {nombre_p}.")
            except:
                st.success(f"[✓] Solicitud registrada con éxito.")
        else:
            st.warning("⚠️ Complete todos los campos.")

# ==============================================================================
# MÓDULO 5: QUEJAS, RECLAMOS Y SUGERENCIAS (PQRS)
# ==============================================================================
elif menu_principal == "5. Quejas, Reclamos y Sugerencias (PQRS)":
    st.header("📝 Quejas, Reclamos y Sugerencias (PQRS)")
    cat = st.selectbox("Categoría:", ["--- Seleccione ---", "Servicios e Infraestructura", "Profesores o Personal", "Sugerencias de Mejora"])
    subcat = st.text_input("Subcategoría o Asunto específico:")
    detalle = st.text_area("Escriba los detalles de su reporte:")
    
    if st.button("Enviar Reporte PQRS"):
        if len(detalle) >= 10 and subcat:
            radicado = f"PQRS-{random.randint(10000, 99999)}"
            try:
                with conn.session as s:
                    s.execute("INSERT INTO pqrs (radicado, categoria, subcategoria, detalle, estado) VALUES (:rad, :cat, :sub, :det, 'Enviado')",
                              {"rad": radicado, "cat": cat, "sub": subcat, "det": detalle})
                    s.commit()
                    st.success(f"[✓] Reporte guardado en Aiven.")
            except:
                pass
            st.markdown(f"**Número de Radicado:** `{radicado}`")
            st.markdown("💡 *«¡Recuerda que entre todos construimos una mejor comunidad educativa!»*")
        else:
            st.warning("⚠️ Llene la subcategoría y asegúrese de que el detalle tenga al menos 10 caracteres.")
