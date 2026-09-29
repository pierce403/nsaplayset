# Project resources

Checked 2026-09-29. [resources.json](resources.json) records 43 resource destinations and their project mappings, primary-source evidence, and verification results. Project pages group them under Videos, Code & schematics, Components, and Training. General conference introductions appear on About.

SLOTSCREAMER, HALIBUTDUGOUT, and ALLOYVIPER already have catalog entries. Each now links the original DEF CON PCIe talk and Securing Hardware's x86 training outline, which covers PCIe memory access and adapting interfaces. This is related training; no current class date or enrollment availability is implied. The JTAG workshop is linked from SAVIORBURST.

## Verification

- Video titles and channels were checked through YouTube metadata, or Internet Archive metadata and matching recording files. Conference schedules or author pages establish attribution and relevance. Full playback was not tested.
- GitHub repositories returned HTTP 200. Repository metadata and file trees establish source, firmware, schematics, PCB, and Gerber availability; checked tree IDs are recorded. Links follow upstream default branches.
- Merchant pages returned HTTP 200 and were matched to original parts lists or project documentation. Brief notes identify discontinued stock, clones, and later hardware revisions. No purchase or compatibility testing was performed.
- Securing Hardware course pages returned HTTP 200 and their outlines were checked for relevance. No enrollment was performed.
- The build checks that every recorded resource appears in the intended page's frontmatter and generated HTML, under the expected group.

The old site's BLINKERCOUGH GitHub username omitted an `i`; the corrected original-author repository contains firmware and PCB files. SLOTSCREAMER's own README directs users to upstream Inception. RfCat now links to its author's GitHub repository.

## Excluded destinations and gaps

- HWtools' original USB3380EVB vendor page contains unrelated casino spam. Bplus' alternative timed out. Neither is recommended as a component seller.
- The original Lisa/M and CryptoCape sales URLs return 404. The Adafruit RTL-SDR listing now describes a different tuner and was out of stock; the matching R820T listing at Hacker Warehouse is used instead.
- TINYALAMO's original Irongeek recording page was identified, but direct access returned HTTP 403. It was not added as a verified recording link.
- Securing Hardware's implant and prototyping course outlines say they are still in development; the established x86 and JTAG outlines are used instead.
- No confirmed published original source was found for ADAPTERNOODLE or CACTUSTUTU, nor separate ALLOYVIPER CAD. No primary maintained Kraken source was verified for DRIZZLECHAIR. These gaps are recorded in the manifest rather than filled with unrelated forks or products.

SOLDERPEEK is represented with its schematics and Gerbers on SAVIORBURST, where the original repository keeps it.
