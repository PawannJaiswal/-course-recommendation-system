import pandas as pd

# Load the dataset
df = pd.read_csv('courses_data.csv')

# Function to convert 'k' values to integers
def convert_k_to_int(val):
    if 'k' in val:
        return float(val.replace('k', '')) * 1000
    return float(val)

# Apply the function to the 'course_students_enrolled' column
df['course_students_enrolled'] = df['course_students_enrolled'].apply(convert_k_to_int).astype(int)

# Save the cleaned data
df.to_csv('cleaned_courses_data.csv', index=False)

print("Data preprocessing complete.")
