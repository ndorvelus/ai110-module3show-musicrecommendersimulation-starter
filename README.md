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

Output of `python -m src.main` for the late-night study profile (`favorite_genre="lofi"`, `favorite_mood="chill"`, `target_energy=0.40`, `target_valence=0.60`):

```
Loading songs from data/songs.csv...
Loaded songs: 20

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

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



