import streamlit as st
import json
import pandas as pd
from datetime import datetime
from costos import COSTOS_UNITARIOS

st.set_page_config(page_title="Gestor de Precios", page_icon="💰", layout="wide")

# Sincronizar con el estado global de app.py
if 'COSTOS_ACTUALES' not in st.session_state:
    st.session_state.COSTOS_ACTUALES = COSTOS_UNITARIOS.copy()

if 'precios_ingredientes' not in st.session_state:
    # Convertir formato de COSTOS_UNITARIOS al formato del gestor
    st.session_state.precios_ingredientes = {}
    for nombre, datos in st.session_state.COSTOS_ACTUALES.items():
        st.session_state.precios_ingredientes[nombre] = {
            "precio": datos["costo"],
            "unidad": datos["unidad_base"],
            "categoria": "General"
        }

# Función para sincronizar cambios con COSTOS_ACTUALES
def sync_to_costos_actuales():
    """Sincroniza los cambios del gestor con COSTOS_ACTUALES"""
    for nombre, datos in st.session_state.precios_ingredientes.items():
        if nombre in st.session_state.COSTOS_ACTUALES:
            st.session_state.COSTOS_ACTUALES[nombre]["costo"] = datos["precio"]
        else:
            # Agregar nuevo ingrediente
            st.session_state.COSTOS_ACTUALES[nombre] = {
                "costo": datos["precio"],
                "unidad_base": datos["unidad"]
            }

st.title("💰 Gestor de Precios de Ingredientes")
st.info("Los cambios aquí se reflejarán automáticamente en la calculadora principal")
st.markdown("---")

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📝 Editar Precios", "➕ Agregar Ingrediente", "📊 Ver Todo"])

# TAB 1: Editar precios
with tab1:
    st.header("Editar Precios de Ingredientes")
    
    if not st.session_state.precios_ingredientes:
        st.info("No hay ingredientes. Agrega algunos en la pestaña 'Agregar Ingrediente'")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            buscar = st.text_input("🔍 Buscar ingrediente:", "")
        
        st.markdown("---")
        
        ingredientes_filtrados = {
            k: v for k, v in st.session_state.precios_ingredientes.items()
            if buscar.lower() in k.lower()
        }
        
        if ingredientes_filtrados:
            for ingrediente, datos in sorted(ingredientes_filtrados.items()):
                with st.expander(f"🥄 {ingrediente} - ${datos['precio']:.5f}/{datos['unidad']}"):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        nuevo_precio = st.number_input(
                            "Precio ($):",
                            min_value=0.0,
                            value=float(datos['precio']),
                            step=0.00001,
                            format="%.5f",
                            key=f"precio_{ingrediente}"
                        )
                    
                    with col2:
                        nueva_unidad = st.text_input(
                            "Unidad:",
                            value=datos['unidad'],
                            key=f"unidad_{ingrediente}"
                        )
                    
                    with col3:
                        st.write("")
                        st.write("")
                        if st.button("💾 Guardar", key=f"guardar_{ingrediente}"):
                            st.session_state.precios_ingredientes[ingrediente]["precio"] = nuevo_precio
                            st.session_state.precios_ingredientes[ingrediente]["unidad"] = nueva_unidad
                            sync_to_costos_actuales()
                            st.success(f"✅ {ingrediente} actualizado")
                            st.rerun()
                    
                    if st.button(f"🗑️ Eliminar {ingrediente}", key=f"eliminar_{ingrediente}"):
                        del st.session_state.precios_ingredientes[ingrediente]
                        if ingrediente in st.session_state.COSTOS_ACTUALES:
                            del st.session_state.COSTOS_ACTUALES[ingrediente]
                        st.success(f"🗑️ {ingrediente} eliminado")
                        st.rerun()
        else:
            st.warning("No se encontraron ingredientes")

# TAB 2: Agregar ingrediente
with tab2:
    st.header("Agregar Nuevo Ingrediente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre_nuevo = st.text_input("Nombre del ingrediente:")
        precio_nuevo = st.number_input("Precio ($):", min_value=0.0, step=0.00001, format="%.5f")
    
    with col2:
        unidad_nueva = st.text_input("Unidad de medida:", value="g")
        categoria_nueva = st.text_input("Categoría:", value="General")
    
    if st.button("➕ Agregar Ingrediente", type="primary"):
        if nombre_nuevo and precio_nuevo >= 0:
            if nombre_nuevo not in st.session_state.precios_ingredientes:
                st.session_state.precios_ingredientes[nombre_nuevo] = {
                    "precio": precio_nuevo,
                    "unidad": unidad_nueva,
                    "categoria": categoria_nueva
                }
                sync_to_costos_actuales()
                st.success(f"✅ {nombre_nuevo} agregado correctamente")
                st.rerun()
            else:
                st.error("⚠️ Ya existe un ingrediente con ese nombre")
        else:
            st.error("⚠️ Complete todos los campos")

# TAB 3: Ver todo
with tab3:
    st.header("Lista Completa de Ingredientes")
    
    if st.session_state.precios_ingredientes:
        df = pd.DataFrame.from_dict(st.session_state.precios_ingredientes, orient='index')
        df.index.name = 'Ingrediente'
        df['precio'] = df['precio'].apply(lambda x: f"${x:.5f}")
        
        st.dataframe(df, use_container_width=True)
        
        # Estadísticas
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Ingredientes", len(st.session_state.precios_ingredientes))
        
        with col2:
            precios_valores = [v["precio"] for v in st.session_state.precios_ingredientes.values()]
            precio_promedio = sum(precios_valores) / len(precios_valores) if precios_valores else 0
            st.metric("Precio Promedio", f"${precio_promedio:.5f}")
        
        # Exportar JSON
        if st.button("📥 Exportar Precios (JSON)"):
            datos_export = {
                "fecha_exportacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ingredientes": st.session_state.precios_ingredientes
            }
            json_str = json.dumps(datos_export, indent=2, ensure_ascii=False)
            st.download_button(
                label="Descargar JSON",
                data=json_str,
                file_name=f"precios_chef_mores_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    else:
        st.info("No h
                  
