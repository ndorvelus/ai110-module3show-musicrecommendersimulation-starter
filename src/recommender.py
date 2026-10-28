import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into dicts, converting id to int and audio features to float."""
    print(f"Loading songs from {csv_path}...")
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

# Vibe-first recipe weights (see "Algorithm Recipe" in README.md); they sum to 1.0
WEIGHTS = {"energy": 0.35, "valence": 0.25, "mood": 0.20, "genre": 0.20}

# Labels in the same family earn half credit
MOOD_FAMILIES = {
    "calm": ["chill", "relaxed", "focused", "dreamy"],
    "bright": ["happy", "carefree", "playful", "euphoric", "flirty", "romantic", "confident"],
    "dark": ["sad", "melancholic", "moody"],
    "intense": ["intense", "angry"],
}
GENRE_FAMILIES = {
    "pop": ["pop", "indie pop", "edm", "latin"],
    "chill": ["lofi", "ambient", "jazz"],
    "rock": ["rock", "metal", "shoegaze"],
    "roots": ["country", "bluegrass"],
    "urban": ["hip hop", "r&b"],
}

def _closeness(value: float, target: float) -> float:
    """Returns 1.0 for an exact match, falling to 0.0 at the opposite end of a 0-1 scale."""
    return 1.0 - abs(value - target)

def _label_match(label: str, favorite: str, families: Dict[str, List[str]]) -> float:
    """Returns 1.0 for an exact label match, 0.5 for the same family, 0.0 otherwise."""
    if label == favorite:
        return 1.0
    for members in families.values():
        if label in members and favorite in members:
            return 0.5
    return 0.0

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song from 0 to 1 with the vibe-first recipe and returns (score, reasons)."""
    energy_points = WEIGHTS["energy"] * _closeness(song["energy"], user_prefs["target_energy"])
    valence_points = WEIGHTS["valence"] * _closeness(song["valence"], user_prefs["target_valence"])
    mood_points = WEIGHTS["mood"] * _label_match(song["mood"], user_prefs["favorite_mood"], MOOD_FAMILIES)
    genre_points = WEIGHTS["genre"] * _label_match(song["genre"], user_prefs["favorite_genre"], GENRE_FAMILIES)

    reasons = [
        f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f} (+{energy_points:.2f})",
        f"valence {song['valence']:.2f} vs target {user_prefs['target_valence']:.2f} (+{valence_points:.2f})",
    ]
    if mood_points > 0:
        relation = "matches" if mood_points == WEIGHTS["mood"] else "is similar to"
        reasons.append(f"mood '{song['mood']}' {relation} '{user_prefs['favorite_mood']}' (+{mood_points:.2f})")
    if genre_points > 0:
        relation = "matches" if genre_points == WEIGHTS["genre"] else "is similar to"
        reasons.append(f"genre '{song['genre']}' {relation} '{user_prefs['favorite_genre']}' (+{genre_points:.2f})")

    score = energy_points + valence_points + mood_points + genre_points
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns the top k songs as (song, score, explanation), sorted from highest to lowest score."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
