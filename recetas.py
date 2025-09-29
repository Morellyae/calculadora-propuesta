# recetas.py

RECETAS = {
    "Crema Pastelera": {
        "descripcion": "Crema básica para rellenos y postres.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Leche", "cantidad": 1000, "unidad": "ml"},
            {"nombre": "Azúcar", "cantidad": 200, "unidad": "g"},
            {"nombre": "Yemas de huevo", "cantidad": 8, "unidad": "unid"},
            {"nombre": "Maicena", "cantidad": 80, "unidad": "g"},
            {"nombre": "Vainilla", "cantidad": 10, "unidad": "ml"},
        ],
        "notas": "Mantener refrigerada hasta el momento de usar."
    },
    "Ganache de Chocolate": {
        "descripcion": "Cobertura cremosa ideal para tortas y rellenos.",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Chocolate cobertura", "cantidad": 500, "unidad": "g"},
            {"nombre": "Crema de leche", "cantidad": 250, "unidad": "ml"},
            {"nombre": "Mantequilla", "cantidad": 50, "unidad": "g"},
        ],
        "notas": "Emulsionar bien hasta obtener textura brillante."
    },
    "Brillo Espejo": {
        "descripcion": "Glaseado para congelados y entremets.",
        "porciones": 15,
        "ingredientes": [
            {"nombre": "Agua", "cantidad": 150, "unidad": "ml"},
            {"nombre": "Azúcar", "cantidad": 300, "unidad": "g"},
            {"nombre": "Leche condensada", "cantidad": 200, "unidad": "g"},
            {"nombre": "Chocolate blanco", "cantidad": 300, "unidad": "g"},
            {"nombre": "Grenetina", "cantidad": 12, "unidad": "g"},
            {"nombre": "Colorante", "cantidad": 5, "unidad": "g"},
        ],
        "notas": "Usar a 35-38 °C para cubrir sin derretir las piezas."
    },
    "Bizcocho Genovés": {
        "descripcion": "Bizcocho esponjoso clásico sin grasas añadidas.",
        "porciones": 8,
        "ingredientes": [
            {"nombre": "Huevos", "cantidad": 4, "unidad": "unid"},
            {"nombre": "Azúcar", "cantidad": 120, "unidad": "g"},
            {"nombre": "Harina", "cantidad": 120, "unidad": "g"},
        ],
        "notas": "Hornea en molde engrasado ligeramente y sin mover la bandeja durante horneado."
    },
    "Torta de Zanahoria": {
        "descripcion": "Torta húmeda con zanahoria y especias.",
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
        "notas": "Agregar nueces o especias adicionales al gusto."
    },
    "Merengue Italiano": {
        "descripcion": "Merengue estabilizado con almíbar caliente.",
        "porciones": 15,
        "ingredientes": [
            {"nombre": "Claras de huevo", "cantidad": 150, "unidad": "g"},
            {"nombre": "Azúcar", "cantidad": 300, "unidad": "g"},
            {"nombre": "Agua", "cantidad": 80, "unidad": "ml"},
        ],
        "notas": "Batir a punto de nieve hasta que enfríe."
    },
    "Masa Quebrada": {
        "descripcion": "Masa base para tartas dulces y saladas.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Harina", "cantidad": 250, "unidad": "g"},
            {"nombre": "Mantequilla fría", "cantidad": 125, "unidad": "g"},
            {"nombre": "Azúcar", "cantidad": 50, "unidad": "g"},
            {"nombre": "Huevo", "cantidad": 1, "unidad": "unid"},
        ],
        "notas": "Refrigerar 30 minutos antes de estirar."
    },
    "Masa Hojaldre": {
        "descripcion": "Masa laminada crocante para pasta hojaldre.",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Harina", "cantidad": 500, "unidad": "g"},
            {"nombre": "Mantequilla", "cantidad": 400, "unidad": "g"},
            {"nombre": "Agua", "cantidad": 250, "unidad": "ml"},
            {"nombre": "Sal", "cantidad": 10, "unidad": "g"},
        ],
        "notas": "Plegar varias vueltas con enfriamientos intermedios."
    },
    "Sirope Básico": {
        "descripcion": "Jarabe simple para humectar bizcochos.",
        "porciones": 20,
        "ingredientes": [
            {"nombre": "Azúcar", "cantidad": 200, "unidad": "g"},
            {"nombre": "Agua", "cantidad": 200, "unidad": "ml"},
            {"nombre": "Licor o esencia", "cantidad": 10, "unidad": "ml"},
        ],
        "notas": "Calentar hasta disolución completa y enfriar antes de usar."
    },
    "Flan de Vainilla": {
        "descripcion": "Flan suave y cremoso de vainilla clásico.",
        "porciones": 8,
        "ingredientes": [
            {"nombre": "Leche", "cantidad": 500, "unidad": "ml"},
            {"nombre": "Huevos", "cantidad": 4, "unidad": "unid"},
            {"nombre": "Azúcar", "cantidad": 120, "unidad": "g"},
            {"nombre": "Vainilla", "cantidad": 10, "unidad": "ml"},
        ],
        "notas": "Cocinar en baño maría y dejar reposar mínimo 4 horas."
    },
    "Buttercream": {
        "descripcion": "Crema de mantequilla dulce para cobertura.",
        "porciones": 12,
        "ingredientes": [
            {"nombre": "Mantequilla", "cantidad": 250, "unidad": "g"},
            {"nombre": "Azúcar glass", "cantidad": 400, "unidad": "g"},
            {"nombre": "Esencia de vainilla", "cantidad": 10, "unidad": "ml"},
            {"nombre": "Leche", "cantidad": 30, "unidad": "ml"},
        ],
        "notas": "Batir bien para airear y que quede cremosa."
    },
    "Pan de Plátano": {
        "descripcion": "Queque húmedo con sabor a plátano maduro.",
        "porciones": 10,
        "ingredientes": [
            {"nombre": "Plátanos maduros", "cantidad": 3, "unidad": "unid"},
            {"nombre": "Harina", "cantidad": 200, "unidad": "g"},
            {"nombre": "Azúcar", "cantidad": 150, "unidad": "g"},
            {"nombre": "Mantequilla", "cantidad": 100, "unidad": "g"},
            {"nombre": "Huevos", "cantidad": 2, "unidad": "unid"},
            {"nombre": "Polvo de hornear", "cantidad": 10, "unidad": "g"},
        ],
        "notas": "Puedes agregar nueces o chips de chocolate al gusto."
    }
}
