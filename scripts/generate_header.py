import os

WIDTH = 1000
HEIGHT = 500

svg = f"""<svg
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}"
xmlns="http://www.w3.org/2000/svg">

<defs>

    <!-- Background -->
    <linearGradient id="bg"
        x1="0" y1="0"
        x2="1" y2="1">

        <stop offset="0%" stop-color="#020B18"/>
        <stop offset="50%" stop-color="#061A32"/>
        <stop offset="100%" stop-color="#020812"/>

    </linearGradient>

    <!-- Border -->
    <linearGradient id="border"
        x1="0" y1="0"
        x2="1" y2="0">

        <stop offset="0%" stop-color="#008CFF"/>
        <stop offset="50%" stop-color="#36D7FF"/>
        <stop offset="100%" stop-color="#0066FF"/>

    </linearGradient>

    <!-- Text gradient -->
    <linearGradient id="name"
        x1="0" y1="0"
        x2="1" y2="0">

        <stop offset="0%" stop-color="#FFFFFF"/>
        <stop offset="55%" stop-color="#28D7FF"/>
        <stop offset="100%" stop-color="#168CFF"/>

    </linearGradient>

    <!-- Glow -->
    <filter id="glow">

        <feGaussianBlur
            stdDeviation="5"
            result="blur"/>

        <feMerge>

            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>

        </feMerge>

    </filter>

</defs>


<!-- ==================================================
     BACKGROUND
     ================================================== -->

<rect
    width="{WIDTH}"
    height="{HEIGHT}"
    rx="28"
    fill="url(#bg)"/>


<!-- ==================================================
     DECORATIVE GLOW
     ================================================== -->

<circle
    cx="70"
    cy="60"
    r="170"
    fill="#008CFF"
    opacity="0.08"/>

<circle
    cx="930"
    cy="420"
    r="190"
    fill="#0066FF"
    opacity="0.07"/>


<!-- ==================================================
     GLASS BORDER
     ================================================== -->

<rect
    x="7"
    y="7"
    width="{WIDTH - 14}"
    height="{HEIGHT - 14}"
    rx="25"
    fill="none"
    stroke="url(#border)"
    stroke-width="2"
    filter="url(#glow)"/>


<!-- ==================================================
     STATUS
     ================================================== -->

<rect
    x="45"
    y="35"
    width="210"
    height="38"
    rx="19"
    fill="#0A2544"
    fill-opacity="0.75"
    stroke="#126AC0"/>

<circle
    cx="68"
    cy="54"
    r="6"
    fill="#38FF88"/>

<text
    x="84"
    y="59"
    font-family="Arial, sans-serif"
    font-size="13"
    fill="#A8DCFF">

    Available for Opportunities

</text>


<!-- ==================================================
     MAIN TITLE
     ================================================== -->

<text
    x="500"
    y="145"
    text-anchor="middle"
    font-family="Arial, sans-serif"
    font-size="48"
    font-weight="bold"
    fill="url(#name)">

    👋 Hey, I'm Dinesh N

</text>


<!-- ==================================================
     ROLE
     ================================================== -->

<text
    x="500"
    y="190"
    text-anchor="middle"
    font-family="Arial, sans-serif"
    font-size="20"
    font-weight="bold"
    fill="#EAF6FF">

    💻 Computer Science Engineering Student

</text>


<text
    x="500"
    y="220"
    text-anchor="middle"
    font-family="Arial, sans-serif"
    font-size="17"
    fill="#8FCBFF">

    Developer • AI Enthusiast • Problem Solver

</text>


<!-- ==================================================
     TERMINAL GLASS PANEL
     ================================================== -->

<rect
    x="170"
    y="250"
    width="660"
    height="65"
    rx="18"
    fill="#061B32"
    fill-opacity="0.85"
    stroke="#008CFF"
    stroke-width="1.5"/>


<!-- Terminal prompt -->

<text
    x="195"
    y="291"
    font-family="monospace"
    font-size="18"
    font-weight="bold"
    fill="#28D7FF">

    &gt; Building the future, one line of code at a time...

</text>


<!-- Blinking cursor -->

<rect
    x="795"
    y="273"
    width="3"
    height="25"
    fill="#28D7FF">

    <animate
        attributeName="opacity"
        values="1;0;1"
        dur="1s"
        repeatCount="indefinite"/>

</rect>


<!-- ==================================================
     JOURNEY
     ================================================== -->

<!-- ==================================================
     SOCIAL LINKS
     ================================================== -->

<a href="YOUR_PORTFOLIO_URL">
    <text
        x="300"
        y="360"
        text-anchor="middle"
        font-family="Arial"
        font-size="28"
        fill="#28C7FF">

        🌐

    </text>

    <text
        x="300"
        y="385"
        text-anchor="middle"
        font-family="Arial"
        font-size="13"
        fill="#A8D8FF">

        PORTFOLIO

    </text>
</a>


<a href="YOUR_LINKEDIN_URL">
    <text
        x="500"
        y="360"
        text-anchor="middle"
        font-family="Arial"
        font-size="28"
        fill="#28C7FF">

        💼

    </text>

    <text
        x="500"
        y="385"
        text-anchor="middle"
        font-family="Arial"
        font-size="13"
        fill="#A8D8FF">

        LINKEDIN

    </text>
</a>


<a href="https://github.com/dxnesh-22">
    <text
        x="700"
        y="360"
        text-anchor="middle"
        font-family="Arial"
        font-size="28"
        fill="#28C7FF">

        🐙

    </text>

    <text
        x="700"
        y="385"
        text-anchor="middle"
        font-family="Arial"
        font-size="13"
        fill="#A8D8FF">

        GITHUB

    </text>
</a>


<!-- ==================================================
     FOOTER
     ================================================== -->

<text
    x="500"
    y="445"
    text-anchor="middle"
    font-family="Arial"
    font-size="12"
    letter-spacing="5"
    fill="#168CFF">

    CODE • LEARN • BUILD • GROW

</text>


</svg>
"""


# ==================================================
# SAVE
# ==================================================

os.makedirs("profile", exist_ok=True)

with open(
    "profile/header.svg",
    "w",
    encoding="utf-8"
) as file:

    file.write(svg)


print("Glass GitHub header generated successfully!")
