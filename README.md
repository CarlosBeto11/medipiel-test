
1. DESCRIPCIÓN GENERAL DE LA SOLUCIÓN.

Se creó este proyecto con la finalidad de solucionar la confirmación de ordenes en caso de que haya stock suficiente de cada producto, de lo contrario no se permitirá capturar la orden.

2. ARQUITECTURA PROPUESTA.

Se optó por utilizar un proyecto de python utilizando fastapi como librería y como manaejador de base de datos postgres en el proyecto de api externa.

3. INSTRUCCIONES DE EJECUCIÓN.

REQUISITOS:
- python 3.10 o mayor
- es necesario crear un archivo .env en proyecto de api externa con la siguiente env var: DATABASE_URL=postgresql://{user}:{password}@localhost:5432/{BD}, cambiando los valores USER, PASSWORD Y BD con la conexión de postgres

API EXTERNA
- Acceder al directorio de api externa (cd api_externa)
- Crear un ambiente virtual para albergar las librerías que utilizaremos (python -m venv venv)
- Activar nuestro ambiente virtual (
    Windows (PowerShell): .\venv\Scripts\activate
    Windows (cmd.exe): venv\Scripts\activate.bat
    Linux/macOS: source venv/bin/activate
)
- Una vez activado, instalar librerías desde el archivo requirements.txt (pip install -r requirements.txt)
- Ejecutar el comando (uvicorn main:app --reload) para levantar el servicio con uvicorn
- Listo, para este punto las tablas se generarán automaticamente en la base de datos.


API INTERNA
- Acceder al directorio de api externa (cd proyecto_interno)
- Crear un ambiente virtual para albergar las librerías que utilizaremos (python -m venv venv)
- Activar nuestro ambiente virtual (
    Windows (PowerShell): .\venv\Scripts\activate
    Windows (cmd.exe): venv\Scripts\activate.bat
    Linux/macOS: source venv/bin/activate
)
- Una vez activado, instalar librerías desde el archivo requirements.txt (pip install -r requirements.txt)
- Ejecutar el archivo main.py

4. Cómo crear e inicializar la base de datos.


5. ENDPOINTS DISPONIBLES
- GET /products/{product_id}
- GET /products
- POST /orders
- GET /orders/{order_id}
- PUT /orders/{order_id}
- GET /inventory-movements
- GET /inventory/{product_id}

6. DECISIONES TÉCNICAS TOMADAS
Se opto por utilizar fastapi porque es una de las librerias mejores documentadas y de mayor performance a la hora de realizar peticiones directamente a la base de datos.


7. MEJORAS FUTURAS
Es posible que se necesite de una mejora en el apartado de solicitudes atomicas, es decir, en caso de que una order no se complete hacer un rollback de toda la información previamente guardada en la BD.

De igual forma es necesario tener transacciones temporales en caso de que varios usuario requiran un producto al mismo tiempo.

8. USO DE HERRAMIENTAS EXTERNAS
- Busquedas en google y geminis
- Las busquedas solo se realizaron cuando se tenía duda en algo en especifico

9. CÓMO CREAR E INICIALIZAR LA BASE DE DATOS.
Para esto necesitaremos crear un servidor local de postgres en nuestra computadora, descargando el siguiente archivo (https://www.postgresql.org/download/).
completa el wizard de instalación y casi al finalizar se te pedirá una contraseña para tu usuario root.

en tu cliente de base de datos (pg4admin, dbeaver etc.), crea una nueva conexión con tu localhost y la contraseña que ingresaste.

una vez que tengas tu conexión, ejecuta el archivo DB structure dentro de tu conexión para crear las tablas y popular el contenido necesario para que funcione la api externa.


POSTMAN COLLECTION:
https://identity.getpostman.com/accounts?continue=https%3A%2F%2Fgo.postman.co%2Fworkspace%2FCarlos-Alberto-Alvarez-Orta%27s-W%7Ec4a0809c-320c-4c61-88cf-96891e18fd2f%2Fcollection%2F43585325-90610e1b-1dce-4a79-89da-0c9d321fdd80%3Faction%3Dshare%26source%3Dcopy-link%26creator%3D43585325&intent=switch-account&target_team=carlosalbertoalvarezorta&authFlowId=769fe783-f234-4574-aa13-6c5682455712