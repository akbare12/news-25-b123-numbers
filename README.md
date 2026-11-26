# The World in One Page — Wednesday, November 25, 2026

[![make.fun rank](https://make.fun/bounty/news-image-20261125/badge/rank/akbare12/news-25-b123-numbers)](https://make.fun/bounty/news-image-20261125)
[![make.fun reward](https://make.fun/bounty/news-image-20261125/badge/reward/akbare12/news-25-b123-numbers)](https://make.fun/bounty/news-image-20261125)
[![make.fun entries](https://make.fun/bounty/news-image-20261125/badge/entries/akbare12/news-25-b123-numbers)](https://make.fun/bounty/news-image-20261125)

A dense one-page front page covering **50 stories from a single day** —
Wednesday, November 25, 2026 — as a 1024×1024 image (`entry.png`).

## The three heroes

1. **Trump hits 14 trade partners with new tariffs** — China 20%, the EU 15%,
   Vietnam 20% — as Washington targets industrial overcapacity.
2. **Kospi crashes 6.16%** — Samsung −9.9%, SK Hynix −11.1%; a circuit
   breaker trips as foreigners sell KRW 1.95tn.
3. **Pakistan's Ali becomes the first foreign astronaut on Tiangong** —
   Muhammad Zeeshan Ali, 40, rides Shenzhou-24 to the station, stays 5–10
   days, then returns with Shenzhou-23.

Each hero carries a WHY IT MATTERS line and a big number badge in its scene.

## The rest of the page

- **10 cards** — Gaza (Hamas security chief Abuelouf killed), Bogor (gold mine
  collapse, 9 dead, 17 trapped 100 m down), Iowa (9,500 lbs of lead azide),
  Cartagena (76 hostages freed), Cairo (tanker fire, 31 dead), Solomon Islands
  (Australia's $740M pact), New York (Macy's 100th parade delayed), Madrid
  (Abrego Garcia, 90 days), Nvidia (−3.9%, S&P downgrade watch), SpaceX
  (1 million satellites cleared).
- **DATE CHECK** — IN: 50 stories, all from 25 Nov. LEFT OUT: Huawei verdict
  24 Nov, PIF Tower attack 24 Nov, Sudan strikes 24 Nov, Nvidia CEO
  reinstated 23 Nov. Nothing from any other date appears anywhere else on
  the page: every card and ALSO item is a 25 November 2026 event.
- **Map** — 13 pins with a readable key: Washington, Brussels, Beijing,
  Hanoi, Seoul, Jiuquan, Gaza, Bogor, Iowa, Cartagena, Cairo, Honiara, Madrid.
- **ALSO** — 37 more stories from the same day.
- **Number strip** — 20%, −6.16%, 9,500 lbs, 76, 31, 9, $740M, −3.9%,
  90 days, 100th, 1M, 5–10 days.

Sources: Reuters, AP, BBC, CNN, Xinhua, Korea Exchange, pm.gov.au.

## How it is built

- `gen.py` renders `entry.png` at build time with Pillow (DejaVu fonts).
  Run `python3 gen.py` to regenerate the image.
- `main.py` is **standard library only** — it copies the pre-rendered
  `entry.png` into `MAKEFUN_OUTPUT_DIR` (default `out/`), verifies the PNG
  header, dimensions (1024×1024) and SHA-256, and exits 0 on success.

## License

MIT — see `LICENSE`.
