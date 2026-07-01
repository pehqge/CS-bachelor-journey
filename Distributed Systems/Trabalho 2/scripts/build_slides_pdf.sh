#!/usr/bin/env bash
# Build a publication-ready PDF from the HTML deck.
#
# Pipeline: headless Chrome prints slides/apresentacao.html in ?export mode
# (one slide per 1280x720 page) straight to the final PDF.
#
# We deliberately do NOT post-process with Ghostscript: gs /ebook flattens the
# cards' low-alpha gradients into opaque dark blobs and mangles the transparency
# compositing (the title ends up overlapped by a dark rectangle). Chrome's print
# is vector, correct, and small enough to email (~1.3 MB), so it ships as-is.
#
# usage:  ./scripts/build_slides_pdf.sh
# needs:  Google Chrome (or Chromium)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HTML="$ROOT/slides/apresentacao.html"
OUT="$ROOT/slides/apresentacao.pdf"

# locate a chrome/chromium binary across macOS and linux
CHROME=""
for c in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "$(command -v google-chrome 2>/dev/null || true)" \
  "$(command -v chromium 2>/dev/null || true)" \
  "$(command -v chromium-browser 2>/dev/null || true)"; do
  if [ -n "$c" ] && [ -x "$c" ]; then CHROME="$c"; break; fi
done
[ -z "$CHROME" ] && { echo "error: no Chrome/Chromium binary found" >&2; exit 1; }

TMP="$(mktemp -d)"
RAW="$TMP/raw.pdf"
trap 'rm -rf "$TMP"' EXIT

echo "rendering deck -> pdf ..."
# print-to-pdf in a throwaway profile so it never touches a real Chrome session.
# virtual-time-budget should make headless exit on its own; the watchdog is a
# backstop because new-headless sometimes lingers after writing the file.
"$CHROME" --headless=new --disable-gpu --no-sandbox \
  --user-data-dir="$TMP/profile" \
  --no-pdf-header-footer \
  --virtual-time-budget=8000 \
  --print-to-pdf="$RAW" \
  "file://$HTML?export" >/dev/null 2>&1 &
CPID=$!
( sleep 45; kill -9 "$CPID" 2>/dev/null || true ) &
WPID=$!
wait "$CPID" 2>/dev/null || true
kill "$WPID" 2>/dev/null || true

[ -s "$RAW" ] || { echo "error: Chrome did not produce a PDF" >&2; exit 1; }
cp "$RAW" "$OUT"

echo "done: $OUT ($(du -h "$OUT" | cut -f1))"
