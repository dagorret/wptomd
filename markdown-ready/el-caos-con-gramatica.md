---
title: El caos con gramática
slug: el-caos-con-gramatica
status: published
legacy_url: https://dagorret.com.ar/el-caos-con-gramatica/
wordpress_id: 1413
published_at: '2026-07-25T16:18:47'
modified_at: '2026-07-26T23:20:19'
wordpress_category_ids:
- 418
wordpress_tag_ids:
- 444
- 442
- 440
- 439
- 434
- 441
- 435
- 437
- 436
- 390
- 443
- 438
- 445
- 433
categories:
- &id001
  id: 418
  name: Matemáticas
  slug: matematicas
tags:
- id: 444
  name: análisis armónico
  slug: analisis-armonico
- id: 442
  name: André–Oort
  slug: andre-oort
- id: 440
  name: conjetura de Kakeya
  slug: conjetura-de-kakeya
- id: 439
  name: ecuación de Boltzmann
  slug: ecuacion-de-boltzmann
- id: 434
  name: geometría algebraica
  slug: geometria-algebraica
- id: 441
  name: geometría simpléctica
  slug: geometria-simplectica
- id: 435
  name: Hong Wang
  slug: hong-wang
- id: 437
  name: Jacob Tsimerman
  slug: jacob-tsimerman
- id: 436
  name: John Pardon
  slug: john-pardon
- id: 390
  name: Mecánica estadística
  slug: mecanica-estadistica
- id: 443
  name: o-minimalidad
  slug: o-minimalidad
- id: 438
  name: teoría cinética
  slug: teoria-cinetica
- id: 445
  name: teoría de modelos
  slug: teoria-de-modelos
- id: 433
  name: Yukun Deng
  slug: yukun-deng
category: *id001
---

_Sobre las cuatro Medallas Fields de 2026: el detalle matemático y qué frontera cruzamos realmente._

> Cuatro medallas premian el cierre de programas que llevaban décadas o siglos trabados: la derivación de Boltzmann desde las leyes de Newton, la conjetura de Kakeya en tres dimensiones, André–Oort para variedades de Siegel y el conteo virtual de curvas en geometría simpléctica. No hay ontología matemática nueva; hay dos métodos genuinos —la o-minimalidad como herramienta aritmética y el trasplante de la maquinaria de cumulantes desde la turbulencia de ondas— y un hilo conceptual común: el pasaje entre escalas y la idea de que la patología, allí donde parecía caos, tiene gramática. Este texto recorre el detalle técnico de los cuatro y termina en lo que no es matemático: quién puede producir un teorema, y dónde.

## Antes de empezar: tres precisiones que conviene corregir

Hay tres deslizamientos frecuentes en la cobertura periodística que conviene sacar del camino antes de entrar en el detalle, porque son exactamente los lugares donde la divulgación se vuelve falsa.

El primero es el problema de Kakeya. La pregunta por “el área mínima necesaria para girar una aguja 360 grados” es el _problema de la aguja_, y está resuelto desde hace un siglo con una respuesta desconcertante: el ínfimo es cero, no se alcanza, y Besicovitch construyó los conjuntos que lo muestran. La _conjetura_ de Kakeya es otra cosa: dice que un conjunto que contiene un segmento unitario en cada dirección, aunque tenga medida de Lebesgue nula, debe tener dimensión de Hausdorff igual a la del espacio ambiente. No se trata de volumen sino de dimensión, y esa diferencia es todo el problema.

El segundo es Deng. No se trata de “escalas de tiempo mucho más largas”: el resultado es cualitativamente distinto. La derivación vale por tiempos arbitrariamente largos, tan largos como exista la solución de la ecuación de Boltzmann. El problema de la derivación queda reducido al problema de la existencia, que es otro problema abierto pero es _otro_ problema.

El tercero es menor pero importa: el método de decoupling de Bourgain y Demeter no es la herramienta central del trabajo de Wang sobre suavizado local. Guth, Wang y Zhang resolvieron la conjetura de suavizado local en el plano con una inducción en escalas y una estimación de función cuadrática inversa, en un registro geométrico más que armónico. El decoupling es pariente, no motor.

Hay un rasgo común a los cuatro trabajos premiados que conviene tener presente desde el comienzo. Ninguno consiste simplemente en demostrar un teorema difícil. Los cuatro modifican la forma en que una comunidad matemática entera aborda un problema. En algunos casos el avance consiste en una técnica nueva; en otros, en demostrar que una intuición utilizada durante décadas era efectivamente correcta. La pregunta relevante, entonces, no es solamente qué probaron, sino qué dejó de ser un obstáculo después de esos trabajos.

## 1. Deng: qué significa exactamente “derivar” Boltzmann

La ecuación de Boltzmann para la densidad de una partícula $f(t,x,v)$ es

$$\partial\_t f + v \cdot \nabla\_x f = Q(f,f)$$

con el operador de colisión

$$Q(f,f)(v) = \int\_{\mathbb{R}^d} \int\_{S^{d-1}} \big[ f(v’)f(v\_\*’) – f(v)f(v\_\*) \big] \, \big((v – v\_\*)\cdot \omega\big)\_+ \, d\omega \, dv\_\*$$

donde $v’, v\_\*’$ son las velocidades post-colisión determinadas por conservación de energía e impulso. La estructura decisiva está en el corchete: es _cuadrático_ en $f$. Y ahí está el escándalo lógico que Boltzmann nunca resolvió. La dinámica newtoniana subyacente involucra la densidad conjunta de dos partículas $f\_2(v, v\_\*)$; escribir $f\_2 = f \cdot f$ es suponer que las dos partículas que están por chocar son estadísticamente independientes. Eso es la _Stosszahlansatz_, la hipótesis de caos molecular. Es exactamente el punto donde entra la irreversibilidad, y es exactamente el punto que Loschmidt y Zermelo atacaron.

El régimen correcto para el límite es el escalado de Boltzmann–Grad: $N$ esferas de radio $\varepsilon$ con

$$N \varepsilon^{d-1} = \alpha \quad \text{constante,} \qquad N \varepsilon^{d} \to 0$$

Es decir: el camino libre medio se mantiene de orden uno mientras la fracción de volumen ocupada tiende a cero. Gas enrarecido, colisiones binarias, nada de correlaciones de tres cuerpos.

Lanford probó en 1975 que en ese límite la jerarquía BBGKY converge a la jerarquía de Boltzmann. Pero su prueba usaba una expansión en serie tipo Duhamel cuyo control se agota: valía sólo para una fracción del tiempo libre medio, algo así como un quinto de una colisión típica por partícula. Cincuenta años sin mover ese techo. La razón es puramente combinatoria: al iterar la expansión, la cantidad de historias de colisión posibles crece factorialmente, y entre ellas están las _recolisiones_, precisamente las que destruyen la independencia. Lanford podía ignorarlas porque en tiempos cortos son raras; en tiempos largos, dominan.

Deng, con Zaher Hani y Xiao Ma, no eliminó las recolisiones: las contabilizó. La estrategia, importada del programa de los dos primeros autores sobre la ecuación cinética de ondas en turbulencia débil, consiste en propagar un _ansatz de cumulantes_ que recuerda la historia completa de colisiones en $[0,t]$, en lugar de intentar restablecer la independencia en cada paso. Esa historia se codifica en objetos combinatorios análogos a diagramas de Feynman —las moléculas de historia de colisión—, se estratifica el tiempo en capas, y el corazón técnico es un algoritmo de corte que descompone esos diagramas y acota sus integrales asociadas. La novedad es que el error deja de acumularse exponencialmente.

El artículo compañero cierra el arco: de la ecuación de Boltzmann, vía límites hidrodinámicos, se obtienen Euler compresible y Navier–Stokes–Fourier incompresible. Eso resuelve el sexto problema de Hilbert en el caso de esferas duras y gas enrarecido: el puente completo desde las leyes de Newton hasta las ecuaciones de la mecánica de fluidos.

Lo que esto significa filosóficamente merece subrayarse, porque es el punto que la prensa no toca. El caos molecular deja de ser una hipótesis externa y pasa a ser un teorema: una consecuencia demostrable de la dinámica reversible más la aleatoriedad del dato inicial. La flecha del tiempo no aparece por magia; aparece porque el conjunto de microestados que se comportan de otro modo tiene medida despreciable respecto de la distribución inicial. Es la versión rigurosa, y a tiempos largos, de aquello que Boltzmann sólo pudo argumentar.

## 2. Pardon: contar cuando el espacio de módulos está roto

El problema de Pardon se enuncia así. Para contar curvas pseudo-holomorfas en una variedad simpléctica uno construye el espacio de módulos $\overline{\mathcal{M}}$ de tales curvas y quiere integrar sobre él. Si $\overline{\mathcal{M}}$ fuera una variedad compacta lisa de la dimensión esperada $d$, tendríamos una clase fundamental $[\overline{\mathcal{M}}] \in H\_d$ y el invariante sería una integral. Nunca lo es. El operador linealizado $D\bar\partial$ no es sobreyectivo, aparecen obstrucciones, isotropías finitas, curvas múltiplemente cubiertas, y el espacio queda con dimensión local variable y singularidades severas.

Lo que se necesita es una _clase fundamental virtual_ $[\overline{\mathcal{M}}]^{\mathrm{vir}} \in \check{H}\_d(\overline{\mathcal{M}}; \mathbb{Q})$: un sustituto de la clase fundamental que viva en la dimensión esperada aunque el espacio real no la tenga. Existían construcciones —perturbaciones de Kuranishi en la escuela de Fukaya y Ono, polifolds en la de Hofer, Wysocki y Zehnder—, pero eran analíticamente pesadísimas y su compatibilidad mutua era, ella misma, un problema abierto.

El aporte de Pardon fue cambiar de registro: reemplazar la construcción analítica por una construcción homológica. Su formalismo de _atlas implícitos_ organiza los datos locales de obstrucción en un sistema de grupos de homología y define la clase virtual mediante un argumento de haces y colímites homotópicos, sin elegir perturbaciones globales. El resultado es funtorial, y esa funtorialidad es lo que permite comparar teorías distintas.

De ahí salen sus aplicaciones mayores: las categorías de Fukaya de variedades de Liouville, y la conjetura MNOP —Maulik, Nekrasov, Okounkov y Pandharipande—, abierta unos veinte años, que afirma que dos maneras de contar curvas en un Calabi–Yau de dimensión tres, la de Gromov–Witten y la de Donaldson–Thomas, coinciden tras el cambio de variable

$$q = -e^{iu}$$

entre las funciones generatrices reducidas $Z’\_{\mathrm{GW}}(u)$ y $Z’\_{\mathrm{DT}}(q)$. Que dos conteos de naturaleza radicalmente distinta —uno simpléctico y transcendente, otro algebraico y esquemático— den el mismo número no es un accidente: es el tipo de coincidencia que la física de cuerdas predice y la matemática debe justificar.

Conviene mencionar sus dos resultados tempranos porque explican la forma de su carrera. De estudiante de grado respondió una pregunta de Gromov de 1983 mostrando que la distorsión de los nudos tóricos $T(p,q)$ no está acotada, es decir, que hay nudos que no se pueden tensar. Y poco después probó la conjetura de Hilbert–Smith en dimensión tres: el grupo de enteros $p$-ádicos $\mathbb{Z}\_p$ no puede actuar fielmente por homeomorfismos sobre una variedad de dimensión tres.

## 3. Tsimerman: la lógica como herramienta aritmética

Acá lo verdaderamente nuevo no es un teorema sino un método, y el método viene de la teoría de modelos.

Una estructura o-minimal es una estructura real donde los subconjuntos definibles de $\mathbb{R}$ son uniones finitas de puntos e intervalos. La estructura relevante es $\mathbb{R}\_{\mathrm{an},\exp}$, que incluye funciones analíticas restringidas y la exponencial. La o-minimalidad es, literalmente, una hipótesis de _mansedumbre_: prohíbe la patología, prohíbe los conjuntos infinitamente oscilantes, prohíbe los fractales.

El teorema de Pila–Wilkie es el motor. Dice que si $X \subseteq \mathbb{R}^n$ es definible en una estructura o-minimal y $X^{\mathrm{trans}}$ es su parte transcendente —lo que queda al sacarle todos los subconjuntos algebraicos positivo-dimensionales—, entonces para todo $\varepsilon > 0$

$$N(X^{\mathrm{trans}}, T) \leq C(X, \varepsilon)\, T^{\varepsilon}$$

donde $N$ cuenta puntos racionales de altura a lo sumo $T$. Traducido: un conjunto manso tiene _muy pocos_ puntos racionales, a menos que contenga pedazos algebraicos enteros.

Conviene detenerse un segundo en qué significa acá “manso”, porque es la palabra que hace todo el trabajo. No quiere decir simple, ni suave, ni pequeño. Quiere decir que el conjunto no puede fingir. Una curva puede ser complicadísima y seguir siendo mansa; lo que no puede es oscilar infinitas veces, acumularse sobre sí misma sin límite, imitar localmente a un objeto algebraico sin serlo. La o-minimalidad prohíbe exactamente ese repertorio de disfraces. Y el teorema de Pila y Wilkie dice, en el fondo, que un objeto que no puede fingir tampoco puede acumular puntos racionales por casualidad: si tiene muchos, es porque adentro hay álgebra de verdad. Todo lo que sigue es la explotación sistemática de esa imposibilidad de simular.

La estrategia de Pila–Zannier para André–Oort se arma entonces como una tenaza. Los puntos especiales de una variedad de Shimura se levantan, vía el dominio fundamental de la aplicación de uniformización —que es definible—, a puntos racionales de un conjunto definible. Si hubiera infinitos puntos especiales fuera de una subvariedad especial, Pila–Wilkie daría una cota superior de $T^{\varepsilon}$. Del otro lado se necesita una cota _inferior_ para el tamaño de la órbita de Galois de un punto especial, del orden de una potencia positiva del discriminante. Si la cota inferior supera a la superior, contradicción, y los puntos especiales tienen que estar contenidos en subvariedades especiales.

El eslabón que faltaba era justamente la cota inferior de Galois para $\mathcal{A}\_g$, el espacio de módulos de variedades abelianas principalmente polarizadas. Tsimerman la obtuvo conectándola con alturas de Faltings y con la conjetura de Colmez en su forma promediada —probada independientemente por Andreatta, Goren, Howard y Madapusi Pera, y por Yuan y Zhang—, y con eso cerró André–Oort para las variedades modulares de Siegel. Es de las pocas veces en que una demostración usa, sin metáfora, lógica matemática, análisis, geometría algebraica y teoría analítica de números en el mismo argumento.

El otro pilar, con Bakker, es el teorema de Chow definible: una subvariedad analítica cerrada de una variedad algebraica que además sea definible en una estructura o-minimal, es algebraica. Es un GAGA o-minimal, y de él se sigue la conjetura de Griffiths sobre la algebraicidad de las imágenes de aplicaciones de períodos. La o-minimalidad dejó de ser una curiosidad de lógicos y pasó a ser infraestructura de la geometría algebraica.

## 4. Wang: dimensión, no volumen

Un conjunto de Kakeya $K \subseteq \mathbb{R}^n$ contiene un segmento unitario en cada dirección. Besicovitch mostró que puede tener medida nula. La conjetura afirma

$$\dim\_{H}(K) = \dim\_{M}(K) = n$$

Davies la probó en el plano en 1971. En dimensión tres la historia es una progresión de cotas: el argumento de Córdoba da $5/2$ por Cauchy–Schwarz sobre intersecciones de tubos; Wolff, en 1995, con su argumento del _cepillo_ —tomar todos los tubos que atraviesan un tubo dado y estimar el volumen de esa unión— alcanzó $(n+2)/2$, que en tres dimensiones es exactamente $5/2$; Katz, Łaba y Tao arañaron $5/2 + 10^{-10}$ en 2000. Ahí quedó, un cuarto de siglo.

La formulación cuantitativa que se usa realmente es en términos de tubos: si $\mathbb{T}$ es una familia de $\delta$-tubos con direcciones $\delta$-separadas, se busca

$$\Big| \bigcup\_{T \in \mathbb{T}} T \Big| \gtrsim\_\varepsilon \delta^{\varepsilon} \cdot \delta^{n – d}$$

y la conjetura corresponde a $d = n$.

Wang y Zahl atacaron primero una clase especial: los conjuntos de Kakeya _pegajosos_, aquellos donde tubos con direcciones cercanas permanecen cercanos, lo que produce una autosemejanza multiescala aproximada. Katz y Tao habían señalado esa clase como el caso duro. En 2022 la resolvieron. Después vino la parte que nadie creía alcanzable: reducir el caso general al pegajoso. Ese es el trabajo de 2025, ciento veintisiete páginas, apoyado en estimaciones de volumen para uniones de conjuntos convexos.

La arquitectura del argumento es una inducción en escalas: mostrar que si la dimensión fuera $d$, entonces también sería $d + \eta$ para cierto incremento uniforme, y que el argumento arranca desde cualquier punto de partida. Uno no prueba millones de incrementos: prueba que cada cota implica la siguiente, y sube la escalera desde $5/2$ hasta $3$. La estructura fina se organiza en _granos_, piezas planas casi rectangulares donde el conjunto se concentra, y el argumento consiste en mostrar que las configuraciones que evitarían la conclusión contradicen la maximalidad de esos granos.

La importancia externa está en la cadena de implicaciones del análisis armónico: restricción de Stein implica suavizado local, que implica Kakeya. Kakeya es el eslabón más débil de la cadena y por eso su caída no resuelve los otros, pero libera técnica. A eso se suma el trabajo de Wang con Guth y Zhang que probó la conjetura de suavizado local en el plano, con la estimación aguda

$$\| e^{it\sqrt{-\Delta}} f \|\_{L^4(\mathbb{R}^2 \times [1,2])} \lesssim\_{\varepsilon} \| f \|\_{W^{\varepsilon,4}}$$

que controla cuánta energía de una onda puede concentrarse en un punto, y que es exactamente la pregunta física detrás de todo el asunto.

Llegados a este punto aparece una pregunta natural. Los cuatro resultados pertenecen a áreas casi inconexas: teoría cinética, geometría simpléctica, lógica aplicada a la aritmética y análisis armónico. ¿Tiene sentido tratarlos como una misma generación matemática? Si la respuesta fuera negativa, la lista de premiados sería apenas una enumeración. Pero si existe un hilo común, entonces la edición 2026 de la Fields dice algo sobre el estado actual de la matemática, además de decir algo sobre cada uno de sus protagonistas.

## Conclusiones: ¿qué hay de nuevo, y qué frontera cruzamos?

La respuesta honesta a la primera pregunta es incómoda, y vale la pena decirla sin adornos: esta camada no inventó objetos nuevos de pensamiento. No hay acá un equivalente a los espacios perfectoides o a la matemática condensada, es decir, a una ontología matemática nueva que reorganice un área entera. Lo que hay es otra cosa, y no es menor: es el _cierre_ de programas largos. Lanford 1975, Kakeya 1917 con la conjetura moderna de los años setenta, Hilbert 1900, André y Oort de fines de los ochenta y mediados de los noventa, MNOP de 2003. Son cuatro medallas por terminar cosas, no por empezarlas.

Dicho esto, hay dos novedades metodológicas genuinas, y son las que van a durar. La primera es la o-minimalidad convertida en herramienta aritmética estándar: que una hipótesis de la teoría de modelos, diseñada por lógicos para clasificar estructuras, se haya vuelto el instrumento con el que se distingue lo algebraico de lo transcendente en geometría, es un desplazamiento de fronteras disciplinares que no tiene muchos precedentes. La segunda es el trasplante de la tecnología diagramática y de cumulantes desde la turbulencia de ondas hacia la dinámica de partículas: Deng y Hani construyeron un método para un problema y descubrieron que servía para otro que llevaba medio siglo trabado. Eso es lo más parecido a una máquina nueva que hay en el conjunto.

Si uno busca un hilo conceptual común, lo encuentra, y es el pasaje entre escalas. Los cuatro resultados son, en el fondo, teoremas sobre cómo se relaciona una descripción fina con una gruesa. Deng pasa del microestado newtoniano al campo cinético y de ahí al fluido. Wang controla cómo interactúan estructuras geométricas a escalas encajadas por inducción. Pardon organiza datos locales de obstrucción en un invariante global. Tsimerman separa lo algebraico de lo transcendente mediante una noción de finitud. Y en los cuatro casos la técnica decisiva es la misma en su forma: probar que la patología no sólo es rara sino _estructurada_. Los conjuntos pegajosos, los cumulantes con memoria, las estructuras o-minimales, los atlas implícitos: todos son maneras de decir que aquello que parecía caos es en realidad un caos con gramática, y que la gramática se puede escribir.

Lo que queda abierto es tanto o más que lo cerrado. Kakeya sigue abierta en dimensión cuatro y superiores, donde la geometría de intersección de tubos se complica cualitativamente, y las conjeturas de restricción y de Bochner–Riesz —que eran la motivación original— siguen intactas. Boltzmann quedó derivada para esferas duras, pero los potenciales de interacción realistas siguen esencialmente fuera de alcance, y el problema de Cauchy global para la propia ecuación de Boltzmann lleva más de ciento cincuenta años sin respuesta, igual que la regularidad global de Navier–Stokes. André–Oort general se completó para toda variedad de Shimura, pero la conjetura de Zilber–Pink, que la contiene, no. En matemática cerrar un problema es sobre todo descubrir cuál era el siguiente.

Hay, sin embargo, una última frontera que no pertenece a la matemática sino a la institución que la produce. Los teoremas son universales; las condiciones para producirlos, no.

Los cuatro resultados premiados son colaborativos: Deng con Hani y Ma, Wang con Zahl y con Guth y Zhang, Tsimerman con Bakker, Brunebarbe, Pila y Shankar. La medalla, en cambio, es individual y tiene tope de edad. Es un dispositivo de consagración diseñado en los años veinte para una práctica científica que ya no existe, y que sigue produciendo un efecto perverso conocido: convierte un trabajo colectivo distribuido en capital simbólico personal, y refuerza así la concentración institucional que lo hizo posible. Los cuatro trabajan en Norteamérica. Dos vienen del sistema de olimpíadas chino, que es una máquina de detección temprana con financiamiento estatal sostenido durante décadas. Nada de esto invalida los teoremas. Pero decir que la matemática es universal y dejar ahí el asunto es no mirar el campo: el talento puede estar distribuido, la infraestructura que lo convierte en teorema no lo está. Esa asimetría es un dato de política científica, y a un país como el nuestro le concierne bastante más que la topología simpléctica.
