# app.py
import streamlit as st
import pandas as pd
import json
from recetas import RECETAS
from costos import COSTOS_UNITARIOS
from exporter import export_to_pdf, export_to_docx

# --- Firebase Imports ---
# NOTA: Estas variables globales se inyectan en el entorno de Canvas/Streamlit
firebaseConfig = json.loads(__firebase_config) if '__firebase_config' in locals() else None
initial_auth_token = __initial_auth_token if '__initial_auth_token' in locals() else None
app_id = __app_id if '__app_id' in locals() else 'default-app-id'

# Importaciones condicionales solo si estamos en un entorno con Firebase
if firebaseConfig:
    # Intento de importación con manejo de errores (necesario para Streamlit)
    try:
        from firebase import firebase_app
        from firebase.firebase_app import initializeApp, getAuth, signInWithCustomToken, signInAnonymously
        from firebase.firebase_app import getFirestore, doc, setDoc, getDoc
        from firebase.firebase_app import onAuthStateChanged
    except Exception as e:
        # En caso de que las importaciones directas fallen en Streamlit
        st.error(f"Error al importar módulos de Firebase: {e}")
        firebaseConfig = None # Deshabilitar Firebase si la importación falla
else:
    # Mensaje informativo si las variables globales no están definidas
    # st.warning("Variables de Firebase no detectadas. La persistencia de costos estará deshabilitada.")
    pass

# --- Inicialización de Firebase (Se ejecuta solo una vez) ---
if 'db' not in st.session_state and firebaseConfig:
    try:
        app = initializeApp(firebaseConfig)
        st.session_state.db = getFirestore(app)
        st.session_state.auth = getAuth(app)
        st.session_state.is_auth_ready = False
        st.session_state.user_id = None
        
        # Listener de estado de autenticación
        def auth_state_changed(user):
            st.session_state.is_auth_ready = True
            if user:
                st.session_state.user_id = user.uid
                # st.toast(f"Autenticado: {user.uid[:8]}...")
            else:
                st.session_state.user_id = "anonymous"
                # st.toast("Autenticación anónima.")
            st.rerun()

        onAuthStateChanged(st.session_state.auth, auth_state_changed)

        # Autenticación inicial
        if initial_auth_token:
            # SINTAXIS CORREGIDA: signInWithCustomToken devuelve una Promesa
            st.session_state.auth.signInWithCustomToken(initial_auth_token)
        else:
            # SINTAXIS CORREGIDA: signInAnonymously devuelve una Promesa
            st.session_state.auth.signInAnonymously()
        
    except Exception as e:
        st.error(f"Error al inicializar Firebase: {e}")
        st.session_state.db = None
        st.session_state.auth = None

# =========================================================================
# --- FIREBASE LOGIC FUNCTIONS ---
# =========================================================================

def get_cost_document_ref():
    """Obtiene la referencia al documento de costos privado del usuario."""
    db = st.session_state.get('db')
    user_id = st.session_state.get('user_id')
    
    if db and user_id and user_id != 'anonymous':
        # Ruta de datos privados: /artifacts/{appId}/users/{userId}/costos_unitarios/data
        return doc(db, f"artifacts/{app_id}/users/{user_id}/costos_unitarios/data")
    return None

def load_user_costs():
    """Carga los costos guardados del usuario o usa los valores por defecto."""
    if not st.session_state.get('is_auth_ready'):
        return COSTOS_UNITARIOS # Usar por defecto mientras se autentica

    doc_ref = get_cost_document_ref()
    if doc_ref:
        try:
            doc_snapshot = doc_ref.get()
            if doc_snapshot.exists:
                # Los datos guardados en Firestore reemplazan los por defecto
                saved_costs = doc_snapshot.to_dict().get("COSTOS", {})
                
                # Fusionar con los por defecto para asegurar que todos los ingredientes existan
                merged_costs = COSTOS_UNITARIOS.copy()
                for key, value in saved_costs.items():
                    if key in merged_costs and 'costo' in value:
                         # Solo actualizamos el valor de 'costo', mantenemos 'unidad_base' del archivo local
                        merged_costs[key]['costo'] = value['costo'] 
                return merged_costs
            
        except Exception as e:
            st.error(f"Error al cargar costos desde Firebase: {e}")
            return COSTOS_UNITARIOS # Fallback a por defecto
            
    return COSTOS_UNITARIOS # Si no hay conexión o usuario anónimo

def save_user_costs(current_costs):
    """Guarda los costos actuales del usuario en Firestore."""
    doc_ref = get_cost_document_ref()
    if doc_ref:
        try:
            # Preparamos los datos a guardar (solo necesitamos el costo y la unidad base)
            data_to_save = {k: {"costo": v["costo"], "unidad_base": v["unidad_base"]} for k, v in current_costs.items()}
            
            # Guardamos en la base de datos
            setDoc(doc_ref, {"COSTOS": data_to_save})
            st.success("¡Costos guardados correctamente en la nube!")
        except Exception as e:
            st.error(f"Error al guardar costos en Firebase: {e}")
    else:
        st.warning("No se pudo guardar: La autenticación anónima no permite escritura. Por favor, ingrese con un usuario si desea guardar los costos.")


# =========================================================================
# --- STREAMLIT APP ---
# =========================================================================

st.set_page_config(page_title="Calculadora de Pastelería Profesional", layout="wide")

# Inicializamos st.session_state.COSTOS_ACTUALES si aún no está cargado
if 'COSTOS_ACTUALES' not in st.session_state:
    st.session_state.COSTOS_ACTUALES = COSTOS_UNITARIOS

# Si la autenticación está lista, cargamos los costos del usuario
if st.session_state.get('is_auth_ready') and 'costs_loaded' not in st.session_state:
    st.session_state.COSTOS_ACTUALES = load_user_costs()
    st.session_state.costs_loaded = True # Evitar recarga infinita

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("Chef More's")

# 1. Mostrar Logo (Corregida la advertencia de Streamlit)
try:
    st.sidebar.image("logo.png", use_container_width=True) 
except FileNotFoundError:
    st.sidebar.warning("Logo (logo.png) no encontrado en el repositorio.")

st.sidebar.markdown("---")
st.sidebar.header("Configuración de Receta")

# 2. Selector de Receta
receta = st.sidebar.selectbox("Selecciona una receta", list(RECETAS.keys()))

# 3. Input de Porciones
data = RECETAS[receta]
default_porciones = data.get("porciones", 10)
porcion = st.sidebar.number_input("Número de porciones", min_value=1, value=default_porciones)
st.sidebar.markdown("---")


# =========================================================================
# 4. EDICIÓN Y PERSISTENCIA DE COSTOS
# =========================================================================
with st.sidebar.expander("⚙️ Configurar y Guardar Costos Unitarios"):
    st.caption("Edita los precios a continuación. Los cambios se aplicarán al instante.")

    # Convertir el diccionario de costos actual en un DataFrame
    costos_df = pd.DataFrame([
        {"Ingrediente": k, "Costo (por g/ml/unid)": v["costo"], "Unidad Base": v["unidad_base"]}
        for k, v in st.session_state.COSTOS_ACTUALES.items()
    ])

    # Permitir al usuario editar el DataFrame (guarda en edited_costos_df)
    edited_costos_df = st.data_editor(
        costos_df,
        column_config={
            "Costo (por g/ml/unid)": st.column_config.NumberColumn(
                "Costo (por g/ml/unid)",
                help="Costo por gramo, mililitro o unidad base del ingrediente.",
                min_value=0.0,
                format="$%.5f", # Mostrar hasta 5 decimales para precisión
            ),
            "Ingrediente": st.column_config.TextColumn(disabled=True),
            "Unidad Base": st.column_config.TextColumn(disabled=True),
        },
        hide_index=True,
        num_rows="fixed",
    )

    # Convertir el DataFrame editado de vuelta a un diccionario y actualizar el estado
    new_costos_dict = {}
    for index, row in edited_costos_df.iterrows():
        nombre = row["Ingrediente"]
        costo = row["Costo (por g/ml/unid)"]
        unidad_base = row["Unidad Base"]
        new_costos_dict[nombre] = {"costo": costo, "unidad_base": unidad_base}
    
    # Actualizar el estado de la sesión con los costos editados para el cálculo inmediato
    st.session_state.COSTOS_ACTUALES = new_costos_dict

    # Botón para guardar en Firebase
    if st.button("💾 Guardar Costos en la Nube", type="primary"):
        if st.session_state.get('db') and st.session_state.get('user_id') != 'anonymous':
            save_user_costs(st.session_state.COSTOS_ACTUALES)
        else:
            st.warning("No se puede guardar: Base de datos no conectada o usuario no autenticado (anónimo).")

st.sidebar.markdown("---")


# --- CUERPO PRINCIPAL ---
st.title("🍰 Calculadora de Pastelería Profesional - Chef More's")

st.subheader(f"📌 {receta}")
st.write(data.get("descripcion", "Sin descripción disponible."))

st.markdown("### Ingredientes")
tabla_ingredientes = []
tabla_costos = []
costo_total_receta = 0.0
costo_por_porcion = 0.0 

# Calcular y mostrar tabla
try:
    porciones_base = data.get("porciones", 10)
    factor_escala = porcion / porciones_base
    
    ingredientes_escalados_para_exportar = []

    for ing in data["ingredientes"]:
        nombre_ingrediente = ing["nombre"]
        cantidad_original = ing.get("cantidad", 0)
        unidad_receta = ing.get("unidad", "")
        cantidad_total = cantidad_original * factor_escala

        # --- Lógica de Costos (Usando COSTOS_ACTUALES editables) ---
        costo_info = st.session_state.COSTOS_ACTUALES.get(nombre_ingrediente)
        costo_unitario_ing = 0.0
        costo_total_ing = 0.0

        if costo_info:
            costo_unitario_ing = costo_info["costo"]
            costo_total_ing = cantidad_total * costo_unitario_ing
            costo_total_receta += costo_total_ing
            
            tabla_costos.append([
                nombre_ingrediente,
                f"{cantidad_total:.2f} {unidad_receta}",
                f"${costo_unitario_ing:.5f}",
                f"${costo_total_ing:.2f}"
            ])
        else:
            tabla_costos.append([nombre_ingrediente, "Costo no definido", "", ""])
        # --- Fin Lógica de Costos ---


        # Formatear la cantidad para la tabla de ingredientes
        if unidad_receta.lower() in ["unid", "unidad"]:
            cantidad_str = f"{int(round(cantidad_total))}"
        else:
            cantidad_str = f"{cantidad_total:.2f}"

        tabla_ingredientes.append([nombre_ingrediente, f"{cantidad_str} {unidad_receta}"])
        
        # Guardar la información escalada para pasarla a la función de exportación
        ingredientes_escalados_para_exportar.append({
            "nombre": nombre_ingrediente,
            "cantidad": cantidad_original, 
            "cantidad_escalada": cantidad_total, 
            "unidad": unidad_receta
        })

    # Mostrar Tabla de Ingredientes
    st.table(tabla_ingredientes)

except KeyError as e:
    st.error(f"Error en la estructura de la receta: falta la clave {e}. Verifica recetas.py")
except ZeroDivisionError:
    st.error("La receta base no puede tener cero porciones.")


# 5. Mostrar Costos
st.markdown("---")
st.markdown("### 💰 Costo Detallado de la Receta")

if costo_total_receta > 0:
    costo_por_porcion = costo_total_receta / porcion
    st.markdown(f"""
        **Costo Total de la Receta ({porcion} porciones):** **${costo_total_receta:.2f}** **Costo por Porción:** **${costo_por_porcion:.2f}**
    """)

    # Tabla de Costos
    st.table(
        [['Ingrediente', 'Cantidad Usada', 'Costo Unitario', 'Costo Total']] + tabla_costos
    )

else:
    st.info("Aún no se han definido los costos unitarios para algunos ingredientes.")


# 6. Notas
st.markdown("---")
st.markdown("### 📝 Notas")
nota = st.text_area("Escribe tus observaciones aquí", value=data.get("notas", ""))

# 7. Exportar
st.markdown("### 📂 Exportar Receta")
col1, col2 = st.columns(2)

# Variables para almacenar los bytes de los archivos
pdf_bytes = b''
docx_bytes = b''
pdf_file_name = f"{receta.replace(' ', '_')}_x{porcion}.pdf"
docx_file_name = f"{receta.replace(' ', '_')}_x{porcion}.docx"

# --- GENERAR PDF ---
with col1:
    try:
        pdf_bytes = export_to_pdf(receta, ingredientes_escalados_para_exportar, porcion, nota, costo_total_receta, costo_por_porcion)
        st.download_button(
            label="Descargar PDF",
            data=pdf_bytes,
            file_name=pdf_file_name,
            mime="application/pdf",
            type="primary"
        )
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        st.warning(f"Error interno al generar el PDF. El botón está deshabilitado. Detalles: {e}")
        st.download_button(
            label="Descargar PDF (Error)",
            data=b'',
            file_name="error.pdf",
            mime="application/pdf",
            disabled=True
        )

# --- GENERAR DOCX ---
with col2:
    try:
        docx_bytes = export_to_docx(receta, ingredientes_escalados_para_exportar, porcion, nota, costo_total_receta, costo_por_porcion)
        st.download_button(
            label="Descargar Word (DOCX)",
            data=docx_bytes,
            file_name=docx_file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="secondary"
        )
    except Exception as e:
        print(f"Error al generar DOCX: {e}")
        st.warning(f"Error interno al generar el DOCX. El botón está deshabilitado. Detalles: {e}")
        st.download_button(
            label="Descargar Word (Error)",
            data=b'',
            file_name="error.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            disabled=True
        )
