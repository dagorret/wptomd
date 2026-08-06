---
title: 'Slackware: the immutable rock (1993)'
slug: from-rock-to-river-the-evolution-of-simplicity-in-linux
status: published
legacy_url: https://dagorret.com.ar/from-rock-to-river-the-evolution-of-simplicity-in-linux/
wordpress_id: 1274
published_at: '2026-06-24T10:02:11'
modified_at: '2026-06-24T10:02:11'
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

Keywords: Arch History, Philosophy, Software,Slackware

In the history of free software, simplicity has always worked as a kind of talisman-word: everyone invokes it, almost no one means the same thing by it. Two projects make this clearer than any manifesto. Slackware and Arch Linux share the same slogan —KISS, Keep It Simple, Stupid— and out of it they built two systems that are nearly opposite. One read simplicity as a rock; the other, as a river. This is the story of that fork, and of why the same word can push you toward such different places.

# Slackware: the immutable rock (1993)

In the early nineties, putting together a Linux system was an artisanal task and, often, a nightmare. In July 1993, a student named Patrick Volkerding set out to do something modest: clean up and fix the scripts of SLS (Softlanding Linux System), the distribution he was using, so he could rely on it in his classes. The result came out so polished that, when he mentioned it, others asked him to share it. He put it online and called it Slackware.

Slackware’s philosophy is not simplicity of use, but simplicity of design. The base system ships with minimal patching, as close as possible to what each original author released: Volkerding avoids cosmetic modifications and distribution-specific patches, so that what runs on your machine looks a lot like what upstream actually published. That fidelity is at once a cost and a virtue: it forces you to understand the software as it is, with no layer of invisible “fixes” in between.

The other pillar is package management. In Slackware, packages are simple compressed archives, and there is no automatic dependency resolution. If a program needs a library, the administrator finds it and installs it by hand. To the modern eye this sounds like masochism; in truth it is an epistemic decision. The knowledge of what the system needs lives in the head of whoever administers it, rather than being delegated to an algorithm. Slackware is also the oldest surviving distribution still standing —it predates even the announcement of Debian, from August 1993. A predictable, tough, long-lived tank that, in return, asks you to know exactly what you are doing.

# Arch Linux: the continuous river (2002)

Nearly a decade later, in March 2002, a Canadian programmer named Judd Vinet released the first version of Arch Linux. His starting point was a twofold dissatisfaction. He liked the cleanliness of distributions like Slackware and their plain-text configuration files, but he did not want to compile and resolve dependencies by hand. On the other side, systems like Debian resolved dependencies at the price of a certain heaviness and a number of hidden automatisms that felt alien to him.

The piece usually missing from this story is CRUX. Before writing a single line of Arch, Vinet drew directly on CRUX, Per Liden’s minimalist distribution, and on its BSD-style ports approach to building packages. Much of Arch’s DNA comes from there: the idea of describing how a package is built in a declarative, readable script —what would later become the PKGBUILD and the Arch Build System— descends from that lineage, not from Slackware. If Slackware is Arch’s aesthetic grandfather, CRUX is its technical father.

On top of that foundation, Vinet added his own contribution. He wrote Pacman, a package manager written in C, fast, operating on simple packages but resolving dependencies in milliseconds: the convenience of Debian without its opacity. He also kept the blank-canvas idea. Arch hands you nothing precooked; after installation you face a terminal and build the system piece by piece. It is simple, yes —but for whoever assembles it, not for whoever uses it.

And it adopted the rolling release model. It is worth being honest about the genealogy here: Arch did not invent continuous releasing —Gentoo is contemporary, and the idea was already circulating— but it made it canonical. Instead of new versions every six months, Arch offers a single stream: you install once and update forever. This is a promise more than a mechanical guarantee, because rolling demands that, every so often, you read the project’s news and get your hands dirty with a manual intervention. But the ideal —a system that never expires because it never “freezes”— became attached to Arch for good.

# The verdict: two simplicities

What is interesting is not deciding which one is better, but seeing that both start from the same commandment and arrive at opposite systems. Slackware’s simplicity is one of design and prediction: few moving parts, little patching, no magic; control is manual and absolute. Arch’s simplicity is one of implementation: nothing superfluous in the system, but a modern engine —Pacman— that automates the tedious without hiding the essential.

Scratch a little and the real difference is not “manual versus automatic.” It is a question about where the system’s knowledge lives. In Slackware, that knowledge lives in the administrator’s head: resolving dependencies by hand is epistemic transparency paid for with labor. In Arch, part of it is delegated to Pacman, but the construction —what you install, what you leave out, how the whole thing ends up assembled— remains yours. Both distributions are, at bottom, different bets about what you are willing to delegate and how much understanding you accept losing when you delegate it.

Slackware was born to be a rock: classic, stable, free of surprises. Arch took that same obsession with control and minimalism and injected an engine able to keep pace with the internet. But perhaps the question they leave open is not which of the two is simpler, but another, more uncomfortable one: every time a tool saves us work, what portion of understanding are we handing over in exchange? The rock and the river do not answer the same way. And maybe that is why, more than thirty years later, both are still alive.
