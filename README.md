[![m](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?ref=zhc1s3ge)
[![m](https://make.fun/badge/news-image-20261125/yangyunkun318/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125?ref=zhc1s3ge)
[![m](https://make.fun/badge/news-image-20261125/yangyunkun318/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?ref=zhc1s3ge)

# THE WORLD — 25 November 2026

A newspaper front page summing up the world's news of Wednesday 25 November
2026 in one image (1024x1024 PNG). Entry for
[Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125)
($100).

## The six stories

All six were first reported on 25 November 2026 (UTC):

1. **HUAWEI GUILTY IN U.S. FRAUD TRIAL** (hero) — A Brooklyn jury convicts
   Huawei on 10 of 12 counts: bank fraud, wire fraud, sanctions breaches
   and trade-secret theft. It is acquitted of racketeering.
2. **PAKISTAN'S FIRST ASTRONAUT IN ORBIT** — Shenzhou-24 lifts off with
   Muhammad Zeeshan Ali, the first Pakistani in orbit and the first
   foreigner aboard China's Tiangong station.
3. **XI PURGES SHANGHAI BOSS** — Chen Jining, Shanghai party chief and
   Politburo member, is placed under a graft probe, the fourth to fall
   since 2025.
4. **UKRAINE'S DRONES SINK RUSSIAN SHIP** — Sea drones sink the corvette
   Merkury and hit a cargo ship off Libya; Zelensky calls it
   self-defence. Two Libyan officers die.
5. **HOUTHIS HIT RIYADH TOWER** — A drone strikes a tower in Riyadh's
   financial district, injuring 11. The coalition orders Hodeidah
   evacuated; Jeddah is threatened. A container ship hits a mine in
   Hormuz.
6. **CIA, SPY CHIEFS HACKED** — Intruders breach an unclassified network
   used by the CIA and ODNI for open-source intelligence. No classified
   data is hit; signs point to China.

Ticker: Trump pardons the Thanksgiving turkeys · Nvidia slides despite
Huang's return · Seoul subway strike called off.

## How it runs

`main.ts` (Node 22, standard library only) copies the pre-rendered
`entry.png` held in this repository to the output directory, verifying
the PNG signature, the 1024x1024 dimensions and the 1 MiB gate:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`render.py` is the Pillow program that drew the front page (flat vector
illustration + real text, deterministic — same input, same bytes). Run it
to regenerate `entry.png` from scratch:

```
python3 render.py
```
