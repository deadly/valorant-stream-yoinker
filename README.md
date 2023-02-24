# Valorant Stream Yoinker
Find the real username behind all hidden names by bypassing streamer mode, check all possible twitch names and print if a streamer is live

# Discord Support Server
https://discord.com/invite/faeM7p92pz

# How to use
**MAKE SURE VALORANT IS OPEN BEFORE RUNNING.** Wait for a game to start, and then names will start printing and being checked.

settings.json:

    - stateInterval: int. change for faster or slower delays between gamestate loop (Slower = less CPU usage. Faster = more CPU usage)

    - twitchReqDelay: int. the delay for the request checking if a streamer is live. If you are getting ratelimited, make this slower. If you want faster loading times, make this faster.
    
    - skipTeamPlayers: boolean. decide whether or not you want to skip team members during the process of checking possible twitch names.
    
    - skipPartyPlayers: boolean. decide whether or not you want to skip party members during the process of checking possible twitch names.

# Example
<p align="center">
    <img src="https://raw.githubusercontent.com/deadly/valorant-stream-yoinker/main/example.png" alt="screenshot of VALORANT Stream Yoinker">
</p>

# Regions
The program will ask you for your region. The available regions are NA, EU, LATAM, BR, AP, KR, and PBE. Type the region that you play on.

# Is This Bannable
USE AT YOUR OWN RISK. With all programs like this, there is no guarantee that it's safe because using the VALORANT API in this manner is against Riot's Terms of Service. No suspensions have been reported so far from using this program. All things considered, I would use this only on an alt account if you don't want to risk the API abuse account suspension on your main, albeit unlikely.


# License
Copyright (c) [2023] [deadly]

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
