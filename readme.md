Bienvenido, este es el proyecto final sobre las Redes Electricas de España, un proyecto basado principal mente en
estraer, procesar y visualizar los datos de las redes electricas de españa para su visualizacion y tambien prediccion
para fechas futuras.

Podras ver mejor la estructura del proyecto en el archivo "estructura.txt".

Miembros: Andre, Eduardo, Luisa, Samuel.

Instrucciones:

    Para poder emplear este proyecto primero deberemos de crear un entorno virtual(.venv) para ejecutar nuestro codigo
    para ello puedes usar el codigo ejecuta esta linea en la terminal desde visual studio en la raiz del proyecto "python3 -m venv venv" despues de esto dependiendo del sistema operativo para activarlo ejecuta lo siguiente:

        Windows:
            .\venv\Scripts\activate
        MacOS, Linux:
            source venv/bin/activate

    Ahora una vez creado el entorno virtual, procedemos a configurar la base de datos, puedes hacerlo ejecutando en MySQL Workbench el codigo sql que se encuentra en la carpeta database. Asegurate de configurarlo con la contraseña "rootroot" es la contraseña por defecto que usara la base de datos, de todas formas si ya tienes tu servidor configurado con otra contraseña puedes ir al archivo ".env" donde puedes cambiar la variable donde viene la contraseña por la que ya tengas configurada.

    Ahora que ya has configurado el acceso a la base de datos y has creado la base de Redes electricas, puedes cargar los datos de dos formas, puedes usar el notebook que esta en la carpeta notebook, dentro de la misma carpeta en la que se encontraba el codigo sql de la base de datos y cargar los datos manualmente, es decir, hacer la extraccion, la limpieza y la carga manualmente. Otra opcion es importar los datos de las tablas de la base de datos que se encuentra en el archivo "database.zip". Una vez hecho esto ya tendriamos la base de datos configurada correctamente.

    El siguiente paso es ejecutar el codigo de la pagina web para poder visualizarlo, para ello desde la terminal de visual studio, situado en la raiz del proyecto ejecutaremos el siguiente codigo que nos abrira directamente en el navegador nuestra pagina web donde podremos visualizar los datos de nuestro proyecto "streamlit run app/main.py".

    Con esto nuestro programa estaria listo para usarse.

Esperamos que os guste :)

PD: En el directorio "app/data/" podemos encontrar una presentación creada por nuestro compañero Eduardo.
