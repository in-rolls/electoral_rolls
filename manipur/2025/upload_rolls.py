#!/usr/bin/env python3
"""Package the scraped Manipur 2025 rolls into clearly-named <=2GB chunks and upload them to
the Harvard Dataverse PDF dataset, streaming one chunk at a time (peak ~2GB disk).

Per language (english / manipuri):
  tar -c (rename each file to manipur_2025_<lang>_AC..part..final.pdf, inside a same-named
  folder) | gzip -n  ->  split the stream into <=2GB chunks named
  manipur_2025_<lang>.tar.gz.part{aa,ab,...}  ->  upload each chunk via the soundscape
  Dataverse uploader (S3 direct), then delete it. Already-uploaded chunk names are skipped
  (resumable). gzip -n + a sorted file list make the byte stream deterministic across reruns,
  so chunk boundaries (and thus names) are stable.

Token is read from /tmp/.dvtoken (never written to the repo or a command line).
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVER = "https://dataverse.harvard.edu"
DOI = "doi:10.7910/DVN/OG47IV"
TOKEN = Path("/tmp/.dvtoken").read_text().strip()
CHUNK = 1900 * 1024 * 1024  # < 2 GB per chunk

# load the soundscape uploader module directly (stdlib + requests only)
_spec = importlib.util.spec_from_file_location(
    "dvupload", "/Users/soodoku/Documents/GitHub/soundscape/src/soundscape/upload.py")
up = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(up)

BUNDLES = [
    ("english", "pdfs/english", "_final_ENG.pdf",
     r"#^pdfs/english/\(.*\)_final_ENG\.pdf#manipur_2025_english/manipur_2025_english_\1_final.pdf#"),
    ("manipuri", "pdfs/manipuri", "_final_BEN.pdf",
     r"#^pdfs/manipuri/\(.*\)_final_BEN\.pdf#manipur_2025_manipuri/manipur_2025_manipuri_\1_final.pdf#"),
]


def suffix(i):  # 0->aa, 1->ab, ... (matches `split` default)
    return chr(97 + i // 26) + chr(97 + i % 26)


def upload_bundle(lang, srcdir, pat, sed, existing):
    files = sorted(str(p.relative_to(HERE)) for p in (HERE / srcdir).glob("*.pdf"))
    listfile = HERE / f".{lang}_filelist.txt"
    listfile.write_text("\n".join(files) + "\n")
    print(f"[{lang}] {len(files)} files -> {lang} bundle", flush=True)

    tar = subprocess.Popen(["tar", "-c", "-s", sed, "-T", str(listfile)],
                           stdout=subprocess.PIPE, cwd=str(HERE))
    gz = subprocess.Popen(["gzip", "-1", "-n", "-c"], stdin=tar.stdout, stdout=subprocess.PIPE)
    tar.stdout.close()

    base = f"manipur_2025_{lang}.tar.gz"
    i = 0
    while True:
        # read exactly CHUNK bytes (or until EOF) from the gzip stream
        buf = bytearray()
        while len(buf) < CHUNK:
            block = gz.stdout.read(min(8 * 1024 * 1024, CHUNK - len(buf)))
            if not block:
                break
            buf += block
        if not buf:
            break
        name = f"{base}.part{suffix(i)}"
        i += 1
        if name in existing:
            print(f"  skip (already in dataset) {name} ({len(buf)/1e9:.2f} GB)", flush=True)
            continue
        chunk_path = HERE / name
        chunk_path.write_bytes(buf)
        print(f"  uploading {name} ({len(buf)/1e9:.2f} GB) ...", flush=True)
        try:
            up.upload_file(SERVER, DOI, TOKEN, chunk_path)
            print(f"  done {name}", flush=True)
        finally:
            chunk_path.unlink(missing_ok=True)
    gz.stdout.close()
    if gz.wait() != 0 or tar.wait() != 0:
        raise RuntimeError(f"tar/gzip failed for {lang}")
    listfile.unlink(missing_ok=True)
    return i


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None  # optional: "english" or "manipuri"
    existing = up._existing_filenames(SERVER, DOI, TOKEN)
    print(f"dataset currently has {len(existing)} files", flush=True)
    total = 0
    for lang, srcdir, pat, sed in BUNDLES:
        if only and lang != only:
            continue
        total += upload_bundle(lang, srcdir, pat, sed, existing)
    print(f"\nDONE: {total} chunks processed.", flush=True)


if __name__ == "__main__":
    sys.exit(main())
