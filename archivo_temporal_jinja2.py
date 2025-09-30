from jinja2 import Environment, FileSystemLoader

# 1. Configuración de Jinja2
# Crea una carpeta llamada 'templates' y guarda allí el archivo HTML.
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('plantilla_jefes.html')

# 2. Simulación de los datos de la base de datos
# En un caso real, esto sería el resultado de una consulta SQL o de un ORM.
# La estructura clave-valor permite asociar cada jefe con una lista de empleados.
data_db = {
    "jefe_andrea": {
        "nombre_jefe": "Andrea G.",
        "empleados": [
            {"nombre": "Carlos M.", "id": "EMP001", "departamento": "Ventas", "telefono": "555-1234", "email": "carlos.m@empresa.com"},
            {"nombre": "Sofía P.", "id": "EMP002", "departamento": "Ventas", "telefono": "555-5678", "email": "sofia.p@empresa.com"},
        ]
    },
    "jefe_juan": {
        "nombre_jefe": "Juan L.",
        "empleados": [
            {"nombre": "Luisa R.", "id": "EMP003", "departamento": "Marketing", "telefono": "555-9101", "email": "luisa.r@empresa.com"},
            {"nombre": "Pedro T.", "id": "EMP004", "departamento": "Marketing", "telefono": "555-1213", "email": "pedro.t@empresa.com"},
            {"nombre": "Marta G.", "id": "EMP005", "departamento": "Marketing", "telefono": "555-1415", "email": "marta.g@empresa.com"},
        ]
    },
    "jefe_roberto": {
        "nombre_jefe": "Roberto V.",
        "empleados": [] # Un jefe sin empleados para probar la cláusula 'else'
    }
}

# 3. Bucle para generar y guardar el HTML personalizado para cada jefe
for jefe_id, datos in data_db.items():
    # Renderizar la plantilla con los datos del jefe actual
    html_final = template.render(
        nombre_jefe=datos["nombre_jefe"],
        empleados=datos["empleados"]
    )
    
    # Aquí puedes guardar el HTML en un archivo o enviarlo directamente por correo.
    nombre_archivo = f"reporte_{jefe_id}.html"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(html_final)
        
    print(f"Correo para {datos['nombre_jefe']} generado en: {nombre_archivo}")

# Al final de este script, tendrás tres archivos HTML:
# reporte_jefe_andrea.html, reporte_jefe_juan.html, y reporte_jefe_roberto.html
# Cada uno con la tabla de empleados correspondiente.