---
title: 'La entropía como problema abierto: estado del arte de un concepto transversal'
slug: la-entropia-como-problema-abierto-estado-del-arte-de-un-concepto-transversal
status: published
legacy_url: https://dagorret.com.ar/la-entropia-como-problema-abierto-estado-del-arte-de-un-concepto-transversal/
wordpress_id: 1374
published_at: '2026-07-14T01:36:02'
modified_at: '2026-07-15T00:00:27'
wordpress_category_ids:
- 21
wordpress_tag_ids:
- 372
- 368
- 370
- 371
- 369
categories:
- &id001
  id: 21
  name: Sistemas
  slug: sistemas
tags:
- id: 372
  name: Divulgación científica
  slug: divulgacion-cientifica
- id: 368
  name: Entropía
  slug: entropia
- id: 370
  name: Epistemología
  slug: epistemologia-2
- id: 371
  name: Filosofía de la ciencia
  slug: filosofia-de-la-ciencia
- id: 369
  name: Termodinámica
  slug: termodinamica
category: *id001
---

### _Primer artículo de la serie Entropía: física, información, sociedad_

Hay pocos conceptos en la historia de la ciencia que hayan atravesado con la misma legitimidad la termodinámica, la mecánica estadística, la teoría de la información, la filosofía del tiempo, la cosmología y la sociología de sistemas. La entropía es uno de ellos, y probablemente el más maltratado por el uso coloquial: reducirla a sinónimo de “desorden” es cómodo, pero oculta que se trata, ante todo, de una magnitud —o de una familia de magnitudes emparentadas— que cuantifica algo mucho más preciso: cuántas configuraciones microscópicas son compatibles con lo que observamos, o cuánta incertidumbre subsiste después de conocer todo lo que podemos conocer sobre un sistema.

Esta primera entrega de la serie no busca todavía problematizar el concepto —eso vendrá en los artículos siguientes, donde entraré con las críticas que tengo preparadas—, sino fijar con rigor dónde está parado hoy el estado del arte, disciplina por disciplina, desde sus fundamentos decimonónicos hasta los debates que siguen abiertos en 2026.

## I. El núcleo termodinámico: de Clausius a la flecha del tiempo

Rudolf Clausius acuñó el término en 1865 a partir del griego _entropía_, transformación, buscando deliberadamente un eco fonético con _energía_. Lo hizo para resolver un problema muy concreto de ingeniería térmica: cuantificar por qué ninguna máquina real alcanza el rendimiento ideal de Carnot. Su definición,

$$dS = \frac{\delta Q\_{\mathrm{rev}}}{T}$$

es una definición operacional, ligada al calor intercambiado de manera reversible a una temperatura dada. Lo que la vuelve filosóficamente incómoda no es la fórmula sino su corolario, el Segundo Principio: en todo proceso espontáneo de un sistema aislado, la entropía del universo no puede disminuir.

Esa desigualdad —ΔS ≥ 0— es la primera ley física de la historia que rompe la simetría temporal de las ecuaciones de Newton. Un video de billar corrido hacia atrás sigue obedeciendo la mecánica clásica; un video de un vaso que se rearma solo, no.

La termodinámica clásica no explica _por qué_ existe esa asimetría, solo la registra con una precisión que ningún experimento ha refutado jamás. Ese vacío explicativo es el que hereda, sin resolverlo del todo, la física estadística.

## II. El puente estadístico: Boltzmann, Gibbs y el nacimiento de la entropía como probabilidad

La contribución de Ludwig Boltzmann,

$$ S = k\_B \ln \Omega$$

no es una reformulación cosmética sino un cambio ontológico: la entropía deja de ser una propiedad del calor y pasa a ser una propiedad del conteo. Ω es el número de microestados compatibles con un macroestado dado, y la ecuación dice, en esencia, que los sistemas evolucionan hacia los macroestados que tienen más maneras de realizarse microscópicamente, no porque exista una fuerza que los empuje hacia el desorden, sino porque esos macroestados son, sencillamente, más numerosos.

La formulación de Gibbs,

$$ S = -k\_B \sum\_i p\_i \ln p\_i$$

generaliza esto a distribuciones de probabilidad no uniformes y es la que sobrevive intacta, salvo por la constante, en la ecuación de Shannon setenta años después.

Vale la pena subrayar algo que se pierde con frecuencia en las divulgaciones: la conexión entre la irreversibilidad macroscópica (Clausius) y la reversibilidad microscópica (las leyes de Newton o de Schrödinger, que sí son deterministas y reversibles) sigue siendo, en sentido estricto, un problema de fundamentos no cerrado.

Existen al menos dos escuelas: la de quienes, siguiendo a Boltzmann, apelan a condiciones iniciales de baja entropía y a argumentos de tipo _coarse-graining_, y la de quienes, siguiendo la línea de Prigogine, sostienen que hay una irreversibilidad genuinamente fundamental en sistemas dinámicos inestables. El consenso operativo de la física contemporánea no es que el problema esté resuelto, sino que es tratable con las herramientas del _coarse-graining_ y de la teoría ergódica, lo cual es distinto de decir que está filosóficamente saldado.

## III. La bisagra hacia la información: Shannon y el principio de Landauer

Claude Shannon tomó la forma funcional de Gibbs para medir, no calor, sino incertidumbre en un canal de comunicación. La homología matemática entre ambas entropías generó desde el primer momento una pregunta que hoy sigue viva: ¿es una analogía formal, o hay una identidad física de fondo entre información y termodinámica?

Rolf Landauer dio en 1961 la respuesta más contundente a favor de la identidad física: borrar un bit de información en un sistema físico —no copiarlo, no moverlo, sino borrarlo de forma lógicamente irreversible— disipa necesariamente un mínimo de calor

$$Q = k\_B T \ln 2$$

Esto no es una curiosidad teórica. Desde 2012 existe verificación experimental directa: Bérut y colaboradores confirmaron el límite de Landauer usando una partícula coloidal atrapada en un potencial de doble pozo modulado ópticamente, mostrando que el calor disipado satura exactamente en la cota predicha en el límite de borrados lentos.

Ese resultado fue replicado y extendido en las dos décadas siguientes a memorias nanomagnéticas de un solo bit, a átomos individuales en el régimen cuántico, e incluso —trabajos muy recientes, de 2025— al régimen cuántico de muchos cuerpos, donde se explora si la cota de Landauer se modifica por efectos de tamaño finito y de correlación con el baño térmico.

El resultado agregado de ese programa experimental es que la equivalencia información-termodinámica no es una metáfora: es una restricción física verificable sobre cualquier proceso de cómputo, biológico o artificial, y por lo tanto una restricción física sobre los límites últimos de cualquier arquitectura computacional, incluidas las que hoy entrenan modelos de lenguaje.

## IV. El problema filosófico: ¿la flecha del tiempo es óntica o epistémica?

Aquí la física estadística entrega el problema a la filosofía sin resolverlo. Arthur Eddington bautizó la “flecha del tiempo” en 1927 para nombrar exactamente esta asimetría que las ecuaciones fundamentales no explican por sí solas. La discusión contemporánea se organiza, todavía hoy, alrededor de dos posiciones que no han logrado zanjarse mutuamente.

La posición subjetivista o epistémica —cuya versión más depurada viene de Edwin Jaynes y su lectura de la entropía como estado de conocimiento del observador, no como propiedad intrínseca del sistema— sostiene que el aumento de entropía refleja nuestra incapacidad de rastrear todos los microestados, no una tendencia real de la naturaleza.

La posición realista u ontológica, asociada a Ilya Prigogine y a su escuela de Bruselas, sostiene en cambio que ciertos sistemas dinámicos —los llamados sistemas caóticos con inestabilidad exponencial de trayectorias— son irreversibles en un sentido fuerte, no reductible a ignorancia del observador.

Prigogine ganó el Nobel de Química en 1977 no por resolver esta disputa sino por otra contribución, quizás más fértil: mostrar que sistemas abiertos lejos del equilibrio no solo disipan entropía, sino que pueden generar espontáneamente estructuras ordenadas —las estructuras disipativas— a costa de exportar entropía al entorno. Esa idea es la que permite, sin violar el Segundo Principio, entender por qué la vida —un fenómeno de orden creciente y sostenido— es termodinámicamente posible. La vida no es una excepción a la entropía; es una tecnología para administrarla.

## V. Información como sustrato: Wheeler, Landauer y la ontología “it from bit”

Un tercer frente filosófico, más radical, se pregunta si la información no será más fundamental que la materia y la energía. John Archibald Wheeler formuló esto como “it from bit”: la sugerencia de que cada partícula, cada campo, incluso el propio espaciotiempo, deriva su existencia de respuestas binarias a preguntas planteadas por dispositivos —una participación observacional que hace del universo, en última instancia, un fenómeno de información procesada.

Esta no es una posición mayoritaria ni consensuada, pero ha ganado tracción justamente por lo que se detalla en la sección siguiente: la física de agujeros negros parece exigir, con una obstinación matemática difícil de despachar, que la información sea tratada como una cantidad físicamente conservada, no como un mero recurso epistémico.

## VI. La frontera dura: entropía, agujeros negros y el problema de la información

Este es, junto con el de la gravedad entrópica, el terreno donde la entropía deja de ser un concepto asentado y se convierte en un problema de investigación activo, sin resolución consensuada. Jacob Bekenstein y Stephen Hawking establecieron en los años setenta que un agujero negro tiene una entropía proporcional al área de su horizonte de eventos —no a su volumen, lo cual ya es una anomalía profunda respecto de la intuición termodinámica ordinaria— y que emite radiación térmica al evaporarse.

El problema, formulado por el propio Hawking en 1976, es que esa radiación parece ser exactamente térmica, es decir, no codifica ninguna información sobre lo que cayó en el agujero negro. Si eso fuera literalmente cierto, la evolución cuántica dejaría de ser unitaria —la información se destruiría—, lo cual contradice un pilar de la mecánica cuántica.

Medio siglo después, en 2025 y 2026, este sigue siendo formalmente un problema abierto, aunque con un desplazamiento importante del consenso: los cálculos de la llamada curva de Page, obtenidos hacia 2019 mediante la técnica de “wormholes de réplica” (Penington, Almheiri y otros), muestran que, bajo el marco de la gravedad cuántica holográfica, la información _debe_ poder recuperarse en la radiación de Hawking, lo cual favorece la unitariedad frente a la pérdida de información.

Ese resultado es hoy el marco dominante, pero no equivale a una resolución completa: sigue sin conocerse el mecanismo explícito por el cual la información queda codificada en la radiación, y coexisten programas de investigación rivales —las construcciones de microestados como “fuzzballs” en teoría de cuerdas, las propuestas de agujeros de gusano en la geometría interior, e incluso posiciones minoritarias que reabren la posibilidad de remanentes de larga vida o universos bebé como depósito de la información perdida.

La comunidad de física teórica organizó en 2025 encuentros dedicados enteramente a conmemorar y balancear estos cincuenta años de disputa, precisamente porque el desacuerdo de fondo entre las distintas escuelas —cuantización canónica de la relatividad general, teoría de cuerdas, enfoques de gravedad semiclásica— sigue vivo.

## VII. La frontera más especulativa: ¿es la gravedad misma una fuerza entrópica?

En 2010 y 2011, Erik Verlinde propuso algo más ambicioso que vincular entropía y agujeros negros: sugirió que la gravedad no es una fuerza fundamental en absoluto, sino un fenómeno emergente, una fuerza entrópica análoga a la elasticidad de un polímero, derivada de gradientes de información codificados en “pantallas holográficas”. La propuesta logró, con supuestos mínimos, rederivar tanto la ley de Newton como las ecuaciones de campo de Einstein, lo cual explica el interés que despertó.

Pero también generó, desde el inicio, un rechazo sostenido por parte de referentes del propio campo de la termodinámica gravitacional: Ted Jacobson —cuyo trabajo de 1995 sobre horizontes de Rindler es la base técnica que Verlinde extiende— declaró no poder “darle sentido” a la extensión; Thanu Padmanabhan, otro pionero del vínculo gravedad-termodinámica, cuestionó el rigor matemático de la noción de pantalla holográfica y dudó abiertamente de que la idea resistiera el paso del tiempo.

Otros trabajos —experimentos con neutrones ultrafríos, por ejemplo— intentaron falsear la propuesta argumentando que una fuerza genuinamente entrópica debería ser más “ruidosa”, más decoherente, de lo que se observa empíricamente, aunque trabajos posteriores han matizado esa objeción modelando la gravedad entrópica como sistema cuántico abierto.

El estado del arte, entonces, no es ni la aceptación ni el descarte: es una hipótesis viva, matemáticamente fértil, empíricamente indecidible en la mayoría de los regímenes accesibles porque sus predicciones coinciden con las de la relatividad general estándar, y sostenida por una minoría cualificada frente a un escepticismo mayoritario de peso comparable.

## VIII. La dimensión sociológica: de la metáfora a la teoría de sistemas formal

El tránsito de la entropía hacia las ciencias sociales tiene dos linajes que conviene no confundir. El primero, más riguroso, es el de Nicholas Georgescu-Roegen, quien en los años setenta introdujo la ley de la entropía en la teoría económica no como metáfora sino como restricción material: el proceso económico no es un flujo circular cerrado, como lo modela la economía neoclásica de manual, sino un proceso unidireccional que transforma recursos de baja entropía —minerales concentrados, combustibles fósiles, suelo fértil— en desechos de alta entropía dispersos e irrecuperables.

De ahí se sigue una tesis incómoda y todavía debatida en economía ecológica: el crecimiento material indefinido es físicamente imposible, no por escasez contingente de un recurso particular, sino por la irreversibilidad termodinámica del propio proceso productivo.

El segundo linaje, el de Niklas Luhmann, usa la entropía en un sentido más técnico-sistémico que metafórico: en su teoría de sistemas sociales autopoyéticos, el entorno de cualquier sistema —la política, el derecho, la economía— es siempre infinitamente más complejo que el sistema mismo, y la entropía se manifiesta como el ruido comunicativo, el malentendido estructural, la imposibilidad de que el sistema procese toda la complejidad de su entorno. Los códigos binarios que cada subsistema social desarrolla —lícito/ilícito en el derecho, tener/no tener en la economía— no eliminan esa complejidad sino que la reducen a una forma procesable, en un mecanismo que Luhmann describe explícitamente en términos de neguentropía.

Joseph Tainter, finalmente, aporta una tercera pieza empírica antes que teórica: en su estudio del colapso de sociedades complejas, muestra que la respuesta institucional a los problemas —una respuesta que consiste, sistemáticamente, en agregar más burocracia, más especialización, más infraestructura— tiene un costo energético marginal creciente, hasta un punto de rendimientos decrecientes en el que la complejidad deja de ser adaptativa y el colapso se vuelve, en cierto sentido preciso, la ruta termodinámicamente más eficiente de disipación del sistema.

## IX. Lo que queda fijado y lo que queda abierto

Conviene cerrar esta primera entrega distinguiendo con precisión ambas categorías, porque de esa distinción depende el resto de la serie. Están sólidamente establecidos, sin controversia científica activa: la formulación termodinámica clásica, la formulación estadística de Boltzmann-Gibbs, la homología formal con la entropía de Shannon, y el principio de Landauer —hoy verificado experimentalmente en múltiples plataformas físicas, desde partículas coloidales hasta sistemas cuánticos de muchos cuerpos—.

Están filosóficamente abiertos, con posiciones académicas legítimas y rivales: el estatuto óntico o epistémico de la flecha del tiempo, y el estatuto ontológico de la información misma. Están en investigación activa, sin resolución consensuada, en la frontera de la física teórica: el mecanismo exacto de recuperación de información en la evaporación de agujeros negros, y la hipótesis —minoritaria pero no descartada— de que la gravedad sea, ella misma, un fenómeno entrópico emergente.

Y está, finalmente, la transferencia a las ciencias sociales, que en sus versiones más serias —Georgescu-Roegen, Luhmann, Tainter— no es una metáfora ornamental sino un intento de formalizar, con distintos grados de rigor matemático, cómo los límites termodinámicos y comunicacionales condicionan la viabilidad de los sistemas económicos, jurídicos e institucionales.

Ese es el mapa. Los artículos siguientes de la serie van a moverse en dos direcciones: profundizar cada frontera con el aparato matemático correspondiente, y —según lo que ya tenés preparado— someter a crítica algunas de las extrapolaciones más audaces, particularmente las que saltan de la homología matemática Boltzmann-Shannon a conclusiones ontológicas fuertes sin justificar el paso.

_Notas y fuentes consultadas para la sección de frontera: coloquio de Netta Engelhardt sobre la paradoja de la información (UBC, enero 2025); encuentro “50 years of the black hole information paradox” (Simons Center for Geometry and Physics, octubre-noviembre 2025); número especial de la revista Entropy sobre el problema de la información en agujeros negros (Calmet, Casadio y Hsu, 2025); trabajos de revisión y controversia sobre gravedad entrópica de Verlinde (Jacobson 1995; Padmanabhan; Abreu y Ananias Neto 2013; Schimmoller et al. 2021); verificación experimental del principio de Landauer (Bérut et al., Nature, 2012; extensiones a memoria nanomagnética, átomos individuales y regímenes cuánticos de muchos cuerpos hasta 2025)._
