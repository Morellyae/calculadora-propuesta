# utils.py
# Funciones reutilizables: escalado, moldes, sustituciones, cálculos y helpers GitHub


import math, os, base64, requests
from typing import List, Dict


DEFAULT_PRICE_BY_KG = {
"harina": 1.20, "azúcar":1.40, "mantequilla":8.00, "leche":1.0, "cacao":10.0,
}
DEFAULT_PRICE_BY_UNIT = {"huevo":0.20}


# Escalado por lista de ingredientes
def scale_ingredients_list(ingredients: List[Dict], method: str, target, base_portions: int, egg_w=60):
base_mass = 0.0
base_units = 0.0
for it in ingredients:
u = it.get('unit','g')
q = float(it.get('qty',0))
if u in ('g','ml'):
base_mass += q
elif u in ('kg','l'):
base_mass += q*1000
elif u in ('pcs','u'):
base_mass += q*egg_w
base_units += q
else:
base_mass += q
factor = 1.0
if method == 'Por Peso total (g)':
if base_mass>0: factor = float(target)/base_mass
elif method == 'Por Porciones':
factor = float(target)/float(base_portions) if base_portions>0 else 1.0
else:
if base_units>0: factor = float(target)/base_units
else: factor = float(target)/float(base_portions)
scaled = []
for it in ingredients:
qs = round(float(it.get('qty',0))*factor,3)
scaled.append({**it, 'qtyScaled':qs})
return scaled, factor, base_mass


# apply substitutions (map) to scaled list
def apply_substitutions_to_scaled(scaled_list, substitutions_map):
new_list = []
notes = []
for it in scaled_list:
applied=False
for key,subs in substitutio



