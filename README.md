# Asistente Virtual de Programación

Este proyecto es un asistente virtual. Es una aplicación de consola que usa APIs externas y servicios en la nube para interactuar con el usuario.


Funcionalidades:
Gestionar Eventos: Crear, eliminar y listar eventos en Google Calendar.
Consultar Clima: Obtener información sobre el clima actual en una ciudad.
Conversión de Moneda: Convertir montos entre diferentes monedas.
Recordatorios: Crear y mostrar recordatorios almacenados en un archivo local.

Requisitos
Python 3.x
Librerías externas: requests, google-auth, google-auth-oauthlib, google-api-python-client, pytz

Instalación
Clona el repositorio:


Luego, instala las dependencias necesarias con pip:
pip install -r requirements.txt

Si no tienes el archivo requirements.txt, puedes instalar las librerías manualmente:
pip install requests google-auth google-auth-oauthlib google-api-python-client pytz


Uso
Configura las credenciales de Google API:

Para que el proyecto interactúe con Google Calendar, necesitarás configurar las credenciales de la API de Google. Esto es necesario para autenticar tu aplicación y permitirle acceder a tu cuenta de Google Calendar.

Ve a Google Cloud Console.
Crea un proyecto o usa uno existente.
Activa la API de Google Calendar para tu proyecto.
Crea las credenciales (tipo OAuth 2.0) y descarga el archivo credentials.json.
Guarda el archivo credentials.json en la raíz de tu proyecto.


Autenticación y Token:

Al ejecutar el código por primera vez, el sistema pedirá autorización para acceder a tu cuenta de Google Calendar. Esto se maneja a través de un flujo de autenticación, que generará un archivo de token (token.pickle) una vez que autorices la aplicación.

El archivo token.pickle guarda el acceso y la sesión de autenticación para futuras ejecuciones, sin necesidad de que el usuario vuelva a autorizarse.

Importante: Nunca subas tus archivos credentials.json o token.pickle a repositorios públicos, ya que contienen información sensible para acceder a tu cuenta.


Una vez configuradas las credenciales, puedes ejecutar el programa:
python main.py

El programa se ejecutará en la terminal y mostrará un menú con las opciones disponibles (gestionar eventos, consultar el clima, convertir monedas, gestionar recordatorios).



Notas Adicionales
Google API y las Claves: La API de Google Calendar requiere que uses OAuth 2.0 para autenticar la aplicación. Asegúrate de obtener y guardar las credenciales de forma segura. Los tokens de acceso se generan automáticamente la primera vez que ejecutas el proyecto, y se almacenan en un archivo token.pickle.

API Keys: Las API Keys se utilizan para autenticar tu aplicación con servicios externos, como el clima o la conversión de monedas. Asegúrate de manejar estas claves con cuidado, ya que proporcionan acceso a servicios de terceros.

Cosas por Implementar
Algunas de las características que no se han implementado completamente en esta versión incluyen:

Autenticación múltiple de usuarios: Actualmente, el sistema solo soporta un usuario. En el futuro, se planea permitir la autenticación de múltiples usuarios para acceder a varios calendarios de Google.
Interfaz gráfica de usuario (GUI): Este proyecto es de línea de comandos. Se planea en el futuro agregar una interfaz gráfica para hacer la experiencia más interactiva.
