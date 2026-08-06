---
title: How to Tame the Brother 161xNW Over the Network Without Losing Your Mind
slug: how-to-tame-the-brother-161xnw-over-the-network-without-losing-your-mind
status: published
legacy_url: https://dagorret.com.ar/how-to-tame-the-brother-161xnw-over-the-network-without-losing-your-mind/
wordpress_id: 1296
published_at: '2026-06-03T08:56:00'
modified_at: '2026-07-10T09:01:27'
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

Keywords: Arch, Brother, CachyOS, dcp-1617nw

### The Definitive Arch Linux/CachyOS Guide

Some hardware feels like it was designed to test the patience of Linux users.

The Brother DCP-1610NW —and its close relatives in the 161x family— fits perfectly into that category. It is a monochrome laser multifunction printer: cheap to run, physically tough, reliable, and clearly built more like a small office tank than a delicate modern gadget.

The problem is not the printer.

The problem is making it work cleanly on Arch Linux or CachyOS over the network, especially when we want both sides of the device to behave properly:

the printer  
and the scanner.

The traditional instinct is to go straight to Brother’s official Linux drivers, hunt for old `.deb` or `.rpm` packages, look for AUR wrappers, and start installing model-specific packages until something works.

That path exists.

But on my system, it was not the right first move.

The cleaner solution was this:

__CUPS + brlaser for printing.__  
__SANE + sane-airscan + Skanlite for scanning.__

No driver archaeology as the first step.  
No old Brother wrapper as the default path.  
No unnecessary proprietary stack unless the clean Linux stack fails.

## The baseline: what was already installed

Before touching anything, I audited the system.

That matters, because a good Linux tutorial should not begin by blindly installing random packages. It should first ask a simpler question:

__What does the system already have?__

On this CachyOS machine, the important pieces were already present:

```
cups
cups-filters
cups-pdf
libcups
libcupsfilters
python-pycups
system-config-printer
sane
sane-airscan
ksanecore
libksane
skanlite
brlaser
```

And CUPS was not only installed. It was already enabled and running:

```css
cups.service: enabled
cups.service: active
```

That changes the whole diagnosis.

This was not a broken printing system.  
This was a system that already had the correct foundation.

The important missing conclusion was not “install everything from Brother.”

The important conclusion was:

__do not overcomplicate what the system can already solve natively.__

## Part 1: Printing — brlaser saved the day

Printing on Linux revolves around CUPS.

CUPS manages printers, queues, jobs, filters, and communication with the device. On Arch Linux and CachyOS, the service is controlled through systemd:

```css
sudo systemctl enable --now cups.service
```

In my case, this was already done. So the command becomes less of an installation step and more of a verification point:

```css
systemctl is-enabled cups.service
systemctl is-active cups.service
```

The real hero for printing was not Brother’s old driver package.

It was:

```
brlaser
```

`brlaser` is a free driver for Brother laser printers. And in this case, it did exactly what a good driver should do: it made the printer usable through CUPS without dragging in unnecessary legacy packaging.

This is the key point of the article:

__Do not start by installing `brother-dcp1610w`. Start with CUPS and brlaser.__

Yes, the AUR contains a package called:

```
brother-dcp1610w
```

And yes, it is described as an LPR and CUPS driver for the Brother DCP-1610W and DCP-1612W printers.

But that does not mean it should be the first recommendation.

If `brlaser` works, it is the cleaner solution.

It avoids the older Brother packaging model.  
It avoids unnecessary AUR dependency on a model-specific wrapper.  
It keeps the printing stack closer to the standard Linux ecosystem.  
And most importantly: it works.

In this setup, `brlaser` saved the day.

## Recommended printing stack

For a clean Arch/CachyOS setup, the printing side should look like this:

```css
sudo pacman -S cups cups-filters system-config-printer brlaser
sudo systemctl enable --now cups.service
```

Then verify:

```css
systemctl is-enabled cups.service
systemctl is-active cups.service
```

Expected result:

```
enabled
active
```

After that, add the printer from KDE Plasma:

```
System Settings → Printers
```

If the Brother appears automatically, use it.  
If not, add it manually by network address.

A network printer should have a stable IP address. Either assign a static IP from the printer/router or create a DHCP reservation for the printer’s MAC address.

For example:

```css
192.168.1.X
```

Do not let a printer depend on a random DHCP lease if you care about reliability.

Once the printer is added, choose the Brother laser driver provided by `brlaser`, print a test page, and stop there if it works.

Do not install extra Brother packages just because they exist.

## Part 2: The scanner — do not rush into brscan4

The scanner side is where many users lose patience.

They install the printer, open Skanlite or another scanning app, and expect the scanner to appear immediately.

If it does not, the traditional reaction is to install Brother’s `brscan4` driver from the AUR.

But that should not be the first step anymore.

On this system, the modern scanning stack was already installed:

```
sane
sane-airscan
skanlite
ksanecore
libksane
```

That matters.

`SANE` is the scanner framework.  
`sane-airscan` provides support for modern network scanning protocols such as eSCL/AirScan and WSD.  
`Skanlite` is the KDE scanning application.

So the clean strategy is:

__First test the modern SANE/AirScan path. Only consider `brscan4` if that fails.__

That is the same philosophy as the printing side:

do not start with the vendor legacy driver  
when the open Linux stack may already solve the problem.

## Recommended scanning stack

For the scanner side, the clean package set is:

```
sudo pacman -S sane sane-airscan skanlite
```

On my system, these were already installed.

To verify whether the scanner is visible to SANE, run:

```
scanimage -L
```

If the scanner is detected, you should see an output line showing a recognized device.

The exact text may vary, but the important thing is that SANE returns a scanner device instead of an empty result.

You can also discover network scanners with:

```
airscan-discover
```

If `airscan-discover` sees the Brother, the system is already detecting it through the modern network scanning path.

At that point, open:

```
Skanlite
```

and scan from KDE.

## Why this order matters

The order is the whole point.

Bad order:

Install random Brother AUR packages.
Try old wrappers.
Hope something works.
Debug later.

Good order:

Check what is already installed.
Verify CUPS.
Use brlaser for printing.
Verify SANE.
Use sane-airscan for network scanning.
Only then consider Brother-specific packages if needed.

This is the difference between administering a system and throwing packages at a problem.

The printer should not force us to abandon the clean Linux stack immediately.  
The scanner should not force us into `brscan4` before we even test AirScan.  
The AUR should be a tool, not a reflex.

## What about brother-dcp1610w?

The AUR package `brother-dcp1610w` exists.

It may be useful in systems where `brlaser` does not work correctly, where the model does not appear in CUPS, or where printing fails with the open driver.

But for this setup, it is not the recommended first path.

So the article’s position is:

Do not start with brother-dcp1610w.
Start with brlaser.
Use brother-dcp1610w only as a fallback.

Fallback command:

```
paru -S brother-dcp1610w
```

Again: fallback, not first move.

## What about brscan4?

The same logic applies to `brscan4`.

The AUR package exists. It provides Brother’s SANE backend for compatible models. It can be useful when the scanner does not work through the modern SANE/AirScan stack.

But if `sane-airscan` detects the device, `brscan4` is unnecessary.

So the article’s position is:

Do not start with brscan4.
Start with sane-airscan.
Use brscan4 only if AirScan/eSCL discovery fails.

Fallback command:

```
paru -S brscan4
```

And only if needed, register the scanner manually by IP:

```
sudo brsaneconfig4 -a name=Brother_Carlos model=DCP-1610W ip=192.168.1.X
```

But this is not the clean first route.

It is the fallback route.

## The real troubleshooting checklist

For printing:

```css
systemctl is-enabled cups.service
systemctl is-active cups.service
```

Expected:

```
enabled
active
```

Check installed printing packages:

```
pacman -Qs cups brlaser system-config-printer
```

Then configure the printer from KDE Plasma:

```
System Settings → Printers
```

For scanning:

```
pacman -Qs sane sane-airscan skanlite
scanimage -L
airscan-discover
```

If SANE sees the scanner, use Skanlite.

If it does not, then —and only then— investigate `brscan4`.

## The bigger lesson

This Brother 161xNW setup is not just about one printer.

It is a reminder of a broader Linux principle:

__Do not confuse vendor support with the best support.__

Sometimes the manufacturer’s driver is necessary.  
Sometimes the AUR package is the right answer.  
Sometimes the old wrapper is the only thing that works.

But not always.

In this case, the clean system stack was already strong:

CUPS was running.  
`brlaser` handled printing.  
SANE was installed.  
`sane-airscan` was available.  
Skanlite was ready.

The right move was not to add more complexity.

The right move was to trust the native stack first.

## Conclusion

The Brother 161xNW is a tank.

But like many tanks, it does not always move gracefully through narrow Linux streets.

The trick is not to panic and install every Brother package you can find.

On Arch Linux and CachyOS, the clean path is:

CUPS for printing.
brlaser as the free Brother laser driver.
system-config-printer or KDE Plasma to add the printer.
SANE for scanning.
sane-airscan for network scanner discovery.
Skanlite as the KDE scanning interface.

Only if that fails should you reach for:

```
brother-dcp1610w
brscan4
```

That distinction matters.

Because the best Linux setup is not the one with the most vendor packages installed.

It is the one with the fewest moving parts that still works.

In this case, `brlaser` saved the printing side.  
And the scanner should first be tested through the modern SANE/AirScan stack before falling back to Brother’s legacy tools.

Less driver archaeology.  
More clean system administration.

That is how you tame the Brother 161xNW on CachyOS without losing your mind.
