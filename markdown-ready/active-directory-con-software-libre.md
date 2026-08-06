---
title: 'Active Directory con Software Libre, Parte 2: el member server con ACLs reales,
  GPO sin humo y el segundo DC'
slug: active-directory-con-software-libre
status: published
legacy_url: https://dagorret.com.ar/active-directory-con-software-libre/
wordpress_id: 1008
published_at: '2026-06-25T21:16:34'
modified_at: '2026-07-30T16:37:13'
wordpress_category_ids:
- 358
- 21
wordpress_tag_ids:
- 138
- 352
categories:
- &id001
  id: 358
  name: English
  slug: english
- id: 21
  name: Sistemas
  slug: sistemas
tags:
- id: 138
  name: Active Directory
  slug: active-directory
- id: 352
  name: Linux
  slug: linux
category: *id001
---

En la __Parte 1 (en revision)__ montamos el Controlador de Dominio bien: realm que no es `.local`, reloj firmado, backup versionado. Pero dejamos tres promesas explícitamente para después, porque son justo el punto donde los tutoriales abandonan al lector: el servidor de archivos __fuera__ del DC, los permisos por rol que de verdad funcionan, y la alta disponibilidad con un segundo DC. Acá las cumplimos. Y, fiel al estilo de la casa, sin vender humo: cada cosa viene con su asterisco honesto.

## 1. El member server: archivos con ACLs reales, no POSIX plano

En la Parte 1 quedó claro por qué los shares no van sobre el DC. Ahora montamos el servidor miembro que sí sirve los archivos. Puede ser otra máquina física o una VM en el mismo fierro; lo que importa es que sea un nodo __separado__ unido al dominio, no el DC haciendo doble función.

### Unión al dominio

El `smb.conf` de un miembro es lo opuesto al de un DC: acá vos sí lo escribís, con `security = ads` y winbind resolviendo identidades del dominio.

```php
[global]
    workgroup = EMPRESA
    realm = AD.EMPRESA.COM.AR
    security = ads
    kerberos method = secrets and keytab
    winbind use default domain = yes
    winbind refresh tickets = yes
    template shell = /bin/bash
    template homedir = /home/%U

    idmap config * : backend = tdb
    idmap config * : range = 3000-7999
    idmap config EMPRESA : backend = rid
    idmap config EMPRESA : range = 10000-999999

    # lo que hace que las ACLs de Windows funcionen de verdad:
    vfs objects = acl_xattr
    map acl inherit = yes
    store dos attributes = yes
```

[ventas]

path = /srv/samba/ventas
read only = no

```php
sudo apt install -y samba winbind libpam-winbind libnss-winbind krb5-user acl attr
sudo net ads join -U administrator
sudo systemctl enable --now smbd nmbd winbind
# /etc/nsswitch.conf: agregar 'winbind' a las líneas passwd: y group:
```

### Verificá antes de tocar un solo permiso

Este es el paso que el 90% se saltea, y después pelea contra permisos que “no andan” cuando en realidad winbind ni siquiera ve a los usuarios del dominio. Confirmá la cadena completa antes de seguir:

```php
wbinfo -t                        # 'secret is good' -> la relación de confianza está sana
wbinfo -u | head                 # winbind lista los usuarios del dominio
wbinfo -g | head                 # y los grupos
getent passwd "EMPRESA\\jdoe"    # NSS resuelve el usuario del dominio
id "EMPRESA\\jdoe"               # uid/gid mapeados por idmap rid
```

Si `wbinfo -u` devuelve usuarios y `id` mapea un uid, recién ahí tiene sentido configurar permisos. Si falla, el problema es de DNS, reloj o el join, no de las ACLs.

### El modelo de permisos que cumple la promesa

La Parte 1 marcó por qué `chown root:"domain admins"` + `chmod 770` no implementa “Ventas entra solo a su carpeta”: POSIX puro es plano y hereda en bloque. Con `acl_xattr` activo, Samba guarda descriptores de seguridad NT completos en los atributos extendidos del archivo, así que podés mapear grupos del dominio igual que en Windows.

El esqueleto base en Linux —dueño de grupo del dominio y bit setgid para que lo herede todo lo que se cree dentro:

```php
sudo mkdir -p /srv/samba/ventas /srv/samba/autorizaciones
sudo chgrp "EMPRESA\\ventas"   /srv/samba/ventas
sudo chgrp "EMPRESA\\gerencia" /srv/samba/autorizaciones
sudo chmod 2770 /srv/samba/ventas /srv/samba/autorizaciones   # 2 = setgid
```

Y las ACLs reales por grupo, con su versión “default” para que se hereden hacia abajo:

```javascript
sudo setfacl -R  -m "g:EMPRESA\\ventas:rwx"   /srv/samba/ventas
sudo setfacl -dR -m "g:EMPRESA\\ventas:rwx"   /srv/samba/ventas
sudo setfacl -R  -m "g:EMPRESA\\gerencia:rwx" /srv/samba/autorizaciones
sudo setfacl -dR -m "g:EMPRESA\\gerencia:rwx" /srv/samba/autorizaciones
```

En la práctica diaria, sin embargo, lo más cómodo y lo que mejor convive con Windows es __gestionar estos permisos desde la pestaña Seguridad del Explorador__ en una máquina unida al dominio: como Samba persiste el descriptor NT en el xattr, lo que hacés desde Windows se respeta tal cual en Linux. Si preferís quedarte en la consola, `smbcacls //localhost/ventas / -U administrator` te deja leer y editar esos mismos descriptores sin salir del servidor. Lo importante conceptual: ya no estás peleando con bits POSIX, estás administrando ACLs de Active Directory que _casualmente_ viven en un filesystem Linux.

## 2. GPO sin humo: qué se hace desde Linux y qué sigue necesitando Windows

Acá hay que ser honesto en las dos direcciones, porque se dicen dos mentiras opuestas. La vieja —”con Samba no hay GPO, es un AD de juguete”— es falsa: Samba implementa GPO de verdad. La nueva —”manejás todo desde Linux, Windows no hace falta”— también es exagerada.

El dato concreto: desde la versión 4.14 Samba incluye soporte para aplicar GPO a clientes Linux, y el comando `samba-tool gpo` permite crear, enlazar y modificar GPO desde la línea de comandos. Hoy `samba-tool gpo manage` cubre un set creciente de políticas server-side: políticas de OpenSSH (por ejemplo `samba-tool gpo manage openssh set` para exigir autenticación Kerberos), de firewalld, de GNOME y otras, que aparecen en el editor bajo Administrative Templates → Samba cuando se cargan las plantillas ADMX de Samba. Esas plantillas se suben al SysVol con `samba-tool gpo admxload`.

Lo que conviene no maquillar: para administrar políticas de __clientes Windows__ en serio —mapeo de unidades, scripts de logon, plantillas administrativas del registro, restricted groups— la vía práctica sigue siendo la consola de Group Policy Management (GPMC) de RSAT desde una estación Windows unida al dominio. No es una limitación del directorio (el AD de Samba guarda y sirve esos GPO perfectamente); es que la _herramienta de edición_ cómoda para el mundo Windows la hace Microsoft. Hay alternativas web de terceros, pero para una pyme honesta la receta es: una VM Windows con RSAT para editar, Samba para almacenar y aplicar.

Un comando que sí conviene tener a mano para auditar lo que existe:

```php
sudo samba-tool gpo listall          # GUID y nombre de cada GPO del dominio
sudo samba-tool gpo aclcheck         # verifica que las ACLs LDAP y de DS coincidan
```

Y una regla de oro que se entiende recién en la sección que sigue: __editá los GPO siempre contra un único DC__ (el que tenga el rol PDC Emulator). El motivo es el SysVol.

## 3. El segundo DC: alta disponibilidad y el agujero del SysVol

Una arquitectura con un solo DC no es “empresarial”, es un punto único de falla con buena prensa. El segundo DC se une al dominio, no se provisiona de nuevo.

### Unir el DC2

En la segunda máquina, con su DNS apuntando al DC1 durante el join:

```
sudo samba-tool domain join ad.empresa.com.ar DC \
     -U administrator --dns-backend=SAMBA_INTERNAL
sudo systemctl unmask samba-ad-dc
sudo systemctl enable --now samba-ad-dc
```

Después, cada DC corre su propio DNS y se resuelve a sí mismo; los clientes deben tener __ambos__ DCs como servidores DNS para que la caída de uno no los deje ciegos. El reloj entre DCs es tan crítico como con los clientes: si el desfasaje supera los 5 minutos en cualquier dirección, empiezan los problemas con las cuentas del AD y con la replicación del dominio, así que el DC2 sincroniza contra el DC1 o contra el mismo pool externo.

La base de datos del directorio (usuarios, equipos, GPO como objetos LDAP) __sí__ se replica sola, vía el protocolo DRS. Verificalo:

```php
sudo samba-tool drs showrepl
sudo samba-tool drs replicate dc2 dc1 dc=ad,dc=empresa,dc=com,dc=ar
sudo samba-tool fsmo show        # dónde quedaron los roles FSMO
```

### El agujero que nadie te cuenta: SysVol no se replica solo

Acá está el límite real de Samba como AD, y omitirlo es deshonesto. Samba todavía no provee replicación de SysVol; mientras no esté implementada, hace falta un workaround para mantenerlo sincronizado. El SysVol es la carpeta (`/var/lib/samba/sysvol`) donde viven los archivos de las GPO y los scripts de logon: si no lo replicás, el DC2 sirve políticas viejas o vacías.

El workaround estándar y más simple es rsync __unidireccional__, y tiene una consecuencia de diseño que hay que respetar: elegís un DC maestro donde hacés todas las modificaciones (ediciones de GPO, scripts de logon), y los demás DC traen los cambios desde ahí, porque cualquier cambio hecho en ellos se sobrescribe al sincronizar. El buen candidato a maestro es el que tiene el rol PDC Emulator, que además es al que la GPMC se conecta por defecto. Esto explica la “regla de oro” de la sección anterior.

Dos detalles que hacen la diferencia entre que funcione y que rompa las GPO:

```php
# en el DC2, jalando desde el maestro (DC1 = PDC Emulator)
rsync -XAavz --delete-after root@dc1:/var/lib/samba/sysvol/ /var/lib/samba/sysvol/
sudo samba-tool ntacl sysvolreset
```

El `-X` y el `-A` no son opcionales: preservan los atributos extendidos y las ACLs POSIX, sin los cuales el SysVol queda con permisos rotos. Y el `samba-tool ntacl sysvolreset` después de cada sync reajusta las ACLs del árbol del SysVol a los valores que el AD espera. Si necesitás edición desde cualquiera de los dos DCs, existen variantes bidireccionales con osync o unison, más complejas, pero para una pyme el esquema maestro único es el más sano.

Un último requisito silencioso: todos los DCs deben usar los mismos mapeos de ID para los usuarios y grupos internos (built-in). Por eso, al sumar el DC2, conviene verificar la consistencia de `idmap.ldb` para las cuentas bien conocidas; si los IDs de los grupos built-in difieren entre DCs, las ACLs replicadas del SysVol terminan apuntando a entidades equivocadas.

## Conclusión

La Parte 1 demostró que un AD libre se monta bien si respetás la separación de funciones y los requisitos criptográficos. La Parte 2 muestra dónde está el trabajo real que los tutoriales esquivan: los archivos viven en un member server con ACLs de Active Directory de verdad —no bits POSIX disfrazados—; las GPO existen y una parte creciente se gestiona desde Linux, pero la edición seria de clientes Windows todavía pasa por RSAT, y conviene saberlo en vez de prometer lo contrario; y la alta disponibilidad con dos DCs es real para el directorio, pero el SysVol exige un workaround de rsync con maestro único que hay que diseñar a conciencia. Ninguna de estas cosas descalifica a Samba: lo vuelven una solución corporativa honesta, con sus bordes documentados. Que es exactamente lo opuesto a una demo que anduvo un viernes.

---

_Nota sobre las fuentes._ Los criterios se contrastan contra el SambaWiki (replicación de SysVol y sus workarounds, configuración de Group Policy), la documentación de `samba-tool gpo`, y las guías de despliegue multi-DC. Los rangos de `idmap`, los nombres de grupo (`EMPRESA\\ventas`) y las rutas son ilustrativos: adaptalos y verificalos contra tu propia red antes de producción.
