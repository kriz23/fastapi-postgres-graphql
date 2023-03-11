Proyecto creado con `Python 3.9.16`

Para ejecutar este proyecto es necesario tener disponible dos tecnologías

- Anaconda
- Docker

Anaconda es necesario para crear un ambiente virtual de python para el desarrollo del aplicativo

Docker es necesario porque la base de datos (Postgres), el aplicativo PgAdmin y la aplicación misma (FastAPI) están
contenerizadas mediante Docker

# Instalar y activar ambiente virtual

## Instalación de Anaconda

Disponible a través de [este enlace](https://www.anaconda.com/products/distribution#Downloads)

Antes de proceder es necesario comprobar la instalación y usabilidad de `conda`

## Creación y activación virtualenv

### _Creación_:

`conda create --name fastapi-graphql python=3.9.16`

### _activación_ :

`conda activate fastapi-graphql`

# Instalación de dependencias

`pip install -r requirements.txt`

Nota: Cuando se instale una nueva dependencia se tiene que ejecutar el comando: `pip freeze > requirements.txt`
para agregarla al archivo de requerimientos.

Nota 2: Es importante aislar el entorno virtual de los paquetes del espacio del usuario global del sistema, para no
estar inyectándole dependencias innecesarias al proyecto.

# Instalar Docker

Seguir las instrucciones de instalaciones disponibles [aquí](https://docs.docker.com/engine/install/) según corresponda
para su sistema operativo.

Para instalaciones en sistemas operativos Linux recomiendo el uso del script [get-docker.sh](https://get.docker.com/),
para usarlo ejecutaremos los siguientes comandos:

1. `curl -fsSL https://get.docker.com -o get-docker.sh`
2. `sh get-docker.sh`

Posteriormente agregamos nuestro usuario al grupo de Docker para poder ejecutar comandos de docker sin necesidad del
superusuario

Ejecutamos `sudo usermod -aG docker <nuestroUsuario>`

Refrescamos (por si las moscas) las configuraciones de nuestro perfil de Bash ejecutando `source ~/.bashrc`

Comprobamos la instalación de Docker ejecutando `docker version`, lo que nos deberá devolver información del Cliente y
el Servidor del motor de Docker que fueron instalados en el equipo.

**Nota:** El script `get-docker.sh` nos instala el paquete `docker-compose-plugin` por lo que no será necesario instalar
manualmente el paquete `docker-compose` usado tradicionalmente. La diferencia entre estos paquete es que el primero se
usa ejecutando `docker compose` mientras que con el segundo hay que ejecutar `docker-compose`, hay que tener en cuenta
esta sútil diferencia para ejecutar los comandos adecuadamente, aunque siempre se puede crear un "alias" para evitar
caer en errores por la costumbre.

**Nota 2:** La aplicación [Docker Desktop](https://www.docker.com/products/docker-desktop/) es completamente
innecesaria, su instalación y uso queda a criterio de quién desee replicar este proyecto.

# Ejecutando el Proyecto

En el archivo `docker-compose.yml` está definido el servicio `app` que es nuestra *API* con *GraphQL*, el cuál también
es un contenedor de Docker, las definiciones para crear la imagen de este contenedor están especificadas en el
archivo `Dockerfile` en este mismo proyecto, por lo que será necesario construir dicha imagen y "adjuntarla" a las
otras dos de nuestro *docker-compose*.

Ejecutamos entonces `docker compose build` (o `docker-compose build` según como se haya realizado la instalación de
docker)

Y luego ejecutamos `docker compose up` para arrancar nuestros contenedores.

El siguiente paso es comprobar la ejecución de los 3 contenedores, para el de la DB y el PgAdmin accederemos a la
interfaz del PgAdmin a través de la ruta `localhost:5050` en el navegador e intentaremos conectarnos a nuestro
contenedor de la DB, el
hostname es el nombre que le pusimos al contenedor es decir `db`, los demás datos se encuentran en el archivo `.env`.

Para comprobar el contenedor de nuestra app accederemos a la ruta `localhost:8000` en el navegador y deberiamos poder
acceder a la ruta `localhost:8000/graphql`.

Lo siguiente será hacer una migración para crear la (o las) tabla en le DB, ejecutaremos lo siguiente:

1. `docker compose run app alembic revision --autogenerate -m "New Migration"`
2. `docker compose run app alembic upgrade head`

Si todo ha salido bien hasta el momento ya podremos agregar y consultar registros de la DB a través de GraphQL.

Para agregar un registro ejecutamos la siguiente mutación:

```graphql
mutation CreateNewPost {
  createNewPost(title: "new title", author: "new author", content: "new content") {
    ok
  }
}
```

Para consultar el atributo `title` podemos ejecutar la siguiente query:

```graphql
query {
  allPosts {
    title
  }
}
```

Así mismo podemos consultar los demás atributos, o consultarlos todos juntos a través de la misma query.

Por último, para consultar un registro por su `id` ejecutamos la siguiente query:

```graphql
query {
  postById(postId: 1) {
    id
    title
    content
  }
}
```

En el ejemplo anterior estamos consultando los atributos `id`, `title` y `content` del registro cuya `id` es `1`.

___

Tomado originalmente de:

[Este videito](https://youtu.be/Puvr82Cm26o) | [Este repositorio](https://github.com/veryacademy/YT_FastAPI_Beginner_Fast-Track-GraphQL)

