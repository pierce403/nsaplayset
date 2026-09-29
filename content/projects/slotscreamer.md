+++
title = "SLOTSCREAMER"
description = "An open hardware and software framework for exploring PCIe direct memory access."
path = "slotscreamer"
weight = 2
[extra]
cover = "/images/archive/projects/slotscreamer-pcie-board.png"
cover_width = 736
cover_height = 1024
cover_alt = "A green PCI Express adapter board carrying the blue SLOTSCREAMER module."
number = "02"
category = "Physical Domination"
interface = "PCIe"
code = "DMA"
year = "2014"
credits = "Joe Fitz"
[[extra.sources]]
label = "Original author\u2019s project overview"
url = "https://securinghardware.com/articles/SLOTSCREAMER/"
[[extra.sources]]
label = "Source and documentation"
url = "https://github.com/NSAPlayset/SLOTSCREAMER"

[[extra.gallery]]
path = "/images/archive/projects/slotscreamer-pcie-board.png"
width = 736
height = 1024
alt = "A green PCI Express adapter board carrying the blue SLOTSCREAMER module."
caption = "The PCIe board shown in the original DEF CON 22 presentation."
credit = "Source presentation: Joe FitzPatrick and Miles Crabill, DEF CON 22 (2014)."
source = "https://raw.githubusercontent.com/NSAPlayset/SLOTSCREAMER/master/Stupid%20PCIe%20Tricks%2C%20featuring%20the%20NSA%20Playset-%20PCIe.pdf"
page = 47
+++

## Overview

Presented at DEF CON 22, SLOTSCREAMER demonstrates memory and I/O access through PCIe. Its original author describes the behavior as a consequence of the interface design, rather than a zero-day exploit.

## Working with the original project

The author’s repository holds the implementation and documentation. Modern DMA protections and platform configuration can change applicability.
