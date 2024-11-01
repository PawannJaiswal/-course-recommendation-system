import pandas as pd

# Load the similarity matrix
similarity_matrix_df = pd.read_csv('similarity_matrix.csv', index_col=0)

# Load the original DataFrame to map course IDs
df = pd.read_csv('cleaned_courses_data.csv')

# Create a mapping from course ID to index
course_id_to_index = df.index


# Function to recommend similar courses
def recommend(course_id):
    if course_id not in course_id_to_index:
        raise ValueError(f"Course ID {course_id} not found in the DataFrame")

    course_index = course_id_to_index[course_id]
    similarity_scores = list(enumerate(similarity_matrix_df.iloc[course_index]))

    # Sort by similarity score and get top recommendations
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    recommended_indexes = [i[0] for i in sorted_scores if i[0] != course_index]

    return recommended_indexes


# Function to display course details
def display_course_details(course_indexes):
    for index in course_indexes:
        course_details = df.iloc[index]
        print(f"Course Title: {course_details['course_title']}")
        print(f"Organization: {course_details['course_organization']}")
        print(f"Certificate Type: {course_details['course_Certificate_type']}")
        print(f"Rating: {course_details['course_rating']}")
        print(f"Difficulty: {course_details['course_difficulty']}")
        print(f"Students Enrolled: {course_details['course_students_enrolled']}")
        print("------")


# Example usage
recommended_indexes = recommend(course_id=134)
print("Recommended courses:")

display_course_details(recommended_indexes)
