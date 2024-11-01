import pandas as pd

# Load cleaned data
df = pd.read_csv('cleaned_courses_data.csv')

# Select features for recommendation
features = df[['course_rating', 'course_difficulty', 'course_students_enrolled']]

# Save selected features
features.to_csv('selected_features.csv', index=False)
