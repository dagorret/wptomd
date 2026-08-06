---
title: ¿Por qué optimizar al máximo puede arruinar tu ciencia? El peligro oculto de
  CachyOS y la bandera -O3
slug: por-que-optimizar-al-maximo-puede
status: published
legacy_url: https://dagorret.com.ar/por-que-optimizar-al-maximo-puede/
wordpress_id: 1047
published_at: '2026-06-06T16:25:33'
modified_at: '2026-06-06T16:25:33'
wordpress_category_ids:
- 21
wordpress_tag_ids:
- 181
- 173
categories:
- &id001
  id: 21
  name: Sistemas
  slug: sistemas
tags:
- id: 181
  name: Ingeniería de Software
  slug: ingenieria-software
- id: 173
  name: Metodología Científica
  slug: metodologia-cientifica
category: *id001
---

Cuando armamos un entorno para investigar, analizar datos econométricos o correr modelos estadísticos, la tentación de la velocidad es enorme. Queremos exprimir cada ciclo del procesador. Es ahí donde entran alternativas de nicho espectaculares como __CachyOS__, prometiendo exprimir el silicio con kernels modificados y binarios hiper-optimizados bajo la agresiva bandera __-O3__ del compilador.

Suena perfecto, ¿no? Más velocidad, papers listos antes, gráficos que se renderizan en milisegundos.

Pero en la ciencia cuantitativa, la velocidad sin control es una trampa. Hay un límite muy delgado entre la eficiencia y lo que llamo __deuda epistémica__: acumular opacidad sobre el sustrato de cómputo hasta perder el rastro de la fidelidad de tus propios datos.

### La ilusión del “terminó con éxito”

El gran peligro del software hiper-optimizado es que el error no te va a tirar un cartel rojo de alerta. No va a colapsar el sistema ni va a dejar un registro de fallo en `journalctl`. El modelo va a correr, la barra de progreso va a llegar al 100% y el programa va a cerrar con un código de salida exitoso.

Pero por debajo, en el nivel del silicio, pasaron cosas.

Al compilar con la bandera __-O3__, el compilador deja de ser un traductor pasivo y se vuelve agresivo. Reordena instrucciones y aplica optimizaciones que asumen que tu código es perfecto. El problema es que gran parte de las bibliotecas matemáticas científicas que usamos (en R, Python o Fortran) tienen décadas encima o manejan la memoria de formas que violan esas suposiciones.

Dos ejemplos rápidos de cómo se rompe la matemática en silencio:

- __El caos del Strict Aliasing:__ Si el compilador agresivo asume que dos variables distintas no apuntan al mismo lugar de la memoria, para ahorrar tiempo va a reutilizar valores viejos que guardó en los registros de la CPU, en lugar de ir a buscar el dato real a la RAM. El cálculo avanza con un número desactualizado. Nadie se entera.
- __La trampa del Punto Flotante:__ En matemática pura, __(a + b) + c__ es igual a __a + (b + c)__. La suma es asociativa. Pero en computación (bajo el estándar IEEE 754), los decimales no son exactos y la propiedad asociativa no se cumple. Cuando __-O3__ reordena y vectoriza las operaciones para distribuirlas en paralelo en los canales de la CPU, altera el orden del cálculo. El error de redondeo microscópico se propaga diferente. Al final del día, tu p-valor cambió en el cuarto decimal.

### Del reactor nuclear de Three Mile Island a tu terminal de Linux

Esto no es un debate caprichoso sobre milisegundos; es un problema de arquitectura de la información.

En 1979, el accidente nuclear de Three Mile Island ocurrió, en parte, porque los paneles de la sala de control indicaban que una válvula crítica estaba cerrada. La interfaz decía la verdad sobre la orden que la computadora había enviado, pero mentía sobre la realidad física de la válvula, que se había quedado trabada abiertamente.

El investigador que corre modelos estadísticos sobre binarios hiper-optimizados está en la misma sala de control: mira una interfaz limpia que reporta normalidad, pero carece de herramientas para verificar si el compilador alteró el comportamiento matemático en el fondo del procesador.

### Arch Linux y la soberanía del entorno Vanilla

¿Por qué sigo eligiendo __Arch Linux__ puro para investigar en lugar de saltar a distros enfocadas en el rendimiento extremo? Por la transparencia estructural.

Arch distribuye sus paquetes en formato _vanilla_ (puro, tal como sus creadores los diseñaron). No hay parches raros de optimización de terceros metidos en el medio. Si NumPy o R hacen un cálculo, sabés que se está ejecutando bajo las condiciones estándar probadas por toda la comunidad científica global.

Además, opera un mecanismo de auditoría distribuida (muy similar a la lógica económica de Hayek): la masa crítica de usuarios reportando sobre una misma base homogénea garantiza que cualquier anomalía salte a la luz de inmediato. Si te corrés a un entorno de nicho hiper-optimizado, te quedás solo en tu propia isla epistémica.

### Conclusión: Desplazar la carga de la prueba

La ciencia exige reproducibilidad. Si tu entorno operativo altera el orden de las instrucciones matemáticas para ganar un 5% de velocidad, la duda ya quedó instalada.

No nos corresponde a los investigadores demostrar analíticamente en qué línea de código falló el decimal; les corresponde a los defensores de la optimización agresiva probar activamente que sus binarios modificados son inmunes a estas desviaciones antes de meterlos en un laboratorio científico.

Para jugar, diseñar o editar video, la velocidad localizada es espectacular. Para hacer ciencia, la prudencia y la predictibilidad metodológica son lo único que importa.

__Ensayo completo y referencias técnicas (v1.4):__ htt[ps://doi.org/10.5281/zenodo.20584492](https://doi.org/10.5281/zenodo.20584492)
