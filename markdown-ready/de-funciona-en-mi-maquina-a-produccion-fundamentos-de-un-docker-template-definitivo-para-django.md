---
title: 'De "Funciona en mi máquina" a Producción: Fundamentos de un Docker Template
  Definitivo para Django'
slug: de-funciona-en-mi-maquina-a-produccion-fundamentos-de-un-docker-template-definitivo-para-django
status: published
legacy_url: https://dagorret.com.ar/de-funciona-en-mi-maquina-a-produccion-fundamentos-de-un-docker-template-definitivo-para-django/
wordpress_id: 1408
published_at: '2026-07-18T23:26:51'
modified_at: '2026-07-18T23:26:54'
wordpress_category_ids:
- 20
wordpress_tag_ids:
- 432
- 430
- 429
- 431
categories:
- &id001
  id: 20
  name: Tecnología
  slug: tecnologia
tags:
- id: 432
  name: boilerplate
  slug: boilerplate
- id: 430
  name: django
  slug: django
- id: 429
  name: docker
  slug: docker
- id: 431
  name: Template
  slug: template
category: *id001
---

Cualquiera que haya trabajado con Django sabe que el framework es una maravilla de la productividad. Sin embargo, el verdadero reto empieza cuando pasamos del entorno local a un servidor de producción real. Configurar bases de datos, aislar las dependencias, gestionar las variables de entorno y escribir scripts repetitivos para levantar contenedores puede convertirse rápidamente en un verdadero dolor de cabeza.

Para solucionar esto de raíz, diseñé __django-quickstart__, un boilerplate/template estructurado para automatizar, aislar y estandarizar el despliegue de Django utilizando contenedores Docker tanto en desarrollo como en producción.

En este artículo desglosamos los __fundamentos, objetivos y conceptos__ detrás de este enfoque de arquitectura orientada a contenedores — y, al cierre, hago una revisión técnica honesta de algunos puntos del template que conviene ajustar antes de llevarlo a un entorno productivo real.

---

## Objetivos de este template

Cuando decidí armar esta estructura, mi meta principal no era solo “hacer andar Docker”. Quería resolver problemas reales de arquitectura y flujos de trabajo en equipos de desarrollo:

1. __Paridad de entornos (desarrollo == producción).__ Eliminar por completo el clásico \*”pero en mi máquina funcionaba”\*. Si corre en tu Docker local, corre en el servidor.
2. __Abstracción de la infraestructura.__ El programador no tiene que lidiar con la instalación local de PostgreSQL o Adminer; todo se orquesta automáticamente con comandos limpios.
3. __Automatización de tareas repetitivas.__ Scripts (`.sh`) listos para usar que agilicen el ciclo de construcción, inicialización y apagado de los servicios.
4. __Seguridad nativa para producción.__ Separar estrictamente las configuraciones de desarrollo y producción en imágenes optimizadas de múltiples etapas (_multi-stage builds_) y archivos Docker Compose dedicados.

> __Aclaración conceptual — “paridad de entornos”__ Esta idea no es original de Docker: es el punto __X (Dev/prod parity)__ de la metodología [The Twelve-Factor App](https://12factor.net/dev-prod-parity), publicada originalmente por ingenieros de Heroku. Propone minimizar la brecha entre desarrollo y producción en tres dimensiones: tiempo (deploys frecuentes), personal (quien programa participa del deploy) y __herramientas__ (usar el mismo motor de base de datos, cache, etc. en ambos entornos). Contenerizar ambos entornos con la misma imagen base es, en esencia, resolver la tercera dimensión.

## Conceptos y arquitectura clave

El repositorio está estructurado bajo tres pilares fundamentales:

### 1. Desacoplamiento de entornos (`dev` vs `prod`)

Un error común es usar el mismo archivo de configuración o el mismo `Dockerfile` para todo. En __django-quickstart__, los entornos están estrictamente divididos mediante archivos gemelos especializados:

- __Desarrollo:__ `Dockerfile`, `docker-compose.dev.yml`, y scripts tipo `run-devel.sh`. Aquí se montan volúmenes en vivo para que los cambios en el código Python se reflejen al instante (_hot reload_).
- __Producción:__ `Dockerfile.prod`, `docker-compose.prod.yml`, y scripts tipo `run-prod.sh`. Esta versión compila el código estático, remueve herramientas de depuración y optimiza el peso de la imagen para despliegues rápidos y seguros.

> __Aclaración conceptual — _multi-stage builds___ Lo que en producción permite “remover herramientas de depuración” y compilar el estático sin arrastrar el peso del compilador es la técnica de __build de múltiples etapas__: el `Dockerfile.prod` usa varias instrucciones `FROM`, y solo la última pasa a formar parte de la imagen final. Según la [documentación oficial de Docker](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/), separar el entorno de build del entorno de runtime “reduce significativamente el tamaño de la imagen y aumenta la seguridad de las imágenes finales”, ya que las herramientas de compilación (compiladores, cabeceras de desarrollo, etc.) nunca llegan a la imagen que corre en producción. Vale aclarar: el `Dockerfile` de desarrollo mostrado en este artículo _no_ es multi-stage (no tendría sentido, porque en dev se necesita el toolchain completo para reconstruir dependencias); el multi-stage aplica específicamente al `Dockerfile.prod`.

### 2. Abstracción por scripts (la interfaz CLI del desarrollador)

En lugar de forzar al equipo a recordar comandos masivos de Docker en la terminal, el proyecto introduce scripts de automatización limpios en la raíz:

- `init-devel.sh`: descarga las imágenes, construye el entorno y corre las migraciones iniciales por primera vez.
- `run-devel.sh` y `stop-devel.sh`: levantan o apagan el entorno de desarrollo en un segundo.
- `build-prod.sh`: compila las imágenes optimizadas listas para subir a tu registro de contenedores (Docker Hub, AWS ECR, etc.).

## El corazón del template: el código que une todo

Para entender la lógica detrás de la orquestación, veamos cómo interactúan el archivo de definición del contenedor y el orquestador de desarrollo.

### El `Dockerfile` (entorno de desarrollo)

Este archivo define el plano de la aplicación. Partimos de una imagen oficial y liviana de Python, configuramos las variables de entorno para evitar que Python escriba archivos innecesarios de caché (`.pyc`), e instalamos las dependencias:

```php
# Dockerfile (Desarrollo)
FROM python:3.11-slim

# Evita que Python escriba archivos .pyc en el disco
ENV PYTHONDONTWRITEBYTECODE=1
# Evita que Python bufferée la salida estándar (logs en tiempo real)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema si fueran necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar requerimientos de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . /app/
```
> Aclaración conceptual — por qué `COPY requirements.txt` va antes que `COPY . /app/` No es casualidad ni prolijidad: Docker cachea cada instrucción (_layer_) por separado, y solo invalida una capa —y todas las siguientes— si su contenido cambió. Copiar primero `requirements.txt` e instalar dependencias, y recién después copiar el resto del código, hace que la instalación de paquetes (la parte lenta) se reutilice desde caché mientras solo cambie el código fuente y no las dependencias. Si se invirtiera el orden, cualquier cambio de una línea en el proyecto forzaría a reinstalar todos los paquetes de Python en cada build.

### El `docker-compose.dev.yml` (orquestación local)

Aquí es donde ocurre la magia del ecosistema. Un solo comando levanta la aplicación Django, una base de datos PostgreSQL y un cliente gráfico como Adminer para auditar los datos sin instalar nada en el sistema operativo anfitrión:

```php
services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=django_db
      - POSTGRES_USER=django_user
      - POSTGRES_PASSWORD=django_password

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DATABASE_URL=postgres://django_user:django_password@db:5432/django_db
    depends_on:
      - db

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_data:
```
> __Nota técnica:__ quité la línea `version: '3.8'` del original. Desde Docker Compose v2 (2022) esa clave de nivel superior está obsoleta: Compose ya usa siempre el schema más reciente disponible sin importar lo que declares ahí, y solo genera una advertencia. Es un detalle menor, pero vale la pena desterrarlo de cualquier plantilla nueva — la [documentación oficial de Docker](https://docs.docker.com/reference/compose-file/version-and-name/) lo confirma explícitamente.

## Conclusión: el verdadero valor del boilerplate

Utilizar un enfoque basado en plantillas como __django-quickstart__ no se trata simplemente de conveniencia técnica. Se trata de __establecer estándares de ingeniería__. Al empaquetar la base de datos, el administrador, las herramientas de automatización y el código en compartimentos estancos, garantizás que la aplicación crezca de forma saludable.

Ya sea que decidas aplicar Clean Architecture, modularizar tus aplicaciones (separando `usuarios`, `roles` y `permisos` en módulos independientes) o exponer APIs complejas, esta base asegura que la infraestructura jamás sea un obstáculo.

Te invito a clonar el repositorio, probar los scripts de inicialización y llevar tu flujo de desarrollo con Django al siguiente nivel.

__Código fuente completo:__ [dagorret/django-quickstart](https://github.com/dagorret/django-quickstart)

---

## Revisión técnica: lo que ajustaría antes de ir a producción

Esta sección no estaba en el original — la agrego porque el artículo promete “seguridad nativa para producción” y hay puntos del `docker-compose.dev.yml` mostrado que, si se replican tal cual en el `docker-compose.prod.yml`, contradicen esa promesa. Ninguno invalida la arquitectura general, que es sólida; son ajustes puntuales.

1. __`DATABASE_URL` no lo interpreta Django por sí solo.__ Django no tiene, de fábrica, ningún mecanismo para parsear una variable `DATABASE_URL` y volcarla en el diccionario `DATABASES` de `settings.py`. Hace falta una librería intermedia — típicamente [`dj-database-url`](https://pypi.org/project/dj-database-url/) o `django-environ` — que traduzca ese string al formato que Django espera. Vale la pena aclararlo en el `README` del template, porque es el primer punto donde alguien nuevo se va a trabar.
2. __Credenciales en texto plano dentro del `docker-compose.yml`.__ `POSTGRES_PASSWORD=django_password` hardcodeado es aceptable para desarrollo local descartable, pero si el mismo patrón se repite en `docker-compose.prod.yml`, cualquiera con acceso de lectura al repositorio tiene la contraseña de la base productiva. La alternativa estándar es usar un archivo `.env` (excluido de git vía `.gitignore`) referenciado con `env_file:`, o directamente [Docker secrets](https://docs.docker.com/engine/swarm/secrets/) si se orquesta con Swarm/Compose en modo secretos.
3. __Adminer no debería exponerse en producción.__ Es una herramienta de administración de base de datos sin capas de autenticación propias más allá del login a la DB — dejarla accesible en el puerto `8080` de un servidor público es superficie de ataque innecesaria. Tiene sentido en `docker-compose.dev.yml`; en el archivo de producción debería eliminarse o, como mínimo, quedar detrás de un túnel/VPN.
4. __Falta mencionar `.dockerignore`.__ Sin él, `COPY . /app/` copia también `.git/`, entornos virtuales locales, archivos `.env` y demás basura de desarrollo dentro de la imagen — infla el build y puede filtrar secretos si alguien hace `docker history` o inspecciona las capas. Vale la pena que el template incluya uno por defecto.
5. __Sin `healthcheck` ni `restart` policy.__ Ninguno de los tres servicios define `healthcheck:` ni `restart:`. Para desarrollo no importa, pero en `docker-compose.prod.yml` es la diferencia entre que Docker reinicie automáticamente un contenedor caído y que el sitio quede abajo hasta que alguien lo note manualmente.

Ninguno de estos puntos es difícil de resolver — son, en todo caso, la lista de tareas naturales para pasar el template de “development-ready” a “production-hardened” en sentido estricto, más allá del multi-stage build que ya está bien encaminado.
