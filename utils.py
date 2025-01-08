# imports

import sqlite3
import pandas as pd
from datetime import datetime
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity


# constants
user_df = pd.read_csv(r"D:\CODES\Projects\nasik\demo2\user_activitY (1).csv")
vectorizer = joblib.load(r"D:\CODES\Projects\nasik\demo2\tfidf_vectorizer.pkl")
ingredient_vectors = joblib.load(
    r"D:\CODES\Projects\nasik\demo2\ingredient_vectors.pkl"
)
recipe_df = pd.read_csv(r"D:\CODES\Projects\nasik\demo2\project_food.csv")
ingredient_vectors = vectorizer.fit_transform(recipe_df["Cleaned-Ingredients"])

# print(ingredient_vectors)


# Step 1: Set up SQLite database
conn = sqlite3.connect(
    "user_activity.db", check_same_thread=False
)  # Connect to SQLite database
cursor = conn.cursor()  # Create cursor to interact with the database


# Create table if not exists
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS user_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipe_name TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
)
conn.commit()


nn = NearestNeighbors(n_neighbors=3, algorithm="brute", metric="cosine")

nn.fit(ingredient_vectors)

simi_tf = cosine_similarity(ingredient_vectors)


# myip = "Garlic Methi Raita Recipe"
# def recommend_recp(myip):
#     x = tfid.transform([myip]).toarray()
#     distances, indices = nn.kneighbors(x)
#     ### get recp name from df
#     idx = indices[0]
#     rr = df.iloc[idx]["recp_name"].tolist()
#     return rr

# recommend_recp(myip)


# adding users data in usersdb
def log_user_search(user_id, recipe_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
    cursor.execute(
        "INSERT INTO user_activity (user_id, recipe_name, timestamp) VALUES (?, ?, ?)",
        (user_id, recipe_name, timestamp),
    )  # Insert the record into the datab.
    conn.commit()  # Commit the changes to the database


# Get the last search of the userdb
def get_last_search(user_id):
    cursor.execute(
        "SELECT recipe_name FROM user_activity WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1",
        (user_id,),
    )
    result = cursor.fetchone()  # Get the last search from the database
    if result:  # If result having something value then
        return result[0]  # Return first value from result
    else:
        return None  # Return None if no resul


#
def knn_rcmd(search_text):
    arr = vectorizer.transform([search_text]).toarray()
    distances, indices = nn.kneighbors(arr)
    sug = recipe_df.iloc[indices[0]]["TranslatedRecipeName"].values
    return sug


# last 3 searches of a user
def get_last_search_recipes(user_id):
    cursor.execute(
        "SELECT recipe_name FROM user_activity WHERE user_id = ? ORDER BY timestamp DESC LIMIT 3",
        (user_id,),
    )
    rows = cursor.fetchall()  # Get all rows from the query
    recipe_names = []  # Create an empty list to store the recipe names
    for row in rows:
        recipe_names.append(row[0])  # Add the recipe name (row[0]) to the list
    return recipe_names  # Return the list of recipe names


def get_recmd(text):

    print(vectorizer)

    return list("Sudesh")


# all users from the database
def get_all_users():
    cursor.execute("SELECT DISTINCT user_id FROM user_activity")  # all unique user IDs
    users = cursor.fetchall()  # Fetch the results
    user_list = []
    for user in users:
        user_list.append(
            f"User {user[0]}"
        )  # Create a list of user strings (e.g., 'User 1')
    return user_list  # Return the list of users
