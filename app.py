import streamlit as st
import random

st.set_page_config(page_title="Chatbot Institución Educativa", page_icon="🤖", layout="centered")

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
# MÓDULO 1: INFORMACIÓN ACADÉMICA Y CALIFICACIONES
# ==============================================================================
def mostrar_tabla_calificaciones(materia, es_bachillerato=False):
    nota_saber_hacer = 85.0
    nota_convivir = 90.0
    nota_prueba_externa = 60.0 if es_bachillerato else 0.0

    if es_bachillerato:
        definitiva = (nota_saber_hacer * 0.70) + (nota_convivir * 0.25) + (nota_prueba_externa * 0.05)
    else:
        definitiva = (nota_saber_hacer * 0.70) + (nota_convivir * 0.30)

    definitiva_val = int(round(definitiva))
    nota_minima = 65
    recuperacion_val = 0
    nivelacion_val = 0

    if definitiva_val >= nota_minima:
        nota_final_val = definitiva_val
    else:
        if recuperacion_val >= nota_minima:
            nota_final_val = recuperacion_val
        else:
            nota_final_val = nivelacion_val if nivelacion_val > 0 else definitiva_val

    st.markdown(f"### Calificaciones: {materia.upper()}")
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
    st.header("📚 Información Académica")
    sub_op = st.selectbox("Seleccione sección:", ["--- Seleccione ---", "Primaria", "Bachillerato", "Sistema de Evaluación"])
    
    if sub_op == "Primaria":
        prim_op = st.selectbox("Seleccione grado:", ["--- Seleccione ---", "Transición", "Primero (1°)", "Segundo (2°)", "Tercero (3°)", "Cuarto (4°)", "Quinto (5°)"])
        if prim_op == "Transición":
            dims = ["Dimensión Socio Afectiva", "Dimensión Comunicativa", "Dimensión Comunicativa Inglés", "Dimensión Cognitiva", "Dimensión Corporal", "Dimensión Artística", "Dimensión Religiosa", "Dimensión Informática", "Dimensión Convivencia"]
            mat_sel = st.selectbox("Seleccione dimensión:", ["--- Seleccione ---"] + dims)
            if mat_sel != "--- Seleccione ---":
                mostrar_tabla_calificaciones(mat_sel, es_bachillerato=False)
        elif prim_op in ["Primero (1°)", "Segundo (2°)", "Tercero (3°)", "Cuarto (4°)", "Quinto (5°)"]:
            mats = ["Matemáticas", "Estadística", "Geometría", "Ciencias Naturales", "Ciencias Sociales", "Ética y Valores", "Cátedra de la Paz", "Artística", "Castellano", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Inglés"]
            mat_sel = st.selectbox("Seleccione materia:", ["--- Seleccione ---"] + mats)
            if mat_sel != "--- Seleccione ---":
                mostrar_tabla_calificaciones(mat_sel, es_bachillerato=False)

    elif sub_op == "Bachillerato":
        bach_op = st.selectbox("Seleccione grado:", ["--- Seleccione ---", "Sexto (6°)", "Séptimo (7°)", "Octavo (8°)", "Noveno (9°)", "Décimo (10°)", "Undécimo (11°)"])
        if bach_op in ["Sexto (6°)", "Séptimo (7°)"]:
            mats = ["Matemáticas", "Estadística", "Geometría", "Ciencias Naturales", "Ciencias Sociales", "Ética y Valores", "Cátedra de la Paz", "Artística", "Lenguaje", "Lectura Crítica", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Inglés"]
        elif bach_op == "Octavo (8°)":
            mats = ["Matemáticas", "Estadística", "Geometría", "Ciencias Naturales", "Historia", "Geografía", "Ética y Valores", "Cátedra de la Paz", "Artística", "Lenguaje", "Lectura Crítica", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Inglés"]
        elif bach_op == "Noveno (9°)":
            mats = ["Matemáticas", "Biología", "Química", "Física", "Historia", "Geografía", "Ética y Valores", "Cátedra de la Paz", "Artística", "Lenguaje", "Lectura Crítica", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Filosofía", "Inglés"]
        elif bach_op in ["Décimo (10°)", "Undécimo (11°)"]:
            mats = ["Matemáticas", "Biología", "Química", "Física", "Ciencias Sociales", "Economía", "Ética y Valores", "Artística", "Lenguaje", "Lectura Crítica", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Filosofía", "Inglés"]
        else:
            mats = []
            
        if mats:
            mat_sel = st.selectbox("Seleccione materia:", ["--- Seleccione ---"] + mats)
            if mat_sel != "--- Seleccione ---":
                mostrar_tabla_calificaciones(mat_sel, es_bachillerato=True)

    elif sub_op == "Sistema de Evaluación":
        st.subheader("Sistema de Evaluación")
        st.write("- **Desempeño Bajo:** Requiere fortalecimiento de los aprendizajes.")
        st.write("- **Desempeño Básico:** Alcanza los aprendizajes fundamentales.")
        st.write("- **Desempeño Alto:** Alcanza satisfactoriamente los aprendizajes.")
        st.write("- **Desempeño Superior:** Demuestra un dominio destacado.")

# ==============================================================================
# MÓDULO 2: PAGOS Y FACTURACIÓN (Actualizado sin gestión de facturación)
# ==============================================================================
elif menu_principal == "2. Pagos y Facturación":
    st.header("💳 Pagos y Facturación")
    op_pagos = st.selectbox("Seleccione opción:", ["--- Seleccione ---", "Pago de Eventos", "Pruebas Saber (Grados 6° a 9°)", "Pruebas Saber y Estado (Grados 10° y 11°)"])
    
    if op_pagos == "Pago de Eventos":
        evento = st.selectbox("Evento:", ["Día de la Familia Javeriana ($80.000)", "Boleta Rifa Institucional ($15.000)"])
        medio = st.selectbox("Medio de pago:", ["Bancolombia (Ahorros # 458-921384-01)", "Nequi (310-892-4102)", "Daviplata (310-892-4102)", "MasterCard"])
        ref = st.text_input("Ingrese la referencia / número de transacción:")
        if st.button("Registrar Pago"):
            if ref:
                st.success(f"[✓] Pago registrado exitosamente por {medio}. Referencia: #{ref}. (Pendiente vinculación a base de datos).")
            else:
                st.warning("⚠️ Debe ingresar una referencia válida.")
                
    elif "Pruebas Saber" in op_pagos:
        st.subheader("Estado de Pruebas Saber")
        st.write("• **Prueba 1 (Diagnóstica):** $35.000 — [P] Pago")
        st.write("• **Prueba 2 (Intermedia):** $35.000 — [PA] Pago Atrasado")
        st.write("• **Prueba 3 (Final):** $35.000 — [D] Deuda Pendiente")
        if "10° y 11°" in op_pagos:
            st.write("• **Prueba Estado Saber 11:** $65.000 — [D] Deuda Pendiente")
        
        p_id = st.selectbox("¿Desea pagar alguna prueba?", ["--- Seleccione ---", "Prueba 1", "Prueba 2", "Prueba 3", "Prueba Estado Saber 11"])
        if p_id != "--- Seleccione ---":
            medio_p = st.selectbox("Medio de pago:", ["Bancolombia", "Nequi", "Daviplata", "MasterCard"])
            ref_p = st.text_input("Referencia de transacción:")
            if st.button("Pagar Prueba"):
                if ref_p:
                    st.success(f"[✓] Pago de {p_id} registrado con éxito con referencia #{ref_p}.")
                else:
                    st.warning("Ingrese una referencia.")

# ==============================================================================
# MÓDULO 3: HORARIOS DE ATENCIÓN Y BIBLIOTECA (Actualizado con cupos y motivos)
# ==============================================================================
elif menu_principal == "3. Horarios de Atención y Biblioteca":
    st.header("⏰ Horarios de Atención y Dependencias")
    op_h = st.selectbox("Seleccione:", ["--- Seleccione ---", "Administración y Secretaría", "Coordinaciones", "Biblioteca Institucional"])
    
    if op_h == "Administración y Secretaría":
        st.write("**Horario de Atención Informativa:** Lunes a Viernes: 8:00 AM - 10:00 AM | 2:00 PM - 4:00 PM")
        st.write("• Contacto: (601) 300-123-4567 | administracion@colegio.edu.co")
        
        st.markdown("---")
        st.subheader("📌 Apartar Cupo - Administración")
        dia_admin = st.selectbox("Seleccione el día:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
        jornada_admin = st.selectbox("Seleccione jornada:", ["--- Seleccione ---", "Mañana", "Tarde"])
        
        if jornada_admin == "Mañana":
            horas_admin = ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM"]
        elif jornada_admin == "Tarde":
            horas_admin = ["2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM"]
        else:
            horas_admin = []
            
        if horas_admin:
            hora_admin = st.selectbox("Seleccione la hora (cupos cada 30 min):", ["--- Seleccione ---"] + horas_admin)
            doc_admin = st.text_input("Documento del acudiente/estudiante:")
            if st.button("Confirmar Reserva en Administración"):
                if dia_admin != "--- Seleccione ---" and hora_admin != "--- Seleccione ---" and doc_admin:
                    st.success(f"[✓] Cupo apartado con éxito en Administración para el día {dia_admin} ({jornada_admin}) a las {hora_admin}.")
                else:
                    st.warning("⚠️ Por favor complete todos los datos para apartar el cupo.")

    elif op_h == "Coordinaciones":
        st.write("**Horario General:** Lunes a Viernes: 8:00 AM - 11:00 AM y 2:00 PM - 4:00 PM")
        
        st.markdown("---")
        st.subheader("📌 Apartar Cupo - Coordinaciones")
        dia_coord = st.selectbox("Seleccione el día:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"], key="d_coord")
        jornada_coord = st.selectbox("Seleccione jornada:", ["--- Seleccione ---", "Mañana", "Tarde"], key="j_coord")
        
        if jornada_coord == "Mañana":
            horas_coord = ["8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM"]
        elif jornada_coord == "Tarde":
            horas_coord = ["2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM"]
        else:
            horas_coord = []
            
        if horas_coord:
            hora_coord = st.selectbox("Seleccione la hora (cupos cada 30 min):", ["--- Seleccione ---"] + horas_coord, key="h_coord")
            nombre_coord_est = st.text_input("Nombre del estudiante / acudiente:")
            if st.button("Confirmar Reserva en Coordinación"):
                if dia_coord != "--- Seleccione ---" and hora_coord != "--- Seleccione ---" and nombre_coord_est:
                    st.success(f"[✓] Cupo apartado con éxito en Coordinación para el día {dia_coord} a las {hora_coord}.")
                else:
                    st.warning("⚠️ Por favor complete todos los campos.")

    elif op_h == "Biblioteca Institucional":
        st.write("**Horario:** Lunes a Viernes: 7:00 AM - 12:00 PM | 1:30 PM - 6:30 PM")
        st.write("**Reglamento:** No está permitido llevar libros a casa. Préstamo interno.")
        
        st.markdown("---")
        st.subheader("📚 Apartar Espacio en Biblioteca")
        sec_bib = st.selectbox("Sección:", ["--- Seleccione ---", "Primaria", "Bachillerato"])
        dia_bib = st.selectbox("Día de la semana:", ["--- Seleccione ---", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"], key="d_bib")
        
        if sec_bib == "Primaria":
            bloques_bib = [
                "1ª Hora (7:00 - 7:50 AM)", "2ª Hora (7:50 - 8:40 AM)", 
                "3ª Hora (8:40 - 9:40 AM)", "4ª Hora (10:00 - 10:50 AM)", 
                "5ª Hora (10:50 - 11:40 AM)", "6ª Hora (11:40 - 12:00 PM)"
            ]
        elif sec_bib == "Bachillerato":
            bloques_bib = [
                "1ª Hora (12:30 - 1:30 PM)", "2ª Hora (1:30 - 2:25 PM)", 
                "3ª Hora (2:25 - 3:20 PM)", "4ª Hora (3:50 - 4:45 PM)", 
                "5ª Hora (4:45 - 5:40 PM)", "6ª Hora (5:40 - 6:30 PM)"
            ]
        else:
            bloques_bib = []
            
        if bloques_bib:
            hora_bib = st.selectbox("Bloque horario de clase:", ["--- Seleccione ---"] + bloques_bib)
            
            # Motivos requeridos antes de guardar
            motivo_bib = st.selectbox("Seleccione el motivo de la reserva:", [
                "--- Seleccione ---",
                "1. Investigación grupal / Trabajo en equipo",
                "2. Lectura y consulta individual",
                "3. Préstamo de material de apoyo pedagógico"
            ])
            
            responsable_bib = st.text_input("Nombre del docente o responsable:")
            
            if st.button("Apartar Espacio en Biblioteca"):
                if dia_bib != "--- Seleccione ---" and hora_bib != "--- Seleccione ---" and motivo_bib != "--- Seleccione ---" and responsable_bib:
                    st.success(f"[✓] Espacio apartado en Biblioteca ({sec_bib}) para el día {dia_bib} en el bloque {hora_bib}.")
                    st.info(f"**Motivo registrado:** {motivo_bib}\n**Responsable:** {responsable_bib}")
                else:
                    st.warning("⚠️ Debe completar todos los campos, incluido el motivo de la reserva.")

# ==============================================================================
# MÓDULO 4: ASESORÍA Y PSICOLOGÍA
# ============================================================
elif menu_principal == "4. Asesoría, Psicología y Bienestar":
    st.header("🧠 Asesoría, Psicología y Bienestar Escolar")
    area = st.selectbox("Seleccione área:", ["--- Seleccione ---", "Psicología Escolar y Orientación", "Fonoaudiología Escolar", "Terapia Ocupacional"])
    
    nombre = st.text_input("Nombre completo del estudiante:")
    grado = st.text_input("Grado (ej. 8°B):")
    contacto = st.text_input("Teléfono o correo de contacto:")
    
    if st.button("Registrar Solicitud / Cita"):
        if nombre and grado and contacto:
            st.success(f"[✓] Solicitud registrada exitosamente para {nombre} ({grado}). El equipo se pondrá en contacto en 24-48 horas.")
        else:
            st.warning("⚠️ Por favor complete todos los campos.")

# ==============================================================================
# MÓDULO 5: QUEJAS, RECLAMOS Y SUGERENCIAS (PQRS)
# ============================================================
elif menu_principal == "5. Quejas, Reclamos y Sugerencias (PQRS)":
    st.header("📝 Quejas, Reclamos y Sugerencias (PQRS)")
    cat = st.selectbox("Categoría:", ["--- Seleccione ---", "Servicios e Infraestructura", "Profesores o Personal de la Institución", "Felicitaciones o Sugerencias de Mejora"])
    
    detalle = st.text_area("Escriba los detalles de su reporte de manera respetuosa:")
    
    if st.button("Enviar Reporte PQRS"):
        if len(detalle) >= 10:
            radicado = f"PQRS-{random.randint(10000, 99999)}"
            st.success(f"[✓] Su mensaje ha sido enviado exitosamente.")
            st.markdown(f"**Número de Radicado:** `{radicado}`")
            st.markdown("💡 *«¡Recuerda que entre todos nos ayudamos a construir una mejor comunidad educativa!»*")
        else:
            st.warning("⚠️ El mensaje es demasiado corto. Por favor proporcione más detalles.")
