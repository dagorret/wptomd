---
title: 'Active Directory with Open Source, Part 2: Real Member Server ACLs, GPOs Without
  the Hype, and the Second DC'
slug: active-directory-with-open-source-part-2-real-member-server-acls-gpos-without-the-hype-and-the-second-dc
status: published
legacy_url: https://dagorret.com.ar/active-directory-with-open-source-part-2-real-member-server-acls-gpos-without-the-hype-and-the-second-dc/
wordpress_id: 1283
published_at: '2026-06-18T09:12:05'
modified_at: '2026-06-18T09:12:05'
wordpress_category_ids:
- 358
- 21
wordpress_tag_ids:
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
- id: 352
  name: Linux
  slug: linux
category: *id001
---

[In Part 1](/active-directory-with-open-source-for-smbs-the-version-that-survives-production-debian-13/), we set up our Domain Controller correctly: an operational realm that bypasses the `.local` trap, signed time protocols, and a robust versioned backup routine. However, we explicitly left three core promises for later because they represent the exact threshold where superficial tutorials abandon the reader: the file server operating completely decoupled from the DC, role-based folder privileges that actually work, and high availability via a secondary DC. Here, we deliver on those promises. And, keeping with our house style, we do it without the marketing fluff—every milestone comes with its honest infrastructure caveat.

### The Honest Architecture, in One Sentence

Separation of concerns: The Domain Controller authenticates and does nothing else; files live on a Member Server; the clock is a cryptographic requirement, not an ornament; backups have versions and a copy outside the network; and nothing hits production without being verified. Everything else is just a detail of that core concept.

From this point forward, every design choice comes accompanied by the typical error it replaces.

---

## 1. The Member Server: File Shares with Real ACLs, Not Flat POSIX

Part 1 established why shared storage directories should never sit directly on your Domain Controller. Now, we build the dedicated Member Server tasked with serving network files. It can be a separate physical chassis or an isolated VM running on the same hardware; what matters is that it is a dedicated node joined to the domain, not a DC pulled into double duty.

### Joining the Domain

The `smb.conf` layout of a Member Server is the exact polar opposite of a DC configuration: here, you write it yourself, leveraging `security = ads` and `winbind` to resolve domain identity structures natively.

```php
[global]
    workgroup = COMPANY
    realm = AD.COMPANY.COM.AR
    security = ads
    kerberos method = secrets and keytab
    winbind use default domain = yes
    winbind refresh tickets = yes
    template shell = /bin/bash
    template homedir = /home/%U

    idmap config * : backend = tdb
    idmap config * : range = 3000-7999
    idmap config COMPANY : backend = rid
    idmap config COMPANY : range = 10000-999999

    # What actually makes Windows ACLs work natively on Linux:
    vfs objects = acl_xattr
    map acl inherit = yes
    store dos attributes = yes

[sales]
    path = /srv/samba/sales
    read only = no
``````php
sudo apt install -y samba winbind libpam-winbind libnss-winbind krb5-user acl attr
sudo net ads join -U administrator
sudo systemctl enable --now smbd nmbd winbind
# /etc/nsswitch.conf: remember to append 'winbind' to both passwd: and group: lines
```

### Verify Before Fast-Forwarding Your Permissions

This is the validation step that 90% of administrators skip, only to find themselves fighting folder access errors later because `winbind` cannot map domain objects. Confirm the entire resolution chain before moving forward:

```php
wbinfo -t                        # 'secret is good' -> Trust relationship is healthy
wbinfo -u | head                 # winbind successfully lists domain users
wbinfo -g | head                 # winbind successfully lists domain groups
getent passwd "COMPANY\\jdoe"    # NSS resolves the specific domain account
id "COMPANY\\jdoe"               # uid/gid are correctly mapped via idmap rid
```

If `wbinfo -u` yields your corporate users and `id` successfully outputs a mapped UID, only then does it make technical sense to deploy folder constraints. If this layer fails, your issue stems from DNS, time sync, or the domain join routine—not your directory file access rules.

### The Permission Layout That Delivers on Its Promise

Part 1 outlined why executing `chown root:"domain admins" + chmod 770` fails to properly isolate a department: pure POSIX permissions are flat and inherit down in an absolute block. With `acl_xattr` enabled, Samba stores complete NT security descriptors inside the file system’s extended attributes. This allows you to map specific domain groups exactly like a Windows server would.

First, we build the underlying directory skeleton on Linux—enforcing group ownership to a domain group and setting the `setgid` bit so that everything created underneath automatically inherits that local group asset:

```php
sudo mkdir -p /srv/samba/sales /srv/samba/authorizations
sudo chgrp "COMPANY\\sales"       /srv/samba/sales
sudo chgrp "COMPANY\\management"  /srv/samba/authorizations
sudo chmod 2770 /srv/samba/sales /srv/samba/authorizations   # 2 = setgid bit
```

Next, we inject the actual domain group ACLs, mapping both the immediate target folder and its “default” mask to force recursion down the directory tree:

```javascript
sudo setfacl -R  -m "g:COMPANY\\sales:rwx"       /srv/samba/sales
sudo setfacl -dR -m "g:COMPANY\\sales:rwx"       /srv/samba/sales
sudo setfacl -R  -m "g:COMPANY\\management:rwx"  /srv/samba/authorizations
sudo setfacl -dR -m "g:COMPANY\\management:rwx"  /srv/samba/authorizations
```

In day-to-day administrative environments, however, the most efficient approach that best integrates with Windows workstations is to manage these security layers directly from the \*\*Security Tab\*\* inside Windows Explorer on a domain-joined PC. Because Samba persists the NT security descriptor into the underlying `xattr`, modifications made via Windows are respected completely by Linux. If you prefer staying strictly inside the terminal, executing `smbcacls //localhost/sales / -U administrator` lets you read and write those exact same descriptors natively. The core conceptual takeaway: you are no longer fighting with POSIX file bits; you are managing Active Directory ACLs that happen to reside on a Linux filesystem.

---

## 2. No-Nonsense GPOs: What Can Be Run From Linux and What Requires Windows

Here, we must treat the architecture honestly in both directions because two opposing myths are frequently peddled online. The old myth—”Samba is a toy AD that doesn’t support real GPOs”—is patently false: Samba implements real Group Policy objects. The newer myth—”You can manage your entire domain policy from Linux; Windows is dead”—is a major exaggeration.

The hard technical facts: from version 4.14 onward, Samba includes built-in engines to apply GPOs directly to Linux client targets, and the `samba-tool gpo` tool allows administrators to create, link, and alter GPOs straight from the command line. Today, `samba-tool gpo manage` covers an expanding set of server-side policies: OpenSSH constraints (e.g., executing `samba-tool gpo manage openssh set` to demand Kerberos key exchanges), firewalld configurations, GNOME settings, and more. These variables manifest neatly under __Administrative Templates → Samba__ inside the policy editor once you ingest Samba’s ADMX files via `samba-tool gpo admxload`.

What we must not sugarcoat: if your job requires managing production Windows clients seriously—mapping network letter drives, orchestrating logon scripts, deploying heavy registry templates, or pushing restricted security groups—the only practical route remains utilizing the \*\*Group Policy Management Console (GPMC)\*\* via \*\*RSAT\*\* on a domain-joined Windows workstation. This isn’t a directory-level constraint (Samba’s AD store saves, parses, and distributes these policies perfectly); it’s simply that the visual tooling required to author complex Windows policies is designed by Microsoft. There are third-party web tools available, but for an honest SMB infrastructure, the recipe is straightforward: use a temporary Windows VM running RSAT for editing, and rely on Samba for secure storage, distribution, and policy application.

A couple of useful terminal utilities to keep handy for audit purposes:

```php
sudo samba-tool gpo listall          # Lists the GUID and display name of every domain GPO
sudo samba-tool gpo aclcheck         # Verifies that LDAP and Directory Service ACL permissions match
```

And a golden rule that becomes transparent in the next section: \*\*always author your GPOs pointing to a single DC—specifically the one holding the PDC Emulator role.\*\* The reason for this is your SysVol directory.

---

## 3. The Second DC: High Availability and the SysVol Hole

An infrastructure architecture reliant on a single Domain Controller is not “enterprise-grade”; it is simply a single point of failure with good PR. A secondary DC is added by joining the active forest, never by provisioning a clean domain from scratch.

### Joining the DC2

On your secondary machine, configure its primary DNS target to point to the active IP of `DC1` during the join procedure:

```
sudo samba-tool domain join ad.company.com.ar DC \
     -U administrator --dns-backend=SAMBA_INTERNAL
sudo systemctl unmask samba-ad-dc
sudo systemctl enable --now samba-ad-dc
```

Once the join completes, each DC runs its own internal DNS server and resolves locally. Your client machines must be configured to list both DCs as their primary and secondary DNS targets so that if one controller experiences a hardware fault, the clients do not lose name resolution. Keeping clocks closely synchronized between DCs is just as critical as it is for network clients: if time drift swings beyond 5 minutes in any direction, replication topology breaks and machine accounts will fail. Ensure `DC2` synchronizes against `DC1` or shares the same external NTP pool.

The core directory database layer (users, computers, and GPOs stored as LDAP entries) replicates automatically across your network via the standard DRS protocol. You can monitor this engine directly:

```php
sudo samba-tool drs showrepl
sudo samba-tool drs replicate dc2 dc1 dc=ad,dc=company,dc=com,dc=ar
sudo samba-tool fsmo show        # Displays which node currently holds your active FSMO roles
```

### The Architecture Gap Nobody Admits: SysVol Does Not Replicate Privately

This is the real current boundary of Samba as an Active Directory platform, and glossing over it is dishonest. Samba does not yet provide built-in replication for the `SysVol` directory; until that feature lands natively, you must deploy an external workaround to keep things synchronized. The `SysVol` directory (located at `/var/lib/samba/sysvol`) is the physical path where GPO files, policy layouts, and logon scripts reside: if you fail to replicate it, `DC2` will distribute stale, outdated, or entirely blank client policies.

The standard and most reliable workaround is a \*\*unidirectional rsync configuration\*\*. This introduces an explicit design requirement: you choose one master DC where all structural policy edits and logon adjustments are made, and your remaining DCs pull those changes down. Any local modification made on a secondary DC will be instantly overwritten during the next synchronization pass. The optimal candidate for your master DC is whichever node holds the \*\*PDC Emulator\*\* role, which is also the exact target the Windows GPMC console hooks into by default. This underpins our golden rule from the section above.

Two precise terminal details make the entire difference between a healthy system and completely broken client GPOs:

```php
# Executed on DC2, pulling data down from your master node (DC1 = PDC Emulator)
rsync -XAavz --delete-after root@dc1:/var/lib/samba/sysvol/ /var/lib/samba/sysvol/
sudo samba-tool ntacl sysvolreset
```

The `-X` and `-A` flags are mandatory: they preserve extended attributes and POSIX ACLs, without which your target SysVol will end up with corrupted file permissions. Running `samba-tool ntacl sysvolreset` immediately following each sync pass recalibrates the security attributes across the SysVol tree to match the exact SIDs the Active Directory environment expects to see. If your workflow strictly demands editing capabilities from any DC simultaneously, more complex bidirectional engines like `osync` or `unison` exist; however, for a standard, dependable SMB environment, a single-master layout is significantly cleaner and easier to maintain.

One final, silent prerequisites check: all Domain Controllers must use identical ID mapping configurations for internal built-in groups and users. Therefore, when provisioning `DC2`, you must verify the absolute consistency of your `idmap.ldb` files for these core accounts. If your built-in group local IDs diverge between your DCs, your replicated SysVol ACLs will end up pointing to entirely different local entities, breaking your domain’s security integrity.

---

## Conclusion

Part 1 proved that an open-source Active Directory environment can be deployed reliably if you respect role isolation and cryptographic time requirements. Part 2 showcases the actual infrastructure legwork that basic online tutorials systematically avoid: your business data lives on a Member Server utilizing native Active Directory ACL descriptors—not hidden behind superficial POSIX bits; GPOs are active and can be increasingly managed via Linux command lines, but heavy Windows endpoint authoring still benefits from RSAT, and knowing this prevents broken deployment promises; and multi-DC high availability is entirely real for your directory database, but your SysVol structure requires an intentional, single-master `rsync` routine engineered to last.

None of these technical requirements disqualify Samba: instead, they solidify it as an honest, enterprise-grade alternative with well-documented operational boundaries. Which happens to be the exact opposite of a basic demo that only managed to run on a Friday afternoon.

> __A note on sources:__ These core engineering paths are cross-referenced directly against official upstream Samba Wiki documentation (specifically multi-DC SysVol replication workarounds and Group Policy deployment architectures), `samba-tool gpo` development manuals, and multi-DC production scaling reference layouts. The mapped idmap allocations, group definitions (e.g., `COMPANY\\sales`), and structural paths used throughout this article are purely illustrative: adapt and audit them within your isolated lab environments before moving to your production network.
