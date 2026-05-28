# Valorant Stream Yoinker + Bomb Timer

Fork of [deadly/valorant-stream-yoinker](https://github.com/deadly/valorant-stream-yoinker) combining **stream detection** and an **auto bomb timer overlay** in one app.

## Features

- **Stream Yoinker** — Reveals real usernames behind streamer mode, checks possible Twitch names, and notifies when a player is live.
- **Bomb Timer** — Auto-detects spike plant on screen and shows a click-through 44s countdown overlay for timing practice.

## Requirements

- Windows
- Python 3.10+
- **Valorant must be running before you start the app**

## Install & run

```bash
pip install -r requirements.txt
python src/main.py
```

On first launch, the app uses the region set in `src/main.py` (`DEFAULT_REGION`, default `eu`).

## Configuration

Settings are defined as constants at the top of `src/main.py`:

| Constant | Description |
|----------|-------------|
| `DEFAULT_REGION` | Valorant region (`na`, `eu`, `latam`, `br`, `ap`, `kr`, `pbe`) |
| `STATE_INTERVAL` | Delay between game-state checks (seconds). Higher = less CPU |
| `TWITCH_REQ_DELAY` | Delay between Twitch live checks. Increase if rate-limited |
| `SKIP_TEAM_PLAYERS` | Skip teammates when checking Twitch names |
| `SKIP_PARTY_PLAYERS` | Skip party members when checking Twitch names |

## Build executable

```bash
pip install pyinstaller
pyinstaller valorant-stream-yoinker-bomb-timer.spec
```

Output: `dist/ValorantStreamYoinkerBombTimer.exe`

## Example

<p align="center">
    <img src="example.png" alt="Valorant Stream Yoinker screenshot">
</p>

## Regions

Available regions: `NA`, `EU`, `LATAM`, `BR`, `AP`, `KR`, `PBE`.  
Server list: https://support-valorant.riotgames.com/hc/en-us/articles/360055678634-Server-Select

## Is this bannable?

**Use at your own risk.** Using the Valorant local API this way is against Riot's Terms of Service. No suspensions have been widely reported, but use on an alt if you want to minimize risk.

## Credits

- Original Stream Yoinker: [deadly/valorant-stream-yoinker](https://github.com/deadly/valorant-stream-yoinker)
- This fork: [Sweizeur/valorant-stream-yoinker-bomb-timer](https://github.com/Sweizeur/valorant-stream-yoinker-bomb-timer)

## License

Copyright (c) 2023 deadly

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
