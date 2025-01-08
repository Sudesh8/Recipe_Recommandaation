import streamlit as st
from utils import (
    knn_rcmd,
    log_user_search,
    get_all_users,
    get_last_search_recipes,
    get_last_search,
)

# Constants
SHOW_LAST_RCMD = True

##### User section
# Sidebar User Selection
users = get_all_users()  # Fetch all users from the database

# Allowing the user to select from the list of users, or show a message if no users exist
if users:
    MyUser = st.sidebar.selectbox(
        "Select User", users, key="user_selectbox"
    )  # Adding unique key
else:
    MyUser = None

# If a valid user is selected
if MyUser:
    st.success(f"Logged in {MyUser}")
    user_id = int(
        MyUser.split(" ")[1]
    )  # Extract user_id from the string, e.g., 'User 1' -> 1

    last_recipe = get_last_search(user_id)
    st.markdown(
        f'<p style="color: blue;">Last search was: {last_recipe}</p>',
        unsafe_allow_html=True,
    )

    # Show recommendations based on the user's last search (if any)
    st.success("Recommendations based on your last search:")

    last_recipes = get_last_search_recipes(user_id)
    last_recipe = get_last_search(user_id)
    if last_recipe:

        st.write(
            knn_rcmd(last_recipe)
        )  # Join last search items into a single string for recommendation
    else:
        st.write("No previous search found.")

    # Search input
    search_text = st.text_input("Search for a New Recipe")
    btn = st.button("Search")

    if btn:
        st.warning(f"Searching for: {search_text}")

        # Log the user's search activity
        log_user_search(user_id, search_text)

        # Show recommendations based on the user's current search
        st.success("Recommendations based on your search:")
        recommended_recipes = knn_rcmd(search_text)
        st.write(recommended_recipes)

else:
    # If no user is selected, prompt user to select a user
    st.warning("No user selected. Please select a user.")
