import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Dataset
data = {
    "movie": [
        "Avengers", "Iron Man", "Thor",
        "Hulk", "Captain America", "Doctor Strange", "Spider-Man"
    ],
    "genres": [
        "Action Adventure Sci-Fi",
        "Action Sci-Fi",
        "Action Fantasy",
        "Action Sci-Fi",
        "Action Adventure",
        "Fantasy Adventure",
        "Action Sci-Fi Adventure"
    ]
}
df = pd.DataFrame(data)

# Vectorize genres
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["genres"])

# Cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Recommendation function (case-insensitive)
def recommend(movie_title):
    # normalize input
    movie_title = movie_title.strip().lower()
    movies_lower = df["movie"].str.lower().tolist()

    if movie_title not in movies_lower:
        return ["Movie not found!"]

    idx = movies_lower.index(movie_title)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]  # top 3
    movie_indices = [i[0] for i in sim_scores]
    return df["movie"].iloc[movie_indices].tolist()

# --- MAIN PROGRAM ---
print("Available movies:", ", ".join(df["movie"].tolist()))
choice = input("Enter a movie you like: ")

print(f"\nIf you liked '{choice}', you may also like: {recommend(choice)}")
