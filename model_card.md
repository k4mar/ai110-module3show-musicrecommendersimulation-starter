# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests 5 songs from a small catalog based on a user's favorite genre, favorite mood, preferred energy level and whether they like acoustic music. It assumes the user can describe their taste with one genre and one mood. It's built for classroom exploration, to show how recommenders turn data into rankings. It isn't meant for real users.

**Not intended for:** real music apps, users whose taste spans many genres, or any decision that matters. It has no listening history, so it can't learn or improve over time.

---

## 3. How the Model Works

Every song gets points:

- **2 points** if its genre is the user's favorite genre.
- **1 point** if its mood is the user's favorite mood.
- **Up to 1 point** for energy. The closer the song's energy is to what the user wants, the more points it gets. A perfect match gets the full point, and a song at the opposite end gets close to zero.
- **0.5 points** if the song's acoustic feel (acoustic vs. electronic/produced) matches what the user likes.

Then every song in the catalog is sorted by points and the top 5 are shown, each with a list of reasons.

**Changes from the starter:** I filled in the empty functions. I added the acoustic bonus using the `likes_acoustic` field from `UserProfile`. I made the energy rule reward closeness instead of "more is better". I made each score return human-readable reasons.

---

## 4. Data

- **18 songs**: the 10 starter songs plus 8 I added.
- **Genres (14):** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, country, edm, r&b, folk, metal, classical, reggae.
- **Moods (13):** happy, chill, intense, relaxed, moody, focused, confident, nostalgic, euphoric, romantic, sad, angry, peaceful.
- **Numeric features:** energy, tempo_bpm, valence, danceability, acousticness (all 0–1 except tempo).
- **Limits:** lofi has 3 songs and pop has 2. Most other genres have only 1. The songs are made up, not real tracks. Many kinds of taste are missing: lyrics, language, era, popularity, regional genres like afrobeats or k-pop.

---

## 5. Strengths

- When a user's genre, mood and energy all line up with a song, that song lands at #1 every time. Examples: *Library Rain* for Chill Lofi, *Storm Runner* for Deep Intense Rock, *Sunrise City* for High-Energy Pop.
- The energy closeness rule works well as a tiebreaker. Among songs with no label match, the ones with the right energy rise to the top. For Chill Lofi, ranks 4–5 were ambient and jazz songs, which actually feel chill.
- Every result explains itself, so it's easy to see why a song showed up.

---

## 6. Limitations and Bias

The biggest weakness I found is that **genre labels dominate the score, and they use exact text matching**. A genre plus mood match is worth 3 points, while energy can only add 1. So *Gym Hero*, an intense workout track, comes in #2 for someone who wants happy pop, just because it's labeled "pop". Meanwhile *Rooftop Lights*, which is happy and has nearly the right energy, falls to #3 because it's labeled "indie pop" instead of "pop". The exact matching also creates a filter bubble against users whose genre isn't in the catalog: a k-pop fan never gets any genre points. In the "conflicted" test (wants high energy but a sad mood), the system picked a slow 0.30-energy folk song as #1 because the labels matched, and ignored the energy request almost completely.

---

## 7. Evaluation

I tested 5 profiles: three normal ones and two edge cases designed to trick the scoring. For each, I checked whether the top 5 "felt" right.

**High-Energy Pop**
```
========================================================================
Profile: High-Energy Pop
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
------------------------------------------------------------------------
1. Sunrise City by Neon Echo (pop, happy)
   Score: 4.48
   Because: genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.80 (+0.98); non-acoustic sound fits your taste (+0.5)
2. Gym Hero by Max Pulse (pop, intense)
   Score: 3.37
   Because: genre match (+2.0); energy 0.93 vs target 0.80 (+0.87); non-acoustic sound fits your taste (+0.5)
3. Rooftop Lights by Indigo Parade (indie pop, happy)
   Score: 2.46
   Because: mood match (+1.0); energy 0.76 vs target 0.80 (+0.96); non-acoustic sound fits your taste (+0.5)
4. Concrete Crown by Blockwise (hip hop, confident)
   Score: 1.48
   Because: energy 0.78 vs target 0.80 (+0.98); non-acoustic sound fits your taste (+0.5)
5. Night Drive Loop by Neon Echo (synthwave, moody)
   Score: 1.45
   Because: energy 0.75 vs target 0.80 (+0.95); non-acoustic sound fits your taste (+0.5)
```

**Chill Lofi**
```
========================================================================
Profile: Chill Lofi
Prefs:   {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
------------------------------------------------------------------------
1. Library Rain by Paper Lanterns (lofi, chill)
   Score: 4.50
   Because: genre match (+2.0); mood match (+1.0); energy 0.35 vs target 0.35 (+1.00); acoustic sound fits your taste (+0.5)
2. Midnight Coding by LoRoom (lofi, chill)
   Score: 4.43
   Because: genre match (+2.0); mood match (+1.0); energy 0.42 vs target 0.35 (+0.93); acoustic sound fits your taste (+0.5)
3. Focus Flow by LoRoom (lofi, focused)
   Score: 3.45
   Because: genre match (+2.0); energy 0.40 vs target 0.35 (+0.95); acoustic sound fits your taste (+0.5)
4. Spacewalk Thoughts by Orbit Bloom (ambient, chill)
   Score: 2.43
   Because: mood match (+1.0); energy 0.28 vs target 0.35 (+0.93); acoustic sound fits your taste (+0.5)
5. Coffee Shop Stories by Slow Stereo (jazz, relaxed)
   Score: 1.48
   Because: energy 0.37 vs target 0.35 (+0.98); acoustic sound fits your taste (+0.5)
```

**Deep Intense Rock**
```
========================================================================
Profile: Deep Intense Rock
Prefs:   {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}
------------------------------------------------------------------------
1. Storm Runner by Voltline (rock, intense)
   Score: 4.49
   Because: genre match (+2.0); mood match (+1.0); energy 0.91 vs target 0.90 (+0.99); non-acoustic sound fits your taste (+0.5)
2. Gym Hero by Max Pulse (pop, intense)
   Score: 2.47
   Because: mood match (+1.0); energy 0.93 vs target 0.90 (+0.97); non-acoustic sound fits your taste (+0.5)
3. Bassline Fever by DJ Kairo (edm, euphoric)
   Score: 1.44
   Because: energy 0.96 vs target 0.90 (+0.94); non-acoustic sound fits your taste (+0.5)
4. Iron Verdict by Skullforge (metal, angry)
   Score: 1.43
   Because: energy 0.97 vs target 0.90 (+0.93); non-acoustic sound fits your taste (+0.5)
5. Sunrise City by Neon Echo (pop, happy)
   Score: 1.42
   Because: energy 0.82 vs target 0.90 (+0.92); non-acoustic sound fits your taste (+0.5)
```

**Edge case: Conflicted (high energy + sad)**
```
========================================================================
Profile: Conflicted (high energy + sad)
Prefs:   {'genre': 'folk', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': True}
------------------------------------------------------------------------
1. Grey Skies Again by The Hollow Pines (folk, sad)
   Score: 3.90
   Because: genre match (+2.0); mood match (+1.0); energy 0.30 vs target 0.90 (+0.40); acoustic sound fits your taste (+0.5)
2. Porch Light Hymn by Willow Creek (country, nostalgic)
   Score: 1.05
   Because: energy 0.45 vs target 0.90 (+0.55); acoustic sound fits your taste (+0.5)
3. Midnight Coding by LoRoom (lofi, chill)
   Score: 1.02
   Because: energy 0.42 vs target 0.90 (+0.52); acoustic sound fits your taste (+0.5)
4. Focus Flow by LoRoom (lofi, focused)
   Score: 1.00
   Because: energy 0.40 vs target 0.90 (+0.50); acoustic sound fits your taste (+0.5)
5. Storm Runner by Voltline (rock, intense)
   Score: 0.99
   Because: energy 0.91 vs target 0.90 (+0.99)
```

**Edge case: Unknown Genre (k-pop)**
```
========================================================================
Profile: Unknown Genre (k-pop)
Prefs:   {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.7, 'likes_acoustic': False}
------------------------------------------------------------------------
1. Rooftop Lights by Indigo Parade (indie pop, happy)
   Score: 2.44
   Because: mood match (+1.0); energy 0.76 vs target 0.70 (+0.94); non-acoustic sound fits your taste (+0.5)
2. Sunrise City by Neon Echo (pop, happy)
   Score: 2.38
   Because: mood match (+1.0); energy 0.82 vs target 0.70 (+0.88); non-acoustic sound fits your taste (+0.5)
3. Night Drive Loop by Neon Echo (synthwave, moody)
   Score: 1.45
   Because: energy 0.75 vs target 0.70 (+0.95); non-acoustic sound fits your taste (+0.5)
4. Concrete Crown by Blockwise (hip hop, confident)
   Score: 1.42
   Because: energy 0.78 vs target 0.70 (+0.92); non-acoustic sound fits your taste (+0.5)
5. Island Sway by Tide & Palm (reggae, relaxed)
   Score: 1.35
   Because: energy 0.55 vs target 0.70 (+0.85); non-acoustic sound fits your taste (+0.5)
```

**Comparing profiles**

- **High-Energy Pop vs. Chill Lofi:** The pop list is all upbeat, electronic songs around 0.75–0.93 energy. The lofi list moves to quiet, acoustic songs around 0.28–0.42. That makes sense: the energy target and the acoustic preference are opposites, so the two lists share no songs.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy, so they overlap. *Gym Hero* shows up in both: for pop because of its genre, and for rock because its mood is "intense". *Sunrise City* is #1 for pop but only #5 for rock, where it gets in on energy alone.
- **Chill Lofi vs. Deep Intense Rock:** Complete opposites, with no shared songs. Rock's list after #2 is filled with EDM and metal purely because of high energy, which shows the catalog has only one real rock song.
- **Deep Intense Rock vs. Conflicted:** Both ask for 0.9 energy, but the conflicted user's #1 is a 0.30-energy folk ballad. The label match (3 points) beats the energy mismatch (only 0.6 points lost). The one song that fits the energy request, *Storm Runner*, falls to #5.
- **High-Energy Pop vs. Unknown Genre (k-pop):** Similar targets, but the k-pop user gets no genre points, so happy-mood songs win. *Rooftop Lights* even beats *Sunrise City* here, because 0.76 is closer to the 0.7 target.

**Why "Gym Hero" keeps showing up for Happy Pop fans, in plain language:** the system gives a big bonus just for having the same genre label as your favorite. Gym Hero is labeled "pop", so it collects that bonus even though it's an intense workout song, not a happy one. The system can't tell that two "pop" songs can feel completely different.

**What surprised me:** <!-- TODO (Kamar): in your own words — e.g. how much the conflicted profile ignored energy, or that k-pop got zero genre credit -->

**Experiment (weight shift):** I halved the genre weight (2.0 → 1.0) and doubled the energy weight (1.0 → 2.0). For High-Energy Pop, *Rooftop Lights* passed *Gym Hero* for #2, which is a more accurate result. For Chill Lofi and Rock, the #1 pick stayed the same, but non-matching genres with the right energy got closer to the top. Full output is in the README.

**Tests:** 5 pytest tests pass. They check sorting, explanations, CSV number conversion, and that energy rewards closeness rather than size.

---

## 8. Future Work

1. **Fuzzy or related genres:** give partial credit for related genres (indie pop ≈ pop, metal ≈ rock), so labels don't create hard walls.
2. **Use more features:** score valence (happiness) and tempo too, so a "happy" user is matched by how a song actually sounds, not only by its label.
3. **Diversity rule:** penalize repeat artists and genres in the top 5, so lists don't get stuck in one lane.

---

## 9. Personal Reflection

<!-- TODO (Kamar): answer these in your own words — this part is graded on specific, honest detail.
- What was your biggest learning moment during this project?
- How did using AI tools help you, and when did you need to double-check them?
- What surprised you about how simple algorithms can still "feel" like recommendations?
- What would you try next if you extended this project? -->
