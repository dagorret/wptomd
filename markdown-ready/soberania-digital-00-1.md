---
title: Soberanía digital. Notas sobre construir un búnker anti–Big Tech con software
  que ya existía hace veinte años
slug: soberania-digital-00-1
status: published
legacy_url: https://dagorret.com.ar/soberania-digital-00-1/
wordpress_id: 17
published_at: '2026-04-23T18:34:38'
modified_at: '2026-08-01T22:00:35'
wordpress_category_ids:
- 33
wordpress_tag_ids:
- 124
- 125
categories:
- &id001
  id: 33
  name: Política
  slug: politica
tags:
- id: 124
  name: Espionaje
  slug: espionaje
- id: 125
  name: Vigilancia Tecnológica
  slug: vigilancia-tecnologica
category: *id001
---

Hay una contradicción silenciosa en la informática contemporánea, y no se discute lo suficiente. Nunca fue tan barato almacenar información, ni tan trivial moverla a través del planeta, ni tan accesible la potencia de cómputo. Y, sin embargo, nunca fue tan difícil poseer lo que uno almacena. La nube vendió durante una década una narrativa impecable —comodidad, sincronización, productividad, escalabilidad—, pero detrás de esa fachada hay un hecho técnico que no admite discusión: quien controla la infraestructura controla los datos. Y quien controla los datos, controla la memoria, las comunicaciones, los hábitos y, en último término, la autonomía de quien los produce.

El problema dejó de ser comercial hace tiempo. Es estructural. Las plataformas modernas convirtieron la informática en un modelo de dependencia permanente sin que casi nadie lo notara. El usuario ya no administra archivos; consume servicios. El administrador ya no configura servidores; alquila paneles. Las instituciones ya no poseen infraestructura; delegan soberanía tecnológica a terceros con quienes nunca van a sentarse en una mesa de negociación real. Y cuando el conocimiento técnico desaparece detrás de interfaces simplificadas —ese gesto tan amable, tan razonable, tan bien diseñado—, la capacidad de auditar y decidir desaparece con él.

Por eso conviene desactivar de entrada el malentendido más común. El _self-hosting_ basado en software libre no es nostalgia romántica, ni fetichismo de terminal, ni una pose ideológica contra las multinacionales. Es, mucho más prosaicamente, ingeniería aplicada a la independencia.

Sin embargo, una segunda lectura exige ser más descarnados: decíamos que la soberanía digital era un problema de ingeniería, pero nos equivocamos. Hoy es un problema de asedio.

## I. La trampa de confundir conveniencia con control (y el mito de la simplicidad)

La infraestructura moderna está saturada de soluciones empaquetadas: stacks enormes de Docker, appliances virtuales, plataformas “un clic”, servidores reescritos en Rust o Go, paneles que abstraen absolutamente todo lo que ocurre debajo. Muchas son técnicamente excelentes —algunas, francamente brillantes—, y sería una torpeza despreciarlas en bloque. Pero todas comparten un problema que rara vez se nombra: reducen la visibilidad del sistema.

Cuando todo funciona, la experiencia es perfecta. Ese es justamente el truco. El problema aparece —y siempre aparece— cuando algo falla. Es ahí donde el administrador descubre, con cierto desconcierto, que no conoce los procesos internos, no entiende el flujo de red, no sabe dónde están los logs reales, depende de _wrappers_ que él no escribió y de capas de abstracción que no controla. La infraestructura se ha convertido en una caja negra. Y las cajas negras son, por definición, incompatibles con cualquier idea seria de soberanía. No se puede defender lo que no se puede inspeccionar.

La vieja escuela Unix resolvía este dilema desde un lugar opuesto: cada componente hacía una sola cosa y la hacía bien. Postfix transportaba SMTP; Dovecot se ocupaba del almacenamiento IMAP; Apache servía la web; MariaDB se encargaba de la persistencia; Unbound resolvía DNS de forma recursiva; Bind9 declaraba autoridad; PHP-FPM ejecutaba; Nextcloud sincronizaba encima de todo eso. Cada servicio con sus logs, sus sockets, sus permisos visibles y sus procesos observables.

Ese conocimiento produce independencia operacional. Pero exige pagar un peaje que la industria ha intentado invisibilizar: la carga mental del mantenimiento.

## II. El costo invisible: la soberanía y la trampa del insomnio

Existe una idealización del administrador que pasa la noche frente a la terminal resolviendo un error a las tres de la mañana. Pero la soberanía digital no puede sostenerse sobre el agotamiento. La razón por la que las plataformas comerciales ganaron no es solo la pereza del usuario; es que el mantenimiento artesanal consume un recurso cada vez más escaso: tiempo de vida.

Cuando tu servidor personal o institucional se cae un domingo por una actualización menor de PHP, o cuando un certificado no renueva por una regla mal mapeada, la independencia empieza a sentirse como un segundo trabajo no pago.

La respuesta a esto no es rendirse ante el panel empaquetado de la nube ni volver al masoquismo del script improvisado. La respuesta es la __automatización transparente__. Usar herramientas de orquestación donde la infraestructura esté escrita como código declarativo, claro y auditable. Automatizar no para ocultar lo que pasa debajo, sino para garantizar que la soberanía sea operacionalmente sostenible en el tiempo.

## III. El correo electrónico como territorio feudalizado

Si hay un lugar donde la idea de soberanía choca de frente contra la realidad, es el correo electrónico. Montar un servidor SMTP propio sigue siendo técnicamente sencillo: Postfix, Dovecot, OpenDKIM, SPF, DMARC y registros inversos en el DNS. En un par de horas, el flujo técnico está listo y los mensajes se firman criptográficamente con precisión.

El problema ya no es técnico; es político. El correo se volvió un territorio colonizado. Los tres o cuatro grandes proveedores mundiales (Gmail, Outlook, Yahoo) han convertido sus mecanismos antispam en herramientas de centralización feudal. Una IP independiente, limpia y correctamente configurada, alojada en un centro de datos neutral, es frecuentemente bloqueada o enviada a la carpeta de spam sin explicación ni posibilidad real de reclamo, simplemente por “falta de reputación”.

Aquí la ilusión del búnker se rompe: el sistema no te rechaza porque tu servidor esté mal configurado; te rechaza porque no pagas peaje en su ecosistema. El antispam contemporáneo ya no protege al usuario del ruido: protege al oligopolio de la existencia de servidores soberanos.

## IV. DNS: la privacidad como arquitectura

Hay capas más glamorosas que el DNS, pero pocas tan críticas. El DNS define quién puede encontrar tus servicios y a quién le estás contando, consulta por consulta, lo que haces en internet.

Resolver consultas internas mediante __Unbound__ es probablemente la decisión de arquitectura más elegante para un hogar, oficina o institución. Un resolver recursivo propio elimina la telemetría de terceros, el _profiling_ comercial y la exposición de la red. El intermediario desaparece: la consulta va directamente de tu servidor a los servidores raíz. Con DNSSEC validado, el sistema deja de confiar en lo que le devuelven y empieza a verificarlo criptográficamente.

Para existir hacia afuera, __Bind9__ sigue siendo la declaración de soberanía pública por excelencia: administrar tus zonas, registros MX, delegaciones y claves sin depender de un panel de terceros es poseer tu identidad digital. Una organización que no controla sus registros DNS es una organización que alquila su existencia en la red.

## V. Nextcloud y la infraestructura como tejido profesional

Mucha gente instala Nextcloud pensando que está montando un “Google Drive libre”, y esa metáfora achica enormemente lo que la herramienta representa. Un despliegue serio se transforma en agenda, contactos, repositorio documental, espacio de colaboración y almacenamiento distribuido.

La clave está en el despliegue nativo y limpio: no como una colección opaca de contenedores pegados con un script heredado de un tutorial, sino integrado al sistema operativo. Con Apache o Nginx delante, PHP-FPM afinado, MariaDB optimizado en `utf8mb4`, Redis en memoria para caché y permisos estrictos.

Cuando el sistema está afinado al hardware real, la experiencia deja de sentirse “casera” y demuestra algo crucial: el software libre no es una alternativa de segunda categoría para presupuestos bajos; es infraestructura de nivel profesional.

## VI. Del búnker individual a la red común

El concepto de “búnker anti-Big Tech” es una metáfora poderosa para la autodefensa inicial. Pero el búnker tiene un límite evidente: es solitario. Si la respuesta a la centralización es que cada individuo o institución levante su propia isla inaccesible, terminamos con una red fragmentada de ermitaños técnicos.

El Software Libre de hace veinte años no triunfó solo por las líneas de código de Apache o Linux, sino porque estaba respaldado por una __comunidad de práctica__. La soberanía digital no puede ser una proeza individual ni un privilegio para quienes pueden pasar diez horas semanales administrando servidores.

El paso lógico tras construir el búnker es abrir la puerta y tejer alianzas. Necesitamos cooperativas de infraestructura, servidores comunitarios para escuelas, barrios y colectivos, donde el conocimiento, la reputación de IP y la carga de mantenimiento se compartan. La soberanía solo es real cuando es colectiva.

## VII. La terminal como acto de autonomía

Construir infraestructura propia no es el camino más rápido ni el más cómodo. Requiere lectura, _debugging_, paciencia con los errores ajenos y propios, y noches frente a la terminal. Pero produce algo que ninguna plataforma comercial puede vender: comprensión. Y en tecnología, comprender es conservar la capacidad de decidir.

Cuando un grupo o una institución controla su DNS, su correo, sus archivos, sus certificados y sus métricas, descubre que internet no es una nube abstracta e inalcanzable dominada por multinacionales. Internet sigue siendo, exactamente igual que en 1995, una red global de máquinas configuradas por personas.

Lo único que cambió fue la concentración de quién configura qué. Y en ese gesto simple de abrir una terminal Linux a las tres de la mañana para configurar tu propio servicio, se demuestra que la red, todavía, puede volver a pertenecerte.
