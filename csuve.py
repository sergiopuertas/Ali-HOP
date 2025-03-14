import csv

# Cada diccionario representa una fila en el CSV.
# Los datos se han extraído (y “unificado”) de los distintos apartados de la guía:
#  - La tabla de frutas (se asigna la recomendación de potasio según la columna; fosforo y sodio se asumen aconsejadas)
#  - Carnes y pescados (con la clasificación de potasio, mientras que fosforo y sodio quedan por defecto)
#  - Grupos de lácteos, cereales, legumbres, frutos secos, bollería, chocolate y bebidas para el fósforo
#  - Alimentos con alto contenido en sodio (se asigna “limitada” en sodio)
data = [
    # Tabla de frutas (recomendaciones para POTASIO; FÓSFORO y SODIO por defecto "aconsejada")
    {"Alimento": "Fruta en almíbar (sin cado)", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Melocotón", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},
    {"Alimento": "Plátano", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},

    {"Alimento": "Frutas en su jugo (sin caldo)", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Naranja", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},
    {"Alimento": "Uva negra", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},

    {"Alimento": "Arándanos", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Caqui", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},
    {"Alimento": "Aguacate", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},

    {"Alimento": "Sandía", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Maracuyá", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},
    {"Alimento": "Coco", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},

    {"Alimento": "Manzana", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Moras", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},
    {"Alimento": "Chirimoya", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},

    {"Alimento": "Pera", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Nectarina", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},
    {"Alimento": "Albaricoque", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},

    {"Alimento": "Pomelo", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Papaya", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},
    {"Alimento": "Grosella negra", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},

    {"Alimento": "Lima", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Frambuesa", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},

    {"Alimento": "Piña", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Ciruelas", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},

    {"Alimento": "Higos chumbos", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Kiwi", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},

    {"Alimento": "Mandarina", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Cerezas", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},

    {"Alimento": "Mango", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Granada", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},

    {"Alimento": "Fresas", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Nísperos", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},

    {"Alimento": "Limón", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Uva blanca", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},

    {"Alimento": "Lichi", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Melón", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "limitada"},

    # Carnes y pescados (clasificación de POTASIO; FÓSFORO y SODIO por defecto "aconsejada")
    {"Alimento": "Pollo", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Pavo", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Conejo", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Cerdo (lomo o solomillo)", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Ternera", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},
    {"Alimento": "Cordero", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},
    {"Alimento": "Carnes grasas y embutidos", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},

    {"Alimento": "Pescadilla", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Merluza", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    # Nota: Algunos pescados aparecen en dos secciones con recomendaciones distintas para cada electrólito.
    {"Alimento": "Gallo", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Rape", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Bacalao", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Lenguado", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Calamar", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Caballa", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Salmón", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Trucha", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},
    {"Alimento": "Sepia", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},
    {"Alimento": "Atún", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},
    {"Alimento": "Halibut", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},
    {"Alimento": "Sardinas", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},
    {"Alimento": "Emperador", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},
    {"Alimento": "Lubina", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},
    {"Alimento": "Bonito", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "desaconsejada"},

    # Sección FÓSFORO: Lácteos
    {"Alimento": "Leche semidesnatada", "Fosforo": "limitada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Yogur (normal o de sabores)", "Fosforo": "limitada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Queso fresco/blanco/requesón", "Fosforo": "limitada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Leche entera", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Quesos curados o semicurados", "Fosforo": "desaconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    {"Alimento": "Quesos untables y fundentes", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Nata", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Lácteos enriquecidos", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Postres lácteos industriales", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},

    # FÓSFORO: Cereales
    {"Alimento": "Avena", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Pan", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Pasta", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Arroz", "Fosforo": "aconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Pan de molde", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Pan de hamburguesa", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},

    # FÓSFORO: Legumbres
    {"Alimento": "Judías blancas", "Fosforo": "limitada", "Sodio": "aconsejada", "Potasio": "aconsejada"},
    {"Alimento": "Habas", "Fosforo": "limitada", "Sodio": "aconsejada", "Potasio": "aconsejada"},

    # FÓSFORO: Frutos secos
    {"Alimento": "Frutos secos", "Fosforo": "limitada", "Sodio": "aconsejada", "Potasio": "aconsejada"},

    # FÓSFORO: Bollería y repostería
    {"Alimento": "Bollería y repostería", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},

    # FÓSFORO: Chocolate
    {"Alimento": "Chocolate", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},

    # FÓSFORO: Bebidas y refrescos azucarados
    {"Alimento": "Bebidas y refrescos azucarados", "Fosforo": "desaconsejada", "Sodio": "aconsejada", "Potasio": "aconsejada"},

    # Sección SODIO (alimentos ricos en sodio → recomendación "limitada" en sodio)
    {"Alimento": "Ahumados y salazones", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    {"Alimento": "Embutidos y fiambres", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    {"Alimento": "Conservas en general", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    # Quesos curados o semicurados ya se incluyeron; para sodio se usa "limitada"
    {"Alimento": "Mariscos y crustáceos", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    {"Alimento": "Encurtidos vegetales (olivas, pepinillos, cebolletas)", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    {"Alimento": "Comida precocinada o manufacturada", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    {"Alimento": "Comida rápida (fast food)", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    {"Alimento": "Snacks comerciales (patatas fritas, galletas saladas)", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    {"Alimento": "Cubitos de carne/pescado (starlux)", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
    {"Alimento": "Salsas comerciales (kétchup, mostaza, mahonesa)", "Fosforo": "aconsejada", "Sodio": "limitada", "Potasio": "aconsejada"},
]

# Escribe el CSV con codificación UTF-8 para conservar tildes y caracteres especiales.
with open("alimentos.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Alimento", "Fosforo", "Sodio", "Potasio"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("CSV generado: alimentos.csv")
