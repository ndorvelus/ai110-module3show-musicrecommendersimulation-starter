"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# target_energy: 0 = calm, 1 = intense; target_valence: 0 = dark, 1 = happy
PROFILES = {
    # Standard listeners
    "High-Energy Pop": {
        "favorite_genre": "pop", "favorite_mood": "happy",
        "target_energy": 0.85, "target_valence": 0.85, "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi", "favorite_mood": "chill",
        "target_energy": 0.40, "target_valence": 0.60, "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock", "favorite_mood": "intense",
        "target_energy": 0.92, "target_valence": 0.35, "likes_acoustic": False,
    },
    # Adversarial / edge cases
    "Sad Banger (conflicting: high energy + sad)": {
        "favorite_genre": "edm", "favorite_mood": "sad",
        "target_energy": 0.90, "target_valence": 0.20, "likes_acoustic": False,
    },
    "Case Trap ('Pop'/'Happy' capitalized)": {
        "favorite_genre": "Pop", "favorite_mood": "Happy",
        "target_energy": 0.85, "target_valence": 0.85, "likes_acoustic": False,
    },
    "Ghost Genre (k-pop/nostalgic, not in catalog)": {
        "favorite_genre": "k-pop", "favorite_mood": "nostalgic",
        "target_energy": 0.60, "target_valence": 0.70, "likes_acoustic": False,
    },
    "Off the Charts (energy 1.5, valence -0.5)": {
        "favorite_genre": "metal", "favorite_mood": "angry",
        "target_energy": 1.5, "target_valence": -0.5, "likes_acoustic": False,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {name} ===")
        print(f"Top recommendations:\n")
        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
