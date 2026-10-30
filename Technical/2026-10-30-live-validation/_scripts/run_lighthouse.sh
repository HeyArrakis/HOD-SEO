#!/bin/bash
# Usage: run_lighthouse.sh <lighthouse-bin> <outdir>  — read-only Lighthouse 13 runs (mobile + desktop) on representative templates
LH="$1"; OUT="$2"; mkdir -p "$OUT"
URLS=(
"https://houseofdiams.com/|home"
"https://houseofdiams.com/shop|shop"
"https://houseofdiams.com/engagement-rings|engagement-rings"
"https://houseofdiams.com/fine-jewellery/bracelet/tennis-bracelet|category-tennis"
"https://houseofdiams.com/shop/rosette-five-flower-bracelet|pdp-bracelet"
"https://houseofdiams.com/blog|blog"
"https://houseofdiams.com/blog/how-long-does-a-custom-engagement-ring-take|article"
"https://houseofdiams.com/bespoke|bespoke"
"https://houseofdiams.com/about|about"
"https://houseofdiams.com/contact|contact"
"https://houseofdiams.com/faq|faq"
)
for e in "${URLS[@]}"; do u="${e%%|*}"; n="${e##*|}"
  for p in mobile desktop; do
    extra=""; [ "$p" = desktop ] && extra="--preset=desktop"
    "$LH" "$u" $extra --quiet --output=json --output-path="$OUT/${n}_${p}.json" --chrome-flags="--headless=new --no-first-run" --max-wait-for-load=60000 || echo "FAIL $n $p"
    echo "done $n $p"
  done
done
echo LH_ALL_DONE
