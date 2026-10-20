#!/usr/bin/env python3
"""Create a neon isometric city where brighter buildings signal real GitHub activity.

Architecture is illustrative; illumination reflects contribution days.
Uses GitHub's contribution calendar via GraphQL. No third-party dependencies.
"""
import datetime as dt
import html
import json
import math
import os
import pathlib
import random
import urllib.error
import urllib.request

username = os.environ.get("USERNAME", "beeleaf101")
token = os.environ.get("GITHUB_TOKEN")
if not token:
    raise SystemExit("GITHUB_TOKEN is required")

query = """
query($user: String!) {
  user(login: $user) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays { date contributionCount }
        }
      }
    }
  }
}
"""
body = json.dumps({"query": query, "variables": {"user": username}}).encode("utf-8")
req = urllib.request.Request(
    "https://api.github.com/graphql", data=body,
    headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json",
        "User-Agent": "neon-github-city-generator",
    },
)
with urllib.request.urlopen(req, timeout=25) as response:
    result = json.load(response)
if result.get("errors"):
    raise SystemExit("GitHub GraphQL error: " + json.dumps(result["errors"]))
user = result.get("data", {}).get("user")
if not user:
    raise SystemExit("GitHub user not found: " + username)
calendar = user["contributionsCollection"]["contributionCalendar"]
all_days = [
    day for week in calendar["weeks"] for day in week["contributionDays"]
]
contributions = sum(day["contributionCount"] for day in all_days)
total = calendar["totalContributions"]
active_days = sum(day["contributionCount"] > 0 for day in all_days)
busiest = max((day["contributionCount"] for day in all_days), default=0)
last = all_days[-112:]
last = [{"contributionCount": 0}] * (112 - len(last)) + last
rng = random.Random(120987)
out = []
def add(s):
    out.append(s)
def esc(s):
    return html.escape(str(s), quote=True)
def poly(points, fill, opacity=1, stroke="none", sw=0.5):
    coords = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    add(f'<polygon points="{coords}" fill="{fill}" opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>')
def txt(x, y, value, size, fill="#d9fbfc", weight="500", extra=""):
    add(f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" {extra}>{esc(value)}</text>')

add('''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="560" viewBox="0 0 1280 560" role="img" aria-label="A futuristic skyline with illuminated buildings based on actual GitHub contribution activity">
<title>Contribution City — neon activity skyline</title>
<defs>
<linearGradient id="back" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#061020"/><stop offset="58%" stop-color="#081c2e"/>
<stop offset="100%" stop-color="#061421"/></linearGradient>
<radialGradient id="atmo"><stop offset="0%" stop-color="#1acabc" stop-opacity=".37"/>
<stop offset="100%" stop-color="#1acabc" stop-opacity="0"/></radialGradient>
<linearGradient id="faceA" x1="0" y1="0" x2="0" y2="1">
<stop stop-color="#20ebd7"/><stop offset="100%" stop-color="#077894"/></linearGradient>
<linearGradient id="faceB" x1="0" y1="0" x2="0" y2="1">
<stop stop-color="#82ffe3"/><stop offset="100%" stop-color="#168bae"/></linearGradient>
<linearGradient id="darkA" x1="0" y1="0" x2="0" y2="1">
<stop stop-color="#155371"/><stop offset="100%" stop-color="#092f48"/></linearGradient>
<linearGradient id="darkB" x1="0" y1="0" x2="0" y2="1">
<stop stop-color="#1a6d82"/><stop offset="100%" stop-color="#103c54"/></linearGradient>
<filter id="softglow"><feGaussianBlur stdDeviation="19"/></filter>
<filter id="brightglow"><feGaussianBlur stdDeviation="4"/></filter>
<clipPath id="frame"><rect x="13" y="13" width="1254" height="534" rx="22"/></clipPath>
</defs>
<rect x="5" y="5" width="1270" height="550" rx="29" fill="#061622" stroke="#28d9c9" stroke-width="2"/>
<rect x="12" y="12" width="1256" height="536" rx="24" fill="url(#back)" stroke="#116c82" stroke-width="1"/>
<g clip-path="url(#frame)">
<ellipse cx="980" cy="318" rx="340" ry="250" fill="url(#atmo)"/>
<ellipse cx="995" cy="496" rx="275" ry="36" fill="#06d3a8" opacity=".18" filter="url(#softglow)"/>
</g>''')

for i in range(70):
    x = rng.randrange(25, 1250)
    y = rng.randrange(25, 440)
    rad = (i % 4 + 1) * .43
    color = ["#b3ffff", "#26edda", "#788cff"][i % 3]
    add(f'<circle cx="{x}" cy="{y}" r="{rad:.2f}" fill="{color}" opacity="{rng.uniform(.18,.58):.2f}"/>')
    if i % 15 == 0:
        add(f'<path d="M {x-5} {y}h10 M{x} {y-5}v10" stroke="{color}" opacity=".6" stroke-width="1"/>')

add('''<g font-family="Consolas,Monaco,monospace">
<rect x="49" y="45" width="114" height="27" rx="13" fill="#0d414f" stroke="#2ed6b9" stroke-opacity=".6"/>
<text x="68" y="63" font-size="13" font-weight="700" fill="#76ffdf">● LIVE DATA</text>
</g>''')
txt(50, 132, "THE CITY I'M BUILDING", 36, "#edffff", "800", 'font-family="Consolas,monospace" letter-spacing=".8"')
txt(51, 167, "A year of code, one illuminated block at a time.", 16, "#9bcfd3", extra='font-family="Consolas,monospace"')
add('<path d="M51 191H521" stroke="#23697a" stroke-width="1"/>')
txt(51, 239, "CONTRIBUTIONS THIS YEAR", 14, "#5cf5dc", "700", 'font-family="Consolas,monospace" letter-spacing="1"')
txt(51, 297, f"{total:,}", 59, "#ecfffe", "800", 'font-family="Consolas,monospace"')
txt(51, 335, f"{active_days} active days", 18, "#c2e7e8", extra='font-family="Consolas,monospace"')
txt(51, 367, f"Busiest day  /  {busiest} contributions", 16, "#8eb9c7", extra='font-family="Consolas,monospace"')
add('<rect x="49" y="403" width="481" height="80" rx="13" fill="#061c2b" stroke="#216479" stroke-width="1"/>')
add('<circle cx="71" cy="429" r="5" fill="#60ffe2"/><circle cx="71" cy="455" r="5" fill="#1d5b70"/>')
txt(86, 434, "Lit towers = days with contributions", 15, "#c9f7ee", extra='font-family="Consolas,monospace"')
txt(86, 461, "Tower shapes are artistic • last 112 days", 13, "#8fb3c4", extra='font-family="Consolas,monospace"')

# Ground plane arranged as a real compact city, not a 365-day strip.
cols, rows = 14, 8
ox, oy = 908, 280
dx, dy = 24, 10.1
def point(c, r):
    return (ox + (c-r) * dx, oy + (c+r) * dy)
poly([(909,263),(1248,406),(1057,496),(717,351)], "#052739", .65, "#2f9c98", .9)
for r in range(rows):
    for c in range(cols):
        x, y = point(c, r)
        poly([(x,y+1),(x+22,y+10),(x,y+20),(x-22,y+10)], "#0b3142", .69, "#19536a", .6)
# Layer by depth for real isometric occlusion.
city = []
for r in range(rows):
    for c in range(cols):
        idx = r * cols + c
        day = last[idx]
        count = day["contributionCount"]
        x, y = point(c, r)
        seed = random.Random(8302 + r*89 + c*47)
        # Decoratively varied architecture, regardless of activity.
        height = 25 + seed.randrange(15, 82)
        if count:
            height += min(79, 28 + int(math.log1p(count)*21))
        width = 15.5 + seed.randrange(0, 6)
        city.append((c+r, y, x, height, width, count, seed))
city.sort(key=lambda b: (b[0], b[1]))
for _, y, x, height, w, count, seed in city:
    active = count > 0
    roof = [(x,y-height),(x+w,y-height+8),(x,y-height+16),(x-w,y-height+8)]
    left = [roof[3],roof[2],(x,y+16),(x-w,y+8)]
    right = [roof[2],roof[1],(x+w,y+8),(x,y+16)]
    poly(left, "url(#faceA)" if active else "url(#darkA)", .94 if active else .72)
    poly(right, "url(#faceB)" if active else "url(#darkB)", .92 if active else .76)
    poly(roof, "#b0ffe7" if active else "#266e83", 1 if active else .72, "#c5ffef" if active else "#23637a", .6)
    if active:
        add(f'<ellipse cx="{x:.1f}" cy="{y-height+11:.1f}" rx="{w+12}" ry="12" fill="#2bffe0" opacity=".19" filter="url(#brightglow)"/>')
    # Tiny rows of pixel windows are brighter on genuine contribution days.
    for k in range(16, int(height)-7, 17):
        yy = y-height+15+k
        op = ".9" if active else ".26"
        window = "#bdfff2" if active else "#60b8c9"
        for offset in (-9, 2):
            add(f'<path d="M{x+offset:.1f} {yy+5:.1f} l5 -2" stroke="{window}" opacity="{op}" stroke-width="1.7" stroke-linecap="round"/>')
            add(f'<path d="M{x+offset-14:.1f} {yy:.1f} l5 2" stroke="{window}" opacity="{op}" stroke-width="1.5" stroke-linecap="round"/>')

# Minimal terminal detail and footer.
add('<path d="M573 520H1225" stroke="#147a85" opacity=".7" stroke-width="1"/>')
txt(582, 535, "NEON CITY // POWERED BY REAL GITHUB CONTRIBUTION DATA", 11, "#70b1b8", extra='font-family="Consolas,monospace" letter-spacing=".3"')
add('</svg>')
dest = pathlib.Path("profile-3d-contrib/profile-night-green.svg")
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text("\n".join(out), encoding="utf-8")
print(f"Generated {dest}: {total} contributions, {active_days} active days, {len(last)} days visualized.")
