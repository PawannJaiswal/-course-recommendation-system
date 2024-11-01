import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the DataFrame
df = pd.read_csv('cleaned_courses_data.csv')

# Print column names for debugging
print("Column names in the DataFrame:", df.columns.tolist())

# Handle non-numeric values in 'course_students_enrolled' and convert to numeric
def convert_students_enrolled(value):
    if isinstance(value, str):
        if 'k' in value:
            return float(value.replace('k', '').replace(',', '').strip()) * 1e3
        elif 'M' in value:
            return float(value.replace('M', '').replace(',', '').strip()) * 1e6
    return float(value)

df['course_students_enrolled'] = df['course_students_enrolled'].map(convert_students_enrolled)

# Define categorical and numerical columns
categorical_columns = ['course_difficulty', 'course_Certificate_type']
numerical_columns = ['course_rating', 'course_students_enrolled']

# Create preprocessing pipeline for categorical features
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(sparse_output=False, drop='first'))
])

# Combine categorical and numerical transformations
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_columns),
        ('num', 'passthrough', numerical_columns)
    ]
)

# Fit and transform the data
features = preprocessor.fit_transform(df)

# Calculate cosine similarity
similarity_matrix = cosine_similarity(features)

# Save the similarity matrix to a CSV file
similarity_matrix_df = pd.DataFrame(similarity_matrix)
similarity_matrix_df.to_csv('similarity_matrix.csv', index=False)

print('Similarity matrix saved as similarity_matrix.csv')
