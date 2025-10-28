# Diccionario que contiene todas las recetas y sus propiedades
RECETAS = {
    "Crema Pastelera": {
        "descripcion": "Clásica crema para rellenar tartas y postres.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Leche", "cantidad": 1000, "unidad": "ml"},
            {"nombre": "Azúcar", "cantidad": 200, "unidad": "g"},
            {"nombre": "Yemas de huevo", "cantidad": 8, "unidad": "unid"},
            {"nombre": "Maicena", "cantidad": 80, "unidad": "g"},
            {"nombre": "Vainilla", "cantidad": 10, "unidad": "ml"},
        ],
        "notas": "Cocinar a fuego medio sin dejar de mover."
    },
    "Ganache de Chocolate": {
        "descripcion": "Ganache clásico para coberturas y rellenos.",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Chocolate cobertura", "cantidad": 500, "unidad": "g"},
            {"nombre": "Crema de leche", "cantidad": 250, "unidad": "ml"},
            {"nombre": "Mantequilla", "cantidad": 50, "unidad": "g"},
        ],
        "notas": "Emulsionar bien hasta obtener textura brillante."
    },
    "Brillo Espejo": {
        "descripcion": "Glaseado brillante para tortas modernas.",
        "porciones": 15,
        "ingredientes": [
            {"nombre": "Agua", "cantidad": 150, "unidad": "ml"},
            {"nombre": "Azúcar", "cantidad": 300, "unidad": "g"},
            {"nombre": "Leche condensada", "cantidad": 200, "unidad": "g"},
            {"nombre": "Chocolate blanco", "cantidad": 300, "unidad": "g"},
            {"nombre": "Grenetina", "cantidad": 12, "unidad": "g"},
            {"nombre": "Colorante", "cantidad": 5, "unidad": "g"},
        ],
        "notas": "Usar tibio para cubrir sin dañar el producto."
    },
    "Bizcocho Genovés": {
        "descripcion": "Bizcocho esponjoso base para pasteles.",
        "porciones": 8,
        "ingredientes": [
            {"nombre": "Huevos", "cantidad": 4, "unidad": "unid"},
            {"nombre": "Azúcar", "cantidad": 120, "unidad": "g"},
            {"nombre": "Harina", "cantidad": 120, "unidad": "g"},
        ],
        "notas": "Batir aireadamente para lograr volumen."
    },
    "Torta de Zanahoria": {
        "descripcion": "Pastel húmedo con zanahoria y especias.",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Zanahoria rallada", "cantidad": 300, "unidad": "g"},
            {"nombre": "Harina", "cantidad": 250, "unidad": "g"},
            {"nombre": "Azúcar", "cantidad": 200, "unidad": "g"},
            {"nombre": "Aceite vegetal", "cantidad": 150, "unidad": "ml"},
            {"nombre": "Huevos", "cantidad": 3, "unidad": "unid"},
            {"nombre": "Polvo de hornear", "cantidad": 10, "unidad": "g"},
            {"nombre": "Canela", "cantidad": 5, "unidad": "g"},
        ],
        "notas": "Añadir nueces o especias si deseas."
    },
    "Merengue Italiano": {
        "descripcion": "Merengue estable con almíbar caliente.",
        "porciones": 15,
        "ingredientes": [
            {"nombre": "Claras de huevo", "cantidad": 150, "unidad": "g"},
            {"nombre": "Azúcar", "cantidad": 300, "unidad": "g"},
            {"nombre": "Agua", "cantidad": 80, "unidad": "ml"},
        ],
        "notas": "Verter almíbar caliente lentamente mientras se bate."
    },
    "Masa Quebrada": {
        "descripcion": "Base crujiente para tartas y quiches.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Harina", "cantidad": 250, "unidad": "g"},
            {"nombre": "Mantequilla fría", "cantidad": 125, "unidad": "g"},
            {"nombre": "Azúcar", "cantidad": 50, "unidad": "g"},
            {"nombre": "Huevo", "cantidad": 1, "unidad": "unid"},
        ],
        "notas": "Refrigerar antes de estirar."
    },
    "Masa Hojaldre": {
        "descripcion": "Masa laminada para versiones hojaldradas.",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Harina", "cantidad": 500, "unidad": "g"},
            {"nombre": "Mantequilla", "cantidad": 400, "unidad": "g"},
            {"nombre": "Agua", "cantidad": 250, "unidad": "ml"},
            {"nombre": "Sal", "cantidad": 10, "unidad": "g"},
        ],
        "notas": "Realizar pliegues con descanso entre cada vuelta."
    },
    "Sirope Básico": {
        "descripcion": "Almíbar para humedecer bizcochos.",
        "porciones": 20,
        "ingredientes": [
            {"nombre": "Azúcar", "cantidad": 200, "unidad": "g"},
            {"nombre": "Agua", "cantidad": 200, "unidad": "ml"},
            {"nombre": "Licor o esencia", "cantidad": 10, "unidad": "ml"},
        ],
        "notas": "Enfriar antes de aplicar sobre la torta."
    },
    "Flan de Vainilla": {
        "descripcion": "Postre cremoso clásico de vainilla.",
        "porciones": 8,
        "ingredientes": [
            {"nombre": "Leche", "cantidad": 500, "unidad": "ml"},
            {"nombre": "Huevos", "cantidad": 4, "unidad": "unid"},
            {"nombre": "Azúcar", "cantidad": 120, "unidad": "g"},
            {"nombre": "Vainilla", "cantidad": 10, "unidad": "ml"},
        ],
        "notas": "Cocinar en baño maría hasta que cuaje y enfriar."
    },
    "Buttercream": {
        "descripcion": "Crema dulce de mantequilla ideal para decorar.",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Mantequilla", "cantidad": 250, "unidad": "g"},
            {"nombre": "Azúcar glass", "cantidad": 400, "unidad": "g"},
            {"nombre": "Esencia de vainilla", "cantidad": 10, "unidad": "ml"},
            {"nombre": "Leche", "cantidad": 30, "unidad": "ml"},
        ],
        "notas": "Batir hasta quedar aireada y suave."
    },
    "Pan de Plátano": {
        "descripcion": "Bizcocho con sabor a plátano maduro.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Plátanos maduros", "cantidad": 3, "unidad": "unid"},
            {"nombre": "Harina", "cantidad": 200, "unidad": "g"},
            {"nombre": "Azúcar", "cantidad": 150, "unidad": "g"},
            {"nombre": "Mantequilla", "cantidad": 100, "unidad": "g"},
            {"nombre": "Huevos", "cantidad": 2, "unidad": "unid"},
            {"nombre": "Polvo de hornear", "cantidad": 10, "unidad": "g"},
            {"nombre": "Canela", "cantidad": 5, "unidad": "g"},
        ],
        "notas": "Agregar nueces o chips al gusto."
    },
    # Recetas nuevas
    "Cheesecake": {
        "descripcion": "Tarta cremosa con base de galletas y relleno de queso.",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Galletas trituradas", "cantidad": 200, "unidad": "g"},
            {"nombre": "Mantequilla", "cantidad": 100, "unidad": "g"},
            {"nombre": "Queso crema", "cantidad": 500, "unidad": "g"},
            {"nombre": "Azúcar", "cantidad": 150, "unidad": "g"},
            {"nombre": "Huevos", "cantidad": 3, "unidad": "unid"},
            {"nombre": "Esencia de vainilla", "cantidad": 10, "unidad": "ml"},
        ],
        "notas": "Hornear base primero y luego agregar relleno."
    },
    "Pie de Limón": {
        "descripcion": "Tarta cítrica con relleno cremoso de limón.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Masa quebrada", "cantidad": 1, "unidad": "base"},
            {"nombre": "Leche condensada", "cantidad": 400, "unidad": "g"},
            {"nombre": "Jugo de limón", "cantidad": 150, "unidad": "ml"},
            {"nombre": "Huevos", "cantidad": 3, "unidad": "unid"},
            {"nombre": "Azúcar", "cantidad": 150, "unidad": "g"},
        ],
        "notas": "Gratinar el merengue solo al final."
    },
    "Brownies": {
        "descripcion": "Postre chocolateado húmedo y denso.",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Chocolate negro", "cantidad": 200, "unidad": "g"},
            {"nombre": "Mantequilla", "cantidad": 150, "unidad": "g"},
            {"nombre": "Azúcar", "cantidad": 200, "unidad": "g"},
            {"nombre": "Huevos", "cantidad": 3, "unidad": "unid"},
            {"nombre": "Harina", "cantidad": 100, "unidad": "g"},
            {"nombre": "Nueces", "cantidad": 50, "unidad": "g"},
        ],
        "notas": "No cocinar demasiado para mantenerlo húmedo."
    },
    "Tres Leches": {
        "descripcion": "Bizcocho bañado en tres tipos de leche (evaporada, condensada y crema).",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Bizcocho base", "cantidad": 1, "unidad": "base"},
            {"nombre": "Leche evaporada", "cantidad": 200, "unidad": "ml"},
            {"nombre": "Leche condensada", "cantidad": 200, "unidad": "ml"},
            {"nombre": "Crema de leche", "cantidad": 200, "unidad": "ml"},
            {"nombre": "Azúcar", "cantidad": 50, "unidad": "g"},
        ],
        "notas": "Empapar con mezcla y refrigerar."
    },
   "Tiramisú": {
        "descripcion": "Postre italiano en capas con café y queso.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Bizcochos de soletilla", "cantidad": 200, "unidad": "g"},
            {"nombre": "Café fuerte", "cantidad": 200, "unidad": "ml"},
            {"nombre": "Queso mascarpone", "cantidad": 400, "unidad": "g"},
            {"nombre": "Huevos", "cantidad": 3, "unidad": "unid"},
            {"nombre": "Azúcar", "cantidad": 100, "unidad": "g"},
            {"nombre": "Cacao en polvo", "cantidad": 20, "unidad": "g"},
        ],
        "notas": "Reposar al menos 4 horas antes de servir."
    },
    "Torta de Calabaza": {
        "descripcion": "Torta húmeda y aromática de calabaza, con harina de avena y almendras. Ideal para acompañar con café o té.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Huevos", "cantidad": 2, "unidad": "unid"},
            {"nombre": "Panela molida o azúcar de caña orgánica", "cantidad": 180, "unidad": "g"},
            {"nombre": "Puré de calabaza", "cantidad": 240, "unidad": "g"},
            {"nombre": "Aceite vegetal", "cantidad": 80, "unidad": "ml"},
            {"nombre": "Esencia de vainilla", "cantidad": 5, "unidad": "ml"},
            {"nombre": "Harina de avena", "cantidad": 120, "unidad": "g"},
            {"nombre": "Harina de almendras", "cantidad": 60, "unidad": "g"},
            {"nombre": "Canela molida", "cantidad": 5, "unidad": "g"},
            {"nombre": "Polvo para hornear", "cantidad": 5, "unidad": "g"},
            {"nombre": "Bicarbonato de sodio", "cantidad": 3, "unidad": "g"},
            {"nombre": "Sal", "cantidad": 1, "unidad": "g"},
            {"nombre": "Jengibre molido", "cantidad": 2, "unidad": "g"}
        ],
        "notas": "Hornear a 180°C durante 45 minutos. Dejar enfriar completamente antes de decorar."
    },
    "Torta de Calabaza Tradicional": {
        "descripcion": "Torta casera esponjosa y aromática con puré de calabaza, canela y vainilla. Ideal para acompañar con café o servir como postre otoñal.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Huevos", "cantidad": 3, "unidad": "unid"},
            {"nombre": "Azúcar", "cantidad": 200, "unidad": "g"},
            {"nombre": "Aceite vegetal", "cantidad": 120, "unidad": "ml"},
            {"nombre": "Puré de calabaza", "cantidad": 250, "unidad": "g"},
            {"nombre": "Esencia de vainilla", "cantidad": 5, "unidad": "ml"},
            {"nombre": "Harina de trigo", "cantidad": 200, "unidad": "g"},
            {"nombre": "Polvo para hornear", "cantidad": 8, "unidad": "g"},
            {"nombre": "Bicarbonato de sodio", "cantidad": 3, "unidad": "g"},
            {"nombre": "Canela molida", "cantidad": 5, "unidad": "g"},
            {"nombre": "Jengibre molido", "cantidad": 2, "unidad": "g"},
            {"nombre": "Nuez moscada", "cantidad": 1, "unidad": "g"},
            {"nombre": "Sal", "cantidad": 1, "unidad": "g"},
            {"nombre": "Leche", "cantidad": 60, "unidad": "ml"}
        ],
        "notas": "Batir los huevos con el azúcar hasta espumar. Agregar el aceite, el puré de calabaza y la vainilla. Incorporar los ingredientes secos tamizados y por último la leche. Hornear a 180°C durante 40–45 minutos o hasta que al insertar un palillo, salga limpio. Dejar enfriar y decorar al gusto."
    },
    "Glaseado de Queso Crema": {
        "descripcion": "Cobertura cremosa y ligeramente cítrica para tortas y cupcakes. Perfecta para la Torta de Calabaza Tradicional.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Queso crema", "cantidad": 200, "unidad": "g"},
            {"nombre": "Mantequilla sin sal", "cantidad": 80, "unidad": "g"},
            {"nombre": "Azúcar en polvo (glass)", "cantidad": 150, "unidad": "g"},
            {"nombre": "Esencia de vainilla", "cantidad": 5, "unidad": "ml"},
            {"nombre": "Ralladura de naranja", "cantidad": 2, "unidad": "g"},
            {"nombre": "Jugo de naranja (opcional)", "cantidad": 10, "unidad": "ml"}
        ],
        "notas": "Batir la mantequilla con el queso crema hasta obtener una mezcla suave. Incorporar el azúcar glass tamizado poco a poco. Añadir la vainilla, ralladura y, si se desea, unas gotas de jugo de naranja para ajustar textura y sabor. Mantener refrigerado hasta usar."
    },
    "Glaseado de Queso Crema Saludable": {
        "descripcion": "Versión ligera del clásico glaseado, sin azúcar refinada ni mantequilla. Dulce natural y textura cremosa, ideal para postres saludables.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Queso crema light", "cantidad": 200, "unidad": "g"},
            {"nombre": "Yogur griego natural sin azúcar", "cantidad": 80, "unidad": "g"},
            {"nombre": "Miel o sirope de agave", "cantidad": 40, "unidad": "g"},
            {"nombre": "Esencia de vainilla", "cantidad": 5, "unidad": "ml"},
            {"nombre": "Ralladura de naranja o limón", "cantidad": 2, "unidad": "g"}
        ],
        "notas": "Mezclar todos los ingredientes con batidor de mano o eléctrico hasta obtener una textura cremosa y uniforme. Ajustar el dulzor al gusto. Mantener refrigerado hasta el momento de usar."
    }
}
