# Manipur 2025 Electoral Rolls (eroll)

### Details
- URL = https://ceomanipur.nic.in/eroll
- Year = Electoral Roll 2025 (final rolls, as of 01/01/2025)
- Scope = **final rolls only**, both languages: **English** (all 60 ACs) and **Manipuri**
  (ACs 1–40 only; ACs 41–60 are published in English only on the site)
- Total expected files ≈ **4,500** (~2,973 English + ~1,544 Manipuri)

This is a **separate scraper** from the older `../manipur.py`, which targets the defunct
2018 site `www.ceomanipur.nic.in/ElectoralRolls.html`.

### How the site works
The CEO Manipur site is an ASP.NET WebForms app. The download flow (reverse-engineered):

1. `GET /eroll` — gets the session cookie and the assembly-constituency dropdown.
2. `POST /eroll.aspx/GetData` `{"selectedValue","selectedText"}` — per AC, the list of
   parts / polling stations and the file size of each available roll (a `0`/absent size
   means that roll does not exist). This is the manifest source of truth.
3. `GET /Captcha/captcha.ashx` — a 6-char captcha image.
4. `GET /ValidateCaptcha.ashx?code=<answer>` — validates against the session. **One
   success unlocks exactly one download.**
5. `GET /FileDownload.ashx?selectedText&selectedValue&partNo&lang=ENG|BEN&type=final` —
   the PDF.

Because every file needs a freshly solved captcha, the script solves them with the
**Anthropic vision API** (`claude-haiku-4-5`). The captcha image is tiny (~23 image
tokens), so the whole run costs well under US$1.

### What the script does
[`manipur.py`](manipur.py):

1. Builds the full expected-file manifest from `GetData` and writes it to
   [`manipur.csv`](manipur.csv) with fields:
   `ac_number, ac_name, part_no, ps_name, lang, roll_type, expected_size_mb, filename,
   raw_bytes, compressed_bytes, pages, status`.
2. For each final roll: solves a captcha, downloads the PDF, validates it
   (`%PDF` magic + page count > 0), and **compresses it with ghostscript** (`/ebook`,
   JPEG re-encode at the same resolution — legibility preserved). The original is replaced
   only when the compressed copy is valid and smaller (~30% saving), otherwise kept.
3. Stores PDFs in `pdfs/english/` and `pdfs/manipuri/` as
   `AC{nn}_part{nnn}_final_{ENG|BEN}.pdf`.
4. Logs everything to `logs/manipur.log` and prints a **reconciliation summary**
   at the end (expected vs downloaded vs failed, per language, bytes saved). It exits
   non-zero if any expected file is missing.

The script is **resumable** — already-downloaded valid PDFs are skipped on re-run.

### Requirements
- Python 3.9+ with the packages in [`requirements.txt`](requirements.txt)
  (`anthropic`, `requests`, `pypdf`).
- **ghostscript** (`gs`) on `PATH` for compression (run with `--no-compress` to skip).
- An Anthropic API key in `ANTHROPIC_API_KEY` (env var, or a gitignored `.env` file in
  this directory containing `ANTHROPIC_API_KEY=...`).

### Running
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...        # or put it in .env (gitignored)

# Smoke test: one assembly constituency, a few files
python manipur.py --ac 1 --limit 5

# Full run (all ~4,500 final rolls)
python manipur.py
```

Useful flags: `--ac N` (single AC), `--limit N` (cap files), `--lang ENG|BEN`,
`--delay SEC`, `--no-compress`, `-v` (debug logging).
