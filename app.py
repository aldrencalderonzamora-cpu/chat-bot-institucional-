import streamlit as st
import random

st.set_page_config(page_title="Chatbot Institución Educativa", page_icon="🤖", layout="centered")

st.title("🤖 Chatbot de la Institución Educativa")
st.write("Bienvenido al sistema de atención institucional.")

# Menú Principal
menu = st.selectbox(
    "Seleccione el módulo que desea consultar:",
    [
        "--- Seleccione una opción ---",
        "1. Información Académica y Calificaciones",
        "2. Pagos, Facturación y Pruebas Saber",
        "3. Horarios de Atención y Biblioteca",
        "4. Asesoría, Psicología y Bienestar",
        "5. Quejas, Reclamos y Sugerencias (PQRS)"
    ]
)

# ============================================================
# MÓDULO 1: INFORMACIÓN ACADÉMICA Y CALIFICACIONES
# ============================================================
if menu == "1. Información Académica y Calificaciones":
    st.header("📚 Módulo de Información Académica")
    
    op_acad = st.selectbox("Seleccione sección:", ["--- Seleccione ---", "Primaria", "Bachillerato", "Sistema de Evaluación"])
    
    if op_acad == "Primaria":
        st.subheader("Grados de Primaria")
        grado_p = st.selectbox("Seleccione el grado:", ["--- Seleccione ---", "Transición", "Primero (1°)", "Segundo (2°)", "Tercero (3°)", "Cuarto (4°)", "Quinto (5°)"])
        
        if grado_p != "--- Seleccione ---":
            if grado_p == "Transición":
                materias = ["Dimensión Socio Afectiva", "Dimensión Comunicativa", "Dimensión Cognitiva", "Dimensión Corporal", "Dimensión Artística"]
            else:
                materias = ["Matemáticas", "Estadística", "Geometría", "Ciencias Naturales", "Ciencias Sociales", "Ética", "Castellano", "Inglés"]
            
            mat_sel = st.selectbox("Seleccione la asignatura a consultar:", ["--- Seleccione ---"] + materias)
            
            if mat_sel != "--- Seleccione ---":
                st.markdown(f"### Calificaciones: {mat_sel.upper()}")
                st.write("**Componentes de evaluación (Primaria):**")
                st.write("- **70%:** Cognitivo y Procedimental (Saber y Hacer) -> Nota: 85")
                st.write("- **30%:** Actitudinal (Convivir) -> Nota: 90")
                st.success("**Definitiva:** 87 (Aprobado)")
                
    elif op_acad == "Bachillerato":
        st.subheader("Grados de Bachillerato")
        grado_b = st.selectbox("Seleccione el grado:", ["--- Seleccione ---", "Sexto (6°)", "Séptimo (7°)", "Octavo (8°)", "Noveno (9°)", "Décimo (10°)", "Undécimo (11°)"])
        
        if grado_b != "--- Seleccione ---":
            materias_b = ["Matemáticas", "Biología", "Química", "Física", "Ciencias Sociales", "Lenguaje", "Lectura Crítica", "Filosofía", "Inglés"]
            mat_b_sel = st.selectbox("Seleccione la asignatura:", ["--- Seleccione ---"] + materias_b)
            
            if mat_b_sel != "--- Seleccione ---":
                st.markdown(f"### Calificaciones: {mat_b_sel.upper()}")
                st.write("**Componentes de evaluación (Bachillerato):**")
                st.write("- **70%:** Cognitivo y Procedimental (Saber y Hacer) -> Nota: 85")
                st.write("- **25%:** Actitudinal (Convivir) -> Nota: 90")
                st.write("- **5%:** Cognitivo (Prueba Externa) -> Nota: 60")
                st.success("**Definitiva:** 83 (Aprobado)")

    elif op_acad == "Sistema de Evaluación":
        st.subheader("Sistema de Evaluación Institucional")
        st.write("- **Desempeño Bajo:** Requiere fortalecimiento de los aprendizajes.")
        st.write("- **Desempeño Básico:** Alcanza los aprendizajes fundamentales.")
        st.write("- **Desempeño Alto:** Alcanza satisfactoriamente los aprendizajes.")
        st.write("- **Desempeño Superior:** Demuestra un dominio destacado.")

# ============================================================
# MÓDULO 2: PAGOS Y FACTURACIÓN
# ============================================================
elif menu == "2. Pagos, Facturación y Pruebas Saber":
    st.header("💳 Pagos y Facturación")
    
    op_pagos = st.selectbox("Seleccione servicio:", ["--- Seleccione ---", "Pago de Eventos (Día de la Familia / Rifas)", "Estado de Pruebas Saber (6° a 9°)", "Pruebas Saber y Estado (10° y 11°)"])
    
    if op_pagos == "Pago de Eventos (Día de la Familia / Rifas)":
        evento = st.selectbox("Concepto:", ["Día de la Familia Javeriana ($80.000)", "Boleta Rifa Institucional ($15.000)"])
        medio = st.selectbox("Medio de pago:", ["Bancolombia (Ahorros # 458-921384-01)", "Nequi (310-892-4102)", "Daviplata (310-892-4102)", "MasterCard"])
        ref = st.text_input("Ingrese la referencia de la transacción:")
        if st.button("Confirmar Pago"):
            if ref:
                st.success(f"[✓] Pago registrado exitosamente por {medio}. Referencia: #{ref}. En verificación por Tesorería.")
            else:
                st.warning("Debe ingresar el número de referencia.")
                
    elif "Pruebas Saber" in op_pagos:
        st.subheader("Estado de Pruebas Saber")
        st.write("• **Prueba 1 (Diagnóstica):** $35.000 — [P] Pago")
        st.write("• **Prueba 2 (Intermedia):** $35.000 — [PA] Pago Atrasado")
        st.write("• **Prueba 3 (Final):** $35.000 — [D] Deuda Pendiente")
        if "10° y 11°" in op_pagos:
            st.write("• **Prueba Estado Saber 11:** $65.000 — [D] Deuda Pendiente")

# ============================================================
# MÓDULO 3: HORARIOS Y BIBLIOTECA
# ============================================================
elif menu == "3. Horarios de Atención y Biblioteca":
    st.header("⏰ Horarios de Atención y Dependencias")
    
    op_h = st.selectbox("Seleccione dependencia:", ["--- Seleccione ---", "Administración y Secretaría", "Coordinaciones", "Biblioteca Institucional"])
    
    if op_h == "Administración y Secretaría":
        st.write("**Horario:** Lunes a Viernes: 8:00 AM - 10:00 AM | 2:00 PM - 4:00 PM")
        st.write("**Teléfono:** (601) 300-123-4567 | **WhatsApp:** +57 310 987 6543")
    elif op_h == "Coordinaciones":
        st.write("**Coordinación Académica:** Prof. Roberto Gómez")
        st.write("**Coordinación de Convivencia:** Dra. María Fernanda López")
    elif op_h == "Biblioteca Institucional":
        st.write("**Norma:** No está permitido llevar libros a casa. Préstamo interno con libro de registro.")
        st.info("Espacios de biblioteca disponibles de lunes a viernes.")

# ============================================================
# MÓDULO 4: ASESORÍA Y PSICOLOGÍA
# ============================================================
elif menu == "4. Asesoría, Psicología y Bienestar":
    st.header("🧠 Asesoría, Psicología y Bienestar Escolar")
    
    servicio = st.selectbox("Área:", ["--- Seleccione ---", "Psicología Escolar", "Fonoaudiología", "Terapia Ocupacional"])
    
    nombre = st.text_input("Nombre completo del estudiante:")
    grado = st.text_input("Grado (ej. 8°B):")
    contacto = st.text_input("Teléfono o correo de contacto:")
    
    if st.button("Enviar Solicitud"):
        if nombre and grado and contacto:
            st.success(f"[✓] Solicitud registrada para {nombre} ({grado}). El equipo se comunicará en 24-48 horas.")
        else:
            st.warning("Por favor complete todos los campos obligatorios.")

# ============================================================
# MÓDULO 5: QUEJAS, RECLAMOS Y SUGERENCIAS (PQRS)
# ============================================================
elif menu == "5. Quejas, Reclamos y Sugerencias (PQRS)":
    st.header("📝 Módulo PQRS")
    
    cat = st.selectbox("Categoría:", ["Infraestructura y Aulas", "Profesores y Personal Institucional", "Felicitaciones o Sugerencias"])
    detalle = st.text_area("Escriba los detalles de su reporte de manera respetuosa:")
    
    if st.button("Enviar PQRS"):
        if len(detalle) >= 10:
            radicado = random.randint(10000, 99999)
            st.success(f"[✓] Mensaje guardado exitosamente. Su número de radicado es: **PQRS-{radicado}**.")
            st.info("💡 «¡Recuerda que entre todos nos ayudamos a construir una mejor comunidad educativa!»")
        else:
            st.warning("El mensaje es muy corto. Por favor proporcione más detalles.")
