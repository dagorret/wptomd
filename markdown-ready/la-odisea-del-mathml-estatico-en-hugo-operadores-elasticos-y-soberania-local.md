---
title: 'La Odisea del MathML Estático en Hugo: Operadores Elásticos y Soberanía Local'
slug: la-odisea-del-mathml-estatico-en-hugo-operadores-elasticos-y-soberania-local
status: published
legacy_url: https://dagorret.com.ar/la-odisea-del-mathml-estatico-en-hugo-operadores-elasticos-y-soberania-local/
wordpress_id: 40
published_at: '2026-07-09T14:15:33'
modified_at: '2026-08-01T21:41:49'
wordpress_category_ids:
- 21
wordpress_tag_ids:
- 128
- 129
categories:
- &id001
  id: 21
  name: Sistemas
  slug: sistemas
tags:
- id: 128
  name: Hugo
  slug: hugo
- id: 129
  name: MathML
  slug: mathml
category: *id001
---

Estaba escribiendo un artículo sobre DNS. Sobre cómo las Big Tech te empujan a usar sus servidores de resolución, o los del ISP, o ninguno que controles vos. El artículo tenía fórmulas simples: latencias de ida y vuelta, sumas con etiquetas descriptivas en español. Nada exótico. La ecuación más compleja era una suma de tres términos con texto explicativo.

Fue ahí donde Hugo me dijo que no.

---

## 1. El Problema de Origen: La Ceguera Sintáctica de Hugo

El motor de renderizado nativo de Hugo se llama __Goldmark__. Es un procesador de Markdown soberbio para texto plano: rápido, predecible, casi infalible. Pero padece de una ceguera matemática absoluta que no es un bug sino una decisión de diseño deliberada: Goldmark no conoce LaTeX y no tiene por qué conocerlo.

El problema concreto aparece al escribir ecuaciones híbridas — las que combinan notación matemática con texto descriptivo en español. Por ejemplo, algo tan inocente como esto:

```
$$25\text{ms (Ida al VPS)} + 33.3\text{ms (Procesamiento Unbound)} = \mathbf{83.3\text{ms}}$$
```

Al encontrarse con los espacios en blanco literales dentro de `\text{}` y con los caracteres de escape, Goldmark asume que la estructura se rompió. En lugar de aislar el bloque como una unidad atómica, lo fragmenta, remueve las barras invertidas y escupe un HTML deforme. La ecuación llega rota al lector. Cualquier script posterior que intente reconstruirla desde el DOM parte de cero con información corrupta.

Lo que empezó como un artículo sobre DNS se convirtió en una odisea sobre cómo publicar matemática en la web sin ceder soberanía.

---

## 2. Las Soluciones Intermedias y Sus Callejones Sin Salida

Antes de llegar a la arquitectura definitiva, transité cuatro caminos que parecían razonables y resultaron ser trampas de diseño.

### Trampa 1 — JavaScript en el cliente vía CDN

La solución clásica: dejar los `$$` en el Markdown y cargar KaTeX o MathJax desde una CDN externa. El navegador descarga el HTML crudo, descarga las librerías pesadas, escanea el texto y dibuja en tiempo de ejecución. __Por qué se descartó:__ hay un retraso visual perceptible mientras el JavaScript procesa (el FOUC, _Flash of Unstyled Content_), consumo innecesario de CPU en dispositivos móviles, y una dependencia crítica de servidores externos que no controlo. Si jsDelivr tiene un microcorte, el blog técnico se rompe ante los ojos del lector. Además, me estaba escribiendo un artículo sobre la dependencia de infraestructura externa. Usar una CDN para renderizar las fórmulas de ese artículo habría sido la ironía perfecta.

### Trampa 2 — Shortcodes con APIs externas

Forzar a Hugo para que intercepte las fórmulas durante la compilación y las envíe mediante `resources.GetRemote` a un microservicio en la nube que devuelva HTML ya procesado. __Por qué se descartó:__ el primer día que compilé sin conexión, la compilación entera del blog falló con un `Panic Error`. Un pipeline estático no puede depender de la disponibilidad de servidores externos en localhost. Un blog de ingeniería que no compila en un avión no es un blog de ingeniería.

### Trampa 3 — Postprocesamiento del HTML generado

Permitir que Hugo generara archivos con los `$$` crudos y luego barrer la carpeta `public/` con un script de Node.js que parchara el código. __Por qué se descartó:__ implica aceptar conscientemente la generación de un “Frankenstein visual” para repararlo después, duplicando los tiempos de lectura y escritura en disco. Es una mala práctica de diseño que esconde el problema en lugar de resolverlo.

### Trampa 4 — MathML nativo precompilado con MathJax

Parecía la solución perfecta: un script Node.js con `mathjax-full` convierte LaTeX a MathML puro durante la compilación local y Hugo inyecta el resultado directamente en el HTML final. Sin JavaScript en el cliente. Sin CDN. Sin dependencias en runtime. Offline total.

En Firefox y Safari funcionó de forma impecable. Luego abrí Chrome.

---

## 3. El Giro Dramático: El Bug Histórico de Chromium

Habiendo elegido el enfoque de MathML nativo precompilado, el éxito parecía asegurado. La arquitectura era correcta. El MathML generado era válido. El estándar MathML Core estaba siendo respetado al pie de la letra. Y sin embargo, al abrir el sitio en Google Chrome, Edge o Brave, la estructura colapsó: los paréntesis de las matrices se renderizaban como símbolos diminutos de tamaño inline en lugar de abrazar la altura completa de la tabla.

Mi primera reacción fue que era algo mío. Revisé el MathML serializado. Revisé los atributos. Revisé el CSS del tema. Todo estaba bien.

No era algo mío.

Es, en palabras del matemático Dave Barton en la lista oficial del W3C Math Working Group en abril de 2023, “el problema arquitectónico fundamental de MathML en browsers por literalmente décadas”. El issue está registrado en el tracker oficial de Chromium como __Issue #1415218__, y Barton lo señaló ante el W3C con una advertencia directa: autores serios no adoptarán MathML nativo en la web hasta que exista un plan concreto para resolverlo.

Para entender el problema hay que entender qué son los _stretchy operators_ en MathML Core. El estándar define que ciertos elementos `<mo>` —paréntesis, corchetes, llaves, integrales— son inherentemente elásticos: deben escalar verticalmente para envolver el contenido al que delimitan. Un `<mo>(</mo>` adyacente a una `<mtable>` de cuatro filas debe estirar su glifo hasta cubrir la altura completa de esa tabla. Eso es lo que TeX hace desde 1978 y lo que MathML Core codifica formalmente.

Firefox lo implementa correctamente apoyándose en fuentes con tabla OpenType MATH. Safari resuelve los casos sin glifos de tamaño variable con un _scale transform_ sobre el glifo más cercano. Chromium, que reintrodujo soporte MathML nativo recién en Chrome 109 —enero de 2023, después de trece años y once meses de ausencia desde el Issue #6606, implementado gracias a cuatro años de trabajo del equipo de Igalia financiado mediante colecta pública— todavía no implementa el _glyph assembly_ completo para construir operadores elásticos cuando el sistema no provee las fuentes matemáticas adecuadas.

El resultado concreto: un `<mo stretchy="true">(</mo>` adyacente a una `<mtable>` produce en Chrome un paréntesis del tamaño de una letra minúscula, flotando en el centro de la matriz.

Intenté todos los parches documentados. `stretchy="true"` explícito en los `<mo>`. Limpieza de atributos `data-mjx-texclass` que MathJax inyecta en el MathML serializado. Conversión a `<mfenced>` —deprecado en MathML Core y que Chrome ignora de todas formas—. Combinaciones de CSS con `line-height: normal` y `font-size: inherit`. Ninguno resolvió el problema de fondo, porque el problema de fondo no es de atributos ni de estilos. Es que Chromium no tiene implementado el algoritmo completo de construcción de glifos elásticos.

El Issue #1415218 sigue abierto mientras escribo esto. Google tiene, según la correspondencia del W3C, “un plan a largo plazo para cambiar cómo funciona el renderizado”. En el universo de los proyectos de infraestructura de browsers, “largo plazo” es una unidad de tiempo que no conviene esperar sentado.

Me rendí. Parcialmente.

---

## 4. Ceder Soberanía, Elegir el Mal Menor

La encrucijada era clara. Las opciones técnicas disponibles que cumplían mis principios —sin JavaScript en el cliente, sin CDN, compilación offline— todas tenían un compromiso:

- SVG precompilado con MathJax: cross-browser perfecto, pero vector rígido. Sin copy-paste de variables. Sin indexación semántica. Los lectores de pantalla ven imagen, no matemática.
- CHTML precompilado con MathJax: HTML+CSS tipográfico real, pero las fuentes matemáticas se cargan desde la CDN de jsDelivr en runtime. No es soberano.
- KaTeX en el cliente: tipografía impecable, pero requiere JavaScript y CDN. Los mismos problemas del inicio.
- KaTeX precompilado en Node.js: genera HTML+CSS puro con las fuentes copiadas localmente. Sin JS en el cliente. Offline. Soberano. Pero no es MathML nativo — es una capa de abstracción sobre el estándar.

Elegí KaTeX precompilado. Es la opción menos mala que cumple los tres principios sin comprometer la tipografía. El precio que pago es que el HTML generado depende de las convenciones internas de KaTeX, no del estándar abierto. Si KaTeX cambia su estructura de clases CSS en una versión mayor, hay que regenerar todo el catálogo. Es un riesgo de mantenimiento acotado y manejable. Lo acepto.

---

## 5. La Arquitectura Final: KaTeX Precompilado

La arquitectura de KaTeX genera una estructura híbrida compuesta por dos capas paralelas en el mismo HTML:

1. Un bloque `<math>` invisible (MathML semántico) para indexación por buscadores y lectores de pantalla.
2. Un árbol de `<span>` con clases CSS posicionadas por coordenadas exactas para el renderizado visual.

El segundo componente no le pide nada al engine MathML del browser. Los `<span>` son HTML puro. Chrome, Firefox y Safari los renderizan de forma idéntica.

El pipeline se compone de cuatro piezas:

```xml
[assets/matematica.json]          ──>  precompilar_math.js
[content/**/matematica.json]      ──>  (con namespace automático)
                                        │
                                        ▼
                              [data/ecuaciones_renderizadas.json]
                                        │
[content/ensayos/*.md]  ──>  {{< eq "clave" >}}  ──>  Hugo inyecta en RAM
```

### El catálogo de fórmulas

Las fórmulas se declaran en JSON, no en el Markdown. La única regla es duplicar las barras invertidas de LaTeX (`\\` en lugar de `\`):

```json
{
  "latencia_unbound": "25\\text{ms (Ida al VPS)} + 33.3\\text{ms (Unbound)} = \\mathbf{58\\text{ms}}",
  "matriz_routing": "\\hat{A} = \\begin{pmatrix} 0 & e^{i\\theta} \\\\ e^{-i\\theta} & 0 \\end{pmatrix}"
}
```

Los catálogos locales en `content/ensayos/mi-articulo/matematica.json` reciben el nombre de la carpeta como namespace automático: la clave `"resultado"` queda disponible como `"mi-articulo.resultado"` en cualquier parte del sitio.

### El script de precompilación

```javascript
const katex = require('katex');

function renderizarFormula(tex) {
  const html = katex.renderToString(tex, {
    displayMode:  true,
    throwOnError: false,
    strict:       false,
  });
  return `<div class="math-block">\${html}</div>`;
}
```

El script incluye caché inteligente por fecha de modificación (`mtimeMs`): si el JSON no cambió desde la última ejecución, reutiliza el output existente. Solo reprocesa lo que cambió.

### El shortcode

Un solo archivo en `layouts/shortcodes/eq.html`, una sola línea:

```
{{ index .Site.Data.ecuaciones_renderizadas (.Get 0) | safeHTML }}
```

Goldmark nunca ve LaTeX. Hugo lee el JSON precompilado directo desde la RAM e inyecta el HTML de KaTeX en la página final. El `| safeHTML` le indica a Hugo que el contenido proviene de una fuente de confianza y debe insertarse sin _escaping_.

### Carga condicional del CSS

Para no penalizar los artículos sin matemática, el CSS de KaTeX se carga solo cuando el _front matter_ del artículo lo declara:

```javascript
---
title: "Teoría de Grafos Cuánticos"
formula: true
---
``````xml
{{ if .Params.formula }}
  <link rel="stylesheet" href="/css/katex.min.css">
{{ end }}
```

### Instalación

```php
# Instalar KaTeX
npm install katex

# Copiar assets al tema (una sola vez)
mkdir -p static/css static/fonts
cp node_modules/katex/dist/katex.min.css static/css/katex.min.css
cp -r node_modules/katex/dist/fonts/.    static/fonts/

# Ciclo de trabajo
node precompilar_math.js && hugo server --cleanDestinationDir --disableFastRender
```

La carpeta `fonts/` debe quedar al mismo nivel que `css/` porque `katex.min.css` referencia las fuentes con rutas relativas (`../fonts/KaTeX_Math-Italic.woff2`). Sin esa estructura, el CSS carga pero las fuentes dan 404.

---

## Conclusión

El artículo sobre DNS finalmente se publicó con las fórmulas de latencia correctas, tipografía impecable, sin JavaScript en el cliente y sin CDN. El pipeline compila offline. Las fuentes matemáticas viven en el propio servidor.

No es la solución que quería. Quería MathML nativo, el estándar abierto, sin capas de abstracción propietarias. El Chromium Issue #1415218 me lo impidió. Lo que los browsers no terminan de implementar bien, los autores técnicos lo resolvemos con herramientas de compilación local. No es nuevo. Es la historia de siempre.

El W3C Math Working Group reconoció formalmente en 2023 que el _stretching_ de operadores es el obstáculo más crítico para la adopción de MathML nativo en la web. Google tiene un plan a largo plazo. Igalia continúa el trabajo que nadie más financia.

Goldmark nunca aprendió matemática. Chrome todavía no terminó de aprenderla. El artículo sobre DNS está publicado de todas formas.

---

## Google a Trabjar. Gracias KaTeX Team

Para cerrar esta bitácora, acá hay un par de demostrecen empíricas. Ecuaciones que, debido a su profunda complejidad estructural, anidamiento hiperbólico y dependencias tipográficas de matrices OpenType MATH, serían absolutamente imposibles de renderizar de forma coherente en Google Chrome de manera nativa sin nuestro pipeline estático de KaTeX.

¡En sus caras, Chromium dev team!

### 1. La Ecuación Funcional de la Función Zeta de Riemann

Un bloque clásico de cálculo avanzado que exige un balance exacto de fracciones, integrales al infinito y escalado de la función Gamma:

$$\zeta(s)=2^{s}\pi^{\,s-1}\sin\!\left(\frac{\pi s}{2}\right)\Gamma(1-s)\zeta(1-s)$$

### 2. Matriz de Autovalores de un Hamiltoniano Cuántico Complejo

La pesadilla geométrica definitiva de Chromium. Una matriz de bloques fraccionarios aninados con exponentes cuánticos, donde los paréntesis elásticos exteriores se estiran por coordenadas CSS absolutas sin confiar un solo píxel al bug de estiramiento del navegador:

H^=(E0+Δγe−iϕ0γeiϕE0−Δβ0βE1) \widehat{H} =
\begin{pmatrix}
E\_0+\Delta & \gamma e^{-i\phi} & 0 \\
\gamma e^{i\phi} & E\_0-\Delta & \beta \\
0 & \beta & E\_1
\end{pmatrix}

Hoy, estas ecuaciones se sirven en texto plano enriquecido, se copian al portapapeles en microsegundos, son indexadas por arañas web y se ven perfectas en cualquier pantalla. El control de la infraestructura volvió a la laptop.
