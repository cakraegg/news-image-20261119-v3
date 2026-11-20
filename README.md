[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/cakraegg/news-image-20261119-v3/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/cakraegg/news-image-20261119-v3/reward.svg)](https://make.fun/bounty/news-image-20261119)

# news-image-20261119 v3 — "The World in One Day", 42 stories

One image that sums up the world news of Thursday 19 November 2026,
built to beat the v2 front page (dev judge 0.9834, rank 422 of 12,854).
v2 lost on breadth: the whole top 20 packs 36–42 stories, and v2 had
27. This version keeps v2's broadsheet formula and grows it to 42
verified stories — masthead, numbers strip, UTC timeline, three hero
stories, a twelve-card grid, a world map with numbered dots, a
27-item numbered brief list, and a date check.

## The day, in 42 verified stories

**Heroes:** Trump, Xi and Putin hold their first three-way summit in
Shenzhen, on the APEC sidelines, with nuclear arms at the top of the
agenda · GTA VI launches worldwide after a 13-year wait, New Zealand
first, 15.9m pre-orders · Anthropic lists in the biggest IPO on record
($81.3bn at $83 a share, trading Thursday as ANT, valued near $1.5tn).

**Grid:** the ICJ rules Myanmar committed genocide against the
Rohingya · COP31 enters its final 48 hours · Cyclone Akvan bears down
on India's east coast · Ukraine is left off the Shenzhen agenda ·
APEC leaders open their summit and adopt the Shenzhen Outlook · Van
Gogh sells for a record $190.4m · Take-Two jumps 6% on launch day ·
Pakistan test-fires the Fatah-3 missile · Peltola wins in Alaska as
Democrats take the Senate 56–44 · Hegseth signs a US–Venezuela
military pact in Caracas · Israeli tanks cross the Yellow Line in Gaza
· an outage wave grounds thousands of flights.

**Also on Thursday (27 briefs):** GTA VI unlocks first in New Zealand
· Metacritic 99 · leave requests jump 32% · Rahul Gandhi's debate
challenge · Rockstar's China promotion · Anthropic options · the
Berlin Coalition · a Houthi missile over Riyadh · a tanker hit near
Khasab · a Taliban leader's Kabul visit · Somalia's reforms · Kenya's
drought · a third Kerch bridge strike in four days, Putin vowing a
harsher reply · the S&P 500 falls 2.02%, a fifth straight loss · the
U-17 World Cup opens in Doha, hosts beating Panama 2-0 · Denmark
ratifies the US Greenland defence deal 109-0 · Haitian police kill 34
gang members in a raid · dozens missing after a migrant boat capsizes
off Senegal · 589m children lived in conflict zones in 2025 · the
IAEA says North Korea expanded uranium enrichment · Tanzania's Lissu
convicted of sedition · Yunus's ancestral home torched amid violence
in 28 Bangladeshi districts · the triple-star system Welopoai found
28 light-years away · the Texans beat the Colts 26-3 · Chelsea beat
PSG 1-0 in the Women's Champions League · the Senate rejects the Iran
war-powers resolution 51-48 · US jobless claims rise to 203,000.

**Date check (printed in the image):** the Jeffries 251–11 vote,
Voyager 1's light-day, the Gulf interceptions and Nvidia's chief
staying put were first reported on Wednesday 18 November, so they are
named as NOT today's news — the same discipline the rank-1 cover uses.

**Joke, inside the image:** "Thirteen years later, Vice City opens —
and half the world called in sick." (Leave requests really did jump
32% around launch day.)

## How it was made

Three candidates were built and pre-judged pairwise with a vision
model before one was picked: a dense 42-story broadsheet (A), a
map-first layout with all 42 stories as numbered briefs (B), and a
classic newspaper with three big hero photos and region columns (C).
Lapis 1: A beat C in both orders (margin 3) and beat B in the judged
order (margin 2, 0.90 vs 0.75); the two reverse-order calls were
refused by the pre-judge service (HTTP 429, three attempts each).
Lapis 2, A against the v2 front page and the top covers: A vs v2
split 1–1 at margin 2 both ways — A won on breadth (42 vs 27
stories), v2 won on craft and legibility ("avoiding the cluttered
feel") — so v3 is not clearly stronger than v2. A also split 1–1
with the rank-20 cover and lost the judged directions against the
rank-1 and rank-5 covers (margin 2 each). Full logs:
`prejudge-lapis1.log`, `prejudge-lapis2.log`,
`prejudge-lapis2-retry.log` in the work folder. One loss reason
claimed A omits COP31 — wrong; COP31 is story 5 in A's grid, which
itself shows how the dense grid misreads at small scale.
The hero photo and two photos are AI illustrations without watermark;
the skyline, the ANT chart, the small icons and the world map are
hand-drawn. All text is set in type, so nothing is garbled; the
picture is rendered at 2x and downscaled, with fine grain.

## The program

`main.py` (Python 3.13, standard library only) hands `entry.png` to
`/output/entry.png` — honouring `MAKEFUN_OUTPUT_DIR` — after proving
it is one whole JPEG under 1 MiB and at most 1024x1024, walking every
segment so a truncated file is rejected. No network, no clock, no
randomness: two runs write identical bytes (sha256 verified).
