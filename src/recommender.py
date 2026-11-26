import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict

# Algorithm Recipe weights (change these to run experiments)
WEIGHTS = {
    "genre": 2.0,     # exact genre match
    "mood": 1.0,      # exact mood match
    "energy": 1.0,    # max points for a perfect energy match
    "acoustic": 0.5,  # bonus when acoustic taste lines up
}

NUMERIC_FIELDS = {
    "id": int,
    "energy": float,
    "tempo_bpm": float,
    "valence": float,
    "danceability": float,
    "acousticness": float,
}


@dataclass
class Song:
    """A song and its audio/label attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """A user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile into the dict format score_song expects."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


class Recommender:
    """OOP wrapper around the functional scoring and ranking logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user."""
        prefs = _profile_to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation of why a song scored the way it did."""
        score, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field, cast in NUMERIC_FIELDS.items():
                row[field] = cast(row[field])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict, weights: Dict = None) -> Tuple[float, List[str]]:
    """Score one song against user prefs and return (score, reasons)."""
    w = weights or WEIGHTS
    score = 0.0
    reasons = []

    if w["genre"] and song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    if w["mood"] and song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    if "energy" in user_prefs:
        # Closeness, not "higher is better": 1.0 at a perfect match, 0.0 at the opposite end.
        closeness = 1.0 - abs(song["energy"] - user_prefs["energy"])
        points = w["energy"] * closeness
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{points:.2f})")

    if "likes_acoustic" in user_prefs:
        is_acoustic = song["acousticness"] >= 0.6
        if is_acoustic == user_prefs["likes_acoustic"]:
            score += w["acoustic"]
            label = "acoustic" if is_acoustic else "non-acoustic"
            reasons.append(f"{label} sound fits your taste (+{w['acoustic']:.1f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    weights: Dict = None) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest first, and return the top k."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
