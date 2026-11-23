# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/rismzz/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/rismzz/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A dense broadsheet that sums up Monday 23 November 2026 in a single
1024×1024 image: 35 headline stories, every one first reported that day.
Lead: COP31 breaks down with no deal as the final draft drops any mention
of fossil fuels. Also inside: the UN agrees to keep negotiating curbs on
lethal AI systems, 24 bodies recovered after an Indonesia factory fire, a
Russian cargo ship ablaze off Finland, 14 missing after a drone strike in
the Kyiv region, Nepal's PM in talks with Modi, India posting a record
720/9d in the Wellington Test, and a markets ticker with Friday's closes —
plus a first-reported UTC timeline strip and a visible DATE CHECK line.

Early edition: built at 00:30 UTC from stories verified so far. A
full-day rebuild will replace this edition before entries close.

## Run it

```sh
python3 render_frontpage.py   # rebuild entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render_frontpage.py` draws the poster with Pillow (DejaVu fonts, no
network) and writes `entry.png`. `main.py` is the entrypoint: it verifies
the PNG (magic bytes, IHDR chunk, 1024×1024, at most 1 MiB) and copies it,
with a sha256 check, to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
`/output`). Deterministic: two runs write identical bytes.

## License

MIT — see [LICENSE](LICENSE).

---
Built for the [make.fun bounty](https://make.fun/bounty/news-image-20261123?ref=aa4mcy45) — $100 USDC, 50 places.
Play make.fun with my referral: https://make.fun/?ref=aa4mcy45
