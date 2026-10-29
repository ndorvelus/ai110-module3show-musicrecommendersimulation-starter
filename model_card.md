# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Goal / Task

VibeMatch suggests songs a listener will probably like.
It looks at one user's taste profile.
It gives every song a score from 0 to 1.
Then it returns the top 5 songs, each with a short reason.

---

## 3. Data Used

- **Size:** 20 songs. The starter file had 10. I added 10 more.
- **Labels:** each song has a genre and a mood.
  There are 17 genres and 16 moods.
- **Numbers:** each song has energy, valence (how happy it sounds), tempo, danceability and acousticness.
  All are 0 to 1, except tempo, which is in beats per minute.
- **What I added:** genres like metal, classical, country and EDM.
  I also added sad and dark songs. The starter file had none.

**Limits:**

- The catalog is tiny.
- Most genres have only 1 song. Lofi has the most, with 3.
- The songs and their numbers are made up. Nobody measured them.
- There are no lyrics, no listening history and no data from other users.

---

## 4. Algorithm Summary

Think of it as a 100-point checklist for each song.

- **Energy (35 points):** how close is the song's energy to what the user wants?
- **Valence (25 points):** how close is the song's happiness to what the user wants?
- **Mood (20 points):** full points for the same mood.
  Half points for a similar mood, like "relaxed" instead of "chill."
- **Genre (20 points):** full points for the same genre.
  Half points for a related genre, like "indie pop" instead of "pop."

The closer a song is, the more points it gets.
The songs with the most points become the top 5.

Tempo, danceability and acousticness are not scored.
In this data they rise and fall with energy, so they would just count energy again.

---

## 5. Observed Behavior / Biases

**What works well:**

- Normal listeners get lists that make sense.
- The Chill Lofi profile gets 5 calm, mellow songs. It looks like a real study playlist.
- Every result explains its score, so you can see why a song was picked.

**Main bias: loud songs win too often.**

- Energy is worth the most points.
- Half the catalog is loud: 10 of 20 songs have energy above 0.70.
- *Gym Hero* (energy 0.93) showed up in 5 of my 7 test lists.
  It even showed up for the rock fan and the sad listener.
- The quietest song, *Nocturne in Grey*, never showed up at all.
- Someone who wants very quiet music gets weaker matches than everyone else.

**Other problems I found:**

- **Capital letters break it.** "Pop" does not match "pop." The user loses all genre and mood points.
- **Mixed wishes get split, not solved.** A user who wants loud *and* sad music gets some loud songs and some sad songs. No song is both.
- **Unknown genres fail quietly.** If the genre isn't in the catalog, the top score drops to 0.60. There is no warning.
- **No input checks.** An energy target of 1.5 gives negative points instead of an error.
- **Filter bubble.** It only suggests more of what the user already likes. It never surprises them.
- **Sound, not meaning.** A sad song with a happy beat counts as happy.

---

## 6. Evaluation Process

**Profiles I tested (7 total):**

- **Normal:** High-Energy Pop, Chill Lofi, Deep Intense Rock.
- **Tricky:**
  - Sad Banger: wants high energy but a sad mood.
  - Case Trap: same as High-Energy Pop, but typed "Pop" and "Happy" with capital letters.
  - Ghost Genre: asks for k-pop, which the catalog doesn't have.
  - Off the Charts: asks for energy 1.5, which is outside the 0 to 1 scale.

The full output for each profile is in the README under "Experiments You Tried."

**What I checked:**

- Does the #1 song make sense?
- Does the top 5 feel like one playlist?
- Does any song keep showing up where it doesn't belong?

**Does it feel right?**
Mostly yes for the normal profiles.
*Sunrise City* topped High-Energy Pop. It matches on every feature.
The worst miss was *Gym Hero* at #3 for the dark rock fan.
<!-- Add your own reaction here: which list would you actually listen to, and which song feels wrong to you? -->

**Why did *Neon Rapture* rank #1 for Sad Banger?**
It got 33 of 35 energy points and all 20 genre points.
But it sounds very happy, so it got only 8 of 25 valence points.
It still won because no song in the catalog is both loud and sad.

**Experiment: double energy, halve genre.**
The scores could go up to 1.25 instead of 1.0. The order still works.
The results got *different*, not better.
Sad Banger improved. Pop and Rock got worse.
For example, a bluegrass song jumped into the pop fan's top 3.
I changed the weights back.

**Comparing profiles:**

- **Pop vs. Lofi:** no songs in common. Pop gets loud, bright songs. Lofi gets quiet, mellow ones. That makes sense, because their energy targets are far apart.
- **Pop vs. Rock:** both want loud music, so both get loud songs. Pop gets happy ones. Rock gets dark ones. Valence is what tells them apart.
- **Lofi vs. Rock:** completely different lists. Rock's scores drop fast after #1 (0.96 to 0.74), because the catalog has only 1 rock song and 1 metal song.
- **Pop vs. Case Trap:** same numbers, different capital letters. Case Trap's scores drop by 0.30 to 0.40, and a bluegrass song ties for #1. That's a bug, not a taste difference.
- **Pop vs. Ghost Genre:** Pop's winner scores 0.99. Ghost Genre's best is only 0.55. With no genre match, the list is a random-looking mix.
- **Rock vs. Sad Banger:** both want loud, dark music. Rock gets a clean list. Sad Banger gets a messy one, because the only "sad" song is a slow country ballad.
- **Rock vs. Off the Charts:** both lists start with heavy songs, so the order still mostly works. But the scores sink toward zero, and one reason shows negative points.

**Why does *Gym Hero* keep showing up for people who want "Happy Pop"?**
*Gym Hero* is labeled "pop," so it gets all 20 genre points.
It's very loud, so it gets most of the 35 energy points.
It's labeled "intense," not "happy," so it gets no mood points.
But it sounds fairly cheerful, so it gets most of the valence points.
That adds up to about 75 out of 100. That's enough for the top 5.
In short, it's a workout song that sneaks in by being loud and labeled "pop."

---

## 7. Intended Use and Non-Intended Use

**Intended use:**

- A classroom project for learning how recommenders work.
- Trying out different weights and seeing what changes.
- Showing how simple rules can create bias.

**Not intended for:**

- Real users or a real music app.
- Large catalogs. It checks every song one by one.
- Making decisions about real artists, like who gets promoted or paid.
- Judging what someone "should" like. It only knows 4 things about a user.

---

## 8. Ideas for Improvement

1. **Fix the input bugs.** Ignore capital letters when matching genre and mood. Reject targets outside 0 to 1.
2. **Add variety to the top 5.** Limit how many songs from the same genre or energy level can appear, so one loud song can't win every list.
3. **Learn from behavior.** Use likes and skips to adjust each user's targets over time, instead of relying only on what they typed.

---

## 9. Personal Reflection

<!-- Write a few sentences in your own words:
- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps -->
