"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:  python -m src.main
"""

import sys

from src.recommender import load_songs, recommend_songs, WEIGHTS

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    # Edge cases / adversarial profiles
    "Conflicted (high energy + sad)": {"genre": "folk", "mood": "sad", "energy": 0.9, "likes_acoustic": True},
    "Unknown Genre (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.7, "likes_acoustic": False},
}

# Experiment: double energy importance, halve genre importance
EXPERIMENT_WEIGHTS = {**WEIGHTS, "genre": 1.0, "energy": 2.0}


def print_recommendations(name, prefs, songs, k=5, weights=None):
    """Print a ranked, explained list of recommendations for one profile."""
    print("=" * 72)
    print(f"Profile: {name}")
    print(f"Prefs:   {prefs}")
    print("-" * 72)
    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k, weights), 1):
        print(f"{rank}. {song['title']} by {song['artist']} ({song['genre']}, {song['mood']})")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    if "--experiment" in sys.argv:
        print(">>> EXPERIMENT: genre weight 2.0 -> 1.0, energy weight 1.0 -> 2.0\n")
        for name in ["High-Energy Pop", "Chill Lofi", "Deep Intense Rock"]:
            print_recommendations(name, PROFILES[name], songs, weights=EXPERIMENT_WEIGHTS)
        return

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
