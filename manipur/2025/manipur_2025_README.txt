Manipur 2025 Electoral Rolls (final rolls) — scanned PDFs
=========================================================

Source : CEO Manipur, https://ceomanipur.nic.in/eroll (Electoral Roll 2025, as of 01-01-2025)
Scope  : Final rolls. English for all 60 Assembly Constituencies (ACs); Manipuri for ACs 1-40
         only (ACs 41-60 are published in English only on the source site).
Counts : 2,955 English + 1,586 Manipuri = 4,541 PDFs.

Packaging
---------
Each language is a gzip-compressed tar archive, split into <2 GB chunks:
  manipur_2025_english.tar.gz.partaa, .partab, ...
  manipur_2025_manipuri.tar.gz.partaa, .partab, ...

Reassemble and extract (per language), e.g.:
  cat manipur_2025_english.tar.gz.part* > manipur_2025_english.tar.gz
  tar xzf manipur_2025_english.tar.gz

Inside, every PDF is named so it is self-describing:
  manipur_2025_english_AC<nn>_part<nnn>_final.pdf
  manipur_2025_manipuri_AC<nn>_part<nnn>_final.pdf
(AC = assembly constituency number; part = polling-station part number.)
