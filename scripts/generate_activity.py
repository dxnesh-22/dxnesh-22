import os
import requests
from datetime import datetime

USERNAME = "dxnesh-22"

query = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

token = os.environ["GITHUB_TOKEN"]

response = requests.post(
    "https://api.github.com/graphql",
    json={
        "query": query,
        "variables": {"login": USERNAME}
    },
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
)

response.raise_for_status()

data = response.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]

total = data["totalContributions"]

days = []

for week in data["weeks"]:
    for day in week["contributionDays"]:
        days.append({
            "date": day["date"],
            "count": day["contributionCount"]
        })

# Keep approximately one year of contributions
days = days[-371:]

# Contribution intensity
max_count = max([d["count"] for d in days], default=1)


def get_color(count):
    if count == 0:
        return "#0B1729"
    elif count <= max_count * 0.20:
        return "#12345A"
    elif count <= max_count * 0.40:
        return "#155A91"
    elif count <= max_count * 0.65:
        return "#1689D4"
    else:
        return "#28C7FF"


# SVG dimensions
WIDTH = 1100
HEIGHT = 500

left = 80
top = 170

cell = 18
gap = 4

svg = f"""<svg width="{WIDTH}" height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}"
xmlns="http://www.w3.org/2000/svg">

<defs>

  <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#061326"/>
    <stop offset="50%" stop-color="#0A1E38"/>
    <stop offset="100%" stop-color="#040C18"/>
  </linearGradient>

  <linearGradient id="border" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#008CFF"/>
    <stop offset="50%" stop-color="#36C7FF"/>
    <stop offset="100%" stop-color="#0066FF"/>
  </linearGradient>

  <filter id="glow">
    <feGaussianBlur stdDeviation="5" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>

</defs>

<!-- Background -->
<rect width="{WIDTH}" height="{HEIGHT}"
rx="28"
fill="url(#background)"/>

<!-- Decorative glow -->
<circle cx="80" cy="40" r="150"
fill="#008CFF"
opacity="0.08"/>

<circle cx="1030" cy="450" r="180"
fill="#0066FF"
opacity="0.08"/>

<!-- Glass border -->
<rect x="7" y="7"
width="{WIDTH-14}"
height="{HEIGHT-14}"
rx="25"
fill="none"
stroke="url(#border)"
stroke-width="2"
filter="url(#glow)"/>

<!-- Title -->
<text x="45" y="65"
font-family="Arial, sans-serif"
font-size="30"
font-weight="bold"
fill="#EAF6FF">
📈 My GitHub Activity
</text>

<text x="45" y="95"
font-family="Arial, sans-serif"
font-size="15"
fill="#75BFFF">
A visual representation of my contributions over time
</text>

<!-- Quote glass -->
<rect x="750" y="38"
width="300"
height="75"
rx="18"
fill="#0A2544"
fill-opacity="0.65"
stroke="#126AC0"/>

<text x="775" y="68"
font-family="Arial"
font-size="13"
font-style="italic"
fill="#8FD5FF">
"Consistency compounds."
</text>

<text x="900" y="94"
font-family="Arial"
font-size="12"
fill="#5DBBFF">
— Dinesh N.
</text>
"""

# Month labels
months = {}

for index, day in enumerate(days):
    date = datetime.strptime(day["date"], "%Y-%m-%d")

    week_index = index // 7

    if date.day <= 7:
        months[date.strftime("%b")] = week_index

for month, week_index in months.items():

    x = left + week_index * (cell + gap)

    svg += f"""
    <text x="{x}" y="{top - 25}"
    font-family="Arial"
    font-size="13"
    fill="#8FBDE5">
    {month}
    </text>
    """

# Weekday labels
weekday_labels = {
    0: "Mon",
    2: "Wed",
    4: "Fri"
}

for row, label in weekday_labels.items():

    y = top + row * (cell + gap) + 13

    svg += f"""
    <text x="35" y="{y}"
    font-family="Arial"
    font-size="12"
    fill="#8FBDE5">
    {label}
    </text>
    """

# Contribution cells
for index, day in enumerate(days):

    week = index // 7
    row = index % 7

    x = left + week * (cell + gap)
    y = top + row * (cell + gap)

    color = get_color(day["count"])

    svg += f"""
    <rect
      x="{x}"
      y="{y}"
      width="{cell}"
      height="{cell}"
      rx="4"
      fill="{color}"
      stroke="#102B49"
      stroke-width="1"/>
    """

# Bottom stats
svg += f"""

<!-- Bottom information -->
<circle cx="65" cy="415"
r="22"
fill="#0A2544"
stroke="#168CFF"/>

<text x="65" y="423"
text-anchor="middle"
font-family="Arial"
font-size="18"
fill="#FFFFFF">
★
</text>

<text x="100" y="413"
font-family="Arial"
font-size="16"
fill="#A8D8FF">
Total Contributions:
</text>

<text x="265" y="413"
font-family="Arial"
font-size="22"
font-weight="bold"
fill="#28C7FF">
{total}
</text>

<!-- Legend -->
<text x="785" y="415"
font-family="Arial"
font-size="13"
fill="#8FBDE5">
Less
</text>
"""

legend_colors = [
    "#0B1729",
    "#12345A",
    "#155A91",
    "#1689D4",
    "#28C7FF"
]

for i, color in enumerate(legend_colors):

    x = 830 + i * 32

    svg += f"""
    <rect x="{x}" y="399"
    width="22"
    height="22"
    rx="4"
    fill="{color}"/>
    """

svg += """

<text x="1005" y="415"
font-family="Arial"
font-size="13"
fill="#8FBDE5">
More
</text>

<!-- Footer -->
<text x="550" y="465"
text-anchor="middle"
font-family="Arial"
font-size="13"
letter-spacing="4"
fill="#168CFF">
CODE • LEARN • BUILD • GROW
</text>

</svg>
"""

os.makedirs("profile", exist_ok=True)

with open("profile/activity.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("GitHub activity SVG generated successfully!")
