#Contenido del repositorio

####**app.py**:
Es el programa principal, la aplicación que se ejecuta.


####**funciones.py**:
Funciones creadas para optimizar el código de *app.py*.


####**requirements.txt**:
Módulos necesarios para el funcionamiento de la aplicación, al tener este nombre [heroku](https://www.heroku.com/) los recoge e instala automáticamente al desplegar la aplicación. 


####**Procfile**:
Fichero específico de  [heroku](https://www.heroku.com/) donde podemos indicar algunas opciones y comandos que se van a ejecutar.


####**templates/**:
Carpeta donde encontramos las diferentes plantilla dinámicas usadas en la aplicación que posteriormente crearan las páginas mediante el motor de plantillas [jinja](http://jinja.pocoo.org/)


####**static/**:
Aquí encontraremos dos subcarpetas: img y css, las cuales contienen las imágenes y los ficheros css de la aplicación respectivamente.


####**upload/**:
Su uso no está implementado.

#Aplicación

#### **Inicio**:
Nada más entrar solo encontraremos la página de inicio y la opción de iniciar sesión. Necesario para usar la aplicación. 
Si ya hemos niciado sesión tendremos una breve descripción de cada apartado del menú y la opción de cerrar sesión.


#### **Iniciar Sesión**: 
Nos llevará hasta la página Microsoft para poder iniciar sesión de forma segura, si es la primera vez que usamos la aplicación nos pedirá una serie de permisos necesarios para el funcionamiento de esta. En cualquier momento podemos revocar los permisos previamente otorgados desde [aquí](https://account.live.com/consent/Manage).


#### **Cerrar Sesión**: 
Si hemos iniciado sesión y queremos desconectarnos tendremos una opción para ello en el menú superior, éste cerrará la sesión y nos redireccionará a la página de inicio como si acabaramos de entrar en la aplicación.


#### **Vista previa**:
Se muestra información de la cuota de almacenamiento disponible y del usuario.


#### **Vista de árbol/Listado**: 
Primero muestra el contenido del raíz. Los ficheros tienen un enlace para poder descargarlos y las carpetas un enlace que muestra el contenido.


#### **Subida simultanea/Subir ficheros**: 
Posibilidad de subir de forma simultanea en ambas plataforma el fichero elegido siempre que se haya iniciado sesión en ambas previamente. Acualmente no disponible.


#### **Contacto**: 
Formulario de contacto para sugerencias y comentarios. Actualmente no disponible.

#URL de la aplicación: [CloudManage](https://cloudsmanage.herokuapp.com/)
