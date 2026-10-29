# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Platforms like Spotify combine collaborative filtering (what similar users play) with content-based filtering (the songs' own attributes). My version is content-based only: it scores each song against one user's taste profile and recommends the top matches. It prioritizes **energy** and **valence**, which together capture a song's vibe, then uses **mood** and **genre** as supporting matches.

### `Song` features

- `genre`: categorical (pop, lofi, rock, ambient, jazz, synthwave, indie pop); related genres like pop and indie pop get partial credit
- `mood`: categorical (happy, chill, intense, relaxed, moody, focused); similar moods like chill, relaxed and focused get partial credit
- `energy`: 0–1, how calm or intense the song feels (main numeric feature)
- `valence`: 0–1, how happy or dark the song sounds (the only numeric feature independent of energy)
- `tempo_bpm`, `danceability`, `acousticness`: stored, but mostly redundant with energy
- `id`, `title`, `artist`: used for display only, not for scoring

### `UserProfile` features

- `favorite_genre`: compared against `Song.genre`
- `favorite_mood`: compared against `Song.mood`
- `target_energy`: the user's preferred energy level (0–1); songs closer to it score higher
- `likes_acoustic`: whether the user prefers acoustic songs; a light preference, since acousticness mostly mirrors low energy
- *Planned:* `target_valence`: the user's preferred happiness level (0–1), so valence can be scored the same way as energy

### Algorithm Recipe (vibe-first)

Each song gets a score from 0 to 1:

```
score = 0.35 × energy closeness
      + 0.25 × valence closeness
      + 0.20 × mood match
      + 0.20 × genre match
```

- **Closeness** = `1 − |song value − user target|`, so a perfect match is 1 and the opposite end of the scale is 0.
- **Mood match** = 1 for the exact mood, 0.5 for a mood in the same family, 0 otherwise:
  - calm: chill, relaxed, focused, dreamy
  - bright: happy, carefree, playful, euphoric, flirty, romantic, confident
  - dark: sad, melancholic, moody
  - intense: intense, angry
- **Genre match** = 1 for the exact genre, 0.5 for a related genre, 0 otherwise:
  - pop: pop, indie pop, edm, latin
  - chill: lofi, ambient, jazz
  - rock: rock, metal, shoegaze
  - roots: country, bluegrass
  - urban: hip hop, r&b
  - reggae, classical and synthwave have no related genres

To recommend, the system scores every song, sorts from highest to lowest and returns the top `k` (default 5). Each result includes a short explanation of which parts of the score it matched.

### Expected biases

- **Hand-made families:** the mood and genre groupings are my own judgment calls. Someone else might put "confident" with "intense" or treat metal and rock as unrelated.
- **Uneven catalog:** lofi has 3 songs while most genres have 1, so lofi fans get fuller lists. Reggae, classical and synthwave can never earn partial genre credit.
- **Extremes get buried:** closeness scoring favors songs near typical targets, so very intense (metal) or very quiet (classical) songs rarely surface unless a user asks for those extremes.
- **Filter bubble:** it only recommends more of what the user already said they like and never introduces anything surprising.
- **Sound, not meaning:** valence measures how happy the audio *sounds*, so a sad song with an upbeat beat will be treated as happy.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Excerpt from `python -m src.main` for the Chill Lofi profile (`favorite_genre="lofi"`, `favorite_mood="chill"`, `target_energy=0.40`, `target_valence=0.60`). All 7 profiles are under [Experiments You Tried](#experiments-you-tried).

```
Loading songs from data/songs.csv...
Loaded songs: 20

=== Chill Lofi ===
Top recommendations:

Midnight Coding - Score: 0.98
Because: energy 0.42 vs target 0.40 (+0.34); valence 0.56 vs target 0.60 (+0.24); mood 'chill' matches 'chill' (+0.20); genre 'lofi' matches 'lofi' (+0.20)

Library Rain - Score: 0.98
Because: energy 0.35 vs target 0.40 (+0.33); valence 0.60 vs target 0.60 (+0.25); mood 'chill' matches 'chill' (+0.20); genre 'lofi' matches 'lofi' (+0.20)

Focus Flow - Score: 0.90
Because: energy 0.40 vs target 0.40 (+0.35); valence 0.59 vs target 0.60 (+0.25); mood 'focused' is similar to 'chill' (+0.10); genre 'lofi' matches 'lofi' (+0.20)

Spacewalk Thoughts - Score: 0.85
Because: energy 0.28 vs target 0.40 (+0.31); valence 0.65 vs target 0.60 (+0.24); mood 'chill' matches 'chill' (+0.20); genre 'ambient' is similar to 'lofi' (+0.10)

Coffee Shop Stories - Score: 0.76
Because: energy 0.37 vs target 0.40 (+0.34); valence 0.71 vs target 0.60 (+0.22); mood 'relaxed' is similar to 'chill' (+0.10); genre 'jazz' is similar to 'lofi' (+0.10)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Stress test: 7 user profiles

`src/main.py` defines 7 profiles in `PROFILES`: three standard listeners and four adversarial ones built to trick the scoring.

| Profile | What it tests |
|---|---|
| High-Energy Pop | A normal, upbeat pop fan |
| Chill Lofi | A calm study listener |
| Deep Intense Rock | A loud, dark rock fan |
| Sad Banger | Conflicting wishes: very high energy (0.90) but a sad mood and dark valence (0.20) |
| Case Trap | Same numbers as High-Energy Pop, but typed `"Pop"` / `"Happy"` with capital letters |
| Ghost Genre | A genre and mood (`k-pop`, `nostalgic`) that don't exist in the catalog |
| Off the Charts | Out-of-range targets: energy 1.5, valence −0.5 |

Output of `python -m src.main` for each profile:

#### High-Energy Pop

```
=== High-Energy Pop ===
Top recommendations:

Sunrise City - Score: 0.99
Because: energy 0.82 vs target 0.85 (+0.34); valence 0.84 vs target 0.85 (+0.25); mood 'happy' matches 'happy' (+0.20); genre 'pop' matches 'pop' (+0.20)

Rooftop Lights - Score: 0.86
Because: energy 0.76 vs target 0.85 (+0.32); valence 0.81 vs target 0.85 (+0.24); mood 'happy' matches 'happy' (+0.20); genre 'indie pop' is similar to 'pop' (+0.10)

Neon Rapture - Score: 0.75
Because: energy 0.95 vs target 0.85 (+0.32); valence 0.90 vs target 0.85 (+0.24); mood 'euphoric' is similar to 'happy' (+0.10); genre 'edm' is similar to 'pop' (+0.10)

Gym Hero - Score: 0.75
Because: energy 0.93 vs target 0.85 (+0.32); valence 0.77 vs target 0.85 (+0.23); genre 'pop' matches 'pop' (+0.20)

Fuego Lento - Score: 0.73
Because: energy 0.72 vs target 0.85 (+0.30); valence 0.76 vs target 0.85 (+0.23); mood 'flirty' is similar to 'happy' (+0.10); genre 'latin' is similar to 'pop' (+0.10)
```

#### Chill Lofi

```
=== Chill Lofi ===
Top recommendations:

Midnight Coding - Score: 0.98
Because: energy 0.42 vs target 0.40 (+0.34); valence 0.56 vs target 0.60 (+0.24); mood 'chill' matches 'chill' (+0.20); genre 'lofi' matches 'lofi' (+0.20)

Library Rain - Score: 0.98
Because: energy 0.35 vs target 0.40 (+0.33); valence 0.60 vs target 0.60 (+0.25); mood 'chill' matches 'chill' (+0.20); genre 'lofi' matches 'lofi' (+0.20)

Focus Flow - Score: 0.90
Because: energy 0.40 vs target 0.40 (+0.35); valence 0.59 vs target 0.60 (+0.25); mood 'focused' is similar to 'chill' (+0.10); genre 'lofi' matches 'lofi' (+0.20)

Spacewalk Thoughts - Score: 0.85
Because: energy 0.28 vs target 0.40 (+0.31); valence 0.65 vs target 0.60 (+0.24); mood 'chill' matches 'chill' (+0.20); genre 'ambient' is similar to 'lofi' (+0.10)

Coffee Shop Stories - Score: 0.76
Because: energy 0.37 vs target 0.40 (+0.34); valence 0.71 vs target 0.60 (+0.22); mood 'relaxed' is similar to 'chill' (+0.10); genre 'jazz' is similar to 'lofi' (+0.10)
```

#### Deep Intense Rock

```
=== Deep Intense Rock ===
Top recommendations:

Storm Runner - Score: 0.96
Because: energy 0.91 vs target 0.92 (+0.35); valence 0.48 vs target 0.35 (+0.22); mood 'intense' matches 'intense' (+0.20); genre 'rock' matches 'rock' (+0.20)

Iron Verdict - Score: 0.74
Because: energy 0.97 vs target 0.92 (+0.33); valence 0.18 vs target 0.35 (+0.21); mood 'angry' is similar to 'intense' (+0.10); genre 'metal' is similar to 'rock' (+0.10)

Gym Hero - Score: 0.69
Because: energy 0.93 vs target 0.92 (+0.35); valence 0.77 vs target 0.35 (+0.14); mood 'intense' matches 'intense' (+0.20)

Faded Polaroids - Score: 0.55
Because: energy 0.52 vs target 0.92 (+0.21); valence 0.40 vs target 0.35 (+0.24); genre 'shoegaze' is similar to 'rock' (+0.10)

Night Drive Loop - Score: 0.51
Because: energy 0.75 vs target 0.92 (+0.29); valence 0.49 vs target 0.35 (+0.21)
```

#### Sad Banger (conflicting: high energy + sad)

```
=== Sad Banger (conflicting: high energy + sad) ===
Top recommendations:

Neon Rapture - Score: 0.61
Because: energy 0.95 vs target 0.90 (+0.33); valence 0.90 vs target 0.20 (+0.08); genre 'edm' matches 'edm' (+0.20)

Broken Porch Light - Score: 0.58
Because: energy 0.30 vs target 0.90 (+0.14); valence 0.22 vs target 0.20 (+0.24); mood 'sad' matches 'sad' (+0.20)

Night Drive Loop - Score: 0.57
Because: energy 0.75 vs target 0.90 (+0.30); valence 0.49 vs target 0.20 (+0.18); mood 'moody' is similar to 'sad' (+0.10)

Iron Verdict - Score: 0.57
Because: energy 0.97 vs target 0.90 (+0.33); valence 0.18 vs target 0.20 (+0.24)

Gym Hero - Score: 0.55
Because: energy 0.93 vs target 0.90 (+0.34); valence 0.77 vs target 0.20 (+0.11); genre 'pop' is similar to 'edm' (+0.10)
```

#### Case Trap ('Pop'/'Happy' capitalized)

```
=== Case Trap ('Pop'/'Happy' capitalized) ===
Top recommendations:

Barnyard Stomp - Score: 0.59
Because: energy 0.85 vs target 0.85 (+0.35); valence 0.88 vs target 0.85 (+0.24)

Sunrise City - Score: 0.59
Because: energy 0.82 vs target 0.85 (+0.34); valence 0.84 vs target 0.85 (+0.25)

Rooftop Lights - Score: 0.56
Because: energy 0.76 vs target 0.85 (+0.32); valence 0.81 vs target 0.85 (+0.24)

Neon Rapture - Score: 0.55
Because: energy 0.95 vs target 0.85 (+0.32); valence 0.90 vs target 0.85 (+0.24)

Gym Hero - Score: 0.55
Because: energy 0.93 vs target 0.85 (+0.32); valence 0.77 vs target 0.85 (+0.23)
```

#### Ghost Genre (k-pop/nostalgic, not in catalog)

```
=== Ghost Genre (k-pop/nostalgic, not in catalog) ===
Top recommendations:

Velvet Hours - Score: 0.55
Because: energy 0.48 vs target 0.60 (+0.31); valence 0.66 vs target 0.70 (+0.24)

Island Time - Score: 0.55
Because: energy 0.55 vs target 0.60 (+0.33); valence 0.85 vs target 0.70 (+0.21)

Fuego Lento - Score: 0.54
Because: energy 0.72 vs target 0.60 (+0.31); valence 0.76 vs target 0.70 (+0.23)

Concrete Crown - Score: 0.52
Because: energy 0.78 vs target 0.60 (+0.29); valence 0.62 vs target 0.70 (+0.23)

Coffee Shop Stories - Score: 0.52
Because: energy 0.37 vs target 0.60 (+0.27); valence 0.71 vs target 0.70 (+0.25)
```

#### Off the Charts (energy 1.5, valence -0.5)

```
=== Off the Charts (energy 1.5, valence -0.5) ===
Top recommendations:

Iron Verdict - Score: 0.64
Because: energy 0.97 vs target 1.50 (+0.16); valence 0.18 vs target -0.50 (+0.08); mood 'angry' matches 'angry' (+0.20); genre 'metal' matches 'metal' (+0.20)

Storm Runner - Score: 0.35
Because: energy 0.91 vs target 1.50 (+0.14); valence 0.48 vs target -0.50 (+0.01); mood 'intense' is similar to 'angry' (+0.10); genre 'rock' is similar to 'metal' (+0.10)

Gym Hero - Score: 0.18
Because: energy 0.93 vs target 1.50 (+0.15); valence 0.77 vs target -0.50 (+-0.07); mood 'intense' is similar to 'angry' (+0.10)

Faded Polaroids - Score: 0.13
Because: energy 0.52 vs target 1.50 (+0.01); valence 0.40 vs target -0.50 (+0.02); genre 'shoegaze' is similar to 'metal' (+0.10)

Night Drive Loop - Score: 0.09
Because: energy 0.75 vs target 1.50 (+0.09); valence 0.49 vs target -0.50 (+0.00)
```

### Experiment: weight shift (energy ×2, genre ×½)

I changed the weights from energy 0.35 / valence 0.25 / mood 0.20 / genre 0.20 to **energy 0.70 / valence 0.25 / mood 0.20 / genre 0.10**, re-ran all 7 profiles, then restored the original weights.

**Is the math still valid?** Yes, with one caveat. The weights now add up to 1.25 instead of 1.0, so the best possible score becomes 1.25 (the highest observed was 1.23) and scores can no longer be read as percentages. Rankings aren't distorted, because scaling every score by the same amount doesn't change the order. This is the same as using normalized weights of 0.56 / 0.20 / 0.16 / 0.08.

| Profile | Original top 5 | Weight-shift top 5 |
|---|---|---|
| High-Energy Pop | Sunrise City, Rooftop Lights, Neon Rapture, Gym Hero, Fuego Lento | Sunrise City, Rooftop Lights, **Barnyard Stomp**, Neon Rapture, Fuego Lento |
| Chill Lofi | Midnight Coding, Library Rain, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories | *(same order)* |
| Deep Intense Rock | Storm Runner, Iron Verdict, Gym Hero, Faded Polaroids, Night Drive Loop | Storm Runner, **Gym Hero**, Iron Verdict, Night Drive Loop, **Neon Rapture** |
| Sad Banger | Neon Rapture, Broken Porch Light, Night Drive Loop, Iron Verdict, Gym Hero | **Iron Verdict**, **Storm Runner**, Night Drive Loop, Neon Rapture, Gym Hero |

**More accurate or just different?** Mostly just different, and in some places worse:
- **Worse for High-Energy Pop:** *Barnyard Stomp*, an acoustic bluegrass song, jumps to #3 for a pop fan who doesn't like acoustic music, because its energy (0.85) is a perfect match.
- **Worse for Deep Intense Rock:** *Gym Hero* (pop, valence 0.77) moves above *Iron Verdict* (metal) for a dark rock fan.
- **Better for Sad Banger:** the slow country song *Broken Porch Light* drops out, and the top spot goes to *Iron Verdict*, which really is both high-energy and dark.
- **No change for Chill Lofi:** its lofi songs already match on every feature.

Doubling energy makes the system care mostly about *how intense* a song is, so songs from unrelated genres with the right intensity crowd in. I kept the original weights.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



