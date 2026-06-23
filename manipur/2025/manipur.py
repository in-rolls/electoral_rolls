#!/usr/bin/env python3
"""Scrape the 2025 Manipur electoral rolls (final rolls) from https://ceomanipur.nic.in/eroll.

The CEO Manipur site is an ASP.NET WebForms application. The flow this script drives,
reverse-engineered from the live endpoints, is:

  1. GET  /eroll                         -> obtain the ASP.NET session cookie and the
                                            assembly-constituency (AC) dropdown options.
  2. POST /eroll.aspx/GetData            -> per AC, the list of parts / polling stations
                                            and the available roll file sizes (the manifest
                                            source of truth: a 0 / absent size means the
                                            roll does not exist for that part).
  3. GET  /Captcha/captcha.ashx          -> a 6-char captcha image, solved with the
                                            Anthropic vision API.
  4. GET  /ValidateCaptcha.ashx?code=..  -> validates the captcha against the session.
                                            One success unlocks exactly ONE download.
  5. GET  /FileDownload.ashx?...         -> the actual PDF (application/pdf).

We fetch only the FINAL rolls: English for all 60 ACs, Manipuri for ACs 1-40 (ACs 41-60
are English-only on the site). Each downloaded PDF is compressed with ghostscript
(JPEG re-encode, resolution preserved) and the original replaced when the compressed copy
is valid and smaller.

The script logs every step, writes a manifest CSV, and reconciles expected vs downloaded
files at the end so the counts add up. It is resumable: already-downloaded valid PDFs are
skipped on re-run.
"""

import argparse
import base64
import csv
import json
import logging
import os
import re
import subprocess
import sys
import time
from logging.handlers import RotatingFileHandler

import requests
from pypdf import PdfReader

# --------------------------------------------------------------------------- config

BASE_URL = "https://ceomanipur.nic.in"
EROLL_URL = BASE_URL + "/eroll"
GETDATA_URL = BASE_URL + "/eroll.aspx/GetData"
CAPTCHA_URL = BASE_URL + "/Captcha/captcha.ashx"
VALIDATE_URL = BASE_URL + "/ValidateCaptcha.ashx"
DOWNLOAD_URL = BASE_URL + "/FileDownload.ashx"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

HERE = os.path.dirname(os.path.abspath(__file__))
PDF_ENGLISH_DIR = os.path.join(HERE, "pdfs", "english")
PDF_MANIPURI_DIR = os.path.join(HERE, "pdfs", "manipuri")
LOG_DIR = os.path.join(HERE, "logs")
LOG_FILE = os.path.join(LOG_DIR, "manipur.log")
MANIFEST_CSV = os.path.join(HERE, "manipur.csv")

CSV_HEADER = (
    "ac_number", "ac_name", "part_no", "ps_name", "lang", "roll_type",
    "expected_size_mb", "filename", "raw_bytes", "compressed_bytes",
    "pages", "status",
)

# Manipuri (BEN) final rolls only exist for ACs 1-40.
MANIPURI_MAX_AC = 40

CAPTCHA_MODEL = "claude-haiku-4-5"
CAPTCHA_MAX_ATTEMPTS = 6          # fresh captcha + solve attempts per file
DOWNLOAD_MAX_ATTEMPTS = 3         # full (captcha + download) attempts per file
REQUEST_TIMEOUT = 60
DOWNLOAD_READ_TIMEOUT = 120       # per-chunk read timeout while streaming a PDF body
NETWORK_RETRIES = 5               # retries on transient network errors per request
SIZE_TOLERANCE = 0.30            # warn if downloaded size deviates this much from expected

MAX_LOG_BYTES = 50 * 1024 * 1024
LOG_BACKUP_COUNT = 5

COMPRESS_ENABLED = True          # toggled off by --no-compress

log = logging.getLogger("manipur_2025")


# --------------------------------------------------------------------------- logging

def configure_logging(verbose=False):
    os.makedirs(LOG_DIR, exist_ok=True)
    log.setLevel(logging.DEBUG if verbose else logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    console.setLevel(logging.DEBUG if verbose else logging.INFO)

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=MAX_LOG_BYTES, backupCount=LOG_BACKUP_COUNT
    )
    file_handler.setFormatter(fmt)
    file_handler.setLevel(logging.DEBUG)

    log.handlers.clear()
    log.addHandler(console)
    log.addHandler(file_handler)


# --------------------------------------------------------------------------- env / key

def load_dotenv():
    """Load KEY=VALUE pairs from a gitignored .env next to this script (no dependency).

    Existing environment variables take precedence and are not overwritten.
    """
    path = os.path.join(HERE, ".env")
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


# --------------------------------------------------------------------------- http

def make_session():
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def request(session, method, url, **kwargs):
    """Issue a request with retries + backoff on transient network errors."""
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    last_exc = RuntimeError("request failed with no captured exception")
    for attempt in range(1, NETWORK_RETRIES + 1):
        try:
            return session.request(method, url, **kwargs)
        except (requests.exceptions.SSLError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as exc:
            last_exc = exc
            wait = min(2 ** attempt, 30)
            log.warning("network error on %s (attempt %d/%d): %s; retrying in %ds",
                        url, attempt, NETWORK_RETRIES, exc, wait)
            time.sleep(wait)
    raise last_exc


# --------------------------------------------------------------------------- manifest

def fetch_ac_list(session):
    """Return [(ac_no:int, selected_text:str), ...] from the eroll page dropdown."""
    resp = request(session, "GET", EROLL_URL)
    resp.raise_for_status()
    html = resp.text
    # <option value="1">1-Khundrakpam</option> (the selected default may carry extra attrs).
    options = re.findall(r'<option[^>]*\svalue="(\d+)"[^>]*>([^<]+)</option>', html)
    acs = []
    seen = set()
    for value, text in options:
        if value == "0":
            continue
        ac_no = int(value)
        if ac_no in seen:
            continue
        seen.add(ac_no)
        acs.append((ac_no, text.strip()))
    acs.sort(key=lambda x: x[0])
    return acs


def fetch_parts(session, ac_no, selected_text):
    """POST GetData for one AC; return the list of part rows (dicts)."""
    body = json.dumps({"selectedValue": str(ac_no), "selectedText": selected_text})
    resp = request(session, "POST", GETDATA_URL, data=body, headers={
        "Content-Type": "application/json",
        "Referer": EROLL_URL,
        "X-Requested-With": "XMLHttpRequest",
    })
    resp.raise_for_status()
    inner = json.loads(resp.json()["d"])
    if inner.get("status") != "success":
        raise RuntimeError("GetData returned status=%r for AC %d" % (inner.get("status"), ac_no))
    return inner.get("data", [])


def filename_for(ac_no, part_no, lang):
    return "AC%02d_part%03d_final_%s.pdf" % (ac_no, int(part_no), lang)


def outdir_for(lang):
    return PDF_ENGLISH_DIR if lang == "ENG" else PDF_MANIPURI_DIR


def build_manifest(session, only_ac=None):
    """Build the list of expected final-roll download tasks from GetData.

    Each task is a dict with the CSV fields plus internal bookkeeping.
    """
    acs = fetch_ac_list(session)
    log.info("found %d assembly constituencies", len(acs))
    if only_ac is not None:
        acs = [a for a in acs if a[0] == only_ac]
        if not acs:
            raise SystemExit("AC %d not found in the dropdown" % only_ac)

    tasks = []
    for ac_no, selected_text in acs:
        # selected_text is like "1-Khundrakpam"; ac_name is the part after the dash.
        ac_name = selected_text.split("-", 1)[1].strip() if "-" in selected_text else selected_text
        rows = fetch_parts(session, ac_no, selected_text)
        log.info("AC %d (%s): %d parts", ac_no, ac_name, len(rows))
        for row in rows:
            part_no = row.get("PART_NO")
            ps_name = (row.get("PS_NAME_EN") or "").strip()
            if part_no is None:
                continue
            # English final roll: every AC.
            eng_size = row.get("FileSize_English")
            if eng_size and float(eng_size) > 0:
                tasks.append(_make_task(ac_no, ac_name, selected_text, part_no, ps_name,
                                        "ENG", float(eng_size)))
            # Manipuri final roll: ACs 1-40 only.
            if ac_no <= MANIPURI_MAX_AC:
                ben_size = row.get("FileSize_Manipuri")
                if ben_size and float(ben_size) > 0:
                    tasks.append(_make_task(ac_no, ac_name, selected_text, part_no, ps_name,
                                            "BEN", float(ben_size)))
    return tasks


def _make_task(ac_no, ac_name, selected_text, part_no, ps_name, lang, expected_mb):
    return {
        "ac_number": ac_no,
        "ac_name": ac_name,
        "selected_text": selected_text,
        "part_no": int(part_no),
        "ps_name": ps_name,
        "lang": lang,
        "roll_type": "final",
        "expected_size_mb": expected_mb,
        "filename": filename_for(ac_no, part_no, lang),
        "raw_bytes": "",
        "compressed_bytes": "",
        "pages": "",
        "status": "pending",
    }


def write_manifest(tasks):
    """(Re)write the manifest CSV from the in-memory task list."""
    tmp = MANIFEST_CSV + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(CSV_HEADER)
        for t in tasks:
            writer.writerow([t[k] for k in CSV_HEADER])
    os.replace(tmp, MANIFEST_CSV)


# --------------------------------------------------------------------------- pdf utils

def pdf_page_count(path):
    """Return the number of pages, or 0 if the file is not a readable PDF."""
    try:
        with open(path, "rb") as fh:
            if fh.read(5) != b"%PDF-":
                return 0
        reader = PdfReader(path)
        return len(reader.pages)
    except Exception:
        return 0


def compress_pdf(src, dst):
    """Compress src -> dst with ghostscript /ebook. Return True on a valid, smaller result."""
    cmd = [
        "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.7",
        "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dQUIET", "-dBATCH",
        "-sOutputFile=" + dst, src,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        log.warning("ghostscript failed: %s", exc)
        if os.path.exists(dst):
            os.remove(dst)
        return False
    if pdf_page_count(dst) <= 0:
        log.warning("compressed PDF is invalid; discarding")
        os.remove(dst)
        return False
    if os.path.getsize(dst) >= os.path.getsize(src):
        # No saving; keep the original.
        os.remove(dst)
        return False
    return True


# --------------------------------------------------------------------------- captcha

class CaptchaSolver:
    """Solve the 6-char CEO Manipur captcha with the Anthropic vision API."""

    def __init__(self, model=CAPTCHA_MODEL):
        import anthropic  # imported lazily so --help works without the SDK
        self.client = anthropic.Anthropic()
        self.model = model

    def solve(self, png_bytes):
        b64 = base64.standard_b64encode(png_bytes).decode("ascii")
        msg = self.client.messages.create(
            model=self.model,
            max_tokens=24,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {
                        "type": "base64", "media_type": "image/png", "data": b64}},
                    {"type": "text", "text": (
                        "This image is a CAPTCHA containing exactly 6 characters drawn from "
                        "uppercase letters A-Z and digits 0-9. Read them left to right and "
                        "reply with ONLY those 6 characters, no spaces, no other text.")},
                ],
            }],
        )
        text = "".join(b.text for b in msg.content if b.type == "text")
        return re.sub(r"[^A-Z0-9]", "", text.strip().upper())


def get_validated_session(session, solver):
    """Fetch a fresh captcha, solve it, and validate. Return True once the session is
    authorized for exactly one download."""
    for attempt in range(1, CAPTCHA_MAX_ATTEMPTS + 1):
        resp = request(session, "GET", CAPTCHA_URL,
                       params={"t": int(time.time() * 1000)},
                       headers={"Referer": EROLL_URL})
        if resp.status_code != 200 or not resp.content:
            log.warning("captcha fetch failed (status %s)", resp.status_code)
            continue
        try:
            answer = solver.solve(resp.content)
        except Exception as exc:
            log.warning("captcha solve error: %s", exc)
            time.sleep(2)
            continue
        if len(answer) != 6:
            log.debug("captcha solver returned %r (len %d); retrying", answer, len(answer))
            continue
        vresp = request(session, "GET", VALIDATE_URL,
                        params={"code": answer}, headers={"Referer": EROLL_URL})
        result = vresp.text.strip().lower()
        if result == "success":
            log.debug("captcha solved on attempt %d (%s)", attempt, answer)
            return True
        log.debug("captcha %r rejected (%s) on attempt %d", answer, result, attempt)
    return False


# --------------------------------------------------------------------------- download

def download_one(session, solver, task, delay):
    """Download, validate and compress a single task's PDF. Updates task in place.

    Returns one of: 'done', 'skipped', 'failed:<reason>'.
    """
    outdir = outdir_for(task["lang"])
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, task["filename"])

    # Resume: a valid existing PDF is left untouched.
    if os.path.exists(dest):
        pages = pdf_page_count(dest)
        if pages > 0:
            task["pages"] = pages
            task["compressed_bytes"] = os.path.getsize(dest)
            task["status"] = "done"
            return "skipped"
        os.remove(dest)  # corrupt; re-download

    params = {
        "selectedText": task["selected_text"],
        "selectedValue": str(task["ac_number"]),
        "partNo": str(task["part_no"]),
        "lang": task["lang"],
        "type": "final",
    }

    for attempt in range(1, DOWNLOAD_MAX_ATTEMPTS + 1):
        if not get_validated_session(session, solver):
            log.warning("could not solve captcha for %s (attempt %d)", task["filename"], attempt)
            continue

        tmp = dest + ".part"
        try:
            resp = request(session, "GET", DOWNLOAD_URL, params=params,
                           headers={"Referer": EROLL_URL}, stream=True,
                           timeout=(15, DOWNLOAD_READ_TIMEOUT))
            ctype = resp.headers.get("Content-Type", "")
            if resp.status_code != 200 or "application/pdf" not in ctype:
                body = resp.text[:120].replace("\n", " ")
                log.warning("download not a PDF for %s (status %s, type %s): %s",
                            task["filename"], resp.status_code, ctype, body)
                time.sleep(delay)
                continue

            size = 0
            with open(tmp, "wb") as fh:
                # The streaming body read is the part most prone to mid-transfer
                # read-timeouts on this flaky host (and to the laptop sleeping),
                # so any network error here just retries this one file.
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        fh.write(chunk)
                        size += len(chunk)
        except requests.exceptions.RequestException as exc:
            log.warning("network error downloading %s: %s; retrying", task["filename"], exc)
            if os.path.exists(tmp):
                os.remove(tmp)
            time.sleep(delay)
            continue

        pages = pdf_page_count(tmp)
        if pages <= 0:
            log.warning("downloaded file for %s is not a valid PDF; retrying", task["filename"])
            os.remove(tmp)
            time.sleep(delay)
            continue

        # Size sanity vs the size advertised by GetData.
        expected = task["expected_size_mb"] * 1_000_000
        if expected and abs(size - expected) > SIZE_TOLERANCE * expected:
            log.warning("%s size %d bytes deviates from expected ~%.2f MB",
                        task["filename"], size, task["expected_size_mb"])

        task["raw_bytes"] = size
        task["pages"] = pages

        # Compress in place (replace original when smaller & valid).
        comp = dest + ".comp"
        if COMPRESS_ENABLED and compress_pdf(tmp, comp):
            os.replace(comp, dest)
            os.remove(tmp)
            task["compressed_bytes"] = os.path.getsize(dest)
            log.info("OK %s | %d pages | %d -> %d bytes (%.0f%% saved)",
                     task["filename"], pages, size, task["compressed_bytes"],
                     100 * (1 - task["compressed_bytes"] / size))
        else:
            os.replace(tmp, dest)
            task["compressed_bytes"] = task["raw_bytes"]
            log.info("OK %s | %d pages | %d bytes (kept original)",
                     task["filename"], pages, size)

        task["status"] = "done"
        return "done"

    task["status"] = "failed:download"
    return "failed:download"


# --------------------------------------------------------------------------- reconcile

def reconcile(tasks):
    """Log the expected-vs-downloaded summary and return the number of failed files.

    Distinguishes genuine failures (status `failed:*`) from files never attempted
    (status `pending`, e.g. under --limit or after an interrupt).
    """
    done = [t for t in tasks if t["status"] == "done"]
    failed = [t for t in tasks if t["status"].startswith("failed")]
    pending = [t for t in tasks if t["status"] == "pending"]
    # Compression ratio only over files downloaded this run (both sizes known);
    # files resumed from disk have a compressed size but no recorded raw size.
    sized = [t for t in done if t["raw_bytes"] and t["compressed_bytes"]]
    raw_total = sum(int(t["raw_bytes"]) for t in sized)
    comp_total = sum(int(t["compressed_bytes"]) for t in sized)

    def count(lang):
        exp = sum(1 for t in tasks if t["lang"] == lang)
        got = sum(1 for t in done if t["lang"] == lang)
        return got, exp

    eng_got, eng_exp = count("ENG")
    ben_got, ben_exp = count("BEN")

    log.info("=" * 60)
    log.info("RECONCILIATION")
    log.info("  expected  : %d files", len(tasks))
    log.info("  downloaded: %d files", len(done))
    log.info("  failed    : %d files", len(failed))
    log.info("  pending   : %d files (not attempted this run)", len(pending))
    log.info("  english   : %d / %d", eng_got, eng_exp)
    log.info("  manipuri  : %d / %d", ben_got, ben_exp)
    if comp_total and raw_total:
        log.info("  bytes     : raw %.2f GB -> compressed %.2f GB (%.0f%% saved)",
                 raw_total / 1e9, comp_total / 1e9, 100 * (1 - comp_total / raw_total))
    if failed:
        log.warning("  FAILED files:")
        for t in failed:
            log.warning("    %s (AC %s part %s %s) -> %s",
                        t["filename"], t["ac_number"], t["part_no"], t["lang"], t["status"])
    log.info("=" * 60)
    return len(failed)


# --------------------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ac", type=int, default=None,
                        help="only process this assembly constituency number (smoke test)")
    parser.add_argument("--limit", type=int, default=None,
                        help="stop after attempting this many files (smoke test)")
    parser.add_argument("--lang", choices=["ENG", "BEN"], default=None,
                        help="restrict to one language (ENG=English, BEN=Manipuri)")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="seconds to sleep between files (politeness)")
    parser.add_argument("--no-compress", action="store_true",
                        help="skip ghostscript compression (download originals only)")
    parser.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    args = parser.parse_args()

    configure_logging(args.verbose)
    load_dotenv()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY is not set. Export it or put it in %s/.env",
                  HERE)
        return 2

    if args.no_compress:
        global COMPRESS_ENABLED
        COMPRESS_ENABLED = False

    session = make_session()
    log.info("building manifest from %s ...", GETDATA_URL)
    tasks = build_manifest(session, only_ac=args.ac)
    if args.lang:
        tasks = [t for t in tasks if t["lang"] == args.lang]
    log.info("manifest: %d expected final-roll files", len(tasks))

    # Mark already-present valid files as done before writing the baseline manifest.
    for t in tasks:
        dest = os.path.join(outdir_for(t["lang"]), t["filename"])
        if os.path.exists(dest) and pdf_page_count(dest) > 0:
            t["status"] = "done"
            t["compressed_bytes"] = os.path.getsize(dest)
    write_manifest(tasks)

    solver = CaptchaSolver()

    pending = [t for t in tasks if t["status"] != "done"]
    if args.limit is not None:
        pending = pending[:args.limit]
    log.info("%d files to download (%d already present)",
             len(pending), len(tasks) - len([t for t in tasks if t['status'] != 'done']))

    try:
        for i, task in enumerate(pending, 1):
            log.info("[%d/%d] %s", i, len(pending), task["filename"])
            # Safety net: no single file (network blip, ghostscript, anything)
            # may ever crash the whole run. Mark it failed and keep going; a
            # later re-run will retry it.
            try:
                result = download_one(session, solver, task, args.delay)
            except Exception as exc:  # noqa: BLE001  deliberate catch-all per-file
                log.exception("unexpected error on %s: %s", task["filename"], exc)
                task["status"] = "failed:exception"
                result = "failed:exception"
            if result.startswith("failed"):
                log.error("FAILED %s -> %s", task["filename"], result)
            if i % 25 == 0:
                write_manifest(tasks)
            time.sleep(args.delay)
    except KeyboardInterrupt:
        log.warning("interrupted by user; writing manifest before exit")
    finally:
        write_manifest(tasks)

    missing = reconcile(tasks)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
