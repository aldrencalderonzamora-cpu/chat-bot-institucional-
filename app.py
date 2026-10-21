import streamlit as st
import random

st.set_page_config(page_title="Chatbot Institución Educativa", page_icon="🤖", layout="centered")

st.title("🤖 Chatbot de la Institución Educativa")
st.write("Bienvenido al sistema de atención institucional. Selecciona una opción del menú para comenzar:")

# Menú Principal
menu = st.selectbox(
    "Seleccione el módulo que desea consultar:",
    [
        "--- Seleccione una opción ---",
        "1. Información Académica",
        "2. Pagos y Facturación",
        "3. Horarios de Atención y Biblioteca",
        "4. Asesoría, Psicología y Bienestar",
        "5. Quejas, Reclamos y Sugerencias (PQRS)"
    ]
)

if menu == "1. Información Académica":
    st.header("📚 Información Académica")
    nivel = st.selectbox("Seleccione sección:", ["--- Seleccione ---", "Primaria", "Bachillerato", "Sistema de Evaluación"])
    
    if nivel == "Primaria":
        st.subheader("Primaria")
        mat_prim = st.selectbox("Seleccione materia:", ["--- Seleccione ---", "Matemáticas", "Español", "Ciencias", "Inglés"])
        if mat_prim == "Matemáticas":
            st.info("Temas: numeración, operaciones, geometría y resolución de problemas.\nDocente responsable: Ana Martínez.")
        elif mat_prim == "Español":
            st.info("Lectura, escritura, ortografía y comprensión de textos.")
        elif mat_prim == "Ciencias":
            st.info("Seres vivos, ambiente, materia y energía.")
        elif mat_prim == "Ingles":
            st.info("Vocabulario, expresiones básicas y comprensión.")
            
    elif nivel == "Bachillerato":
        st.subheader("Bachillerato")
        st.write("Materias: Matemáticas, ciencias, inglés, tecnología, sociales y lenguaje.")
        st.write("Proyectos de investigación, emprendimiento y servicio social obligatorio.")
        
    elif nivel == "Sistema de Evaluación":
        st.subheader("Sistema de Evaluación")
        st.write("- **Bajo:** Requiere fortalecimiento.")
        st.write("- **Básico:** Alcanza aprendizajes fundamentales.")
        st.write("- **Alto:** Alcanza satisfactoriamente los aprendizajes.")
        st.write("- **Superior:** Demuestra dominio destacado.")

elif menu == "2. Pagos y Facturación":
    st.header("💳 Pagos y Facturación")
    pago_op = st.selectbox("Seleccione gestión:", ["--- Seleccione ---", "Día de la Familia ($80.000)", "Rifa Institucional ($15.000)", "Pruebas Saber"])
    
    if "Día de la Familia" in pago_op or "Rifa" in pago_op:
        concepto = "Día de la Familia" if "Día" in pago_op else "Rifa Institucional"
        medio = st.selectbox("Medio de pago:", ["Bancolombia", "Nequi", "Daviplata", "MasterCard"])
        ref = st.text_input("Ingrese la referencia de pago:")
        if st.button("Registrar Pago"):
            if ref:
                st.success(f"¡Pago de {concepto} registrado con éxito a través de {medio} (Ref: #{ref})!")
            else:
                st.warning("Debe ingresar el número de referencia.")
                
    elif pago_op == "Pruebas Saber":
        st.write("Estado de Pruebas Saber: [P] Pago | [PA] Atrasado | [D] Deuda")
        st.code("Prueba 1 (Diagnóstica) - $35.000 - [P]\nPrueba 2 (Intermedia) - $35.000 - [PA]\nPrueba 3 (Final) - $35.000 - [D]")

elif menu == "3. Horarios de Atención y Biblioteca":
    st.header("⏰ Horarios y Biblioteca")
    dep = st.selectbox("Dependencia:", ["--- Seleccione ---", "Administración y Secretaría", "Coordinaciones", "Biblioteca Institucional"])
    
    if dep == "Administración y Secretaría":
        st.write("Lunes a Viernes: 8:00 AM - 10:00 AM | 2:00 PM - 4:00 PM")
        st.write("Teléfono: (601) 300-123-4567 | Correo: administracion@colegio.edu.co")
    elif dep == "Coordinaciones":
        st.write("Coordinación Académica y Convivencia: Lunes a Viernes de 8:00 AM a 11:00 AM.")
    elif dep == "Biblioteca Institucional":
        st.write("Reglamento: No está permitido llevar libros a casa. Préstamo interno con firma de compromiso.")

elif menu == "4. Asesoría, Psicología y Bienestar":
    st.header("🧠 Psicología y Bienestar Escolar")
    tipo_c = st.selectbox("Servicio:", ["--- Seleccione ---", "Psicología Escolar", "Fonoaudiología", "Terapia Ocupacional"])
    
    nombre_est = st.text_input("Nombre completo del estudiante:")
    grado_est = st.text_input("Grado (ej. 8°B):")
    contacto_est = st.text_input("Teléfono o correo de contacto:")
    
    if st.button("Solicitar Cita / Remisión"):
        if nombre_est and grado_est and contacto_est:
            st.success(f"¡Solicitud registrada para {nombre_est} ({grado_est})! El equipo se pondrá en contacto pronto.")
        else:
            st.warning("Por favor completa todos los campos.")

elif menu == "5. Quejas, Reclamos y Sugerencias (PQRS)":
    st.header("📝 Módulo PQRS")
    cat = st.selectbox("Categoría del reporte:", ["Infraestructura y Aulas", "Personal Docente / Administrativo", "Sugerencias y Felicitaciones"])
    detalle = st.text_area("Describa su novedad de manera respetuosa:")
    
    if st.button("Enviar Reporte PQRS"):
        if len(detalle) >= 10:
            rad = random.randint(10000, 99999)
            st.success(f"¡Reporte enviado con éxito! Su número de radicado es: **PQRS-{rad}**.")
            st.info("«¡Recuerda que entre todos nos ayudamos a construir una mejor comunidad educativa!»")
        else:
            st.warning("El mensaje es muy corto. Por favor proporcione más detalles.")
