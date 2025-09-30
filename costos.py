# costos.py
# Diccionario que define el costo por unidad de medida base (g, ml, o unid).
# Los valores son ejemplos. El usuario debe actualizarlos con sus costos reales.
# Moneda: Usamos pesos/unidad (ej. CRC - Costa Rica, MXN - México, etc.)

COSTOS_UNITARIOS = {
    # Lácteos y Grasas
    "Leche": {"unidad_base": "ml", "costo": 0.001},  # Ejemplo: 1 CRC por ml
    "Crema de leche": {"unidad_base": "ml", "costo": 0.003},
    "Mantequilla": {"unidad_base": "g", "costo": 0.008},
    "Queso crema": {"unidad_base": "g", "costo": 0.015},
    "Queso mascarpone": {"unidad_base": "g", "costo": 0.025},
    "Leche condensada": {"unidad_base": "g", "costo": 0.012},
    "Leche evaporada": {"unidad_base": "ml", "costo": 0.002},

    # Secos y Azúcares
    "Azúcar": {"unidad_base": "g", "costo": 0.002},
    "Azúcar glass": {"unidad_base": "g", "costo": 0.003},
    "Harina": {"unidad_base": "g", "costo": 0.0015},
    "Maicena": {"unidad_base": "g", "costo": 0.004},
    "Polvo de hornear": {"unidad_base": "g", "costo": 0.01},
    "Grenetina": {"unidad_base": "g", "costo": 0.05},
    "Cacao en polvo": {"unidad_base": "g", "costo": 0.02},
    "Canela": {"unidad_base": "g", "costo": 0.03},
    "Nueces": {"unidad_base": "g", "costo": 0.05},
    "Galletas trituradas": {"unidad_base": "g", "costo": 0.007},
    "Bizcochos de soletilla": {"unidad_base": "g", "costo": 0.015},

    # Chocolates y Saborizantes
    "Chocolate cobertura": {"unidad_base": "g", "costo": 0.02},
    "Chocolate blanco": {"unidad_base": "g", "costo": 0.025},
    "Chocolate negro": {"unidad_base": "g", "costo": 0.025},
    "Vainilla": {"unidad_base": "ml", "costo": 0.01},
    "Esencia de vainilla": {"unidad_base": "ml", "costo": 0.005},
    "Licor o esencia": {"unidad_base": "ml", "costo": 0.02},
    "Colorante": {"unidad_base": "g", "costo": 0.05},

    # Frutas y otros
    "Huevo": {"unidad_base": "unid", "costo": 0.15},
    "Huevos": {"unidad_base": "unid", "costo": 0.15},
    "Yemas de huevo": {"unidad_base": "unid", "costo": 0.1},
    "Claras de huevo": {"unidad_base": "g", "costo": 0.005}, # Convertimos claras a gramos para precisión
    "Aceite vegetal": {"unidad_base": "ml", "costo": 0.0015},
    "Agua": {"unidad_base": "ml", "costo": 0.0}, # Agua es gratis
    "Sal": {"unidad_base": "g", "costo": 0.001},
    "Zanahoria rallada": {"unidad_base": "g", "costo": 0.003},
    "Plátanos maduros": {"unidad_base": "unid", "costo": 0.25},
    "Jugo de limón": {"unidad_base": "ml", "costo": 0.005},
    "Café fuerte": {"unidad_base": "ml", "costo": 0.002},

    # Bases completas
    "Bizcocho base": {"unidad_base": "base", "costo": 1.5},
    "Masa quebrada": {"unidad_base": "base", "costo": 1.0},
    "base": {"unidad_base": "base", "costo": 1.0}
}
