import streamlit as st
import json
import pandas as pd
from datetime import datetime
import io

# Configuración de la página
st.set_page_config(page_title="Gestor de Precios", page_icon="💰", layout="wide")

# Inicializar session_state para precios
if 'precios_ingredientes' not in st.session_state:
    st.session_state.precios_ingredientes = {
        # Precios por defecto (puedes personalizarlos)
        "Harina": {"precio": 1500, "unidad": "kg", "categoria": "Básicos"},
        "Azúcar": {"precio": 1200, "unidad": "kg", "categoria": "Básicos"},
        "Huevos": {"precio": 150, "unidad": "unidad", "categoria": "Básicos"},
        "Mantequilla": {"precio": 4500, "unidad": "kg", "categoria": "Lácteos"},
        "Leche": {"precio": 800, "unidad": "litro", "categoria": "Lácteos"},
        "Chocolate": {"precio": 8000, "unidad": "kg", "categoria": "Especiales"},
        "Vainilla": {"precio": 3000, "unidad": "100ml", "categoria": "Especiales"},
    }

if 'lista_activa' not in st.session_state:
    st.session_state.lista_activa = "Principal"

if 'listas_precios' not in st.session_state:
    st.session_state.listas_precios = {
        "Principal": st.session_state.precios_ingredientes.copy()
    }

# Título principal
st.title("💰 Gestor de Precios de Ingredientes")
st.markdown("---")

# Sidebar para gestión de listas
with st.sidebar:
    st.header("📋 Listas de Precios")

    # Selector de lista activa
    lista_seleccionada = st.selectbox(
        "Lista activa:",
        options=list(st.session_state.listas_precios.keys()),
        key="selector_lista"
    )

    if lista_seleccionada != st.session_state.lista_activa:
        st.session_state.lista_activa = lista_seleccionada
        st.session_state.precios_ingredientes = st.session_state.listas_precios[lista_seleccionada].copy()
        st.rerun()

    st.markdown("---")

    # Crear nueva lista
    with st.expander("➕ Nueva Lista"):
        nuevo_nombre = st.text_input("Nombre de la nueva lista:")
        copiar_desde = st.selectbox(
            "Copiar precios de:",
            options=["Vacía"] + list(st.session_state.listas_precios.keys())
        )

        if st.button("Crear Lista"):
            if nuevo_nombre and nuevo_nombre not in st.session_state.listas_precios:
                if copiar_desde == "Vacía":
                    st.session_state.listas_precios[nuevo_nombre] = {}
                else:
                    st.session_state.listas_precios[nuevo_nombre] = st.session_state.listas_precios[copiar_desde].copy()
                st.success(f"✅ Lista '{nuevo_nombre}' creada")
                st.rerun()
            elif nuevo_nombre in st.session_state.listas_precios:
                st.error("⚠️ Ya existe una lista con ese nombre")

    # Eliminar lista
    if len(st.session_state.listas_precios) > 1:
        with st.expander("🗑️ Eliminar Lista"):
            if st.button(f"Eliminar '{st.session_state.lista_activa}'"):
                if st.session_state.lista_activa != "Principal":
                    del st.session_state.listas_precios[st.session_state.lista_activa]
                    st.session_state.lista_activa = "Principal"
                    st.session_state.precios_ingredientes = st.session_state.listas_precios["Principal"].copy()
                    st.success("✅ Lista eliminada")
                    st.rerun()
                else:
                    st.error("⚠️ No se puede eliminar la lista Principal")

    st.markdown("---")

    # Exportar/Importar
    st.header("💾 Respaldo")

    # Exportar JSON
    if st.button("📥 Exportar Precios"):
        datos_export = {
            "fecha_exportacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "listas": st.session_state.listas_precios
        }
        json_str = json.dumps(datos_export, indent=2, ensure_ascii=False)
        st.download_button(
            label="Descargar JSON",
            data=json_str,
            file_name=f"precios_chef_mores_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

    # Importar JSON
    archivo_importar = st.file_uploader("📤 Importar Precios", type=['json'])
    if archivo_importar is not None:
        try:
            datos_import = json.load(archivo_importar)
            if "listas" in datos_import:
                st.session_state.listas_precios = datos_import["listas"]
                st.session_state.precios_ingredientes = st.session_state.listas_precios[st.session_state.lista_activa]
                st.success("✅ Precios importados correctamente")
                st.rerun()
        except Exception as e:
            st.error(f"⚠️ Error al importar: {str(e)}")

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs(["📝 Editar Precios", "➕ Agregar Ingrediente", "📊 Ver Todo", "🔄 Ajuste Masivo"])

# TAB 1: Editar precios
with tab1:
    st.header(f"Editar Precios - Lista: {st.session_state.lista_activa}")

    if not st.session_state.precios_ingredientes:
        st.info("📋 No hay ingredientes en esta lista. Agrega algunos en la pestaña 'Agregar Ingrediente'")
    else:
        # Filtros
        col1, col2 = st.columns([2, 1])
        with col1:
            buscar = st.text_input("🔍 Buscar ingrediente:", "")
        with col2:
            categorias = ["Todas"] + list(set([v["categoria"] for v in st.session_state.precios_ingredientes.values()]))
            filtro_cat = st.selectbox("Filtrar por categoría:", categorias)

        st.markdown("---")

        # Mostrar ingredientes para editar
        ingredientes_filtrados = {
            k: v for k, v in st.session_state.precios_ingredientes.items()
            if (buscar.lower() in k.lower()) and
               (filtro_cat == "Todas" or v["categoria"] == filtro_cat)
        }

        if ingredientes_filtrados:
            for ingrediente, datos in sorted(ingredientes_filtrados.items()):
                with st.expander(f"🥄 {ingrediente} - ₡{datos['precio']:,.0f}/{datos['unidad']}"):
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

                    with col1:
                        nuevo_precio = st.number_input(
                            "Precio (₡):",
                            min_value=0.0,
                            value=float(datos['precio']),
                            step=10.0,
                            key=f"precio_{ingrediente}"
                        )

                    with col2:
                        nueva_unidad = st.text_input(
                            "Unidad:",
                            value=datos['unidad'],
                            key=f"unidad_{ingrediente}"
                        )

                    with col3:
                        nueva_categoria = st.text_input(
                            "Categoría:",
                            value=datos['categoria'],
                            key=f"cat_{ingrediente}"
                        )

                    with col4:
                        st.write("")
                        st.write("")
                        if st.button("💾", key=f"guardar_{ingrediente}"):
                            st.session_state.precios_ingredientes[ingrediente] = {
                                "precio": nuevo_precio,
                                "unidad": nueva_unidad,
                                "categoria": nueva_categoria
                            }
                            st.session_state.listas_precios[st.session_state.lista_activa] = st.session_state.precios_ingredientes.copy()
                            st.success(f"✅ {ingrediente} actualizado")
                            st.rerun()

                    if st.button(f"🗑️ Eliminar {ingrediente}", key=f"eliminar_{ingrediente}"):
                        del st.session_state.precios_ingredientes[ingrediente]
                        st.session_state.listas_precios[st.session_state.lista_activa] = st.session_state.precios_ingredientes.copy()
                        st.success(f"🗑️ {ingrediente} eliminado")
                        st.rerun()
        else:
            st.warning("No se encontraron ingredientes con ese criterio")

# TAB 2: Agregar ingrediente
with tab2:
    st.header("Agregar Nuevo Ingrediente")

    col1, col2 = st.columns(2)

    with col1:
        nombre_nuevo = st.text_input("Nombre del ingrediente:")
        precio_nuevo = st.number_input("Precio (₡):", min_value=0.0, step=10.0)

    with col2:
        unidad_nueva = st.text_input("Unidad de medida:", value="kg")
        categoria_nueva = st.text_input("Categoría:", value="Básicos")

    if st.button("➕ Agregar Ingrediente", type="primary"):
        if nombre_nuevo and precio_nuevo > 0:
            if nombre_nuevo not in st.session_state.precios_ingredientes:
                st.session_state.precios_ingredientes[nombre_nuevo] = {
                    "precio": precio_nuevo,
                    "unidad": unidad_nueva,
                    "categoria": categoria_nueva
                }
                st.session_state.listas_precios[st.session_state.lista_activa] = st.session_state.precios_ingredientes.copy()
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
        # Convertir a DataFrame
        df = pd.DataFrame.from_dict(st.session_state.precios_ingredientes, orient='index')
        df.index.name = 'Ingrediente'
        df['precio'] = df['precio'].apply(lambda x: f"₡{x:,.0f}")
        df = df.sort_values('categoria')

        st.dataframe(df, use_container_width=True)

        # Exportar a CSV
        csv = df.to_csv(encoding='utf-8-sig')
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name=f"precios_{st.session_state.lista_activa}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

        # Estadísticas
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Ingredientes", len(st.session_state.precios_ingredientes))

        with col2:
            categorias_unicas = len(set([v["categoria"] for v in st.session_state.precios_ingredientes.values()]))
            st.metric("Categorías", categorias_unicas)

        with col3:
            precio_promedio = sum([v["precio"] for v in st.session_state.precios_ingredientes.values()]) / len(st.session_state.precios_ingredientes)
            st.metric("Precio Promedio", f"₡{precio_promedio:,.0f}")
    else:
        st.info("📋 No hay ingredientes en esta lista")

# TAB 4: Ajuste masivo
with tab4:
    st.header("Ajuste Masivo de Precios")
    st.markdown("Aplica un porcentaje de aumento o descuento a todos los precios")

    col1, col2 = st.columns(2)

    with col1:
        tipo_ajuste = st.radio("Tipo de ajuste:", ["Aumento", "Descuento"])
        porcentaje = st.number_input("Porcentaje (%):", min_value=0.0, max_value=100.0, value=10.0, step=1.0)

    with col2:
        st.write("")
        st.write("")
        aplicar_a = st.multiselect(
            "Aplicar a categorías:",
            options=["Todas"] + list(set([v["categoria"] for v in st.session_state.precios_ingredientes.values()])),
            default=["Todas"]
        )

    if st.button("🔄 Aplicar Ajuste", type="primary"):
        if porcentaje > 0:
            multiplicador = 1 + (porcentaje/100) if tipo_ajuste == "Aumento" else 1 - (porcentaje/100)

            for ingrediente, datos in st.session_state.precios_ingredientes.items():
                if "Todas" in aplicar_a or datos["categoria"] in aplicar_a:
                    nuevo_precio = datos["precio"] * multiplicador
                    st.session_state.precios_ingredientes[ingrediente]["precio"] = round(nuevo_precio, 2)

            st.session_state.listas_precios[st.session_state.lista_activa] = st.session_state.precios_ingredientes.copy()
            st.success(f"✅ Ajuste del {porcentaje}% aplicado correctamente")
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>💰 Gestor de Precios - Chef More's</p>
    <p style='font-size: 12px;'>Los precios se guardan automáticamente en la sesión actual</p>
</div>
""", unsafe_allow_html=True)
