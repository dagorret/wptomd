---
title: 'El Secreto Matemático detrás de Google: El Problema de la Matriz Diagonal
  y los Autovalores en el Círculo Unitario'
slug: el-secreto-matematico-detras-de-google-el-problema-de-la-matriz-diagonal-y-los-autovalores-en-el-circulo-unitario
status: published
legacy_url: https://dagorret.com.ar/el-secreto-matematico-detras-de-google-el-problema-de-la-matriz-diagonal-y-los-autovalores-en-el-circulo-unitario/
wordpress_id: 1401
published_at: '2026-07-23T19:02:00'
modified_at: '2026-07-16T16:13:28'
wordpress_category_ids:
- 418
- 20
wordpress_tag_ids:
- 410
- 415
- 413
- 411
- 416
- 135
- 414
- 182
- 412
categories:
- &id001
  id: 418
  name: Matemáticas
  slug: matematicas
- id: 20
  name: Tecnología
  slug: tecnologia
tags:
- id: 410
  name: Álgebra Lineal
  slug: algebra-lineal
- id: 415
  name: Algoritmos
  slug: algoritmos
- id: 413
  name: Autovalores
  slug: autovalores
- id: 411
  name: Google PageRank
  slug: google-pagerank
- id: 416
  name: Infraestructura de Red
  slug: infraestructura-de-red
- id: 135
  name: Inteligencia Artificial
  slug: inteligencia-artificial
- id: 414
  name: Matrices
  slug: matrices
- id: 182
  name: Sistemas Complejos
  slug: sistemas-complejos
- id: 412
  name: Teoría de Redes
  slug: teoria-de-redes
category: *id001
---

¿Cómo se relaciona un problema abstracto de álgebra lineal avanzada con el motor de búsqueda que cambió la historia de la humanidad? La respuesta está en una elegante manipulación de matrices: encontrar una matriz diagonal positiva $D$ que sea capaz de domar los autovalores de una matriz cualquiera $M$.

A continuación, desglosamos el problema, la teoría matemática que lo sustenta y cómo Google aplicó un concepto emparentado a escala global — sin ocultar dónde esa aplicación se aparta del teorema original.

## 1. El Problema Explicado

Supongamos que tenemos una matriz compleja $M \in \mathbb{C}^{n \times n}$ y queremos modificarla de manera controlada. Para ello, la multiplicamos por una matriz diagonal con valores reales y estrictamente positivos:

$$D = \text{diag}(d\_1, d\_2, \dots, d\_n) \quad \text{con } d\_i > 0$$

El desafío consiste en elegir adecuadamente esta matriz $D$ de modo que todos los autovalores del producto resultante, $\sigma(DM)$, queden atrapados de forma obligatoria exactamente sobre el círculo unitario en el plano complejo o en el origen:

$$\sigma(DM) \subset S^1 \cup \{0\} \quad \text{donde} \quad S^1 = \{ z \in \mathbb{C} : |z| = 1 \}$$

¿Es esto siempre posible? ¿Qué herramientas teóricas garantizan que podamos “forzar” a los autovalores de una matriz a adoptar esta estructura geométrica tan particular?

## 2. La Teoría Explicada

Este desafío matemático se enmarca dentro de lo que en la literatura se conoce como el __Problema de Autovalores Inversos Multiplicativos (MIEP)__. La teoría detrás de su viabilidad y límites se divide en dos grandes frentes:

### El Teorema de Existencia (en el plano complejo)

Si permitimos que las entradas de nuestra matriz diagonal $D$ sean números complejos, el matemático Shmuel Friedland demostró en 1975 un resultado fundamental:

> __Teorema:__ Si todos los menores principales de la matriz $M$ son distintos de cero, siempre existe una matriz diagonal $D$ tal que el producto $DM$ (o $MD$) tiene exactamente el espectro de autovalores prescrito que deseemos (en nuestro caso, sobre el círculo unitario). Además, el número de matrices $D$ que cumplen esta propiedad es, a lo sumo, $n!$.

### La restricción a diagonales positivas ($D > 0$)

Si limitamos estrictamente a $D$ a ser una matriz real y definida positiva ($d\_i > 0$), la solución no siempre está garantizada para cualquier matriz $M$ arbitraria.

- __El obstáculo:__ Si la matriz original $M$ es estrictamente nilpotente (como una matriz triangular con ceros en la diagonal), cualquier escalado $DM$ seguirá siendo nilpotente, atrapando todos sus autovalores en el $\{0\}$ sin posibilidad de llevarlos a la frontera del círculo unitario.
- __La viabilidad:__ Para clases de matrices con estructuras dominantes (como las $H$-matrices o matrices con diagonales estrictamente dominantes), sí es posible encontrar un escalado positivo $D > 0$ que acote y localice con precisión los autovalores en la región unitaria deseada a través de la contracción de sus discos de Gerschgorin.

## 3. El Caso Histórico de Google — y dónde la analogía se aparta del teorema

A finales de la década de los 90 y principios de los 2000, los fundadores de Google se toparon con un problema estructuralmente emparentado al intentar ordenar la inmensidad de la Web.

### El problema de Google

Google representó la Web a través de una matriz gigante de adyacencia $M$, donde un $1$ en la posición $(i, j)$ significaba que la página $i$ tenía un enlace hacia la página $j$. Para calcular la relevancia (el famoso PageRank), necesitaban encontrar un estado estacionario: el autovector correspondiente al autovalor dominante $\lambda = 1$ (el cual vive en el círculo unitario). Sin embargo, una matriz de enlaces web cualquiera no tiene por qué tener este autovalor, ni ser estable.

### La solución mediante escalado diagonal ($D^{-1}M$)

¿Cómo estructuraron matemáticamente la Web para forzar la convergencia? Aplicaron un escalado diagonal multiplicando $M$ por la inversa de una matriz diagonal positiva $D$:

$$D^{-1}M$$

Aquí, la matriz diagonal $D$ guardaba en sus entradas el grado de salida de cada página: $d\_i = \text{out-degree}(i)$ (la cantidad de enlaces salientes de la página $i$). Al multiplicar por $D^{-1}$ (cuyas entradas en la diagonal son $1/d\_i$):

1. __Normalización por filas:__ convirtieron la matriz de la Web en una matriz estocástica por filas (donde todas las filas sumaban exactamente $1$).
2. __Garantía de Perron-Frobenius:__ por el Teorema de Perron-Frobenius para matrices no negativas, esta transformación garantiza de forma inmediata que el radio espectral de la matriz resultante sea exactamente $1$.
3. __Autovalor en el círculo unitario:__ el autovalor dominante quedó anclado en la frontera del círculo unitario ($\lambda = 1$), permitiendo que el algoritmo iterativo de Google convergiera siempre hacia la solución única que determinaba la importancia de cada página.

### Una aclaración honesta

Vale una aclaración honesta: esta aplicación de Google no es una instancia directa del Problema de Autovalores Inversos Multiplicativos que acabamos de exponer. Friedland y el MIEP responden a la pregunta _“dado un espectro objetivo arbitrario, ¿existe una $D$ que lo produzca?”_ — un problema de existencia no trivial. Google, en cambio, nunca necesitó resolver ese problema: la matriz $D$ (los grados de salida) se construye de forma directa y trivial, y es el Teorema de Perron-Frobenius para matrices no negativas — un resultado distinto, más antiguo, y que no depende de la teoría de Friedland — el que garantiza que el autovalor dominante caiga exactamente en $\lambda = 1$. El puente conceptual entre ambos problemas (elegir $D$ para controlar el espectro de $DM$) es real y vale la pena señalarlo, pero la “solución” de Google no es una aplicación del teorema de 1975: es un caso más simple, resuelto por otra vía.

## 4. De la Teoría a la Práctica: Algoritmos para “Domar” el Espectro

Si la teoría de Friedland nos asegura que la matriz diagonal $D$ existe bajo ciertas condiciones, la siguiente pregunta lógica es de carácter puramente computacional: ¿cómo la calculamos de forma eficiente en la vida real? Como bien apunta Moody Chu (1998) en su revisión del problema, pasar de la existencia teórica a la convergencia numérica es un abismo de complejidad.

A nivel de ingeniería de sistemas e infraestructura de software, se utilizan tres grandes enfoques algorítmicos para resolver el MIEP en matrices de gran escala:

- __Métodos de homotopía y continuación:__ consisten en deformar continuamente una matriz fácil de resolver (cuyo espectro ya conocemos) hacia nuestra matriz objetivo $M$. A lo largo de esta “curva de deformación”, se resuelven ecuaciones diferenciales ordinarias para seguir la trayectoria de la matriz diagonal $D$.
- __Métodos de proyección e iteración (tipo Newton):__ se formulan como la búsqueda de raíces de un sistema de ecuaciones no lineales donde la función objetivo es la diferencia entre el espectro actual de $DM$ y el espectro deseado. Aunque son brutalmente rápidos (convergencia cuadrática), requieren un excelente “punto de partida” para no colapsar.
- __Optimización en variedades riemannianas:__ para problemas donde $D$ debe mantener restricciones geométricas estrictas (como ser estrictamente positiva), se optimiza una función de costo que mide la “distancia” al espectro objetivo directamente sobre la superficie geométrica (variedad) que definen las matrices diagonales.

## 5. El Futuro del MIEP: Resiliencia de Redes e Inteligencia Artificial

Controlar el espectro de una matriz mediante un escalado diagonal no es solo un truco de álgebra lineal; es una de las herramientas más potentes para diseñar los sistemas complejos del mañana. Hoy en día, el legado de estos problemas de autovalores inversos se aplica en áreas críticas de la tecnología:

- __Inmunización y resiliencia de redes de infraestructura:__ en redes eléctricas, de transporte o de telecomunicaciones (como los cables submarinos de fibra óptica), el autovalor dominante de la matriz de adyacencia determina qué tan rápido se propaga una falla o un virus. Diseñar un escalado $D$ equivale a decidir estratégicamente dónde colocar “amortiguadores” o defensas para alterar el espectro de la red, garantizando que un fallo local no tire el sistema entero de forma exponencial.
- __Estabilización de redes neuronales recurrentes (RNN):__ en Inteligencia Artificial, las RNN procesan información secuencial multiplicando estados ocultos por una matriz de pesos $W$. Si los autovalores de $W$ se escapan del círculo unitario, los gradientes explotan; si se encogen hacia el origen, los gradientes se desvanecen. Utilizar técnicas inspiradas en el escalado multiplicativo para forzar que los autovalores de la matriz de transiciones queden atrapados en $S^1 \cup \{0\}$ es una de las técnicas más sofisticadas para lograr que una IA mantenga memoria a largo plazo sin desestabilizarse.

## Referencias

Para quienes deseen profundizar en la demostración formal o en los algoritmos prácticos para calcular estas matrices de escalado:

1. Friedland, S. (1975). On inverse multiplicative eigenvalue problems for matrices. _Linear Algebra and its Applications_, 12(2), 127–137. https://doi.org/10.1016/0024-3795(75)90061-0 _¿Por qué es clave?_ Es la demostración teórica definitiva sobre la existencia de la matriz $D$ en el espacio complejo cuando los menores principales no se anulan.
2. Chu, M. T. (1998). Inverse Eigenvalue Problems. _SIAM Review_, 40(1), 1–39. https://doi.org/10.1137/S0036144596303984 (disponible también en JSTOR: https://www.jstor.org/stable/2652996) _¿Por qué es clave?_ Es el mapa general y el análisis de viabilidad práctica de los problemas de autovalores inversos, ideal para quienes buscan diseñar algoritmos numéricos para calcular $D$.
