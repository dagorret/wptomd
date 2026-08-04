# wptomd

`wptomd` convierte artículos HTML de WordPress en documentos Markdown limpios.

Es una herramienta privada para rescatar el contenido editorial de [Dagorret.com.ar](https://dagorret.com.ar). WordPress es la fuente histórica; el Markdown generado es el documento que se conserva.

## Instalación

Se necesita Python 3.12 o superior. Desde la raíz del proyecto:

```bash
python -m venv .venv
source .venv/bin/activate.fish
python -m pip install -e ".[dev]"
```

El comando de activación mostrado corresponde a Fish. Si se utiliza Bash o Zsh, activar el mismo entorno con:

```bash
source .venv/bin/activate
```

Para comprobar la instalación:

```bash
wptomd --help
```

## Uso rápido

Los comandos no crean directorios de salida. Los directorios que se indiquen deben existir previamente. Si el archivo de destino ya existe, la operación falla salvo que se utilice `--force`.

### Convertir un archivo HTML

Convierte un archivo HTML local y deja el Markdown junto al archivo original:

```bash
wptomd convert input/articulo.html
```

Genera:

```text
input/articulo.md
```

El nombre se normaliza como slug. Por ejemplo, `Artículo útil.html` genera `articulo-util.md`.

### Usar una ruta absoluta

Se aceptan rutas relativas y absolutas:

```bash
wptomd convert /home/carlos/legacy/articulo.html
```

Genera:

```text
/home/carlos/legacy/articulo.md
```

### Elegir un archivo de salida

Con `-o` o `--output` se puede indicar un archivo concreto. Su directorio padre debe existir:

```bash
wptomd convert input/articulo.html \
  -o content/articulo.md
```

Genera exactamente:

```text
content/articulo.md
```

Si `content/` no existe, la operación falla y `wptomd` no lo crea.

### Elegir un directorio de salida

Si `-o` apunta a un directorio existente, el nombre del Markdown se obtiene del HTML:

```bash
wptomd convert input/articulo.html \
  -o content/
```

Genera:

```text
content/articulo.md
```

### Convertir un directorio

Convierte todos los archivos `.html` situados directamente dentro de `legacy/`:

```bash
wptomd convert-directory legacy/
```

Cada Markdown queda junto a su HTML:

```text
legacy/
    articulo1.html
    articulo1.md
    articulo2.html
    articulo2.md
```

No se buscan archivos dentro de subdirectorios.

También se puede indicar un directorio de salida existente:

```bash
wptomd convert-directory legacy/ \
  -o content/
```

En ese caso todos los Markdown se escriben dentro de `content/`.

Si un archivo falla, el comando informa el error, continúa con los demás, muestra un resumen y termina con código 1. Si todos se convierten correctamente, termina con código 0.

### Convertir desde una URL

Descarga una página individual mediante HTTP y la convierte con el mismo conversor:

```bash
wptomd convert-url \
  https://dagorret.com.ar/el-modelo-base-00-2/
```

Genera:

```text
output/el-modelo-base-00-2.md
```

El directorio `output/` debe existir previamente. `convert-url` no lo crea.

También se puede indicar un archivo:

```bash
wptomd convert-url URL \
  -o content/modelo-base.md
```

O un directorio existente:

```bash
wptomd convert-url URL \
  -o content/
```

En el segundo caso se genera `content/<slug>.md`.

### Sobrescribir una salida

Sin `--force`, un archivo existente no se modifica:

```bash
wptomd convert input/articulo.html
```

Para sobrescribirlo explícitamente:

```bash
wptomd convert input/articulo.html --force
```

`--force` sobrescribe silenciosamente. No se muestra un mensaje adicional de sobrescritura. La opción está disponible en `convert`, `convert-directory` y `convert-url`.

Debe utilizarse solamente cuando se quiera regenerar el Markdown desde su HTML original y se hayan revisado las posibles ediciones manuales del archivo existente.

### Ver la ayuda

```bash
wptomd --help
wptomd convert --help
wptomd convert-directory --help
wptomd convert-url --help
```

## Qué convierte

Actualmente `wptomd` puede:

- convertir un archivo HTML local;
- convertir los archivos `.html` de un directorio local, sin recorrer subdirectorios;
- descargar y convertir un artículo individual desde una URL `http` o `https`;
- detectar contenido dentro de `.entry-content`, `.wp-block-post-content`, `article`, `main` o `body`;
- obtener el título desde el `h1` editorial, el `<title>` o el nombre del archivo;
- generar slugs ASCII seguros;
- convertir encabezados, párrafos, listas, enlaces, imágenes, tablas y blockquotes;
- conservar captions de imágenes;
- convertir `<br>` en saltos de línea Markdown;
- normalizar entidades HTML y espacios no separables;
- eliminar `script`, `style`, `noscript`, separadores y spacers de WordPress;
- convertir fórmulas QuickLaTeX inline a `$...$`;
- convertir fórmulas QuickLaTeX display a bloques `$$...$$`;
- generar frontmatter YAML con la identificación y procedencia del documento.

## Markdown generado

El resultado es un documento Markdown UTF-8 con frontmatter YAML:

```markdown
---
title: El modelo base 00-2
slug: el-modelo-base-00-2
status: published
legacy_url: https://dagorret.com.ar/el-modelo-base-00-2/
---

## Introducción

Texto normalizado del artículo.

### Datos

| Columna A | Columna B |
| --- | --- |
| A | B |

> Una cita importante.

La fórmula inline queda como $x^2$.

$$
\frac{a}{b}
$$

![Descripción de la imagen](imagen.jpg)
```

El frontmatter contiene:

- `title`: título editorial detectado.
- `slug`: identificador seguro del documento.
- `status`: actualmente `published`.
- `legacy_url`: URL original cuando se usó `convert-url`.
- `legacy_source`: nombre del archivo HTML cuando se usó `convert` o `convert-directory`.

## Objetivo del proyecto

El objetivo es rescatar el patrimonio editorial de Dagorret.com.ar y convertirlo en un repositorio permanente de documentos Markdown:

```text
WordPress
    ↓
HTML
    ↓
Markdown limpio
    ↓
Git
    ↓
Astro
    ↓
Sitio estático
```

WordPress es la fuente histórica, no el repositorio editorial futuro. Markdown será el formato canónico y deberá poder conservarse, versionarse y leerse sin depender de un CMS. Astro será un consumidor posterior de esos documentos para generar el sitio estático.

`wptomd` no pretende ser un conversor universal de WordPress. Sus reglas están orientadas al contenido y a los residuos encontrados en Dagorret.com.ar, incluidos los elementos de WordPress y QuickLaTeX que utiliza ese sitio.

Las capacidades que todavía no existen —como REST API, descarga masiva, caché, concurrencia, base de datos, procesamiento de JavaScript o gestión permanente de imágenes— no forman parte de esta herramienta actualmente.

Por el momento el proyecto permanece privado.
