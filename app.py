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
def mostrar_tabla_calificaciones(materia, grado_nombre, es_bachillerato=False):
    # Simulando notas variadas según el estudiante/grado de ejemplo
    nota_saber_hacer = 78.0 if "Transición" in grado_nombre else 85.0
    nota_convivir = 80.0
    nota_prueba_externa = 60.0 if es_bachillerato else 0.0

    if es_bachillerato:
        definitiva = (nota_saber_hacer * 0.70) + (nota_convivir * 0.25) + (nota_prueba_externa * 0.05)
    else:
        definitiva = (nota_saber_hacer * 0.70) + (nota_convivir * 0.30)

    definitiva_val = int(round(definitiva))
    nota_minima = 65
    
    # Estados de ejemplo variados (algunos ganan, otros recuperan, otros nivelan)
    if "Matemáticas" in materia and es_bachillerato:
        recuperacion_val = 68  # Recuperó y pasó
        nivelacion_val = 0
        nota_final_val = recuperacion_val
    elif definitiva_val < nota_minima:
        recuperacion_val = 55
        nivelacion_val = 70   # Niveló y pasó
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
    st.header("📚 Información Académica")
    sub_op = st.selectbox("Seleccione sección:", ["--- Seleccione ---", "Primaria", "Bachillerato", "Sistema de Evaluación"])
    
    if sub_op == "Primaria":
        prim_op = st.selectbox("Seleccione grado:", ["--- Seleccione ---", "Transición", "Primero (1°)", "Segundo (2°)", "Tercero (3°)", "Cuarto (4°)", "Quinto (5°)"])
        if prim_op == "Transición":
            dims = ["Dimensión Socio Afectiva", "Dimensión Comunicativa", "Dimensión Comunicativa Inglés", "Dimensión Cognitiva", "Dimensión Corporal", "Dimensión Artística", "Dimensión Religiosa", "Dimensión Informática", "Dimensión Convivencia"]
            mat_sel = st.selectbox("Seleccione dimensión:", ["--- Seleccione ---"] + dims)
            if mat_sel != "--- Seleccione ---":
                mostrar_tabla_calificaciones(mat_sel, "Transición", es_bachillerato=False)
        elif prim_op in ["Primero (1°)", "Segundo (2°)", "Tercero (3°)", "Cuarto (4°)", "Quinto (5°)"]:
            mats = ["Matemáticas", "Estadística", "Geometría", "Ciencias Naturales", "Ciencias Sociales", "Ética y Valores", "Cátedra de la Paz", "Artística", "Castellano", "Convivencia", "Educación Física", "Tecnología", "Educación Religiosa", "Inglés"]
            mat_sel = st.selectbox("Seleccione materia:", ["--- Seleccione ---"] + mats)
            if mat_sel != "--- Seleccione ---":
                mostrar_tabla_calificaciones(mat_sel, prim_op, es_bachillerato=False)

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
                mostrar_tabla_calificaciones(mat_sel, bach_op, es_bachillerato=True)

    elif sub_op == "Sistema de Evaluación":
        st.subheader("Sistema de Evaluación")
        st.write("- **Desempeño Bajo:** Requiere fortalecimiento de los aprendizajes.")
        st.write("- **Desempeño Básico:** Alcanza los aprendizajes fundamentales.")
        st.write("- **Desempeño Alto:** Alcanza satisfactoriamente los aprendizajes.")
        st.write("- **Desempeño Superior:** Demuestra un dominio destacado.")

# ==============================================================================
# MÓDULO 2: PAGOS Y FACTURACIÓN (Con filtro de grado para Pruebas Saber)
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
        medio = st.selectbox("Medio de pago:", ["Bancolombia (Ahorros # 458-921384-01)", "Nequi (310-892-4102)", "Daviplata (310-892-4102)", "MasterCard"])
        ref = st.text_input("Ingrese la referencia / número de transacción:")
        
        if st.button("Registrar Pago"):
            if doc_estudiante and ref:
                st.success(f"[✓] Pago registrado para el documento {doc_estudiante} vía {medio}. Ref: #{ref}. (Listo para Base de Datos).")
            else:
                st.warning("⚠️ Debe ingresar el documento del estudiante y una referencia válida.")
                
    elif op_pagos == "Pruebas Saber (Grados 6° a 9°)":
        st.subheader("📚 Pruebas Saber (Grados 6° a 9°)")
        grado_saber = st.selectbox("Seleccione el grado:", ["--- Seleccione ---", "6° (Sexto)", "7° (Séptimo)", "8° (Octavo)", "9° (Noveno)"])
        
        if grado_saber != "--- Seleccione ---":
            st.write("• **Costo total de las 3 pruebas:** $30.000 COP")
            st.write("  - Prueba 1 (Diagnóstica): $10.000 — [P] Pagado")
            st.write("  - Prueba 2 (Intermedia): $10.000 — [D] Deuda Pendiente")
            st.write("  - Prueba 3 (Final): $10.000 — [D] Deuda Pendiente")
            
            p_saber_sel = st.selectbox("Seleccione la prueba a pagar:", ["--- Seleccione ---", "Prueba 2 (Intermedia) - $10.000", "Prueba 3 (Final) - $10.000"])
            if p_saber_sel != "--- Seleccione ---":
                medio_s = st.selectbox("Medio de pago:", ["Bancolombia", "Nequi", "Daviplata", "MasterCard"])
                ref_s = st.text_input("Referencia de transacción:")
                if st.button("Pagar Prueba Saber"):
                    if doc_estudiante and ref_s:
                        st.success(f"[✓] Pago de {p_saber_sel} registrado para el documento {doc_estudiante} en {grado_saber} con ref #{ref_s}.")
                    else:
                        st.warning("⚠️ Ingrese el documento del estudiante y la referencia de pago.")
                        
    elif op_pagos == "Preicfes y Pruebas ICFES (Grados 10° y 11°)":
        st.subheader("🎓 Preicfes y Pruebas ICFES (Grados 10° y 11°)")
        grado_pre = st.selectbox("Seleccione el grado:", ["--- Seleccione ---", "10° (Décimo)", "11° (Undécimo)"])
        
        if grado_pre != "--- Seleccione ---":
            st.write("• **Costo total acumulado:** $270.000 COP (4 pruebas en total)")
            st.write("  - Preicfes Sesión 1: $45.000 — [P] Pagado")
            st.write("  - Preicfes Sesión 2: $45.000 — [PA] Pago Atrasado")
            st.write("  - Preicfes Sesión 3: $45.000 — [D] Deuda Pendiente")
            st.write("  - Examen Oficial ICFES: $135.000 — [D] Deuda Pendiente (Costo mayor)")
            
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
                        st.success(f"[✓] Pago de {p_pre_sel} registrado para el documento {doc_estudiante} en {grado_pre} con ref #{ref_p}.")
                    else:
                        st.warning("⚠️ Ingrese el documento del estudiante y la referencia de pago.")
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
                    st.success(f"[✓] Cupo apartado en Administración para el día {dia_admin} ({jornada_admin}) a las {hora_admin}. (Listo para DB)")
                else:
                    st.warning("⚠️ Por favor complete todos los datos.")

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
                    st.success(f"[✓] Cupo apartado en Coordinación para el día {dia_coord} ({jornada_coord}) a las {hora_coord}. (Listo para DB)")
                else:
                    st.warning("⚠️ Por favor complete todos los campos.")

    elif op_h == "Biblioteca Institucional":
        st.write("**Horario:** Lunes a Viernes: 7:00 AM - 12:00 PM | 1:30 PM - 6:30 PM")
        
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
            motivo_bib = st.selectbox("Seleccione el motivo de la reserva:", [
                "--- Seleccione ---",
                "1. Investigación grupal / Trabajo en equipo",
                "2. Lectura y consulta individual",
                "3. Préstamo de material de apoyo pedagógico"
            ])
            responsable_bib = st.text_input("Nombre del docente o responsable:")
            
            if st.button("Apartar Espacio en Biblioteca"):
                if dia_bib != "--- Seleccione ---" and hora_bib != "--- Seleccione ---" and motivo_bib != "--- Seleccione ---" and responsable_bib:
                    st.success(f"[✓] Espacio apartado en Biblioteca ({sec_bib}) el día {dia_bib} en el bloque {hora_bib}.")
                    st.info(f"**Motivo:** {motivo_bib}\n**Responsable:** {responsable_bib}")
                else:
                    st.warning("⚠️ Debe completar todos los campos, incluido el motivo.")

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
            st.success(f"[✓] Solicitud de cita guardada para {nombre} ({grado}). El equipo se pondrá en contacto en 24-48 horas.")
        else:
            st.warning("⚠️ Por favor complete todos los campos.")

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
            st.success(f"[✓] Su mensaje ha sido registrado exitosamente.")
            st.markdown(f"**Número de Radicado:** `{radicado}`")
            st.markdown("💡 *«¡Recuerda que entre todos nos ayudamos a construir una mejor comunidad educativa!»*")
        else:
            st.warning("⚠️ Asegúrese de llenar la subcategoría y que el detalle tenga al menos 10 caracteres.")
