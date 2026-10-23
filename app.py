import streamlit as st
import random
import pandas as pd
from sqlalchemy import text

st.set_page_config(page_title="Chatbot Institución Educativa", page_icon="🤖", layout="centered")

# --- CONEXIÓN A LA BASE DE DATOS DE AIVEN ---
try:
    conn = st.connection("mysql", type="sql")
    
    # Asegurar tablas con estructura robusta
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
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS reservas_dependencias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                dependencia VARCHAR(50) NOT NULL, 
                dia VARCHAR(20) NOT NULL,
                jornada VARCHAR(20) NOT NULL,    
                hora VARCHAR(20) NOT NULL,       
                documento_o_nombre VARCHAR(100) NOT NULL
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
                estado VARCHAR(30) DEFAULT 'Solicitada'
            );
        """))
        s.execute(text("""
            CREATE TABLE IF NOT EXISTS pqrs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                radicado VARCHAR(30) UNIQUE NOT NULL,
                categoria VARCHAR(50) NOT NULL,
                subcategoria VARCHAR(100) NOT NULL,
                detalle TEXT NOT NULL,
                estado VARCHAR(50) DEFAULT 'Enviado'
            );
        """))
        s.commit()
        
        # Insertar los 12 estudiantes base si está vacía la tabla
        res = s.execute(text("SELECT COUNT(*) FROM estudiantes")).fetchone()
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
                s.execute(text("INSERT IGNORE INTO estudiantes (documento, nombre_completo, grado, correo) VALUES (:doc, :nom, :grad, :corr)"),
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
        "5. Quejas, Reclamos y Sugerencias (PQRS)",
        "6. 📊 Panel de Administración / Base de Datos"
    ]
)

# ==============================================================================
# MÓDULO 1: INFORMACIÓN ACADÉMICA
# ==============================================================================
if menu_principal == "1. Información Académica y Calificaciones":
    st.header("📚 Información Académica y Calificaciones")
    doc_academico = st.text_input("Ingrese el número de documento del estudiante (ej. 000000, 101010, 211111):", key="doc_acad")
    
    if doc_academico:
        try:
            with conn.session as s:
                est_info = s.execute(text("SELECT nombre_completo, grado FROM estudiantes WHERE documento = :doc"), {"doc": doc_academico}).fetchone()
            
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
                    
                    sh = round(rng.uniform(30.0, 98.0), 1)
                    conv = round(rng.uniform(60.0, 100.0), 1)
                    ext = round(rng.uniform(20.0, 100.0), 1) if es_bach else 0.0
                    
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
    
    doc_estudiante = st.text_input("Ingrese el número de documento del estudiante:", key="doc_pago")
    
    if doc_estudiante:
        try:
            with conn.session as s:
                est_info = s.execute(text("SELECT id, nombre_completo, grado FROM estudiantes WHERE documento = :doc"), {"doc": doc_estudiante}).fetchone()
            
            if est_info:
                est_id, nombre_est, grado_est = est_info[0], est_info[1], est_info[2]
                st.success(f"Estudiante: **{nombre_est}** | Grado: **{grado_est}**")
                
                # Filtro por grados
                es_primaria = any(g in grado_est for g in ["Transición", "Primero", "Segundo", "Tercero", "Cuarto", "Quinto", "1°", "2°", "3°", "4°", "5°"])
                es_media = any(g in grado_est for g in ["Sexto", "Séptimo", "Octavo", "Noveno", "6°", "7°", "8°", "9°"])
                es_alta = any(g in grado_est for g in ["Décimo", "Undécimo", "10°", "11°"])
                
                opciones_disponibles = ["--- Seleccione ---", "Pago de Eventos"]
                if es_media:
                    opciones_disponibles.append("Pruebas Saber (Grados 6° a 9°)")
                elif es_alta:
                    opciones_disponibles.append("Preicfes y Pruebas ICFES (Grados 10° y 11°)")
                
                op_pagos = st.selectbox("Seleccione la categoría de pago:", opciones_disponibles)
                
                if op_pagos != "--- Seleccione ---":
                    if op_pagos == "Pago de Eventos":
                        sub_conceptos = ["Día de la Familia Javeriana ($30.000)", "Boleta Rifa Institucional ($15.000)"]
                    elif op_pagos == "Pruebas Saber (Grados 6° a 9°)":
                        sub_conceptos = ["Prueba 1 (Inicial) - $10.000", "Prueba 2 (Intermedia) - $10.000", "Prueba 3 (Final) - $10.000"]
                    else:
                        sub_conceptos = ["Preicfes Sesión 1 - $45.000", "Preicfes Sesión 2 - $45.000", "Preicfes Sesión 3 - $45.000", "Examen Oficial ICFES - $135.000"]
                        
                    concepto_sel = st.selectbox("Seleccione el concepto específico:", ["--- Seleccione ---"] + sub_conceptos)
                    
                    if concepto_sel != "--- Seleccione ---":
                        # ------------------------------------------------------
                        # LÓGICA DE JERARQUÍA / PRELACIÓN
                        # ------------------------------------------------------
                        # Semilla única basada en el Documento + la Categoría de Pago
                        seed_val = int(doc_estudiante) + sum(ord(c) for c in op_pagos)
                        rng = random.Random(seed_val)
                        
                        # Determina hasta qué índice de la lista tiene pagado (Nivel de avance)
                        # Ej: Nivel 0 = Ninguno pagado | Nivel 1 = Pagado hasta el primer ítem, etc.
                        nivel_pago_aleatorio = rng.randint(0, len(sub_conceptos))
                        posicion_actual = sub_conceptos.index(concepto_sel)
                        
                        # Validar si existe un pago registrado de forma real en Aiven
                        with conn.session as s:
                            pago_db = s.execute(text("""
                                SELECT referencia_transaccion FROM pagos 
                                WHERE estudiante_id = :eid AND concepto = :conc AND estado = 'Aprobado'
                            """), {"eid": est_id, "conc": concepto_sel}).fetchone()
                        
                        # Regla Jerárquica: Si la posición del ítem es menor al nivel alcanzado o ya se pagó en DB -> PAGADO
                        if pago_db or posicion_actual < nivel_pago_aleatorio:
                            estado_final = "PAGADO"
                            ref_mostrada = pago_db[0] if pago_db else f"REF-SEQ-{rng.randint(1000, 9999)}"
                        else:
                            estado_final = "DEBE"
                        
                        st.write("---")
                        if estado_final == "PAGADO":
                            st.info(f"🟢 **Estado del concepto:** **PAGADO** (Ref: #{ref_mostrada}). El estudiante se encuentra al día con esta obligación.")
                        else:
                            st.warning(f"🔴 **Estado del concepto:** **DEBE**. Debe cancelar esta prueba/sesión para continuar en la secuencia.")
                            
                            # Verificar si la prueba anterior está pendiente para mostrar advertencia de prelación
                            if posicion_actual > 0:
                                concepto_anterior = sub_conceptos[posicion_actual - 1]
                                with conn.session as s:
                                    pago_ant_db = s.execute(text("SELECT id FROM pagos WHERE estudiante_id = :eid AND concepto = :conc AND estado = 'Aprobado'"), {"eid": est_id, "conc": concepto_anterior}).fetchone()
                                
                                if not pago_ant_db and (posicion_actual - 1) >= nivel_pago_aleatorio:
                                    st.caption(f"⚠️ *Nota: Se recomienda cancelar primero el concepto previo ({concepto_anterior}).*")

                            medio = st.selectbox("Medio de pago:", ["Bancolombia", "Nequi", "Daviplata", "MasterCard"])
                            ref_input = st.text_input("Ingrese la referencia de la transacción:")
                            
                            if st.button("Registrar Pago"):
                                if ref_input:
                                    try:
                                        with conn.session as s:
                                            dup_ref = s.execute(text("SELECT COUNT(*) FROM pagos WHERE referencia_transaccion = :ref"), {"ref": ref_input}).fetchone()[0]
                                            if dup_ref > 0:
                                                st.error(f"⚠️ La referencia #{ref_input} ya se encuentra registrada.")
                                            else:
                                                val_pago = "$30.000" if "30.000" in concepto_sel else ("$15.000" if "15.000" in concepto_sel else ("$135.000" if "ICFES" in concepto_sel else ("$45.000" if "45.000" in concepto_sel else "$10.000")))
                                                s.execute(text("INSERT INTO pagos (estudiante_id, concepto, valor, medio_pago, referencia_transaccion, estado) VALUES (:eid, :conc, :val, :med, :ref, 'Aprobado')"),
                                                          {"eid": est_id, "conc": concepto_sel, "val": val_pago, "med": medio, "ref": ref_input})
                                                s.commit()
                                                st.success(f"[✓] ¡Pago guardado con éxito en Aiven!")
                                                st.rerun()
                                    except Exception as ex:
                                        st.error("⚠️ Error al registrar el pago.")
                                else:
                                    st.warning("⚠️ Ingrese una referencia válida.")
            else:
                st.error("⚠️ El documento ingresado no se encuentra registrado en la base de datos.")
        except Exception as ex:
            st.warning("⚠️ Error al consultar la información.")
    else:
        st.info("💡 Ingrese el número de documento del estudiante para ver su estado de cuenta.")
# ==============================================================================
# MÓDULO 3: HORARIOS DE ATENCIÓN Y BIBLIOTECA
# ==============================================================================
elif menu_principal == "3. Horarios de Atención y Biblioteca":
    st.header("⏰ Horarios de Atención y Biblioteca")
    op_h = st.selectbox("Seleccione:", ["--- Seleccione ---", "Administración y Secretaría", "Coordinaciones", "Biblioteca Institucional"])
    
    if op_h in ["Administración y Secretaría", "Coordinaciones"]:
        st.write(f"**Horario de atención general:** Lunes a Viernes (Mañana: 8:00 AM - 10:00 AM | Tarde: 2:00 PM - 4:00 PM)")
        dia = st.selectbox("Día:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
        jornada = st.selectbox("Jornada:", ["--- Seleccione ---", "Mañana", "Tarde"])
        
        if jornada == "Mañana":
            hora = st.selectbox("Hora:", ["--- Seleccione ---", "8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM"])
        elif jornada == "Tarde":
            hora = st.selectbox("Hora:", ["--- Seleccione ---", "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM"])
        else:
            hora = "--- Seleccione ---"
            st.info("💡 Seleccione una jornada para habilitar las horas correspondientes.")

        doc_res = st.text_input("Documento o Nombre:")
        
        if st.button("Confirmar Reserva"):
            if dia != "--- Seleccione ---" and jornada != "--- Seleccione ---" and hora != "--- Seleccione ---" and doc_res:
                try:
                    with conn.session as s:
                        verificar = s.execute(text("""
                            SELECT COUNT(*) FROM reservas_dependencias 
                            WHERE dependencia = :dep AND dia = :dia AND jornada = :jor AND hora = :hor
                        """), {"dep": op_h, "dia": dia, "jor": jornada, "hor": hora}).fetchone()[0]
                        
                        if verificar > 0:
                            st.error(f"⚠️ Lo sentimos, el cupo para **{op_h}** el día **{dia}** en la jornada **{jornada}** a las **{hora}** ya está ocupado.")
                        else:
                            s.execute(text("INSERT INTO reservas_dependencias (dependencia, dia, jornada, hora, documento_o_nombre) VALUES (:dep, :dia, :jor, :hor, :doc)"),
                                      {"dep": op_h, "dia": dia, "jor": jornada, "hor": hora, "doc": doc_res})
                            s.commit()
                            st.success(f"[✓] ¡Cupo guardado con éxito en Aiven para {op_h} ({dia} {jornada} - {hora})!")
                except Exception as ex:
                    st.warning("⚠️ Ocurrió un error al guardar la reserva.")
            else:
                st.warning("⚠️ Complete todos los campos correctamente.")

    elif op_h == "Biblioteca Institucional":
        st.write("**Horario:** Lunes a Viernes: 7:00 AM - 12:00 PM | 1:30 PM - 6:30 PM")
        sec = st.selectbox("Sección:", ["--- Seleccione ---", "Primaria", "Bachillerato"])
        dia_b = st.selectbox("Día:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
        
        if sec == "Primaria":
            bloques_disp = [
                "--- Seleccione ---",
                "1ª Hora (7:00 - 7:50 AM)",
                "2ª Hora (7:50 - 8:40 AM)",
                "3ª Hora (8:40 - 9:40 AM)",
                "4ª Hora (10:00 - 10:50 AM)",
                "5ª Hora (10:50 - 11:40 AM)",
                "6ª Hora (11:40 - 12:00 PM)"
            ]
        elif sec == "Bachillerato":
            bloques_disp = [
                "--- Seleccione ---",
                "1ª Hora (12:30 - 1:30 PM)",
                "2ª Hora (1:30 - 2:25 PM)",
                "3ª Hora (2:25 - 3:20 PM)",
                "4ª Hora (3:50 - 4:45 PM)",
                "5ª Hora (4:45 - 5:40 PM)",
                "6ª Hora (5:40 - 6:30 PM)"
            ]
        else:
            bloques_disp = ["--- Seleccione ---"]
            
        bloque = st.selectbox("Bloque horario de clase:", bloques_disp)
        motivo = st.selectbox("Motivo:", ["--- Seleccione ---", "1. Investigación grupal", "2. Lectura individual", "3. Préstamo de material"])
        responsable = st.text_input("Nombre del docente o responsable:")
        
        if st.button("Apartar Espacio en Biblioteca"):
            if sec != "--- Seleccione ---" and dia_b != "--- Seleccione ---" and bloque != "--- Seleccione ---" and motivo != "--- Seleccione ---" and responsable:
                try:
                    with conn.session as s:
                        verificar_bib = s.execute(text("""
                            SELECT COUNT(*) FROM reservas_biblioteca 
                            WHERE seccion = :sec AND dia = :dia AND hora_bloque = :hor
                        """), {"sec": sec, "dia": dia_b, "hor": bloque}).fetchone()[0]
                        
                        if verificar_bib > 0:
                            st.error(f"⚠️ El bloque **{bloque}** en la sección de **{sec}** para el día **{dia_b}** ya se encuentra ocupado.")
                        else:
                            s.execute(text("INSERT INTO reservas_biblioteca (seccion, dia, hora_bloque, responsable, motivo, estado) VALUES (:sec, :dia, :hor, :resp, :mot, 'RES')"),
                                      {"sec": sec, "dia": dia_b, "hor": bloque, "resp": responsable, "mot": motivo})
                            s.commit()
                            st.success(f"[✓] ¡Espacio de biblioteca reservado con éxito en Aiven!")
                except Exception as ex:
                    st.warning("⚠️ Ocurrió un error al procesar la reserva.")
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
                    dup_cita = s.execute(text("""
                        SELECT COUNT(*) FROM citas_psicologia 
                        WHERE estudiante_nombre = :nom AND contacto = :cont AND estado = 'Solicitada'
                    """), {"nom": nombre_p, "cont": contacto_p}).fetchone()[0]
                    
                    if dup_cita > 0:
                        st.warning(f"⚠️ Ya existe una solicitud de cita pendiente para **{nombre_p}**.")
                    else:
                        s.execute(text("INSERT INTO citas_psicologia (estudiante_nombre, grado, contacto, modalidad, estado) VALUES (:nom, :grad, :cont, :mod, 'Solicitada')"),
                                  {"nom": nombre_p, "grad": grado_p, "cont": contacto_p, "mod": modalidad_p})
                        s.commit()
                        st.success(f"[✓] Cita guardada en Aiven para {nombre_p}.")
            except Exception as ex:
                st.warning("⚠️ Error al registrar la cita.")
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
                    while s.execute(text("SELECT COUNT(*) FROM pqrs WHERE radicado = :rad"), {"rad": radicado}).fetchone()[0] > 0:
                        radicado = f"PQRS-{random.randint(10000, 99999)}"
                        
                    s.execute(text("INSERT INTO pqrs (radicado, categoria, subcategoria, detalle, estado) VALUES (:rad, :cat, :sub, :det, 'Enviado')"),
                              {"rad": radicado, "cat": cat, "sub": subcat, "det": detalle})
                    s.commit()
                    st.success(f"[✓] Reporte guardado con éxito en la base de datos.")
            except Exception as ex:
                pass
            st.markdown(f"**Número de Radicado:** `{radicado}`")
            st.markdown("💡 *«¡Recuerda que entre todos construimos una mejor comunidad educativa!»*")
        else:
            st.warning("⚠️ Llene la subcategoría y asegúrese de que el detalle tenga al menos 10 caracteres.")

# ==============================================================================
# MÓDULO 6: PANEL DE ADMINISTRACIÓN (Protegido por clave de acceso)
# ==============================================================================
elif menu_principal == "6. 📊 Panel de Administración / Base de Datos":
    st.header("🔒 Acceso Restringido - Panel de Administración")
    
    # Campo para ingresar la contraseña de administrador
    clave_admin = st.text_input("Ingrese la clave secreta de administrador:", type="password")
    
    # Puedes cambiar 'admin123' por la contraseña que tú prefieras
    if clave_admin == "admin123":
        st.success("🔑 Acceso concedido como Administrador.")
        st.write("Selecciona una tabla para auditar los registros guardados en Aiven:")
        
        tabla_a_ver = st.selectbox("Seleccionar tabla:", [
            "estudiantes", 
            "reservas_dependencias", 
            "reservas_biblioteca", 
            "pagos", 
            "citas_psicologia", 
            "pqrs"
        ])
        
        try:
            with conn.session as s:
                resultado = s.execute(text(f"SELECT * FROM {tabla_a_ver}")).fetchall()
                columnas = s.execute(text(f"SHOW COLUMNS FROM {tabla_a_ver}")).fetchall()
                nombres_columnas = [col[0] for col in columnas]
                
                if resultado:
                    df = pd.DataFrame(resultado, columns=nombres_columnas)
                    st.write(f"### Registros en `{tabla_a_ver}` ({len(df)} filas)")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info(f"La tabla `{tabla_a_ver}` está vacía actualmente.")
        except Exception as ex:
            st.error(f"Error al leer la base de datos: {ex}")
    elif clave_admin != "":
        st.error("❌ Clave incorrecta. Acceso denegado.")
    else:
        st.info("💡 Ingrese la contraseña de administrador para desbloquear los datos.")
