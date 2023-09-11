import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances
from sqlalchemy import create_engine

# Load data from the database
db_uri = 'mysql+pymysql://root:123456789@localhost/demo'
engine = create_engine(db_uri)
data_query = "SELECT * FROM coupon_user"
df = pd.read_sql_query(data_query, engine)
df = df.drop_duplicates(subset=['email', 'offer_title'])

# Create a user-voucher interaction matrix
interaction_matrix = df.pivot_table(index='offer_title', columns='email', aggfunc='size', fill_value=0)
print("shape of interaction_matrix",interaction_matrix.shape)


# Calculate the cosine similarity between vouchers based on user interactions
cosine_sim_matrix = cosine_similarity(interaction_matrix)
print("shape of cosine_sim_matrix",cosine_sim_matrix.shape)

voucher_similarity = 1 - pairwise_distances(interaction_matrix, metric='cosine')



# Function to get recommended vouchers for a given offer title
def get_recommendations(user_email, num_recommendations=5):
    user_idx = interaction_matrix.index.get_loc(user_email)
    similar_users = list(enumerate(voucher_similarity[user_idx]))
    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)
    similar_users = similar_users[1:num_recommendations+1]
    similar_user_indices = [idx for idx, _ in similar_users]
    
    recommended_vouchers = interaction_matrix.iloc[similar_user_indices].sum(axis=0)
    recommended_vouchers = recommended_vouchers[recommended_vouchers > 0].sort_values(ascending=False).index
    
    return recommended_vouchers

# Example: Get recommendations for a specific user
target_offer_title = 'Upto 35% Off On Groceries'
recommended_vouchers = get_recommendations(target_offer_title)

print("Recommended voucher for", target_offer_title, ":", recommended_vouchers)