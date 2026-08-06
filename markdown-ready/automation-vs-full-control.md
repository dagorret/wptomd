---
title: Automation vs. Full Control
slug: automation-vs-full-control
status: published
legacy_url: https://dagorret.com.ar/automation-vs-full-control/
wordpress_id: 1301
published_at: '2026-05-26T09:01:27'
modified_at: '2026-05-26T09:01:27'
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

Keywords: Arch, Backup, KDE, Kup, rsync

### Demystifying Backups in KDE Plasma: Kup vs. rsync

Yesterday, we talked about a simple but fundamental idea: a backup should not be a complex ceremony, but a reproducible habit. In  ___“[Backups with rclone: Synchronizing Without Making Life Complicated](/backups-with-rclone-synchronizing-without-making-life-complicated/)”___ , the focus was on synchronizing a work environment to the cloud using `rclone`, excluding what is disposable and preserving what actually matters.

Today, the scenario changes.

We are no longer talking about the cloud.  
We are talking about external drives.  
About laptops.  
About KDE Plasma.  
About automation.  
About control.  
And, above all, about predictability.

Because when a backup depends on a USB drive, a critical question appears:

__Who is really in control of the process: the graphical environment or us?__

## The appeal of automation

KDE Plasma offers a modern, comfortable, and deeply integrated desktop experience. Within that ecosystem, Kup appears as an attractive tool for managing backups through a graphical interface.

The promise is clear: connect an external drive, let the system detect it, and allow the backup to run automatically.

For an average user, that is ideal.

No commands to remember.  
No terminal to open.  
No need to think too much.  
The backup simply happens.

And, in principle, that is a good thing.

The problem appears when we stop looking at backups as a convenience and start looking at them as a critical procedure.

At that point, the question changes.

It is no longer enough to know that “something is being copied.”  
We want to know what is being copied, when it is being copied, where it is being copied to, under what conditions it is triggered, and which real process is doing the work.

In other words: we need to audit the automation.

## The scientific audit of Kup

One of the most interesting ways to understand a graphical tool is to observe what it does underneath.

From the interface, Kup looks like an autonomous backup system. It has assistants, profiles, destinations, rules, and notifications. But when inspected more closely, an important technical truth appears:

__Kup does not reinvent backups: it acts as an elegant intermediary on top of classic system tools.__

Through process inspection and behavioral observation via DBus, it is possible to verify that Kup ultimately executes operations supported by tools already well known in the Unix world, especially `rsync`.

This does not take away from its value. On the contrary: it is a good design decision. `rsync` is robust, proven, efficient, and widely understood by system administrators.

But it changes the way we should interpret Kup.

Kup is not magic.  
It is not an unavoidable black box.  
It is not a mysterious synchronization engine.

It is a graphical layer that organizes triggers, profiles, and conditions to execute backup logic that, underneath, remains recognizable to any advanced Linux user.

And that conclusion is liberating.

Because if there is `rsync` underneath, then we can compare, audit, replicate, and, if necessary, replace it.

## The problem is not rsync: it is the triggers

When people talk about automatic backups, attention is often placed on the copying tool. But in this case, the most delicate point is not `rsync`.

The delicate point is the trigger.

Kup can be conditioned by events from the graphical environment and the hardware: drive connection, destination availability, mount paths, volume identification, and internal timers.

That enables a comfortable experience, but it also introduces a layer of indeterminism.

For example: we connect the external drive and expect the backup to run. But between the physical connection and the actual backup execution, several pieces are involved:

The system detects the device.  
The graphical environment mounts it.  
The mount point is assigned.  
Kup recognizes that the destination is available.  
The profile is activated.  
The backup is scheduled or executed according to its rules.

In practice, this may mean that the backup does not start exactly at the moment we connect the drive, but after a certain delay. For example, a few minutes later.

That is not necessarily bad. In fact, it may be desirable to avoid premature execution while the device is still initializing.

But from an administrator’s perspective, it introduces an uncomfortable question:

__Am I looking at a guarantee, or am I trusting a chain of assumptions?__

## The danger of indeterminism

Indeterminism in backups does not always appear as an obvious error. Sometimes it is more subtle.

It does not fail every day.  
It does not always fail.  
It does not fail loudly.  
It fails exactly when we needed it not to.

One of the weakest points is the identification of the external drive.

Many graphical environments mount devices using human-readable names: the volume label, the drive name, or a generated path under `/run/media/user/DRIVE_NAME`.

That is convenient for humans, but it is not always ideal for critical scripts.

Why?

Because names can be repeated.  
Labels can change.  
Paths can vary.  
Mounting may depend on the active user.  
The graphical environment may behave differently depending on the session.  
Two drives may have similar names.  
A minor change can break a path that seemed stable.

When a backup depends on a textual path, we are trusting a convenient abstraction, not the real identity of the hardware.

For ordinary tasks, that may be enough.

For critical backups, it is not.

## Hardening the backup with UUIDs

The pragmatic way to reduce that uncertainty is to identify the drive by its UUID.

The UUID does not describe what the drive is called from the user’s perspective. It describes a more stable identity of the filesystem or partition.

Instead of saying:

```
/run/media/carlos/BackupDisk
```

we can build a strategy based on:

```
/dev/disk/by-uuid/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

Or we can use the UUID as a precondition before executing any synchronization.

The idea is simple: the script should not ask, “Is something called BackupDisk mounted?” It should ask:

__Is the exact device I authorize as a backup destination present?__

That completely changes the operational safety of the process.

A script hardened by UUID can verify the device, mount the destination if necessary, validate the final path, and only then execute `rsync`.

This way, the backup stops depending on a visual assumption and starts depending on a concrete identity.

## Kup as convenience, rsync as contract

After auditing Kup, the conclusion should not necessarily be to abandon it.

The more interesting conclusion is to understand what role it plays.

Kup is excellent as an automation layer for an everyday workflow. If I connect the external drive and want the system, after a few minutes, to do its job without asking me anything, Kup is convenient.

But `rsync` remains the technical contract.

It is the tool I can read.  
I can execute it.  
I can log it.  
I can test it with `--dry-run`.  
I can version it inside a script.  
I can adapt it per laptop.  
I can isolate it by date.  
I can review it line by line.

Kup offers automation.  
`rsync` offers control.

And there is no need to choose only one side.

## The definitive hybrid strategy

The best solution is not always to replace one tool with another. Sometimes, it is to make them coexist.

In this case, the hybrid strategy makes a lot of sense:

__Kup remains running in the background for systematic backups.__  
When we connect the USB drive, KDE Plasma detects it, Kup recognizes the destination, and after a short delay, it automatically runs the backup.

That workflow is ideal for routine use.

Connect the drive.  
Keep working.  
The backup happens.  
Receive a notification.  
No need to open a terminal every time.

But alongside that, there is a second path:

__A manual and independent terminal script.__

This script does not depend on the graphical interface, does not depend on the visible name of the drive, and does not depend on weak assumptions. It can identify the destination by UUID, create a structure per laptop, and freeze time using dates.

For example, each manual execution could save the backup using this structure:

```
Backup_${NOTEBOOK}/2026-06-01/
```

This way, the backup is not only a current copy. It also becomes a temporal snapshot of a machine’s state.

This is especially useful when working with multiple laptops or when we want to preserve a point before a major update, a system migration, a reinstall, or an environment change.

## Automation for routine, control for critical moments

The key to this strategy is separating use cases.

For day-to-day work, automation.

Kup can take care of maintaining a systematic, transparent, and comfortable copy. We do not need to turn every routine backup into a solemn manual operation.

But for important moments, full control.

Before reinstalling.  
Before changing distributions.  
Before touching partitions.  
Before updating critical components.  
Before traveling.  
Before handing over a machine.  
Before experimenting.

That is when it makes sense to run the manual script, verify the UUID, review the destination, and freeze the state by date.

The combination is powerful because it covers two different needs:

Kup reduces friction.  
The script reduces uncertainty.

## The value of being able to audit

A backup that cannot be audited is a promise.

And promises do not restore files.

Being able to audit means knowing which tool was executed, which paths it used, which files it excluded, which destination received the data, and under which drive identity it worked.

It means being able to answer specific questions:

Did this backup go to the correct drive?  
Did it run today?  
Did it copy this laptop or another one?  
Did it overwrite previous files?  
Did it create a date-based copy?  
Did it fail because of permissions?  
Did it depend on a graphical session?  
Can I repeat the process from a terminal?

When we use graphical tools, these questions often remain hidden behind buttons and notifications. When we use scripts, they are exposed in plain text.

And in system administration, plain text is still a form of power.

## This is not about distrusting KDE

None of this means KDE Plasma or Kup are bad tools.

On the contrary.

Automation well integrated into the desktop is valuable. For many users, it is the difference between having a backup and having nothing.

But an advanced user should not settle for something that “seems to work.” They should be able to understand the mechanism, audit it, and build an independent alternative.

The point is not to reject the graphical environment.

The point is not to depend exclusively on it.

KDE can simplify the routine.  
Kup can automate the trigger.  
`rsync` can execute the real logic.  
The UUID can harden the identity of the destination.  
The manual script can provide absolute control when it matters.

Each piece has a role.

## Conclusion

The discussion between Kup and `rsync` should not be framed as a war between graphical interface and terminal.

It is a discussion between automation and control.

Kup is comfortable, integrated, and sufficient for many everyday scenarios. But when we need absolute predictability over external drives, it is worth looking beneath the interface and understanding what is actually happening.

The audit shows that there is no magic: there are triggers, processes, mount paths, and classic tools doing the real work.

And once we understand that, we can design a better strategy.

Automate the repetitive.  
Audit what matters.  
Identify drives by UUID.  
Separate laptops.  
Freeze backups by date.  
Keep an independent manual path.

The ideal backup is not necessarily the most automatic one or the most handcrafted one.

It is the one that combines convenience with verifiability.

Because when the day comes to restore, it will not matter how elegant the interface was.  
Only one thing will matter:

that the data is there, on the correct drive, on the correct date, and that we can trust it.
