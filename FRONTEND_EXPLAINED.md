# 🌐 Understanding the Frontend Code
### `rainfall_dashboard.html` — Explained for High School Students

---

## What is the "Frontend"?

If the backend is the kitchen, the **frontend** is the dining room — everything
the customer actually sees and touches. It is the visual part of any website
or app.

Our frontend is a single file called `rainfall_dashboard.html`. When you open
it in a browser, it becomes a full interactive dashboard with:
- Animated falling rain in the background
- Cards showing cities that are raining right now
- A search bar for any city in the world
- A bar chart comparing rainfall across months
- A language switcher and a light/dark theme toggle

All of this is built from just three technologies:

| Technology | What it does | Analogy |
|-----------|-------------|---------|
| **HTML** | Structures the page (the skeleton) | The frame of a building |
| **CSS** | Styles everything (colours, layout, animation) | The paint, furniture, and decorations |
| **JavaScript** | Makes things interactive and dynamic | The electrician who makes the lights switch on |

---

## The Big Picture: What Does the Dashboard Do?

```
┌──────────────────────────────────────────────────────────────┐
│               WHAT THE DASHBOARD DOES                        │
│                                                              │
│  STEP 1        STEP 2       STEP 3       STEP 4             │
│  --------      --------     --------     --------           │
│  Set up        Build the    Respond      Update             │
│  themes  ──▶   page     ──▶ to user ──▶  everything        │
│  & data        content      actions      on the screen      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 1 — Setting Up Themes and Data

Before the page even draws anything, JavaScript prepares two things:
the colour themes and the data.

### Colour themes (CSS variables)

CSS **variables** are like named paint colours you can reuse everywhere.
Instead of writing the same blue hex code in 50 places, you define it once
and reference it by name:

```css
:root {
    --rain1: #3b82f6;   /* a blue colour for rain */
    --rain2: #60a5fa;   /* a lighter blue */
}
```

Then anywhere you want that blue, you write `var(--rain1)` instead of
`#3b82f6`. If you ever want to change the colour, you only update one line.

For dark and light themes, we use **data attributes** — a label we attach
to the whole HTML document:

```css
[data-theme="dark"] {
    --bg: #0b1120;       /* very dark navy background */
    --text: #e2eaf4;     /* near-white text */
    --card: #141f30;     /* dark card colour */
}

[data-theme="light"] {
    --bg: #f0f6ff;       /* soft blue-white background */
    --text: #0f2040;     /* near-black text */
    --card: #ffffff;     /* pure white card colour */
}
```

When a user clicks the theme toggle, JavaScript flips the label from
`data-theme="dark"` to `data-theme="light"`, and instantly every element
that uses `var(--bg)` or `var(--text)` updates simultaneously — no
reloading, no extra code needed. That is the power of CSS variables.

### Data storage (JavaScript objects and arrays)

JavaScript stores the dashboard's data in named structures:

```javascript
const CITIES = [
    { name:"Tokyo", country:"Japan", flag:"🇯🇵", mm:22, temp:18, wind:14, humidity:84, type:"rain" },
    { name:"Mumbai", country:"India", flag:"🇮🇳", mm:67, temp:27, wind:22, humidity:95, type:"heavy" },
    // ... 10 more cities
];
```

This is an **array of objects**. An array `[...]` is an ordered list. Each
item in the list is an **object** `{...}` — a collection of named properties.
Think of it like a table: each city is a row, and its properties
(name, mm, temp) are the columns.

```javascript
const CITY_DB = {
    "london": { name:"London", today:8, monthly:62, annual:640, humidity:78, condition:"Light Rain", wind:18 },
    "tokyo":  { name:"Tokyo",  today:22, monthly:148, annual:1530, ... },
    // ... 20 more cities
};
```

`CITY_DB` is a **dictionary** (also called an object in JavaScript). Instead
of a numbered list, you look things up by name — like a real dictionary where
you look up "london" and find all the facts about London.

### Translations (multi-language support)

```javascript
const T = {
    en: { searchPh: "Search any city…", searchBtn: "Search", citiesTitle: "🌧 Cities Raining Right Now" },
    zh: { searchPh: "搜索全球任意城市…",   searchBtn: "搜索",  citiesTitle: "🌧 正在降雨的城市" },
    ar: { searchPh: "ابحث عن أي مدينة…",   searchBtn: "بحث",   citiesTitle: "🌧 المدن الممطرة الآن" },
    fr: { searchPh: "Rechercher une ville…",searchBtn: "Rechercher", citiesTitle: "🌧 Villes sous la pluie" },
};
```

`T` holds all four languages. When a user picks a language, we simply swap
which set of text strings we use. `T['zh']` gives us all the Chinese text,
`T['fr']` gives us all the French text — same structure, different words.

---

## Step 2 — Building the Page Content

### The HTML skeleton

HTML uses **tags** — pairs of angle-bracket labels that wrap content:

```html
<div class="city-card">
    <div class="city-name">🇯🇵 Tokyo</div>
    <div class="city-mm">22 mm</div>
</div>
```

`<div>` is a generic box (short for "division"). The `class` attribute gives
the box a name so CSS can style it and JavaScript can find it.

The page is structured like a set of nested boxes:

```
<body>
  ├── <nav class="topbar">          ← The top navigation bar
  │     ├── Logo
  │     ├── Language switcher
  │     └── Theme toggle
  │
  ├── <div class="search-section">  ← The search bar
  │
  └── <div class="wrap">            ← Main content area
        ├── Hero stats (4 cards)
        ├── City cards grid
        ├── Monthly chart
        └── Station table
```

### Generating cards with JavaScript

Instead of writing 12 city cards by hand in HTML, JavaScript builds them
automatically from the `CITIES` array:

```javascript
function renderCities() {
    const grid = document.getElementById('cities-grid');
    const maxMm = Math.max(...CITIES.map(c => c.mm));   // find the highest rainfall

    grid.innerHTML = CITIES.map(c => {
        const pct = Math.round(c.mm / maxMm * 100);     // what % of max is this city?
        return `
            <div class="city-card" onclick="searchCity('${c.name.toLowerCase()}')">
                <div class="city-name">${c.flag} ${c.name}</div>
                <div class="city-mm">${c.mm} mm</div>
                <div class="mini-fill" style="width:${pct}%"></div>
            </div>`;
    }).join('');
}
```

Let's unpack this step by step:

1. `document.getElementById('cities-grid')` — finds the HTML element with the
   id `cities-grid`. Think of it like calling a person's name and they raise
   their hand.

2. `Math.max(...CITIES.map(c => c.mm))` — extracts just the `mm` value from
   every city (`map`), then finds the maximum of all those values. The `...`
   (spread operator) "unpacks" the array into individual arguments for `Math.max`.

3. `.map(c => ...)` — transforms every item in `CITIES` into an HTML string.
   Arrow functions `c => expression` are a short way of writing a function
   that takes `c` (one city) and returns something.

4. The backtick strings `` `<div>${c.name}</div>` `` are **template literals** —
   they let you embed variable values directly inside a string using `${...}`.

5. `.join('')` — sticks all those HTML strings together into one big string
   with no gaps between them.

6. `grid.innerHTML = ...` — pours the finished HTML string into the grid
   element, instantly populating the page with 12 city cards.

### The bar chart (Chart.js)

Drawing a bar chart from scratch involves a lot of complex maths (calculating
pixel positions for every bar, drawing axes, handling hover states). Instead,
we use a library called **Chart.js** — a pre-built tool that does all of that
for us:

```javascript
chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
        datasets: [
            { label: '2024', data: [45,52,68,82,95,114,87,91,76,58,43,61], backgroundColor: 'rgba(59,130,246,0.75)' },
            { label: '2023', data: [38,49,72,78,88,108,82,95,70,52,38,55], backgroundColor: 'rgba(255,255,255,0.10)' }
        ]
    },
    options: { responsive: true, maintainAspectRatio: false }
});
```

We give Chart.js three things:
- **type** — what kind of chart (`'bar'`, `'line'`, `'pie'`, etc.)
- **data** — the labels and numbers to plot
- **options** — how it should look and behave

Chart.js does all the drawing work using an HTML `<canvas>` element — a
blank rectangular area on the page that JavaScript can draw shapes on
pixel by pixel (like a digital whiteboard).

---

## Step 3 — Responding to User Actions

### The search bar

```javascript
function onSearchInput(val) {
    const q = val.toLowerCase();
    const filtered = SUGGESTIONS.filter(s => s.city.toLowerCase().includes(q));
    // Show matching suggestions in the dropdown
}
```

Every time the user types a letter, `onSearchInput` runs. It:
1. Converts the typed text to lowercase so "London" and "london" both match
2. `.filter()` keeps only the suggestions that **include** the typed text
3. Updates the dropdown list with the matching results

This runs on every single keystroke — that is how autocomplete works.

```javascript
function searchCity(key) {
    const data = CITY_DB[key] || CITY_DB[Object.keys(CITY_DB).find(k => k.includes(key))];

    if (!data) {
        // City not found — generate fake data
        const fake = {
            today: Math.round(Math.random() * 40),
            monthly: Math.round(30 + Math.random() * 150),
            // ...
        };
        showResult(fake);
    } else {
        showResult(data);  // City found — show real data
    }
}
```

`CITY_DB[key]` tries to look up the city directly by name. The `||` (OR operator)
means "if that fails, try the next thing." `Object.keys(CITY_DB).find(...)` searches
all the keys (city names) for a partial match — so searching "lon" would
still find "london."

`Math.random()` generates a random number between 0 and 1. Multiplying it by
40 gives a random number between 0 and 40. This is used to simulate data for
cities that are not in our database, so the search never returns an empty result.

### The theme toggle

```javascript
function toggleTheme() {
    theme = theme === 'dark' ? 'light' : 'dark';    // flip between dark and light
    document.documentElement.setAttribute('data-theme', theme);  // update the label
    document.getElementById('theme-thumb').textContent = theme === 'dark' ? '🌙' : '☀️';
    renderChart();  // redraw the chart with the new colour palette
}
```

`theme === 'dark' ? 'light' : 'dark'` is called a **ternary operator** — a
compact if-else. Read it as: "if theme equals dark, use light, otherwise use dark."

`document.documentElement` refers to the `<html>` element at the very root of
the page. Setting `data-theme` on it triggers the CSS variable swap that changes
every colour simultaneously.

### The language switcher

```javascript
function setLang(l) {
    lang = l;   // remember the chosen language
    document.getElementById('lang-flag').textContent = LANG_FLAGS[l];  // update the flag icon

    // Update every piece of text on the page
    document.getElementById('search-input').placeholder = T[lang].searchPh;
    document.getElementById('search-btn').textContent   = T[lang].searchBtn;
    document.getElementById('cities-title').textContent = T[lang].citiesTitle;
    // ... and so on for every label
}
```

`T[lang]` uses the `lang` variable (e.g. `'zh'`) to pick the right set of
translations from our `T` object. Then we find each element by its id and
replace its text content.

Arabic also needs the whole page to be read right-to-left:

```javascript
document.body.style.direction = lang === 'ar' ? 'rtl' : 'ltr';
```

One line of JavaScript flips the entire reading direction of the page.

---

## Step 4 — Updating Everything on Screen

### The rain animation

```javascript
(function spawnRain() {
    const bg = document.getElementById('rain-bg');
    for (let i = 0; i < 55; i++) {
        const d = document.createElement('div');
        d.className = 'raindrop';
        d.style.cssText = `
            left: ${Math.random() * 100}%;
            height: ${12 + Math.random() * 22}px;
            animation-duration: ${0.7 + Math.random() * 1.4}s;
            animation-delay: -${Math.random() * 2}s;
        `;
        bg.appendChild(d);
    }
})();
```

This creates 55 individual raindrop elements and places each at a random
horizontal position (`left: X%`) with a random height, speed, and start
time. The function is immediately called — notice the `()` at the very end.
This is called an **IIFE** (Immediately Invoked Function Expression).

The actual movement is handled by CSS:

```css
@keyframes fall {
    0%   { transform: translateY(0);     opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: 0.6; }
    100% { transform: translateY(110vh); opacity: 0; }
}
```

`@keyframes` defines an animation — here, a raindrop starting at the top
(0%), becoming visible, moving down to 110% of the viewport height, and
fading out. CSS loops this animation automatically using `animation: fall
linear infinite` — no JavaScript needed once the drops are created.

### The init function

```javascript
applyLang();   // called once when the page first loads
```

This single line at the very end kicks everything off. It calls `applyLang()`,
which calls `renderCities()`, `renderTable()`, and `renderChart()` — filling
the entire page with content in one go.

---

## How HTML, CSS, and JavaScript Work Together

Here is a concrete example: the city cards.

```
  HTML defines the container:          CSS styles the cards:
  ┌──────────────────────┐             ┌────────────────────────────────┐
  │ <div id="cities-grid"│             │ .city-card {                   │
  │ class="cities-grid"> │             │   background: var(--card);     │
  │ </div>               │             │   border-radius: 16px;         │
  └──────────────────────┘             │   transition: all 0.25s;       │
                                       │ }                              │
                                       └────────────────────────────────┘

  JavaScript fills it with content:
  ┌───────────────────────────────────────────────────────────┐
  │ grid.innerHTML = CITIES.map(c =>                          │
  │     `<div class="city-card">                              │
  │         <div class="city-name">${c.flag} ${c.name}</div>  │
  │         <div class="city-mm">${c.mm} mm</div>             │
  │      </div>`                                              │
  │ ).join('')                                                │
  └───────────────────────────────────────────────────────────┘

  Result the user sees:
  ┌────────────────────────────────────────────────┐
  │  🇯🇵 Tokyo      🇮🇳 Mumbai     🇬🇧 London        │
  │  22 mm          67 mm          8 mm            │
  │  ██████         ████████████   ██              │
  └────────────────────────────────────────────────┘
```

---

## Key Concepts to Remember

| Concept | What it means | Example in the code |
|---------|--------------|---------------------|
| **HTML tag** | A labelled box wrapping content | `<div class="city-card">...</div>` |
| **CSS class** | A style rule applied to elements | `.city-card { border-radius: 16px }` |
| **CSS variable** | A named, reusable value | `var(--rain1)` for a blue colour |
| **Data attribute** | A custom label on an HTML element | `data-theme="dark"` |
| **Array** | An ordered list of items | `const CITIES = [...]` |
| **Object** | A collection of named properties | `{ name:"Tokyo", mm:22 }` |
| **Function** | A reusable block of code | `function renderCities() { ... }` |
| **Event** | Something the user does | Typing, clicking, pressing Enter |
| **Template literal** | A string with variable values inside | `` `${c.name} — ${c.mm} mm` `` |
| **filter()** | Keep only matching items from an array | Finding cities matching the search |
| **map()** | Transform every item in an array | Turning city objects into HTML strings |
| **innerHTML** | The HTML content inside an element | Setting card content dynamically |

---

## Try It Yourself — Mini Challenges

1. **Change a colour** — Open `rainfall_dashboard.html` in a text editor.
   Find `--rain1:#3b82f6` and change it to `--rain1:#e11d48` (red).
   Open the file in your browser. What changed?

2. **Add your city** — Find the `CITY_DB` object and add your nearest city:
   ```javascript
   "yourcity": { name:"Your City", country:"Your Country",
                 today:5, monthly:45, annual:600,
                 humidity:70, condition:"Cloudy", wind:12 }
   ```
   Then search for it in the dashboard.

3. **Change rain speed** — Find `animation-duration:${0.7+Math.random()*1.4}s`
   and change `0.7` to `2.0`. Reload the page. What happens to the rain?

4. **Add a 5th language** — Copy the `en` block in `const T = {...}` and
   translate all the values into Spanish (or any language you know). Add a
   🇪🇸 button to the language menu.

5. **Increase the raindrop count** — Find `for (let i = 0; i < 55; i++)` and
   change `55` to `150`. What happens?

---

*Great work! You now understand how a real web dashboard is built
using HTML, CSS, and JavaScript working together as a team.*
