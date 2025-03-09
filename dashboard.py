import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset (replace with your actual dataset path)
@st.cache_data
def load_data():
    # Example dataset structure: ['Student', 'Date', 'Score', 'Assignment', 'Underrepresented']
    data = pd.DataFrame({
        'Student': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
        'Date': pd.date_range(start='2024-01-01', periods=3, freq='M').tolist() * 3,
        'Score': [85, 88, 90, 78, 80, 83, 92, 95, 97],
        'Assignment': ['A1', 'A2', 'A3', 'A1', 'A2', 'A3', 'A1', 'A2', 'A3'],
        'Underrepresented': [True, False, True, False, False, True, True, False, True]
    })
    return data

df = load_data()

df['Date'] = pd.to_datetime(df['Date'])

# Streamlit UI
st.title("Student Performance Dashboard")

# Dropdown to select a student
students = df['Student'].unique()
selected_student = st.selectbox("Select a student:", students)

# Filter data for selected student
student_data = df[df['Student'] == selected_student]

# Calculate mean scores for all students
mean_scores = df.groupby('Date')['Score'].mean()

# Calculate assignment statistics for entire class
assignment_stats = df.groupby('Assignment')['Score'].agg(['mean', 'min', 'max'])

# Filter underrepresented students
underrepresented_stats = df[df['Underrepresented']].groupby('Student')['Score'].agg(['mean', 'min', 'max'])

# Streamlit layout
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Top-left: Mean score graph
with col1:
    st.subheader("Class Mean Scores")
    fig1, ax1 = plt.subplots(figsize=(5, 3))
    ax1.plot(mean_scores.index, mean_scores.values, linestyle='--', color='gray', label='Class Average')
    ax1.plot(student_data['Date'], student_data['Score'], marker='o', linestyle='-', label=f"{selected_student}'s Scores")
    ax1.set_title(f"Performance of {selected_student}")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Score")
    ax1.legend()
    ax1.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

# Bottom-left: Assignment stats table
with col3:
    st.subheader("Class Assignment Statistics")
    st.dataframe(assignment_stats)

# Top-right: Bar chart for each student
with col2:
    st.subheader(f"{selected_student}'s Scores by Assignment")
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    student_assignment_scores = student_data.groupby('Assignment')['Score'].mean()
    ax2.bar(student_assignment_scores.index, student_assignment_scores.values, color='blue')
    ax2.set_xlabel("Assignment")
    ax2.set_ylabel("Score")
    ax2.set_title("Scores by Assignment")
    st.pyplot(fig2)

# Bottom-right: Underrepresented student statistics
with col4:
    st.subheader("Underrepresented Students Statistics")
    st.dataframe(underrepresented_stats)
