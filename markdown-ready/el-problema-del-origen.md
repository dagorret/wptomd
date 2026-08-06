---
title: El problema del origen de Linux
slug: el-problema-del-origen
status: published
legacy_url: https://dagorret.com.ar/el-problema-del-origen/
wordpress_id: 1025
published_at: '2026-06-26T17:48:10'
modified_at: '2026-06-26T17:48:10'
wordpress_category_ids:
- 33
- 21
wordpress_tag_ids:
- 180
- 352
categories:
- &id001
  id: 33
  name: Política
  slug: politica
- id: 21
  name: Sistemas
  slug: sistemas
tags:
- id: 180
  name: Historia del Pensamiento
  slug: historia-pensamiento
- id: 352
  name: Linux
  slug: linux
category: *id001
---

## __1. La historia en un renglón__

La historia oficial cabe en un renglón, y ahí está toda su fuerza. __Linus Torvalds creó Linux. Punto.__ No pide contexto, no pide genealogía, no pide que nadie se sienta incómodo. Un pibe, una obra, una fecha. Es la forma más vieja que tenemos de contar las cosas: alguien baja del monte con el fuego y nosotros, agradecidos, dejamos de preguntar de dónde salió el fuego.

Pero basta acercarse un poco para que el renglón se afloje. Porque en 1991, cuando aparece aquel mensaje tímido en un grupo de noticias —_“estoy haciendo un sistema operativo, nada serio, apenas un hobby”_—, casi todo lo que iba a volver posible a Linux ya estaba puesto sobre la mesa:

- __Unix:__ Existía hacía veinte años y había fijado para siempre una manera de pensar la máquina: archivos, procesos, un árbol, una shell, la idea de que todo se compone con todo.
- __Minix:__ Existía justamente para ser leído; un Unix de juguete que Andrew Tanenbaum había escrito para sus alumnos.
- __BSD:__ Existía, y estaba más maduro que cualquier cosa que un estudiante pudiera improvisar en una pieza.
- __GNU:__ Venía construyendo desde 1983 las herramientas de un Unix libre, pieza por pieza.
- __GCC:__ El compilador existía desde 1987, y sin un compilador libre no hay nada que compilar en libertad.
- __Internet:__ Existía, angosta y académica, pero suficiente para que un mensaje encontrara en pocas semanas exactamente a la gente que sabía qué hacer con él.
- __El procesador Intel 386:__ Daba vueltas desde 1985, y con él la posibilidad concreta de tener multitarea de verdad sobre una máquina barata, en un escritorio, sin sala refrigerada ni presupuesto de facultad.

Y estaba, sobre todo, una __cultura__: miles de personas ya entrenadas en compartir código, en arreglar lo ajeno, en discutir arquitectura por correo con una devoción casi litúrgica.

Mirá esa lista un segundo. No es una lista de piezas que faltaban. Es una lista de piezas que ya estaban. El campo de 1991 no estaba vacío, esperando a un genio. Estaba lleno. Lleno hasta el borde.

---

## __2. El truco del frasco sobresaturado__

Y ahí, sin que uno lo busque, aparece la imagen.

Hay un truco de laboratorio que parece magia barata de feria. Tomás un líquido transparente, quieto, de aspecto inofensivo. Lo tocás con un cristalito, una mota, casi nada. Y en segundos el frasco entero se vuelve sólido, de golpe, como si el tiempo se hubiera apurado, y encima larga calor. Lo que tenías no era un líquido cualquiera: era una __solución sobresaturada__. Un líquido que contiene mucho más de lo que debería poder contener, sostenido en un equilibrio nervioso, a punto de. No le falta nada para cristalizar. Le sobra todo. Lo único que está esperando es una excusa.

El campo de 1991 era exactamente eso.

Torvalds fue la excusa. La mota. El cristalito que alguien dejó caer en el frasco en el momento justo. No fabricó la sustancia: la sustancia llevaba años sobresaturada. No produjo el calor de la cristalización: ese calor ya estaba adentro, contenido, esperando. Lo que hizo —y no es poco— fue tocar el líquido en el lugar y el instante exactos. Cuando le agradecemos a Torvalds, le estamos agradeciendo a la mota de polvo. Y la mota, conviene no olvidarlo, también hizo algo: estuvo ahí, y cayó.

Porque una semilla no es nada y a la vez lo es todo. Un frasco sobresaturado va a cristalizar igual, con esta mota o con otra; eso es casi inevitable. Pero la forma que toma el cristal —su red, su geometría, su manera de ordenarse— depende de la semilla que lo gatilló.

Tanenbaum, que sabía bastante más que Torvalds, le dijo en el 92 que la red estaba mal elegida: que un núcleo monolítico era una idea vieja, que el futuro eran los microkernels. Tenía razón en abstracto y se equivocó en concreto. La solución cristalizó lo mismo, pero cristalizó alrededor de la red que traía la semilla del estudiante, no la del profesor. __El campo decidió que iba a haber un cristal. Torvalds decidió qué cristal.__

## __3. El azar y la incertidumbre legal__

Y después está el azar, que es la parte que más nos cuesta perdonar. Cuál mota cae primero, cuál toca el líquido antes que las otras, es pura contingencia.

En 1991 había otra semilla lista, más vieja, más madura, mejor terminada: __BSD__. Un Unix libre que le llevaba años de ventaja a cualquier cosa que un finlandés pudiera escribir entre dos parciales. ¿Por qué el frasco no cristalizó alrededor de BSD? Es una de esas preguntas cuya respuesta da un poco de vértigo: porque justo en esos años BSD estaba metido en un juicio —quién era dueño de qué partes del código de Unix— que le tapó el frasco con un cartel de incertidumbre legal en el peor momento imaginable. La semilla estaba, pero estaba guardada en un frasco que nadie se animaba a destapar.

La inevitabilidad, vista de cerca, está hecha de accidentes.

---

## __4. Redes, agencia y distribución__

Hay nombres para todo esto, claro. __Langdon Winner__ se pasó años pensando dónde reside la agencia: cuánto de lo que un objeto técnico hace está en el objeto y cuánto en el ordenamiento que lo rodea. __Bruno Latour__ discutió toda su vida que la capacidad de hacer que algo ocurra no es una propiedad de las personas sino un efecto de las redes: que nadie actúa solo, que a cada uno lo hacen actuar el procesador, el compilador, la lista de correo, la licencia, el frasco entero.

Desde ahí, _“Torvalds creó Linux”_ es casi una falta de ortografía. Pero la verdad es que la solución sobresaturada ya nos había contado lo mismo unos párrafos antes, y sin notas al pie. A veces una imagen sabe más que una teoría, y además llega primero.

Y lo lindo, o lo inquietante, es que el truco se repite hacia abajo, en cada escalón. Porque las fechas, en estas historias, nunca son adorno: son frascos. Cuando uno escribe 1993 al lado de __Slackware__ y 2002 al lado de __Arch Linux__ no está poniendo datos, está marcando recipientes. Cada distribución fue su propia solución sobresaturada esperando su propia mota. ¿Hubiera existido Slackware sin Patrick Volkerding? ¿Arch sin Judd Vinet? La pregunta vuelve idéntica en cada nivel, y en cada nivel produce el mismo escalofrío: ¿esto tenía que pasar, o dependió de que una persona, una tarde cualquiera, dejara caer su cristalito en lugar de irse a dormir?

## __5. La pregunta de fondo: ¿Personas o condiciones?__

En algún momento uno se da cuenta de que ya no está hablando de Linux. De que la pregunta de abajo, la que sostiene a todas las demás, no tiene nada de técnica. Es esta:

¿Cuánto de la historia les pertenece a las personas y cuánto a las condiciones? ¿Qué parte del mundo que habitamos la eligió alguien, y qué parte simplemente ocurrió, porque las cosas estaban demasiado sobresaturadas como para no ocurrir?

Es la disputa más vieja que tiene la historia —__el gran hombre contra la marea anónima__— y tiene la gracia de no resolverse jamás, porque las dos partes tienen razón al mismo tiempo y se niegan a darse la mano. La mota importa. El frasco importa más. Y sin embargo, sin la mota, el frasco se queda líquido para siempre.

Por eso, sospecho, inventamos los orígenes. No los encontramos: los inventamos después, cuando ya todo cristalizó y necesitamos un lugar donde apoyar el agradecimiento. Señalamos la mota y decimos _“acá empezó”_, porque es más fácil agradecerle a una mota que a una solución entera. El frasco no tiene nombre. La sustancia sobresaturada no recibe cartas.

Entonces elegimos un punto, le ponemos una fecha y una cara, y lo llamamos origen. Torvalds, probablemente, era reemplazable. Pero el agradecimiento necesita un destinatario, y los destinatarios no se reemplazan: se eligen. __El origen no es el lugar donde las cosas empezaron. Es el lugar donde decidimos, mucho después, ponernos a agradecer.__
