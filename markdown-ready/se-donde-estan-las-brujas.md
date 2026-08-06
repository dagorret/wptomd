---
title: Sé dónde están las brujas
slug: se-donde-estan-las-brujas
status: published
legacy_url: https://dagorret.com.ar/se-donde-estan-las-brujas/
wordpress_id: 1039
published_at: '2026-06-20T11:04:22'
modified_at: '2026-06-20T11:04:22'
wordpress_category_ids:
- 33
wordpress_tag_ids:
- 168
- 180
- 354
categories:
- &id001
  id: 33
  name: Política
  slug: politica
tags:
- id: 168
  name: Estudios Culturales
  slug: estudios-culturales
- id: 180
  name: Historia del Pensamiento
  slug: historia-pensamiento
- id: 354
  name: Informática
  slug: informatica
category: *id001
---

> Acá en Informática no hay histeria. Hay argumento. No anda la Wi-Fi por el DNS, el cable, el viento, el sol o un terremoto. Porque las brujas, sé dónde están… y no es ahí.»

En los pasillos de cualquier dirección de sistemas o unidad de tecnología informática, el aire suele estar viciado de urgencias ajenas. El usuario común se desespera, el directivo se impacienta y el teléfono arde. Ante la caída de un servicio crítico, el entorno tiende naturalmente a la histeria colectiva.

Sin embargo, en el corazón de un equipo técnico de alto rendimiento, la histeria es un lujo inútil. En la trinchera del soporte y la infraestructura, la única verdad que vale es la que puede medirse y, por lo tanto, argumentarse. Todo lo demás es ruido.

## El mito de las brujas informáticas

Es común escuchar el diagnóstico perezoso del “no anda”. A veces, incluso dentro de los equipos técnicos en formación, se apela a una suerte de misticismo tecnológico: “ayer funcionaba y hoy no”, “se rompió solo”, “debe ser una maña del servidor”. Atribuir los fallos a la volatilidad del azar o a la brujería del software es el primer paso hacia el fracaso operativo.

Conviene ser honestos en este punto, porque la trampa está justo acá. No voy a decir que los sistemas son perfectamente deterministas y que nunca pasa nada raro: existen las condiciones de carrera, existen los heisenbugs que se evaporan apenas los mirás de cerca, existe el bit que se voltea por radiación y que la memoria ECC corrige en silencio precisamente porque ocurre. El mundo real es más sucio que el manual. Lo que sostengo es algo más fuerte y más útil que el determinismo: los sistemas son auditables. Toda falla deja rastro, aun la que parece capricho.

Y ahí está la clave de todo el asunto. La bruja no es la ausencia de causa: es la ausencia de medición. El fantasma aparece exactamente en el hueco que deja una causa que nadie observó. Donde no se mide, se cuela el relato. Por eso el verdadero líder informático sabe dónde están las brujas, y no están en el azar: están en la falta de documentación, en el mantenimiento postergado, en las pruebas mal hechas, en el comando de diagnóstico que nadie tipeó. La Wi-Fi no se cae por un capricho del destino. Se cae por una colisión de canales, una asignación fallida del DHCP, un Categoría 6 estrangulado en un paso técnico, una tormenta de broadcast o, sí, el DNS que volvió a fallar. Ninguna de esas cosas es magia. Todas dejan huella. La magia es solamente el nombre que le ponemos a la huella que no fuimos a buscar.

## De la opinión al dato

Dirigir un equipo técnico con templanza exige desterrar la cultura de la suposición. Cuando un ProLiant cae o el almacenamiento iSCSI de un NAS empieza a perder latencia, las opiniones subjetivas restan tiempo y suman confusión. La excelencia técnica no consiste en adivinar mejor, sino en dejar de adivinar.

Ahora bien, llamar a esto “el método científico en el rack” sería quedarse corto, y hasta un poco ingenuo. Lo que hacemos bajo presión se parece menos a la física de laboratorio y más al diagnóstico clínico: razonamos por abducción, buscando la mejor explicación disponible para los síntomas que tenemos delante, y avanzamos por bisección, partiendo el problema al medio una y otra vez hasta arrinconar la causa. El primer gesto es siempre aislar: ¿falla todo el segmento o solo una boca del switch? Recién entonces medimos, porque los logs, los analizadores de paquetes, las trazas de ruta y el consumo de memoria en tiempo real son los únicos testigos que no mienten. Y solo con esa evidencia sobre la mesa formulamos una hipótesis. No se cambia un parámetro “por si acaso”: se propone una corrección basada en el comportamiento registrado del hardware, y se verifica. Un equipo que aprende a hablar en el idioma de los datos es un equipo inmune a la desesperación. Cuando el resto de la organización corre en círculos, el informático lee el flujo de paquetes.

## El rol del líder: exigir el argumento

Conducir un área tecnológica no implica saber resolver al instante cada error de memoria ni cada línea de código. Implica gestionar la metodología del pensamiento del equipo. Es un trabajo sobre la cabeza de la gente antes que sobre los fierros.

Exigir que un problema se presente con un argumento empírico, y no con una queja abstracta, transforma la cultura de una oficina. Obliga al técnico a investigar antes de reportar, a respaldar su sospecha con una captura, un ping, una traza, un código de error del kernel. Sube la vara de todos, porque vuelve costoso el “no anda” y barato el “lo medí, esto es lo que veo”.

Al final del día los servidores se caen, las redes se saturan y los contenedores fallan. Es parte del territorio; no hay infraestructura que no tiemble. Pero cuando tiembla, el respeto y la autoridad no se ganan gritando más fuerte, sino sosteniendo la solución sobre la base sólida de la evidencia. Porque en la informática, como en la ciencia, la evidencia mata a los fantasmas… y, de paso, a cualquier bruja.
