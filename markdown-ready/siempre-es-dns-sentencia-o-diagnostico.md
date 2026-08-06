---
title: 'Siempre Es el DNS: sentencia o diagnostico'
slug: siempre-es-dns-sentencia-o-diagnostico
status: published
legacy_url: https://dagorret.com.ar/siempre-es-dns-sentencia-o-diagnostico/
wordpress_id: 16
published_at: '2026-06-22T08:26:15'
modified_at: '2026-06-22T08:26:15'
wordpress_category_ids:
- 21
wordpress_tag_ids:
- 123
categories:
- &id001
  id: 21
  name: Sistemas
  slug: sistemas
tags:
- id: 123
  name: Resolución de Nombres
  slug: resolucion-nombres
category: *id001
---

Alguien aparece con la urgencia ya cargada. “No anda la wifi”, dice, y casi en la misma frase viene el nombre del culpable: lo dejó así el que estuvo antes, alguien tocó algo, hay un responsable y no soy yo. El veredicto llega antes que la evidencia. La sentencia está firmada antes de que nadie haya mirado una sola pantalla.

En esta casa no operamos sobre “parece que anda”. Operamos sobre certeza técnica, y la certeza técnica tiene un requisito incómodo: hay que ir a buscarla. Lo que sigue no es una guía de troubleshooting de DNS —no me interesan acá los comandos— sino la anatomía de por qué esa primera frase, la del culpable, es casi siempre falsa, y de dónde sale en realidad el fantasma.

## 1. “No anda la wifi” no es un diagnóstico

Conviene separar dos cosas que la urgencia funde en una sola. Una observación describe un estado del sistema: tal servicio responde, tal otro no, en tal capa, a tal hora. Una sentencia, en cambio, hace dos movimientos a la vez: declara que todo está roto y reparte la culpa. “No anda la wifi” pertenece al segundo grupo. Es vaga —no dice qué dejó de andar, ni dónde, ni desde cuándo—, es total —todo o nada, sin grados— y, sobre todo, necesita un acusado. Esas tres propiedades no son casuales: son exactamente lo que un juicio precisa para sostenerse sin pruebas. Mientras la falla siga siendo vaga y total, cualquiera puede ser el responsable. La imprecisión no es un defecto del relato; es su combustible.

El diagnóstico empieza, literalmente, por negarse a firmar esa sentencia. No porque uno sea bueno, sino porque la sentencia no contiene información. “No anda la wifi” no me dice nada que pueda medir. “Tengo conectividad pero no resuelvo nombres” me dice todo.

## 2. El chequeo que nadie hizo

Porque eso era lo que estaba pasando, y era trivial de ver. La red andaba. Los paquetes circulaban sin problema. Lo único caído era la traducción de nombres a números: una capa específica, nombrable, y para colmo ubicada arriba y afuera de la máquina del que se quejaba. La distinción es de manual y se resuelve en diez segundos: si una dirección numérica responde y un nombre no, el problema no es la red, no es el cable, no es la wifi y no es la persona que estuvo antes. Es la resolución.

Ese es el detalle que vuelve el episodio casi cómico, si no fuera tan típico. Quien acusaba estaba parado sobre la prueba de que su propio veredicto era falso. Tenía conectividad: la wifi, eso que declaraba muerto, funcionaba perfectamente. Le alcanzaba con bajar la vista diez segundos para ver que la falla no estaba donde apuntaba el dedo. Nunca bajó la vista. Y ahí está el punto que me interesa: la histeria no vivía en la falla. La falla era chiquita y estaba quieta. La histeria vivía en el hueco entre la queja y el chequeo, en ese espacio que se abre cuando alguien decide sentenciar en lugar de mirar.

## 3. Siempre es DNS (y nunca es brujería)

Hay una salvedad honesta que hacer acá, y es que el componente que falló no fue una elección inocente del destino. Era DNS. De toda la infraestructura, justo el que arrastra más mitología. Existe un folklore entero en la cultura sysadmin alrededor de la idea de que, al final, siempre es DNS: esa resignación medio cómica de descartarlo una y otra vez para que termine siendo, efectivamente, eso. Es el fantasma perfecto de la infraestructura: invisible, intermitente, el último que uno revisa y el que tenía la culpa.

Pero el folklore tiene dos lecturas, y la diferencia entre ellas es la diferencia entre un equipo maduro y uno hechizado. La lectura perezosa es mística: “el DNS se rompe solo, es maña, es brujería”. La lectura disciplinada es exactamente la opuesta: precisamente porque sabemos que muchas veces es DNS, la sospecha entrenada apunta a una capa nombrable, no a una persona nombrable. El fantasma es ubicable. El chivo expiatorio es una ficción. Que sea “siempre DNS” no es una maldición: es una pista. Y una pista es lo contrario de un hechizo.

## 4. La cacería necesita un humano; el método nombra una capa

Acá se ve la mecánica completa. Una cacería de brujas necesita dos cosas para funcionar: que la falla sea difusa y que haya alguien a quien señalar. El método empírico ataca las dos a la vez. En el momento en que nombrás la capa —no “no anda la wifi” sino “el resolver upstream dejó de responder”—, la bruja y el chivo expiatorio se evaporan juntos. Ya no hay un todo roto: hay un componente preciso. Y como el componente no tiene cara ni turno, ya no hay a quién culpar. La precisión técnica es, sin que nadie lo proponga así, un acto de justicia: deja de haber inocentes que defender porque deja de haber acusados.

Por eso el veredicto sin chequeo no es, en el fondo, un error técnico. Es un acto moral —repartir culpa— disfrazado de juicio técnico. Y la única forma de desactivarlo no es discutir el relato, que siempre tiene respuesta, sino poner la evidencia sobre la mesa. Hay un tratamiento más formal de por qué esto es así, de por qué el diagnóstico es en el fondo una práctica epistemológica y no una destreza mecánica; lo desarrollé aparte, con el rigor que el tema pide. Acá me quedo en la trinchera, que es donde la cosa pasa de verdad.

## Cierre: diez segundos de mirar

Cuando hice los chequeos y dije lo que había: que era DNS, upstream, fuera de nuestro alcance y de la mano de nadie del equipo, lo que vino fue silencio. Durante un tiempo lo leí como incomodidad. Hoy lo leo como lo que era: una hipótesis falsada en vivo, sin nada para responder. El relato necesita aire; el dato lo deja sin oxígeno.

Queda la salvedad, porque esta casa no promete finales heroicos. El chequeo no te hace tener razón: te hace ser auditable, que es distinto y es más. A veces la causa está genuinamente fuera de tu control —un upstream que no manejás, como en este caso—, y entonces no hay nada que arreglar en el momento. Pero incluso ahí, lo que el método te da no es la solución: es el derecho a nombrar la capa en lugar de señalar a una persona. Los diez segundos de mirar antes de sentenciar no siempre arreglan la red. Siempre disuelven el tribunal.
