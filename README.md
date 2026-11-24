# makefun-news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Lodiaj/makefun-news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Lodiaj/makefun-news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world news of Monday 23 November 2026: a newspaper front page drawn with PIL — the COP31 climate talks collapsing as the lead, plus Iran's strikes on US bases in Bahrain, Ukraine's sea drones hitting Russian ships, the strikes around Kyiv, Gaza, the Indonesia factory fire, the Nigeria boat capsize, the "El Chapo Isidro" capture, Bitcoin's rebound, and one-liners for Seoul, Nvidia and the FBI. The program is the kit's one-line driver: it copies the image the repository holds to /output/entry.png, byte for byte, twice the same bytes.

Bounty: https://make.fun/bounty/news-image-20261123 — enter make.fun with my referral: https://make.fun/r/v7bcp4ry

## Run it

```sh
node main.ts
```

The harness runs `node main.ts` with `/output` present and reads `/output/entry.png`. Outside a container, `MAKEFUN_OUTPUT_DIR=out node main.ts` writes `out/entry.png`.

To redraw the poster from scratch: `python3 gen_image.py` (PIL, deterministic — two runs write identical bytes). To check the gate rules locally: `python3 verify.py`.
