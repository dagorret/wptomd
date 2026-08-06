---
title: 'El Triunfo del Pragmatismo: Por Qué (Aún) Sigo Eligiendo WordPress'
slug: el-triunfo-del-pragmatismo-por-que-aun-sigo-eligiendo-wordpress
status: published
legacy_url: https://dagorret.com.ar/el-triunfo-del-pragmatismo-por-que-aun-sigo-eligiendo-wordpress/
wordpress_id: 1340
published_at: '2026-07-11T12:16:20'
modified_at: '2026-07-11T13:52:32'
wordpress_category_ids:
- 21
wordpress_tag_ids:
- 367
- 363
- 185
- 365
- 366
- 364
categories:
- &id001
  id: 21
  name: Sistemas
  slug: sistemas
tags:
- id: 367
  name: Cloudflare
  slug: cloudflare
- id: 363
  name: CMS
  slug: cms
- id: 185
  name: Infraestructura
  slug: infraestructura
- id: 365
  name: Nginx
  slug: nginx
- id: 366
  name: Rendimiento
  slug: rendimiento
- id: 364
  name: WordPress
  slug: wordpress
category: *id001
---

Es una tentación recurrente en el mundo de los sistemas: mirar de reojo el panel de administración de WordPress y sentir que uno arrastra una herramienta de 2003 mal disimulada bajo actualizaciones cosméticas. En una industria que durante la última década construyó buena parte de su prestigio técnico alrededor de los generadores de sitios estáticos, el aislamiento de contenedores y la pureza del código plano, WordPress suele quedar del lado equivocado del argumento, casi por default.

​Yo mismo sostuve esa posición durante bastante tiempo. Pero someter la infraestructura a condiciones de estrés reales —y no a la intuición sobre lo que “debería” ser más eficiente— obliga a revisar esa jerarquía. Lo que sigue es el resultado de comparar alternativas por su comportamiento medible, no por su reputación, y de leer con más detenimiento los números de adopción real que rara vez acompañan a los argumentos técnicos sobre elegancia arquitectónica.

### ​1. El descarte de Docker

​En la búsqueda de un entorno aislado y reproducible, el primer paso lógico parecía ser Docker: un contenedor para Nginx, otro para PHP-FPM, otro para MariaDB. Es una arquitectura con ventajas reales en portabilidad y en consistencia entre entornos de desarrollo y producción, y no hay razón para negarlo.

​Pero en un VPS de recursos medidos, esa capa de abstracción tiene un costo que no es teórico: el consumo base de memoria por contenedor, la gestión de volúmenes sobre disco y el enrutamiento de red interno entre servicios restan ciclos de reloj que, en un servidor con recursos ajustados, terminan siendo relevantes. Sacar Docker de la ecuación y correr Nginx, PHP y MariaDB directamente sobre el sistema operativo eliminó ese intermediario. El resultado fue un entorno donde los procesos hablan de manera directa con el kernel, reduciendo la latencia interna del stack.

### ​2. Los límites de los generadores estáticos (Hugo)

​La promesa de un generador de sitios estáticos como Hugo es real: HTML puro, sin base de datos, sin PHP, servido desde caché o memoria. Es, en términos de tiempo de respuesta puro, la opción más rápida posible.

​El problema no es de rendimiento sino de flujo editorial. Escribir con cierta frecuencia implica subir una imagen sobre la marcha, corregir una errata desde el celular, o previsualizar un borrador sin pasar por un pipeline. En Hugo, cada edición exige un _commit_, una compilación y un despliegue. Y el minimalismo del modelo se rompe apenas se necesita un buscador interno o una categorización dinámica compleja: lo que en WordPress es una consulta indexada nativa a la base de datos, en un generador estático requiere inyectar indexadores externos en JavaScript. La velocidad de entrega no compensa la fricción si termina frenando al autor.

### ​3. El costo real de desarrollar un CMS propio (Faro)

​Frente a la frustración con las herramientas existentes, la reacción natural de cualquier desarrollador es construir la propia solución. Así surgió Faro, mi intento de CMS a medida sobre Laravel, pensado desde el inicio con la optimización como prioridad.

​Laravel es un entorno sólido y bien diseñado, pero construir un CMS moderno desde cero deja ver la escala real del problema: un flujo editorial completo —gestión de bloques, procesamiento de imágenes, previsualización en tiempo real, borradores automáticos, seguridad perimetral— consume una cantidad de tiempo desproporcionada frente al beneficio. Mantener y desarrollar ese sistema en paralelo se vuelve un trabajo de ingeniería constante que compite directamente con el tiempo disponible para escribir. Esto no invalida a Faro como proyecto de desarrollo en sí mismo; sí lo descarta, al menos por ahora, como la base de este blog en particular.

### ​4. October CMS y Blogger

​El resto del espectro se descarta con menos vueltas. October CMS, también construido sobre Laravel, es una herramienta potente pensada para ingenieros de software, pero introduce sobreingeniería para un blog de contenidos: mezcla la lógica de backend con la gestión de páginas, obligando a pensar como desarrollador incluso para editar un párrafo.

​Blogger, por su parte, implica renunciar a cualquier control sobre la infraestructura: sin acceso a Nginx, sin control de cabeceras HTTP, sin posibilidad de optimizar nada por debajo de la capa de presentación, la plataforma es un nodo prescindible que Google puede reconfigurar o discontinuar sin que medie ninguna decisión propia.

### ​5. Los números bajo estrés real

​La teoría es maleable; los datos de producción, menos. Para justificar el regreso a WordPress sobre metal nativo —sin Docker, con FastCGI Cache configurado directamente en Nginx— sometí al servidor a un test de estrés con ráfagas de peticiones simultáneas contra el sitemap del sitio.

​Sin caché activada, apenas diez usuarios simultáneos forzando el procesamiento dinámico bastaban para clavar la CPU del VPS al 100% durante tres a cinco segundos, mientras el servidor compilaba PHP y consultaba las tablas de la base de datos en cada petición. Con FastCGI Cache activado —evitando que las peticiones toquen PHP o MariaDB salvo cuando el contenido cambia— el comportamiento cambió de manera notable: con treinta peticiones simultáneas el uso de CPU se estabilizó en torno al 75% en los picos dinámicos, y al subir a cincuenta peticiones simultáneas el tiempo de respuesta bajó a un segundo, con la CPU todavía tocando el 100% pero resolviendo mucho más volumen por unidad de tiempo. Llevado al extremo, el servidor procesó ráfagas de quince mil peticiones simultáneas manteniendo el uso de CPU en apenas 29,6%, devolviendo códigos HTTP 200 en milisegundos.

​Esto se traduce en las métricas de experiencia de usuario: en Google PageSpeed Insights el sitio alcanzó 100/100 en escritorio y 92/100 en dispositivos móviles, incluyendo el renderizado de ecuaciones matemáticas complejas vía KaTeX sin demoras visuales perceptibles.

### ​6. Un poco de contexto de mercado

​Vale la pena separar la anécdota del patrón general, porque el argumento anterior es válido para mi caso de uso —un blog personal de publicación frecuente— pero no dice nada por sí solo sobre qué tan representativo es ese caso.

​En volumen absoluto, WordPress no es una opción entre varias: según W3Techs, a mediados de 2026 impulsa alrededor del 41,5% de todos los sitios web del mundo, lo que equivale a cerca del 60% del mercado de sitios que efectivamente usan algún CMS identificable. Es una cifra que viene creciendo de forma sostenida desde el 21% que tenía en 2014, y que en 2021 marcó un punto de inflexión: fue el primer año en que un único CMS superó en cantidad de sitios a la suma de todos los sitios sin ningún CMS, algo que hasta entonces nunca había ocurrido. Lo interesante es que esa dominancia no se limita a la cola larga de sitios pequeños: el reporte Cloudflare Radar de 2025 sobre los cinco mil dominios de mayor tráfico del mundo muestra que el software libre —WordPress más Drupal— sigue concentrando más de la mitad de ese segmento de altísima escala, desmintiendo la idea de que WordPress es solo una solución para proyectos chicos.

​Los generadores estáticos, en cambio, ocupan un nicho mucho más fragmentado y, en términos relativos, minúsculo. Entre quienes efectivamente usan un SSG, ningún actor concentra el mercado de forma comparable a como lo hace WordPress en el suyo: Gatsby, Astro y Hugo se reparten porciones similares, todas rondando el 23-25% del segmento SSG. El ecosistema completo del Jamstack —el nombre bajo el que se agrupó buena parte de este movimiento entre 2016 y 2023— alcanzó un mercado estimado de 1.410 millones de dólares en 2024, una fracción diminuta comparada con la escala de la economía que gira alrededor de WordPress.

​Y es revelador que el propio término Jamstack haya sido retirado por Netlify, la empresa que lo acuñó, a fines de 2023, reemplazado por la etiqueta más amplia de “arquitectura composable”: la promesa original de sitios puramente estáticos terminó absorbida por frameworks híbridos como Next.js o Astro, que combinan generación estática, renderizado en el servidor y regeneración incremental según la página, en lugar de imponer un único modelo de entrega para todo el sitio. Diez años de literatura técnica sobre el tema —desde los primeros manifiestos de 2016 hasta los capítulos anuales del Web Almanac de HTTP Archive— documentan ese mismo recorrido: el estático puro ganó la discusión sobre rendimiento teórico y perdió la discusión sobre flujo de trabajo real, y terminó disolviéndose dentro de arquitecturas híbridas en vez de reemplazar a los CMS dinámicos.

​¿Y quién compone, en la práctica, ese universo de sitios? Una porción sustancial es exactamente el tipo de proyecto que este artículo describe: se estima que existen más de 600 millones de blogs activos e inactivos en el mundo, sobre un total de entre 1.100 y 1.500 millones de sitios, lo que ubica a la publicación tipo blog —personal o corporativa— como una fracción muy relevante del total, más de un tercio según distintas mediciones. Del otro lado, más del 65% de los sitios corporativos incluye una sección de blog, y entre las empresas Fortune 500 el porcentaje que mantiene un blog público pasó de aproximadamente 50% en 2010 a más de 77% en la actualidad.

​En cuanto a tamaño, los sitios corporativos chicos y medianos —el tipo de proyecto donde la elección de CMS realmente se discute, más allá de los casos extremos de e-commerce masivo o medios de gran escala— convergen de forma consistente en un rango de entre 8 y 30 páginas según distintos estudios de agencias y firmas de diseño web, con los sitios de servicios profesionales tendiendo a la parte alta de ese rango (15 a 20 páginas) y los sitios de negocios locales más simples a la parte baja. Es, en términos de complejidad de contenido, un universo mucho más cercano al de un blog bien estructurado que al de una aplicación web compleja, lo cual explica en buena medida por qué un CMS pensado originalmente para blogs terminó siendo la base por defecto también para ese segmento.

### ​Conclusión

​WordPress no gana esta comparación por tener el código más elegante ni por ser la opción con mejor rendimiento teórico en el papel. Gana por una combinación menos vistosa: un modelo de datos maduro para contenido editorial, un ecosistema que resuelve en meses lo que un desarrollo propio tarda años en igualar, y una base instalada tan grande que la mayoría de los problemas de rendimiento y seguridad ya fueron identificados y resueltos por alguien más antes de que uno los encuentre.

​Sacarle de encima el lastre de los plugins innecesarios, correrlo sobre metal nativo en lugar de un stack en contenedores, y ponerle por delante un caché a nivel de servidor web respaldado por las reglas perimetrales de un WAF cambia por completo el panorama de rendimiento. Los números de la prueba de estrés lo confirman, y los números de adopción a escala global explican por qué esa combinación —lejos de ser una rareza— es también la que terminó eligiendo la mayor parte de la web que se le parece a este proyecto. No es una cuestión de afecto por un framework en particular: es una cuestión de eficiencia medida, tanto en el propio servidor como en el patrón que siguió el resto de la industria.

_Fuentes de los datos de mercado citados: W3Techs (Usage Statistics and Market Share of Content Management Systems, julio 2026), Cloudflare Radar (2025), HTTP Archive Web Almanac (capítulo CMS), Netlify/Jamstack (informe State of Jamstack), wmtips.com (market share de generadores estáticos), y agregadores de estadísticas de sitios de pequeñas empresas (Wix, Forbes, Zippia, Colorlib, DemandSage)._
