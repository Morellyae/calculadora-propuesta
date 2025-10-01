# 📖 Manual de Usuario – Calculadora de Recetas *Chef More’s*

Bienvenida a la herramienta oficial de cálculo de recetas de **Chef More’s**.
Este manual explica paso a paso cómo usar la aplicación, gestionar costos y exportar recetas.

---

## 1️⃣ Inicio de la aplicación
- Abre la aplicación desde:
  👉 [Calculadora Propuesta – Chef More’s](https://calculadora-propuesta-wut98rp3bfmnntjyxdfmwv.streamlit.app)
- En el menú lateral verás las secciones principales:
  - **Cargar Receta**
  - **Costo detallado**
  - **Gestor de Precios**
  - **Exportar Receta**

---

## 2️⃣ Crear una receta
1. Ingresa el **nombre de la receta**.
2. Agrega los **ingredientes** y sus cantidades.
   - Los precios se cargan automáticamente desde la base de costos.
3. Si el ingrediente no existe, añádelo desde el **Gestor de Precios**.

---

## 3️⃣ Consultar costo detallado
La pestaña **“Costo Detallado de la Receta”** muestra:
- Ingredientes y cantidades.
- Precio unitario.
- Subtotal por ingrediente.
- **Costo total** de la receta.

---

## 4️⃣ Gestor de Precios
1. Entra a la pestaña **Gestor de Precios**.
2. Aquí puedes:
   - **Editar precios** de ingredientes existentes.
   - **Agregar nuevos ingredientes** (con nombre y precio).
3. Los cambios se aplican en tiempo real en `st.session_state.COSTOS_ACTUALES`.
4. Opcional: sincronizar con **Firebase** para guardar los cambios y mantenerlos en futuras sesiones.

---

## 5️⃣ Exportar receta
1. Ve a la pestaña **Exportar Receta**.
2. Elige el formato:
   - **Word (.docx)**
   - **PDF (.pdf)**
3. El documento incluye:
   - Logo de *Chef More’s* en la parte superior.
   - Ingredientes, pasos y costos.
   - Pie de página con branding personalizado.

---

## 6️⃣ Ejemplo de uso
1. Crear receta **“Tarta de Chocolate”**.
2. Revisar costos detallados (harina, cacao, mantequilla, azúcar, huevos, etc.).
3. Ajustar el precio del cacao en el Gestor de Precios.
4. Revisar nuevamente el costo total actualizado.
5. Exportar la receta en PDF → se genera con logo y pie de página.

---

## 7️⃣ Notas importantes
- El **logo** aparece automáticamente en la app y en los reportes.
- El **pie de página** está integrado en PDF y Word.
- Si usas Firebase: recuerda **sincronizar antes de cerrar sesión** para no perder cambios.

---

## 📌 Créditos
Desarrollado por **Chef More’s** 👩‍🍳 con apoyo de IA para la gestión de recetas, costos y reportes.
