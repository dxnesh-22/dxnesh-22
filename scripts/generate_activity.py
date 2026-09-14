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

result = response.json()

if "errors" in result:
    raise Exception(result["errors"])

data = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]

total = data["totalContributions"]
weeks = data["weeks"]


# ==================================================
# CARD DIMENSIONS
# ==================================================

WIDTH = 900
HEIGHT = 430

LEFT = 55
TOP = 145

CELL = 12
GAP = 3


# ==================================================
# COLORS
# ==================================================

BACKGROUND = "#061326"
BORDER = "#168CFF"

EMPTY = "#0B1729"
LEVEL_1 = "#12345A"
LEVEL_2 = "#155A91"
LEVEL_3 = "#1689D4"
LEVEL_4 = "#28C7FF"


# ==================================================
# FIND MAX CONTRIBUTION COUNT
# ==================================================

all_counts = []

for week in weeks:
    for day in week["contributionDays"]:
        all_counts.append(day["contributionCount"])

max_count = max(all_counts, default=1)


def get_color(count):

    if count == 0:
        return EMPTY

    if max_count <= 1:
        return LEVEL_4

    ratio = count / max_count

    if ratio <= 0.20:
        return LEVEL_1

    elif ratio <= 0.40:
        return LEVEL_2

    elif ratio <= 0.65:
        return LEVEL_3

    else:
        return LEVEL_4


# ==================================================
# SVG START
# ==================================================

svg = f"""<svg
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}"
xmlns="http://www.w3.org/2000/svg">

<defs>

    <!-- Background gradient -->

    <linearGradient
        id="background"
        x1="0"
        y1="0"
        x2="1"
        y2="1">

        <stop
            offset="0%"
            stop-color="#061326"/>

        <stop
            offset="50%"
            stop-color="#0A1E38"/>

        <stop
            offset="100%"
            stop-color="#040C18"/>

    </linearGradient>


    <!-- Blue border -->

    <linearGradient
        id="border"
        x1="0"
        y1="0"
        x2="1"
        y2="0">

        <stop
            offset="0%"
            stop-color="#008CFF"/>

        <stop
            offset="50%"
            stop-color="#36C7FF"/>

        <stop
            offset="100%"
            stop-color="#0066FF"/>

    </linearGradient>


    <!-- Glow -->

    <filter id="glow">

        <feGaussianBlur
            stdDeviation="5"
            result="blur"/>

        <feMerge>

            <feMergeNode
                in="blur"/>

            <feMergeNode
                in="SourceGraphic"/>

        </feMerge>

    </filter>

</defs>


<!-- ==================================================
     BACKGROUND
     ================================================== -->

<rect
    width="{WIDTH}"
    height="{HEIGHT}"
    rx="24"
    fill="url(#background)"/>


<!-- Decorative blue glow -->

<circle
    cx="70"
    cy="30"
    r="130"
    fill="#008CFF"
    opacity="0.08"/>


<circle
    cx="850"
    cy="390"
    r="150"
    fill="#0066FF"
    opacity="0.07"/>


<!-- ==================================================
     GLASS BORDER
     ================================================== -->

<rect
    x="6"
    y="6"
    width="{WIDTH - 12}"
    height="{HEIGHT - 12}"
    rx="22"
    fill="none"
    stroke="url(#border)"
    stroke-width="2"
    filter="url(#glow)"/>


<!-- ==================================================
     TITLE
     ================================================== -->

<text
    x="40"
    y="55"
    font-family="Arial, sans-serif"
    font-size="27"
    font-weight="bold"
    fill="#EAF6FF">

    📈 My GitHub Activity

</text>


<text
    x="40"
    y="82"
    font-family="Arial, sans-serif"
    font-size="13"
    fill="#75BFFF">

    A visual representation of my contributions over time

</text>


<!-- ==================================================
     QUOTE GLASS PANEL
     ================================================== -->

<rect
    x="640"
    y="30"
    width="220"
    height="65"
    rx="16"
    fill="#0A2544"
    fill-opacity="0.65"
    stroke="#126AC0"/>


<text
    x="660"
    y="58"
    font-family="Arial"
    font-size="11"
    font-style="italic"
    fill="#9BD9FF">

    "Consistency compounds."

</text>


<text
    x="760"
    y="80"
    font-family="Arial"
    font-size="10"
    fill="#5DBBFF">

    — Dinesh N.

</text>
"""


# ==================================================
# MONTH LABELS
# ==================================================

# Track months already displayed
seen_months = set()

for week_index, week in enumerate(weeks):

    if not week["contributionDays"]:
        continue

    first_day = week["contributionDays"][0]

    date = datetime.strptime(
        first_day["date"],
        "%Y-%m-%d"
    )

    month = date.strftime("%b")

    if month in seen_months:
        continue

    seen_months.add(month)

    # Month label starts at the same x position
    # as the first contribution cell of that week.
    x = LEFT + week_index * (CELL + GAP)

    # Special handling for the first month.
    # This prevents September from touching
    # the left edge of the SVG.
    if week_index == 0:
        x = LEFT

    # Prevent labels from going beyond the card.
    if x <= WIDTH - 45:

        svg += f"""
<text
    x="{x}"
    y="{TOP - 20}"
    font-family="Arial, sans-serif"
    font-size="11"
    fill="#8FBDE5">

    {month}

</text>
"""


# ==================================================
# WEEKDAY LABELS
# ==================================================

weekday_labels = {
    1: "Mon",
    3: "Wed",
    5: "Fri"
}

for row, label in weekday_labels.items():

    y = TOP + row * (CELL + GAP) + 10

    svg += f"""
<text
    x="12"
    y="{y}"
    font-family="Arial, sans-serif"
    font-size="10"
    fill="#8FBDE5">

    {label}

</text>
"""


# ==================================================
# CONTRIBUTION GRID
# ==================================================

for week_index, week in enumerate(weeks):

    for row, day in enumerate(week["contributionDays"]):

        if row >= 7:
            continue

        x = LEFT + week_index * (CELL + GAP)

        y = TOP + row * (CELL + GAP)

        color = get_color(
            day["contributionCount"]
        )

        svg += f"""
<rect
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="3"
    fill="{color}"
    stroke="#102B49"
    stroke-width="0.7"/>
"""


# ==================================================
# TOTAL CONTRIBUTIONS
# ==================================================

svg += f"""

<!-- Contribution icon -->

<circle
    cx="55"
    cy="350"
    r="19"
    fill="#0A2544"
    stroke="#168CFF"/>


<text
    x="55"
    y="357"
    text-anchor="middle"
    font-family="Arial"
    font-size="15"
    fill="#FFFFFF">

    ★

</text>


<!-- Contribution label -->

<text
    x="85"
    y="347"
    font-family="Arial"
    font-size="13"
    fill="#A8D8FF">

    Total Contributions:

</text>


<!-- Contribution number -->

<text
    x="230"
    y="350"
    font-family="Arial"
    font-size="20"
    font-weight="bold"
    fill="#28C7FF">

    {total}

</text>
"""


# ==================================================
# CONTRIBUTION LEGEND
# ==================================================

svg += """

<text
    x="640"
    y="347"
    font-family="Arial"
    font-size="11"
    fill="#8FBDE5">

    Less

</text>
"""


legend_colors = [
    EMPTY,
    LEVEL_1,
    LEVEL_2,
    LEVEL_3,
    LEVEL_4
]

for i, color in enumerate(legend_colors):

    x = 675 + i * 24

    svg += f"""
<rect
    x="{x}"
    y="335"
    width="17"
    height="17"
    rx="3"
    fill="{color}"/>
"""


# ==================================================
# FOOTER
# ==================================================

svg += """

<text
    x="805"
    y="347"
    font-family="Arial"
    font-size="11"
    fill="#8FBDE5">

    More

</text>


<text
    x="450"
    y="400"
    text-anchor="middle"
    font-family="Arial"
    font-size="11"
    letter-spacing="4"
    fill="#1689FF">

    CODE • LEARN • BUILD • GROW

</text>


</svg>
"""


# ==================================================
# SAVE SVG
# ==================================================

os.makedirs(
    "profile",
    exist_ok=True
)

with open(
    "profile/activity.svg",
    "w",
    encoding="utf-8"
) as file:

    file.write(svg)


print(
    "GitHub activity SVG generated successfully!"
)
