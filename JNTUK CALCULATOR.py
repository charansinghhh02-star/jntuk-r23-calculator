import streamlit as st

# Set up the web page title and layout
st.set_page_config(page_title="JNTUK R23 CGPA Calculator", layout="wide")

# Official JNTUK R23 Grading Map
GRADE_POINTS = {
    "S (Superior - 90% & Above)": 10,
    "A (Excellent - 80-89%)": 9,
    "B (Very Good - 70-79%)": 8,
    "C (Good - 60-69%)": 7,
    "D (Average - 50-59%)": 6,
    "E (Pass - 40-49%)": 5,
    "F (Fail - Below 40%)": 0,
    "Ab (Absent)": 0
}

st.title("🎓 JNTUK B.Tech R23 Portal")
st.subheader("Multi-Semester SGPA & CGPA Calculator")

# Legal Disclaimer Box for Safety against Copyright
st.caption(
    "⚠️ **Legal Disclaimer:** This is an unofficial application built strictly for student "
    "educational and self-evaluation purposes. All registered names, structures, and regulation "
    "handbooks belong exclusively to Jawaharlal Nehru Technological University Kakinada (JNTUK). "
    "No copyright infringement intended."
)

# List of all semesters from 1-1 to 4-2
semesters = ["1-1", "1-2", "2-1", "2-2", "3-1", "3-2", "4-1", "4-2"]

# Create visual tabs at the top of the website for each semester
tabs = st.tabs(semesters)

# Dictionaries to store total points and credits for CGPA calculation
sem_total_points = {}
sem_total_credits = {}

# Loop through each tab to create the semester input forms
for index, sem_name in enumerate(semesters):
    with tabs[index]:
        st.write(f"### Semester {sem_name} Data Entry")
        
        # Let the user choose how many subjects they had in this semester
        num_subjects = st.number_input(
            f"Number of subjects in {sem_name}:", 
            min_value=0, max_value=12, value=0, key=f"num_{sem_name}"
        )
        
        total_points = 0.0
        total_credits = 0.0
        
        # Generate input rows dynamically for each subject
        for i in range(int(num_subjects)):
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                st.text_input(f"Subject {i+1} Name", value=f"Subject {i+1}", key=f"name_{sem_name}_{i}")
            
            with col2:
                # Credit Selection Dropdown
                credit = st.selectbox(
                    f"Credits", 
                    [0.5, 1.0, 1.5, 2.0, 3.0, 4.0], 
                    index=4, key=f"credit_{sem_name}_{i}"
                )
            
            with col3:
                # Official JNTUK R23 Grade Selection Dropdown
                grade_str = st.selectbox(
                    f"Grade", 
                    list(GRADE_POINTS.keys()), 
                    key=f"grade_{sem_name}_{i}"
                )
                
            grade_value = GRADE_POINTS[grade_str]
            total_points += (credit * grade_value)
            total_credits += credit

        # Calculate and display individual Semester SGPA
        if total_credits > 0:
            sgpa = total_points / total_credits
            st.success(f"**Semester {sem_name} SGPA:** {sgpa:.2f}")
            # Save data for final cumulative calculation
            sem_total_points[sem_name] = total_points
            sem_total_credits[sem_name] = total_credits
        else:
            st.info("Add subjects above to calculate this semester's SGPA.")

# Dashboard Summary Side-Bar or Header Panel for overall performance
st.markdown("---")
st.write("## 📊 Cumulative Dashboard Summary")

grand_total_points = sum(sem_total_points.values())
grand_total_credits = sum(sem_total_credits.values())

if grand_total_credits > 0:
    final_cgpa = grand_total_points / grand_total_credits
    # Official JNTUK Percentage mapping: (CGPA - 0.75) * 10
    final_percentage = max(0.0, (final_cgpa - 0.75) * 10)
    
    c1, c2, c3 = st.columns(3)
    c1.metric(label="Total Earned Credits", value=f"{grand_total_credits:.1f}")
    c2.metric(label="Cumulative CGPA", value=f"{final_cgpa:.2f} / 10.00")
    c3.metric(label="Equivalent Percentage", value=f"{final_percentage:.2f}%")
else:
    st.warning("Please fill out at least one semester tab above to see your overall Cumulative CGPA.")

# Author Signature Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>🎨 Created by charan singh</p>", 
    unsafe_allow_html=True
)