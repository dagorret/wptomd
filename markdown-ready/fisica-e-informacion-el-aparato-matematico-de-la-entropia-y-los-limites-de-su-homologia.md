---
title: 'Física e información: el aparato matemático de la entropía y los límites de
  su homología'
slug: fisica-e-informacion-el-aparato-matematico-de-la-entropia-y-los-limites-de-su-homologia
status: published
legacy_url: https://dagorret.com.ar/fisica-e-informacion-el-aparato-matematico-de-la-entropia-y-los-limites-de-su-homologia/
wordpress_id: 1378
published_at: '2026-08-01T19:25:11'
modified_at: '2026-07-14T23:54:40'
wordpress_category_ids:
- 21
wordpress_tag_ids:
- 375
- 368
- 374
- 377
- 373
- 376
categories:
- &id001
  id: 21
  name: Sistemas
  slug: sistemas
tags:
- id: 375
  name: Claude Shannon
  slug: claude-shannon
- id: 368
  name: Entropía
  slug: entropia
- id: 374
  name: John Archibald Wheeler
  slug: john-archibald-wheeler
- id: 377
  name: Mecánica cuántica
  slug: mecanica-cuantica
- id: 373
  name: Rolf Landauer
  slug: rolf-landauer
- id: 376
  name: Teoría de la información
  slug: teoria-de-la-informacion
category: *id001
---

### _Segundo artículo de la serie Entropía: física, información, sociedad_

El primer artículo de esta serie trazó el mapa general: qué está sólidamente establecido, qué es filosóficamente abierto y qué es investigación de frontera sin resolución. Esta segunda entrega baja a un solo tramo de ese mapa —el que va de Boltzmann a Shannon y de ahí a Landauer— pero lo hace con el aparato matemático completo, porque es precisamente en el detalle técnico donde se juega la pregunta que quiero empezar a responder acá: ¿en qué sentido preciso son “la misma cosa” la entropía física y la entropía de la información, y en qué punto exacto ese parentesco deja de sostener las conclusiones ontológicas que se le suelen colgar?

Adelanto la tesis que voy a defender: hay al menos tres afirmaciones distintas que la literatura tiende a tratar como si fueran una sola —la homología matemática, la identidad física acotada y la primacía ontológica de la información— y cada una exige una justificación que no hereda automáticamente de la anterior.

## I. Boltzmann: contar microestados

Partamos del ensemble microcanónico, el más simple. Un sistema aislado con energía fija E puede realizarse mediante Ω(E) microestados distintos, todos igualmente probables por el postulado de igual probabilidad a priori. Boltzmann define

$$ S = k\_B \ln \Omega$$

y esta fórmula, grabada en su tumba en Viena, tiene una propiedad que conviene hacer explícita porque es la que después migra a la información: es una función estrictamente creciente y cóncava del número de configuraciones microscópicas compatibles con lo que sabemos macroscópicamente.

Si dos subsistemas independientes tienen Ω₁ y Ω₂ microestados, el sistema compuesto tiene Ω₁Ω₂, y como el logaritmo convierte productos en sumas, la entropía es aditiva: $S = S\_1 + S\_2$. Esta aditividad no es un detalle técnico menor, es la propiedad que Shannon va a exigirle axiomáticamente a su propia medida setenta años más tarde, y es también la propiedad que, como voy a mostrar en la sección V, se rompe con más facilidad de la que se suele admitir cuando se sale del equilibrio.

La conexión con la termodinámica clásica de Clausius se obtiene derivando: para un sistema en contacto térmico, puede mostrarse que $1/T = \partial S/\partial E$, lo cual recupera la temperatura como parámetro conjugado de la energía en el sentido termodinámico exacto, y a partir de ahí se reconstruye

$$dS = \frac{\delta Q\_{\mathrm{rev}}}{T}$$

La estadística no reemplaza a la termodinámica: la deriva, mostrando que las leyes macroscópicas de Clausius son el límite de números muy grandes (N ~ 10²³) aplicado a un conteo combinatorio subyacente.

## II. Gibbs: de la equiprobabilidad a la distribución general

Boltzmann asume que todos los microestados accesibles son igualmente probables, lo cual es razonable en un sistema aislado en equilibrio pero deja de serlo apenas el sistema intercambia energía con un reservorio térmico. J. Willard Gibbs generaliza el resultado para el ensemble canónico, donde la probabilidad de cada microestado i con energía $E\_i$ sigue la distribución de Boltzmann-Gibbs

$$p\_i = \frac{e^{-E\_i/k\_BT}}{Z}, \quad Z = \sum\_i e^{-E\_i/k\_BT}$$

siendo Z la función de partición. La entropía se escribe entonces como

$$ S = -k\_B \sum\_i p\_i \ln p\_i$$

que es la forma que sobrevive, casi letra por letra, en la ecuación de Shannon. Nótese que esta expresión no exige ya equiprobabilidad: es una medida de la dispersión de la propia distribución de probabilidad, y se reduce a la fórmula de Boltzmann exactamente cuando todos los $p\_i$ son iguales a $1/\Omega$.

Este es el primer punto que quiero fijar con precisión, porque va a ser central en la sección V: la fórmula de Gibbs es matemáticamente general, pero su identificación con “la” entropía termodinámica del sistema depende de que la distribución $p\_i$ sea, específicamente, la distribución de Boltzmann-Gibbs de equilibrio con un reservorio a temperatura T. No cualquier distribución de probabilidad sobre microestados produce, al insertarla en esa fórmula, un número que coincida con lo que un calorímetro mediría.

## III. Shannon: la misma forma, derivada desde axiomas completamente distintos

Claude Shannon, en 1948, no estaba pensando en calor ni en microestados sino en canales de comunicación: quería una función $H(p\_1, \ldots, p\_n)$ que midiera la incertidumbre promedio asociada a una fuente que emite el símbolo i con probabilidad $p\_i$.

Exigió tres propiedades —continuidad en las $p\_i$, monotonía (para distribuciones uniformes sobre n símbolos equiprobables, H debe crecer con n), y aditividad para decisiones compuestas (si una elección se descompone en dos elecciones sucesivas, la incertidumbre total debe ser la suma ponderada de las incertidumbres parciales)— y demostró, en un apéndice de su artículo fundacional, que la única función que satisface esas tres condiciones, salvo una constante multiplicativa, es

$$H = -K \sum\_i p\_i \log p\_i$$

Es crucial notar el orden de los hechos, porque suele invertirse en las versiones divulgativas: Shannon no tomó prestada la fórmula de la termodinámica y la reinterpretó; la dedujo de manera independiente a partir de axiomas puramente combinatorios sobre información, y solo después adoptó el nombre “entropía”.

Fue en una conversación ya célebre con John von Neumann: este le habría dicho, según la anécdota que el propio Shannon relató después, que la función ya tenía ese nombre en mecánica estadística y que además nadie sabía realmente qué era la entropía, de modo que en cualquier discusión Shannon tendría ventaja. Es una anécdota simpática, pero también el origen documentado de una confusión terminológica que la literatura técnica sigue señalando ochenta años después como fuente activa de malentendidos entre disciplinas.

## IV. La homología exacta: qué es literalmente lo mismo

Hecho esto explícito, la homología formal entre las tres expresiones es innegable y vale la pena escribirla sin eufemismos. Si se toma logaritmo en base 2 en vez de logaritmo natural, y se fija K = 1, la entropía de Shannon en bits y la entropía de Gibbs en unidades de $k\_B$ son la misma función matemática aplicada al mismo objeto formal: una distribución de probabilidad sobre un conjunto de estados.

La entropía residual de un sistema con degeneración configuracional en el cero absoluto —la que aparece en tablas termoquímicas para explicar por qué ciertos sólidos no alcanzan entropía nula pese al tercer principio— es, en particular, calculable exactamente con la fórmula de Shannon aplicada a la distribución de configuraciones congeladas, y coincide numéricamente, salvo por la constante de conversión de unidades, con mediciones calorimétricas reales.

Trabajos recientes de física computacional han llevado esta equivalencia a un terreno todavía más concreto: demuestran que la entropía termodinámica de sistemas de materia condensada real —metales, semiconductores, óxidos, tanto en fase sólida como líquida— puede recuperarse con precisión de benchmark a partir de la compresibilidad algorítmica de trayectorias de dinámica molecular, es decir, contando literalmente cuántos bits hacen falta para describir el microestado con una precisión dada. En ese sentido restringido, la afirmación de que “la entropía termodinámica es información” no es una metáfora ni una exageración divulgativa: es un resultado técnico verificable.

## V. Donde la homología se rompe: la falacia de la identificación general

Pero —y este es el punto que quiero establecer con el mismo rigor que el anterior, no como intuición sino como resultado demostrado— esa equivalencia no es general. Tiene, como mínimo, dos limitaciones técnicas precisas que la literatura de física estadística documenta y que la divulgación casi nunca menciona.

La primera es dinámica: la entropía de Shannon de la densidad de probabilidad ρ(x,t) de un sistema clásico es invariante bajo evolución hamiltoniana —es una consecuencia directa del teorema de Liouville, que preserva el volumen en el espacio de fases— y por lo tanto no reproduce, por sí sola, el crecimiento monótono que exige el Segundo Principio.

Si uno calculara ingenuamente “la entropía de Shannon del universo” tomando la densidad de probabilidad exacta de todas sus partículas evolucionando bajo las leyes fundamentales, esa cantidad sería constante en el tiempo, no creciente: el aumento de entropía termodinámica que observamos depende de un paso adicional —el coarse-graining, la renuncia deliberada a rastrear correlaciones microscópicas finas— que no está contenido en la fórmula de Shannon como tal, sino en una decisión metodológica sobre qué grado de descripción nos interesa.

La segunda limitación es todavía más contundente y viene de un resultado publicado en 2019 por Gao, Gallicchio y Roitberg: demostraron formalmente que la distribución de Boltzmann-Gibbs generalizada es la única distribución de probabilidad para la cual la entropía de Gibbs-Shannon coincide exactamente con la entropía termodinámica del sistema. Dicho de otro modo, la igualdad entre ambas entropías no es una propiedad genérica de “cualquier sistema con incertidumbre”, sino una coincidencia numérica que ocurre exactamente en el caso particular del equilibrio con un reservorio térmico, y se rompe fuera de él.

La revisión técnica más extensa sobre el tema —un trabajo de 2017 dedicado enteramente a desenredar la “maraña” terminológica de la entropía— llega a una conclusión todavía más quirúrgica: ni siquiera dentro de la propia termodinámica hay una sola magnitud llamada “entropía”; hay al menos una entropía residual configuracional que sí coincide formalmente con Shannon, y una entropía térmica que en general no lo hace de manera directa.

Un artículo reciente que provocativamente se titula, aludiendo al affaire Sokal, “Thermodynamics ≠ Information Theory”, documenta cómo esta imprecisión terminológica —heredada de la broma de von Neumann— se propaga sin control hacia la biología y la economía, donde se invoca “la entropía” para legitimar argumentos que en realidad dependen de cuál de las dos magnitudes, técnicamente distintas, se está usando.

## VI. Landauer: donde la identidad física sí está probada, pero acotada

Frente a esta homología matemática parcial, el principio de Landauer ofrece algo categóricamente más fuerte: no una analogía formal sino una identidad física demostrada, aunque acotada a un protocolo específico.

El argumento canónico se construye con el motor de Szilárd, una idealización del demonio de Maxwell: una única molécula en una caja, un pistón que puede insertarse para dividir la caja en dos mitades, y una medición que determina en qué mitad está la molécula. Esa medición produce un bit de información mutua $I(X;M)$ entre el microestado X del sistema y el resultado M de la medición; en el caso ideal de medición sin error y dos resultados equiprobables, $I(X;M) = \ln 2$.

Ese bit de información permite, en principio, extraer trabajo del baño térmico —moviendo el pistón en la dirección correcta según el resultado de la medición— por una cantidad exactamente igual a $k\_B T \ln 2$, lo cual parecería violar el Segundo Principio si el ciclo se repitiera indefinidamente.

La resolución, que es el contenido preciso del principio de Landauer, es que el ciclo no puede cerrarse sin borrar la memoria del demonio —sin resetear el registro que guardó el resultado de la medición— y ese borrado, por ser una operación lógicamente irreversible (dos estados posibles de memoria colapsan a uno solo), disipa necesariamente un calor $Q \geq k\_B T \ln 2$ al entorno. El balance neto respeta el Segundo Principio exactamente.

La versión moderna y más general de este resultado —la desigualdad de Sagawa-Ueda— formaliza esto como una segunda ley generalizada para sistemas con retroalimentación de medición, donde el trabajo extraíble está acotado no solo por la diferencia de energía libre sino por esa diferencia más la información mutua obtenida.

Lo que distingue a este resultado de la homología de la sección V es que aquí no hay ambigüedad de coincidencia numérica en un caso particular: hay una predicción cuantitativa, universal para cualquier sistema físico que implemente lógicamente el borrado de un bit, y esa predicción fue verificada experimentalmente de manera directa en 2012 por Bérut y colaboradores, usando una partícula coloidal individual atrapada ópticamente en un potencial de doble pozo, donde el calor disipado satura exactamente en el límite de Landauer para protocolos de borrado lentos.

La verificación se extendió después a memoria nanomagnética de un solo bit, a átomos individuales en régimen genuinamente cuántico, y —trabajos de 2025— al régimen cuántico de muchos cuerpos, donde se investigan correcciones de tamaño finito y efectos de correlación con baños no markovianos. Este es, en el estado del arte actual, el resultado más sólido de toda la cadena Boltzmann-Shannon-Landauer: no una homología de forma sino una ley física verificada, y por eso mismo el que hay que aislar cuidadosamente de las extrapolaciones que siguen.

## VII. El salto que no está justificado: de Landauer a “it from bit”

Con estos tres resultados ya distinguidos con precisión —homología matemática general pero parcial (secciones IV-V), identidad física demostrada pero acotada a un protocolo de borrado lógico (sección VI)— estamos en condiciones de examinar la extrapolación que anuncié al principio: el salto de John Archibald Wheeler hacia “it from bit”, la tesis de que toda entidad física, todo it, deriva en última instancia su existencia de respuestas binarias a preguntas planteadas por un aparato de medición.

La literatura filosófica y física especializada en este punto —que no es unánime en su rechazo, pero sí es mayoritariamente crítica— separa con cuidado dos lecturas de esa tesis que Wheeler mismo tendía a mezclar. Hay una lectura epistemológica, que es prácticamente incontrovertida: todo lo que sabemos sobre cualquier sistema físico nos llega codificado en resultados de medición discretos, en bits. Y hay una lectura metafísica, mucho más fuerte y mucho más discutida: que las entidades físicas mismas son, en algún sentido literal, estructuras informacionales, y que sin actos de medición no habría, en rigor, hechos determinados sobre el mundo.

La objeción estándar a esta segunda lectura —formulada, entre otros, por George Ellis en un trabajo que invierte deliberadamente el aforismo de Wheeler en “bit from it”— es que confunde tres tipos de información que conviene no fusionar: la información de Shannon, que cuantifica incertidumbre pero es agnóstica a qué significan los símbolos; la información semántica, que sí carga contenido significativo pero presupone ya un sistema físico —un sustrato— capaz de portar ese significado; y la información física en el sentido de Landauer, que como vimos es real pero está definida sobre procesos termodinámicos concretos, no sobre “toda la realidad” sin más.

El argumento de Ellis, y el de trabajos posteriores que retoman la discusión, es que ninguna de las tres, ni siquiera las dos últimas —que sí tienen anclaje físico genuino—, permite invertir la relación de dependencia que Wheeler propone: se necesita ya un it, un sistema físico con grados de libertad determinados, para que la pregunta “¿en qué microestado está?” tenga siquiera sentido, y por lo tanto el bit deriva del it con la misma legitimidad, o más, que a la inversa.

Un trabajo reciente que sistematiza esta discusión distingue explícitamente, en los mismos términos que vengo usando en este artículo, una lectura “epistemológica no controvertida” de una lectura “metafísica mucho más discutida”, y concluye que la segunda enfrenta las objeciones estándar contra el idealismo: resulta difícil especificar qué elecciones binarias existían antes de que hubiera observadores, y hacer que la física dependa de mentes es una consecuencia que la enorme mayoría de los físicos en ejercicio no está dispuesta a aceptar.

## VIII. Diagnóstico de la falacia: tres afirmaciones, tres niveles de garantía epistémica

Lo que este recorrido matemático permite hacer, y que es el aporte específico de este segundo artículo respecto del primero, es nombrar con precisión dónde está el error de razonamiento cuando alguien pasa de “la entropía de Boltzmann y la de Shannon tienen la misma fórmula” a “por lo tanto el universo es, en el fondo, información”.

El error no es afirmar la homología —que es real, aunque acotada— ni afirmar la identidad física de Landauer —que es real, verificada, y más fuerte que la homología—. El error es tratar esas dos afirmaciones, de garantía epistémica muy distinta, como si fueran peldaños de una misma escalera que conduce naturalmente a una tercera afirmación, la ontológica, que en realidad requiere premisas adicionales —sobre la naturaleza de la medición, sobre el estatuto del observador, sobre qué cuenta como “existir”— que ni la mecánica estadística ni la termodinámica de la información proveen por sí solas.

Cada peldaño presta su autoridad técnica al siguiente sin que el siguiente haya pagado el precio argumental que le correspondía. Es, en el sentido más preciso del término, una falacia de equivocación: la palabra “información” cambia de referente —de incertidumbre estadística, a calor disipado en un borrado lógico, a sustrato último de la realidad— sin que el cambio se declare, y la solidez empírica de Landauer se transfiere, indebidamente, a una tesis que Landauer nunca formuló ni sus experimentos podrían formular.

Esto no es, quiero subrayarlo antes de cerrar, un argumento contra la posibilidad de que la información resulte ser, en algún sentido todavía por precisar, más fundamental que la materia. Es un argumento sobre el estándar de prueba: mostrar una homología matemática y una ley física verificada no alcanza, por sí solo, para sostener una tesis ontológica de ese calibre, y quien quiera defenderla tiene una tarea filosófica pendiente —independiente del aparato de Boltzmann-Gibbs-Shannon-Landauer— que consiste en dar cuenta de qué sería un bit sin un sistema físico que lo instancie.

Mientras esa tarea no esté hecha, lo más honesto es sostener las tres afirmaciones por separado, con el grado de confianza que cada una efectivamente tiene, en lugar de dejarlas fundirse en una sola narrativa que suena más impactante de lo que sus premisas permiten.

_Notas y fuentes consultadas: derivación axiomática de Shannon (1948) y su forma canónica; Gao, Gallicchio y Roitberg, “The Generalized Boltzmann Distribution is the Only Distribution in Which the Gibbs-Shannon Entropy Equals the Thermodynamic Entropy” (2019); revisión “Researchers in an Entropy Wonderland” sobre la pluralidad de nociones de entropía; “Thermodynamics ≠ Information Theory: Science’s Greatest Sokal Affair” sobre la conflación terminológica desde la anécdota de von Neumann; Bérut et al., verificación experimental del principio de Landauer (Nature, 2012) y extensiones a régimen cuántico de muchos cuerpos (2025); Sagawa y Ueda sobre la segunda ley generalizada con retroalimentación de medición; Ellis, “Bit from It”, como inversión crítica del aforismo de Wheeler; trabajos recientes que distinguen la lectura epistemológica de la lectura metafísica de “it from bit” y sus objeciones estándar._
