import streamlit as st
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# # Load the pre-trained model and ingredient vectors
vectorizer = joblib.load("tfidf_vectorizer.pkl")
ingredient_vectors = joblib.load("ingredient_vectors.pkl")

print(ingredient_vectors)


recipe_df = pd.read_csv("project_food.csv")
print(recipe_df)

# Ensure the vectorizer is fitted
ingredient_vectors = vectorizer.fit_transform(recipe_df["Cleaned-Ingredients"])
print(ingredient_vectors)


# Ensure the vectorizer is properly fitted
user_vector = vectorizer.transform(recipe_df["Cleaned-Ingredients"])


# Load the user activity data
user_df = pd.read_csv("user_activitY (1).csv")
print(user_df)


# Define the recommendation function
def recommend_Xrecipes(selected_user):
    # Get user's last activity
    user_activity = user_df[user_df["user_id"] == selected_user]
    if user_activity.empty:
        return ["No history found for this user."]

    # Get the last searched or viewed recipe ID
    last_activity = user_activity.sort_values(by="timestamp", ascending=False).iloc[0]
    last_recipe_id = last_activity["recipe_id"]

    # Find the corresponding recipe in the recipe DataFrame
    if last_recipe_id not in recipe_df["recipe_id"].values:
        return ["Last activity recipe not found in the database."]

    user_recipe = recipe_df[recipe_df["recipe_id"] == last_recipe_id]

    # Find similar recipes
    user_vector = vectorizer.transform(user_recipe["Cleaned-Ingredients"])
    similarities = cosine_similarity(user_vector, ingredient_vectors)
    similar_recipe_indices = similarities.argsort()[0][::-1][
        1:6
    ]  # Exclude the current recipe

    recommended_recipes = recipe_df.iloc[similar_recipe_indices][
        "TranslatedRecipeName"
    ].tolist()
    return recommended_recipes


print("-----------------------------------------")


# Streamlit App UI
st.title("Recipe Recommendation System")

# User Selection
user_ids = user_df["user_id"].unique()
selected_user = st.selectbox("Select User", options=["Select User"] + list(user_ids))

# Get recommendations when a user selects an ID and presses the button
if selected_user != "Select User":
    if st.button("Get Recommendations"):
        recommendations = recommend_Xrecipes(selected_user)
        st.write("### Recommended Recipes:")
        for recipe in recommendations:
            st.write(f"- {recipe}")
else:
    st.write("Please select a user ID to get recommendations.")
