---
title: The RAM Myth (And Why I Stopped Watching the Resource Monitor)
slug: the-ram-myth-and-why-i-stopped-watching-the-resource-monitor
status: published
legacy_url: https://dagorret.com.ar/the-ram-myth-and-why-i-stopped-watching-the-resource-monitor/
wordpress_id: 1272
published_at: '2026-06-27T12:11:58'
modified_at: '2026-06-27T12:11:58'
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

__Keywords__: Productivity, Reproducibility, Sysadmin

Every now and then, the same image pops up on my timeline: one Linux distribution pitted against another, compared solely by how many megabytes of RAM they consume at idle. Ubuntu allegedly starts at 6 GB, Arch at 512 MB, followed by a hundred comments debating it as if everything was at stake. I looked at those charts for years. Over time, I learned that almost all of that debate is just noise.

​It is not that RAM never matters—it matters when it matters, and we will get to that—but measuring an operating system by its idle consumption is like measuring a car by how much fuel it burns while turned off in the garage. When you actually work with this stuff, productivity isn’t measured there. It is measured in something else: how much control you have over your environment, how much of what you do today can be repeated tomorrow without rethinking it, and how much pragmatism you inject into your decisions.

​This is, more than anything, a testimony. It is what years of fighting with servers and workflows have made crystal clear to me.

## ​1. The Distro Doesn’t Matter (And That’s a Good Thing)

​Let’s be blunt: the distribution you choose, in the end, doesn’t matter. Whether a system spends one or two gigabytes more or less of base memory is almost irrelevant because under the hood, they all do the exact same thing. The same kernel, the same tools, the same processes.

​What changes is the number of steps you are willing to walk to get to the same place. If you install Ubuntu, you might start at 800 MB at idle; a snap here, a background service there. If you go with Debian or Arch, you start at 120 MB or so. The real difference between those two numbers? Convenience versus control, nothing more.

​And both options are entirely legitimate. If you want something to work right NOW, you pull up the Nextcloud instance that comes ready out of the box in Ubuntu—one command, and it runs. Zero friction. But if you are looking for raw power and surgical efficiency, you go to Debian or Arch, set up what you need by hand—an Nginx server, a PHP setup for a couple of email accounts—and leave the entire system breathing easily at 512 MB. One isn’t inherently better than the other; each simply charges you the toll in a different currency. One charges you in hardware resources; the other, in your own time.

## ​2. Real Production, Not Empty Desktop Screenshots

​Performance isn’t proven with a neofetch screenshot on a freshly installed, empty desktop. It is proven under fire, on the server, with real people using it. And that is where these numbers actually start to mean something.

​I run PHP servers processing thousands of operations per minute. In calm periods, they sit at a comfortable, quiet 2.3 GB of RAM. The moment of truth is quite different: during a massive simultaneous exam in Moodle—which is one of the heaviest tasks you can ask from a database and a web server at the same time—the consumption barely touches 8 GB. It doesn’t crash, it doesn’t drag. It holds up.

​On the other extreme, I have my personal server: the website, the mail server, and Nginx all running on just 123 MB of RAM. Not only does it stay alive, but it also hosts an Emacs instance in server mode, allowing me to log in via terminal, spin up the client, and read my email directly from there. The exact same operating system scales from that absolute misery of memory up to a massive simultaneous exam without changing its core philosophy. I don’t know many other things that can make that journey without breaking a sweat.

## ​3. The Day I Had to Clean 15,000 Documents

​Not long ago, I faced a task that would have been an absolute clicking torture in any other system: cleaning a document database of 15,000 Word files. Doing that by hand, or using graphical tools, is an invitation to disaster; you either die of old age or the machine freezes halfway through.

​In Linux, the problem is solved from a different angle: reproducible automation and a bit of well-directed brute force. The concept is simple. If the compressed archive yields the same hash, the cleaning recipe applies equally to everything. And if something fails, I don’t redo all 15,000 files: I generate a hash per directory, mathematically isolate the blocks that don’t match, and redo only those. The rest remains untouched.

​The workflow ended up being a pipeline of scripts that convert those heavy .docx files into Markdown, unify them into a single clean block, and upload them to Google Drive. Why go through all that trouble? To ensure that when I feed that material into an AI tool—like NotebookLM or Claude—the source data is pure, structured, and free of the syntactic garbage that Word injects everywhere. The beautiful thing isn’t just that I solved it that afternoon. The beautiful thing is that it became reproducible: what took me a while to think through today can be executed tomorrow in a single second with one command.

## ​4. My Desktop, No Magic Tricks Included

​To get real work done, you don’t need an experimental kernel with a magical scheduler that prioritizes the window in front of your face. That is great for gaming. For development, you need something else: a predictable, mature environment that behaves exactly the same way today as it will next week. When your day consists of compiling in the background, querying the database, and writing code all at the same time, predictability is worth more than any optimization trick.

​My machine runs CachyOS with KDE Plasma. At idle, it hovers around 2 GB—completely normal for a modern desktop environment—and when I really push it, it climbs to 8 or 9.5 GB max. My mind operates in three distinct states, and I have a specific tool for each one:

- ​__The Terminal (Kitty + Vim):__ For the fine-grained work, the line-by-line coding, quick Postgres queries, running a script, and moving on.
- ​__Emacs:__ My control center for notes, documentation, and above all, organizing my thoughts.
- ​__PyCharm:__ For when the project scales up and I need to see the full code map, heavy refactoring, and the debugger.

​Here is the point that almost no one mentions in those Twitter threads: if the consumption goes up, it doesn’t go up “because of Linux.” It goes up because Firefox has ten heavy tabs open, because PyCharm is built on Java and eats its fair share, and because there are Docker containers spinning in the background. The system, beneath all of that, responds instantly. The memory is spent by the tools I chose to use, and I spend it on purpose.

## ​The End of the Day

​When the workday ends, I shut down the containers, see that the workflow did exactly what it was supposed to do, and watch all of that history immortalized in a script pushed to the repo… that feeling is priceless. It is knowing that you built a tool customized to your exact needs, and that tomorrow it remains entirely yours.

​I have nothing against other systems. If what you want is status, or a closed Unix system that simply works so you can open it in a coffee shop, a Mac is a perfectly reasonable decision: you pay for it, and you enjoy it. Windows also has its place for everyday casual use. It is not a matter of picking teams. It is something else: I choose Linux because almost everything I do is executed under my own rules, knowing exactly what is happening under the hood, with the absolute certainty that the environment belongs to me. I don’t use the system to stare at loading screens or to argue about gigabytes on a Twitter image. I use it because, in the end, what matters most to me isn’t how much RAM I save. It’s being the owner of my own work.
