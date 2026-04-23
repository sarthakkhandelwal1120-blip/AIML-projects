import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# ==============================
# DATASET (More realistic)
# ==============================
docs = [
    "python machine learning data science deep learning ai",
    "data analysis python pandas numpy statistics",
    "html css javascript frontend react web design",
    "java spring backend api development database",
    "android kotlin mobile app development",
    "cybersecurity ethical hacking network security"
]

roles = [
    "Data Scientist",
    "Data Analyst",
    "Web Developer",
    "Backend Developer",
    "Mobile App Developer",
    "Cybersecurity Specialist"
]

# ==============================
# TF-IDF
# ==============================
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs).toarray()

# ==============================
# Feature Scaling
# ==============================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ==============================
# PCA
# ==============================
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# ==============================
# KMeans Clustering
# ==============================
kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
labels = kmeans.fit_predict(X_pca)

print("✅ Model trained successfully!\n")

# ==============================
# Prediction Function
# ==============================
def analyze_resume(resume_text):
    # Transform input
    vec = vectorizer.transform([resume_text]).toarray()
    vec_scaled = scaler.transform(vec)
    vec_pca = pca.transform(vec_scaled)

    # Predict cluster
    cluster = kmeans.predict(vec_pca)[0]

    # Find closest role using similarity
    similarity = cosine_similarity(vec, X)
    best_match_index = similarity.argmax()

    predicted_role = roles[best_match_index]
    confidence = similarity[0][best_match_index]

    return cluster, predicted_role, confidence

# ==============================
# USER INPUT
# ==============================
print("📄 Enter your resume text (skills, technologies):\n")
resume_input = input("👉 ")

cluster, role, confidence = analyze_resume(resume_input)

# ==============================
# OUTPUT
# ==============================
print("\n🔍 ANALYSIS RESULT")
print("---------------------------")
print(f"Cluster Assigned : {cluster}")
print(f"Predicted Role   : {role}")
print(f"Confidence Score : {round(confidence*100, 2)}%")

# ==============================
# SUGGESTIONS
# ==============================
if confidence < 0.3:
    print("\n⚠️ Tip: Add more technical skills (python, html, ML, etc.)")
else:
    print("\n✅ Strong match for this role!")