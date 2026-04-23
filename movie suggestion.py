import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample dataset
data = {
    'title': ['Inception', 'Titanic', 'Avatar', 'Interstellar', 'The Matrix'],
    'description': [
        'dream mind bending thriller',
        'romantic ship tragedy',
        'alien planet adventure',
        'space time travel',
        'virtual reality action'
    ]
}

df = pd.DataFrame(data)

# ML Model
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['description'])
similarity = cosine_similarity(tfidf_matrix)


def recommend(movie):
    if movie not in df['title'].values:
        return ["Movie not found"]

    idx = df[df['title'] == movie].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:4]

    return [df.iloc[i[0]]['title'] for i in scores]


# GUI
def get_recommendations():
    movie = entry.get()
    result = recommend(movie)
    messagebox.showinfo("Recommendations", "\n".join(result))


root = tk.Tk()
root.title("Movie Recommender")
root.geometry("400x300")

tk.Label(root, text="Enter Movie Name").pack(pady=10)
entry = tk.Entry(root)
entry.pack()

tk.Button(root, text="Recommend", command=get_recommendations).pack(pady=20)

root.mainloop()