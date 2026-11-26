# 🎵 Music Recommender Simulation — VibeFinder 1.0

## Project Summary

VibeFinder is a small content-based music recommender written in Python. It reads an 18-song catalog from a CSV file, compares every song with a user's "taste profile" (favorite genre, favorite mood, target energy and whether they like acoustic music), gives each song a score, and returns the top 5. Each recommendation shows the reasons it got its points, so you can see why a song was picked.

---

## How The System Works

**How real apps do it.** Spotify, YouTube and TikTok mix two main ideas. *Collaborative filtering* uses other people's behavior: if listeners who like the songs you like also play song X, you probably will too. It runs on signals like plays, skips, likes, saves, playlist adds and repeat listens. *Content-based filtering* uses the song itself: genre, mood, tempo, energy, acoustic sound and so on. It recommends songs that resemble what you already like. Real platforms combine both with huge amounts of data and machine-learned models. My version is content-based only, because there's no listening history, and it uses a hand-written scoring rule I can read and explain.

**Features used**

- `Song`: `genre`, `mood`, `energy` (0.0–1.0), `acousticness` (0.0–1.0). `tempo_bpm`, `valence` and `danceability` are loaded but not scored yet.
- `UserProfile`: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

**Algorithm Recipe (Scoring Rule — one song)**

| Check | Points |
|---|---|
| Genre matches exactly | +2.0 |
| Mood matches exactly | +1.0 |
| Energy closeness | `1.0 − abs(song energy − target energy)`, from 0 to +1.0 |
| Acoustic taste lines up (song acousticness ≥ 0.6 and the user likes acoustic, or < 0.6 and they don't) | +0.5 |

Max score is 4.5. The energy rule rewards being *close* to the target, not just having more or less energy. A 0.8-energy fan gets the most points for a 0.8 song and fewer for both 0.3 and 1.0 songs.

**Ranking Rule — the whole list.** The scoring rule judges one song at a time. The ranking rule runs it on every song, sorts by score from highest to lowest, and keeps the top `k`. You need both: a score alone doesn't tell you what to show first, and you can't sort without a score.

**Data flow**

```
User prefs ──► for each song in songs.csv: score_song() ──► sort by score ──► top K with reasons
```

**Bias I expect before testing.** Genre is worth twice as much as mood, so the system will probably push same-genre songs to the top even when their mood is wrong. Genre matching is also exact text, so "indie pop" won't count as "pop".

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main                # all 5 profiles
   python -m src.main --experiment   # weight-shift experiment
   ```

### Running Tests

```bash
pytest
```

5 tests: the 2 starter tests, plus tests for CSV loading, energy closeness and sort order.

---

## Sample Recommendation Output

Default "pop / happy" profile:

```
Loaded songs: 18

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

Output for all five profiles is in [model_card.md](model_card.md#7-evaluation).

---

## Experiments You Tried

**Weight shift: genre 2.0 → 1.0, energy 1.0 → 2.0** (`python -m src.main --experiment`)

- **High-Energy Pop:** *Rooftop Lights* (indie pop, happy) moved up from #3 to #2, passing *Gym Hero* (pop, intense). For someone who wants happy pop, that's better. A happy song at the right energy beats a workout track that only shares the genre label.
- **Chill Lofi:** The top 3 didn't change. *Spacewalk Thoughts* (ambient, chill) got much closer to #3. The list became a little more varied without getting worse.
- **Deep Intense Rock:** Same order, but the gap between #1 and the rest shrank. The only rock song still wins easily because it matches on everything.

Takeaway: lowering the genre weight made results a bit **more accurate** for the pop profile, not just different. It cut down on "same genre, wrong vibe" picks.

**Edge-case profiles:** see the Evaluation section of the model card. These were a "conflicted" high-energy + sad profile and a profile for a genre that isn't in the catalog (k-pop).

---

## Limitations and Risks

- Tiny catalog (18 songs). Most genres have only one song, so after the first one or two picks the rest of the list is filled by energy alone.
- Genre and mood use exact text matching. "indie pop" ≠ "pop", and a k-pop fan gets no genre points at all.
- Genre + mood (3 points) outweigh energy (1 point max), so a user's energy preference gets overridden when the labels match.
- No lyrics, language, artist familiarity, listening history or popularity.

More detail in the model card.

---

## Reflection

[**Model Card**](model_card.md)

This project showed me that a recommender turns data into a prediction through choices people make. Someone decides which features count, how much each one is worth, and how to break ties. The code itself is tiny: score each song, sort, take the top 5. But every weight is an opinion about what "good taste" means. When genre was worth 2 points, a workout track beat a genuinely happy song for a happy-pop listener, just because of a label. Halving that weight made the results feel more accurate.

Bias shows up in two places: the data and the rules. The catalog has three lofi songs and only one song for most other genres, so some listeners get much better lists than others. Exact text matching means anyone whose genre isn't spelled the same way, or isn't in the catalog at all (like k-pop), gets left out. Real platforms with millions of users can turn small choices like these into large filter bubbles. That's why documenting limitations in something like a model card matters.
