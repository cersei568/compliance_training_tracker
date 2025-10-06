import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Compliance & Training Tracker",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .alert-card {
        background: #ff6b6b;
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
    .success-card {
        background: #51cf66;
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
    .warning-card {
        background: #ffd43b;
        padding: 15px;
        border-radius: 8px;
        color: #333;
        margin: 10px 0;
    }
    .info-card {
        background: #4dabf7;
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .employee-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'employees' not in st.session_state:
    st.session_state.employees = pd.DataFrame({
        'employee_id': ['E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007', 'E008'],
        'name': ['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Emily Brown', 'David Lee', 'Lisa Anderson', 'Tom Davis', 'Anna Martinez'],
        'role': ['Safety Officer', 'Forklift Operator', 'Manager', 'HR Specialist', 'Forklift Operator', 'Safety Officer', 'Manager', 'Warehouse Worker'],
        'department': ['Operations', 'Warehouse', 'Management', 'HR', 'Warehouse', 'Operations', 'Management', 'Warehouse'],
        'email': ['john.smith@company.com', 'sarah.j@company.com', 'mike.w@company.com', 'emily.b@company.com', 
                 'david.l@company.com', 'lisa.a@company.com', 'tom.d@company.com', 'anna.m@company.com'],
        'hire_date': ['2020-01-15', '2019-06-01', '2018-03-20', '2021-05-10', '2020-12-15', '2019-02-28', '2017-07-15', '2021-04-01'],
        'status': ['Active', 'Active', 'Active', 'Active', 'Active', 'Active', 'Active', 'Active'],
        'phone': ['555-0101', '555-0102', '555-0103', '555-0104', '555-0105', '555-0106', '555-0107', '555-0108']
    })

if 'certifications' not in st.session_state:
    st.session_state.certifications = pd.DataFrame({
        'cert_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008'],
        'employee_id': ['E001', 'E002', 'E003', 'E001', 'E005', 'E006', 'E002', 'E004'],
        'cert_name': ['OSHA 30', 'Forklift License', 'Leadership Cert', 'First Aid', 'Forklift License', 'OSHA 30', 'Safety Training', 'HR Compliance'],
        'issue_date': ['2023-01-15', '2023-06-01', '2023-03-20', '2023-05-10', '2022-12-15', '2023-02-28', '2023-07-15', '2023-04-01'],
        'expiry_date': ['2024-01-15', '2024-06-01', '2026-03-20', '2025-05-10', '2023-12-15', '2024-02-28', '2024-07-15', '2025-04-01'],
        'status': ['Active', 'Active', 'Active', 'Active', 'Expired', 'Active', 'Active', 'Active'],
        'issuing_organization': ['OSHA', 'State DOT', 'Leadership Academy', 'Red Cross', 'State DOT', 'OSHA', 'Safety Institute', 'SHRM']
    })

if 'trainings' not in st.session_state:
    st.session_state.trainings = pd.DataFrame({
        'training_id': ['T001', 'T002', 'T003', 'T004', 'T005'],
        'training_name': ['Workplace Safety', 'Data Privacy & Security', 'Leadership Development', 'Anti-Harassment', 'Emergency Response'],
        'description': ['Basic workplace safety procedures', 'GDPR and data protection', 'Management skills', 'Workplace conduct', 'Emergency protocols'],
        'duration_hours': [4, 2, 8, 3, 4],
        'required_for_roles': ['All', 'All', 'Manager', 'All', 'Safety Officer,Forklift Operator'],
        'frequency': ['Annual', 'Annual', 'Once', 'Annual', 'Semi-Annual'],
        'compliance_type': ['OSHA', 'Legal', 'Professional', 'Legal', 'OSHA']
    })

if 'training_assignments' not in st.session_state:
    st.session_state.training_assignments = pd.DataFrame({
        'assignment_id': ['A001', 'A002', 'A003', 'A004', 'A005', 'A006', 'A007', 'A008'],
        'employee_id': ['E001', 'E002', 'E003', 'E004', 'E001', 'E005', 'E006', 'E007'],
        'training_id': ['T001', 'T001', 'T003', 'T002', 'T005', 'T001', 'T005', 'T003'],
        'assigned_date': ['2024-01-01', '2024-01-01', '2024-01-15', '2024-01-10', '2024-01-05', '2024-01-12', '2024-01-08', '2024-01-20'],
        'due_date': ['2024-03-01', '2024-03-01', '2024-04-15', '2024-03-10', '2024-03-05', '2024-03-12', '2024-03-08', '2024-04-20'],
        'completion_date': ['2024-02-15', None, '2024-02-20', '2024-02-28', None, None, '2024-02-25', None],
        'status': ['Completed', 'In Progress', 'Completed', 'Completed', 'Overdue', 'In Progress', 'Completed', 'Not Started'],
        'score': [95.0, None, 88.0, 92.0, None, None, 90.0, None]
    })

if 'skills_matrix' not in st.session_state:
    st.session_state.skills_matrix = pd.DataFrame({
        'skill_id': ['S001', 'S002', 'S003', 'S004', 'S005'],
        'skill_name': ['Safety Protocols', 'Equipment Operation', 'Leadership', 'Compliance Knowledge', 'Emergency Response'],
        'required_for_roles': ['All', 'Forklift Operator', 'Manager', 'HR Specialist,Safety Officer', 'Safety Officer'],
        'proficiency_levels': ['Beginner,Intermediate,Advanced,Expert', 'Beginner,Intermediate,Advanced,Expert', 
                              'Beginner,Intermediate,Advanced,Expert', 'Beginner,Intermediate,Advanced,Expert',
                              'Beginner,Intermediate,Advanced,Expert']
    })

if 'employee_skills' not in st.session_state:
    st.session_state.employee_skills = pd.DataFrame({
        'employee_id': ['E001', 'E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007'],
        'skill_id': ['S001', 'S005', 'S002', 'S003', 'S004', 'S002', 'S001', 'S003'],
        'current_level': ['Expert', 'Advanced', 'Advanced', 'Advanced', 'Expert', 'Intermediate', 'Advanced', 'Expert'],
        'required_level': ['Advanced', 'Advanced', 'Advanced', 'Expert', 'Advanced', 'Advanced', 'Advanced', 'Advanced'],
        'last_assessed': ['2024-01-15', '2024-01-15', '2024-01-20', '2024-01-10', '2024-01-18', '2024-01-22', '2024-01-12', '2024-01-25']
    })

# Helper Functions
def generate_employee_id():
    """Generate a new unique employee ID"""
    if st.session_state.employees.empty:
        return 'E001'
    
    existing_ids = st.session_state.employees['employee_id'].tolist()
    numbers = [int(id[1:]) for id in existing_ids]
    new_number = max(numbers) + 1
    return f'E{str(new_number).zfill(3)}'

def calculate_days_until_expiry(expiry_date):
    """Calculate days until certification expiry"""
    if pd.isna(expiry_date):
        return None
    expiry = pd.to_datetime(expiry_date)
    today = datetime.now()
    return (expiry - today).days

def get_expiration_alerts():
    """Get certifications expiring soon"""
    df = st.session_state.certifications.copy()
    df['days_until_expiry'] = df['expiry_date'].apply(calculate_days_until_expiry)
    
    expired = df[df['days_until_expiry'] < 0]
    expiring_soon = df[(df['days_until_expiry'] >= 0) & (df['days_until_expiry'] <= 30)]
    expiring_warning = df[(df['days_until_expiry'] > 30) & (df['days_until_expiry'] <= 90)]
    
    return expired, expiring_soon, expiring_warning

def assign_training_by_role(role):
    """Auto-assign mandatory trainings based on role"""
    trainings = st.session_state.trainings
    mandatory = trainings[
        (trainings['required_for_roles'].str.contains(role, case=False, na=False)) |
        (trainings['required_for_roles'].str.contains('All', case=False, na=False))
    ]
    return mandatory

def calculate_compliance_score(employee_id):
    """Calculate compliance score for an employee"""
    assignments = st.session_state.training_assignments[
        st.session_state.training_assignments['employee_id'] == employee_id
    ]
    
    if len(assignments) == 0:
        return 0
    
    completed = len(assignments[assignments['status'] == 'Completed'])
    total = len(assignments)
    
    return round((completed / total) * 100, 1)

def generate_transcript(employee_id):
    """Generate training transcript for an employee"""
    employee = st.session_state.employees[st.session_state.employees['employee_id'] == employee_id].iloc[0]
    assignments = st.session_state.training_assignments[
        st.session_state.training_assignments['employee_id'] == employee_id
    ]
    
    # Merge with training details
    trainings = st.session_state.trainings
    transcript = assignments.merge(trainings, on='training_id', how='left')
    transcript = transcript[transcript['status'] == 'Completed']
    
    return employee, transcript

def analyze_skills_gap(employee_id):
    """Analyze skills gap for an employee"""
    employee_skills = st.session_state.employee_skills[
        st.session_state.employee_skills['employee_id'] == employee_id
    ]
    
    skills = st.session_state.skills_matrix
    gap_analysis = employee_skills.merge(skills, on='skill_id', how='left')
    
    # Define proficiency levels
    levels = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Expert': 4}
    
    gap_analysis['current_level_num'] = gap_analysis['current_level'].map(levels)
    gap_analysis['required_level_num'] = gap_analysis['required_level'].map(levels)
    gap_analysis['gap'] = gap_analysis['required_level_num'] - gap_analysis['current_level_num']
    
    return gap_analysis

def auto_assign_mandatory_trainings(employee_id):
    """Automatically assign all mandatory trainings for new employee"""
    employee = st.session_state.employees[st.session_state.employees['employee_id'] == employee_id].iloc[0]
    mandatory_trainings = assign_training_by_role(employee['role'])
    
    new_assignments = []
    for _, training in mandatory_trainings.iterrows():
        # Check if already assigned
        existing = st.session_state.training_assignments[
            (st.session_state.training_assignments['employee_id'] == employee_id) &
            (st.session_state.training_assignments['training_id'] == training['training_id'])
        ]
        
        if existing.empty:
            new_assignment = {
                'assignment_id': f'A{str(len(st.session_state.training_assignments) + len(new_assignments) + 1).zfill(3)}',
                'employee_id': employee_id,
                'training_id': training['training_id'],
                'assigned_date': datetime.now().strftime('%Y-%m-%d'),
                'due_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'completion_date': None,
                'status': 'Not Started',
                'score': None
            }
            new_assignments.append(new_assignment)
    
    if new_assignments:
        st.session_state.training_assignments = pd.concat(
            [st.session_state.training_assignments, pd.DataFrame(new_assignments)],
            ignore_index=True
        )
    
    return len(new_assignments)

# Main App
def main():
    st.markdown('<h1 class="main-header">📚 Compliance & Training Tracker</h1>', unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio(
        "Select Module",
        ["🏠 Dashboard", "👥 Employee Management", "🚨 Certification Alerts", 
         "📚 Training Management", "📈 Compliance Reporting", 
         "📜 Training Transcripts", "🎯 Skills Gap Analysis"]
    )
    
    # Sidebar Stats
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.metric("Total Employees", len(st.session_state.employees))
    st.sidebar.metric("Active Trainings", len(st.session_state.training_assignments[
        st.session_state.training_assignments['status'].isin(['Not Started', 'In Progress'])
    ]))
    expired, expiring_soon, _ = get_expiration_alerts()
    st.sidebar.metric("⚠️ Expiring Certs", len(expiring_soon))
    
    # DASHBOARD
    if page == "🏠 Dashboard":
        st.header("📊 Compliance Dashboard")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        expired, expiring_soon, expiring_warning = get_expiration_alerts()
        total_employees = len(st.session_state.employees)
        completed_count = st.session_state.training_assignments[
            st.session_state.training_assignments['status'] == 'Completed'
        ].shape[0]
        total_assignments = st.session_state.training_assignments.shape[0]
        avg_compliance = (completed_count / total_assignments * 100) if total_assignments > 0 else 0
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{total_employees}</h3>
                <p>Total Employees</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{len(expired)}</h3>
                <p>Expired Certs</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{len(expiring_soon)}</h3>
                <p>Expiring Soon (30d)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{avg_compliance:.1f}%</h3>
                <p>Avg Compliance</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Training Status Distribution")
            status_counts = st.session_state.training_assignments['status'].value_counts()
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Compliance by Department")
            employees = st.session_state.employees
            assignments = st.session_state.training_assignments
            
            dept_compliance = []
            for dept in employees['department'].unique():
                dept_employees = employees[employees['department'] == dept]['employee_id']
                dept_assignments = assignments[assignments['employee_id'].isin(dept_employees)]
                if len(dept_assignments) > 0:
                    compliance = len(dept_assignments[dept_assignments['status'] == 'Completed']) / len(dept_assignments) * 100
                else:
                    compliance = 0
                dept_compliance.append({'Department': dept, 'Compliance %': compliance})
            
            dept_df = pd.DataFrame(dept_compliance)
            fig = px.bar(dept_df, x='Department', y='Compliance %', color='Compliance %',
                        color_continuous_scale='RdYlGn', text='Compliance %')
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent Activity
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Recent Completions")
            recent = st.session_state.training_assignments[
                st.session_state.training_assignments['status'] == 'Completed'
            ].copy()
            
            if not recent.empty and 'completion_date' in recent.columns:
                recent = recent[recent['completion_date'].notna()]
                if not recent.empty:
                    recent = recent.sort_values('completion_date', ascending=False).head(5)
                    display_recent = recent.merge(st.session_state.employees, on='employee_id', how='left')
                    display_recent = display_recent.merge(st.session_state.trainings, on='training_id', how='left')
                    st.dataframe(
                        display_recent[['name', 'training_name', 'completion_date', 'score']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No recent completions")
            else:
                st.info("No recent completions")
        
        with col2:
            st.subheader("⚠️ Overdue Trainings")
            overdue = st.session_state.training_assignments[
                st.session_state.training_assignments['status'] == 'Overdue'
            ].copy()
            
            if not overdue.empty:
                display_overdue = overdue.merge(st.session_state.employees, on='employee_id', how='left')
                display_overdue = display_overdue.merge(st.session_state.trainings, on='training_id', how='left')
                st.dataframe(
                    display_overdue[['name', 'training_name', 'due_date']].head(5),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.success("✅ No overdue trainings!")
    
    # EMPLOYEE MANAGEMENT
    elif page == "👥 Employee Management":
        st.header("👥 Employee Management")
        
        tab1, tab2, tab3 = st.tabs(["📋 View Employees", "➕ Add New Employee", "✏️ Edit/Deactivate"])
        
        with tab1:
            st.subheader("Employee Directory")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                dept_filter = st.multiselect(
                    "Filter by Department",
                    ['All'] + st.session_state.employees['department'].unique().tolist(),
                    default=['All']
                )
            with col2:
                role_filter = st.multiselect(
                    "Filter by Role",
                    ['All'] + st.session_state.employees['role'].unique().tolist(),
                    default=['All']
                )
            with col3:
                status_filter = st.selectbox(
                    "Filter by Status",
                    ['All', 'Active', 'Inactive']
                )
            
            # Apply filters
            filtered_employees = st.session_state.employees.copy()
            
            if 'All' not in dept_filter and dept_filter:
                filtered_employees = filtered_employees[filtered_employees['department'].isin(dept_filter)]
            
            if 'All' not in role_filter and role_filter:
                filtered_employees = filtered_employees[filtered_employees['role'].isin(role_filter)]
            
            if status_filter != 'All':
                filtered_employees = filtered_employees[filtered_employees['status'] == status_filter]
            
            # Display employee cards
            st.markdown(f"### Showing {len(filtered_employees)} employees")
            
            for _, emp in filtered_employees.iterrows():
                compliance_score = calculate_compliance_score(emp['employee_id'])
                
                # Get active certifications count
                emp_certs = st.session_state.certifications[
                    (st.session_state.certifications['employee_id'] == emp['employee_id']) &
                    (st.session_state.certifications['status'] == 'Active')
                ]
                
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    <div class="employee-card">
                        <h4>👤 {emp['name']}</h4>
                        <p><strong>ID:</strong> {emp['employee_id']} | <strong>Status:</strong> {emp['status']}</p>
                        <p><strong>Role:</strong> {emp['role']}</p>
                        <p><strong>Department:</strong> {emp['department']}</p>
                        <p>📧 {emp['email']} | 📞 {emp['phone']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.metric("Compliance Score", f"{compliance_score}%")
                with col3:
                    st.metric("Active Certs", len(emp_certs))
                with col4:
                    st.metric("Hire Date", emp['hire_date'])
            
            # Export employee list
            st.markdown("---")
            col1, col2 = st.columns([4, 1])
            with col2:
                csv = filtered_employees.to_csv(index=False)
                st.download_button(
                    label="📥 Export to CSV",
                    data=csv,
                    file_name=f"employees_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with tab2:
            st.subheader("➕ Add New Employee")
            
            with st.form("add_employee_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Full Name *", placeholder="John Doe")
                    new_email = st.text_input("Email *", placeholder="john.doe@company.com")
                    new_phone = st.text_input("Phone", placeholder="555-0123")
                    new_role = st.selectbox(
                        "Role *",
                        ['Manager', 'Safety Officer', 'Forklift Operator', 'Warehouse Worker', 
                         'HR Specialist', 'Supervisor', 'Technician', 'Administrator']
                    )
                
                with col2:
                    new_department = st.selectbox(
                        "Department *",
                        ['Operations', 'Warehouse', 'Management', 'HR', 'Logistics', 
                         'Maintenance', 'Quality Control', 'Administration']
                    )
                    new_hire_date = st.date_input("Hire Date *", datetime.now())
                    new_status = st.selectbox("Status", ['Active', 'Inactive'])
                    auto_assign = st.checkbox("Auto-assign mandatory trainings", value=True)
                
                st.markdown("---")
                col1, col2, col3 = st.columns([2, 1, 1])
                with col2:
                    submit_button = st.form_submit_button("➕ Add Employee", type="primary")
                with col3:
                    clear_button = st.form_submit_button("🔄 Clear")
                
                if submit_button:
                    # Validation
                    if not new_name or not new_email:
                        st.error("❌ Please fill in all required fields (marked with *)")
                    elif new_email in st.session_state.employees['email'].values:
                        st.error("❌ An employee with this email already exists!")
                    else:
                        # Generate new employee ID
                        new_emp_id = generate_employee_id()
                        
                        # Add new employee
                        new_employee = pd.DataFrame({
                            'employee_id': [new_emp_id],
                            'name': [new_name],
                            'role': [new_role],
                            'department': [new_department],
                            'email': [new_email],
                            'hire_date': [new_hire_date.strftime('%Y-%m-%d')],
                            'status': [new_status],
                            'phone': [new_phone if new_phone else 'N/A']
                        })
                        
                        st.session_state.employees = pd.concat(
                            [st.session_state.employees, new_employee],
                            ignore_index=True
                        )
                        
                        # Auto-assign trainings if selected
                        assigned_count = 0
                        if auto_assign:
                            assigned_count = auto_assign_mandatory_trainings(new_emp_id)
                        
                        st.success(f"""
                        ✅ Employee added successfully!
                        
                        **Employee ID:** {new_emp_id}
                        **Name:** {new_name}
                        **Role:** {new_role}
                        **Department:** {new_department}
                        
                        {f'🎓 {assigned_count} mandatory trainings auto-assigned!' if auto_assign else ''}
                        """)
                        
                        st.balloons()
                        st.rerun()
            
            # Quick stats
            st.markdown("---")
            st.subheader("📊 Employee Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Employees", len(st.session_state.employees))
            with col2:
                active_count = len(st.session_state.employees[st.session_state.employees['status'] == 'Active'])
                st.metric("Active", active_count)
            with col3:
                dept_count = st.session_state.employees['department'].nunique()
                st.metric("Departments", dept_count)
            with col4:
                role_count = st.session_state.employees['role'].nunique()
                st.metric("Roles", role_count)
        
        with tab3:
            st.subheader("✏️ Edit or Deactivate Employee")
            
            # Select employee to edit
            edit_employee = st.selectbox(
                "Select Employee",
                st.session_state.employees['employee_id'].tolist(),
                format_func=lambda x: f"{st.session_state.employees[st.session_state.employees['employee_id']==x]['name'].iloc[0]} ({x})"
            )
            
            if edit_employee:
                employee = st.session_state.employees[
                    st.session_state.employees['employee_id'] == edit_employee
                ].iloc[0]
                
                st.markdown("---")
                
                with st.form("edit_employee_form"):
                    st.markdown(f"### Editing: {employee['name']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_name = st.text_input("Full Name", value=employee['name'])
                        edit_email = st.text_input("Email", value=employee['email'])
                        edit_phone = st.text_input("Phone", value=employee['phone'])
                        edit_role = st.selectbox(
                            "Role",
                            ['Manager', 'Safety Officer', 'Forklift Operator', 'Warehouse Worker', 
                             'HR Specialist', 'Supervisor', 'Technician', 'Administrator'],
                            index=['Manager', 'Safety Officer', 'Forklift Operator', 'Warehouse Worker', 
                                  'HR Specialist', 'Supervisor', 'Technician', 'Administrator'].index(employee['role'])
                            if employee['role'] in ['Manager', 'Safety Officer', 'Forklift Operator', 'Warehouse Worker', 
                                                    'HR Specialist', 'Supervisor', 'Technician', 'Administrator'] else 0
                        )
                    
                    with col2:
                        edit_department = st.selectbox(
                            "Department",
                            ['Operations', 'Warehouse', 'Management', 'HR', 'Logistics', 
                             'Maintenance', 'Quality Control', 'Administration'],
                            index=['Operations', 'Warehouse', 'Management', 'HR', 'Logistics', 
                                  'Maintenance', 'Quality Control', 'Administration'].index(employee['department'])
                            if employee['department'] in ['Operations', 'Warehouse', 'Management', 'HR', 'Logistics', 
                                                          'Maintenance', 'Quality Control', 'Administration'] else 0
                        )
                        edit_hire_date = st.date_input(
                            "Hire Date",
                            value=pd.to_datetime(employee['hire_date'])
                        )
                        edit_status = st.selectbox(
                            "Status",
                            ['Active', 'Inactive'],
                            index=['Active', 'Inactive'].index(employee['status'])
                        )
                    
                    st.markdown("---")
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col2:
                        update_button = st.form_submit_button("💾 Update", type="primary")
                    with col3:
                        deactivate_button = st.form_submit_button("🔒 Deactivate", type="secondary")
                    
                    if update_button:
                        # Update employee
                        idx = st.session_state.employees[
                            st.session_state.employees['employee_id'] == edit_employee
                        ].index[0]
                        
                        st.session_state.employees.at[idx, 'name'] = edit_name
                        st.session_state.employees.at[idx, 'email'] = edit_email
                        st.session_state.employees.at[idx, 'phone'] = edit_phone
                        st.session_state.employees.at[idx, 'role'] = edit_role
                        st.session_state.employees.at[idx, 'department'] = edit_department
                        st.session_state.employees.at[idx, 'hire_date'] = edit_hire_date.strftime('%Y-%m-%d')
                        st.session_state.employees.at[idx, 'status'] = edit_status
                        
                        st.success("✅ Employee updated successfully!")
                        st.rerun()
                    
                    if deactivate_button:
                        idx = st.session_state.employees[
                            st.session_state.employees['employee_id'] == edit_employee
                        ].index[0]
                        
                        st.session_state.employees.at[idx, 'status'] = 'Inactive'
                        st.warning(f"⚠️ {employee['name']} has been deactivated")
                        st.rerun()
                
                # Show employee details
                st.markdown("---")
                st.subheader("📊 Employee Overview")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    compliance = calculate_compliance_score(edit_employee)
                    st.metric("Compliance Score", f"{compliance}%")
                
                with col2:
                    assignments = len(st.session_state.training_assignments[
                        st.session_state.training_assignments['employee_id'] == edit_employee
                    ])
                    st.metric("Total Trainings", assignments)
                
                with col3:
                    certs = len(st.session_state.certifications[
                        st.session_state.certifications['employee_id'] == edit_employee
                    ])
                    st.metric("Certifications", certs)
    
    # CERTIFICATION ALERTS
    elif page == "🚨 Certification Alerts":
        st.header("🚨 Certification Expiration Alerts")
        
        expired, expiring_soon, expiring_warning = get_expiration_alerts()
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="alert-card">
                <h3>{len(expired)}</h3>
                <p>Expired Certifications</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="warning-card">
                <h3>{len(expiring_soon)}</h3>
                <p>Expiring Within 30 Days</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="info-card">
                <h3>{len(expiring_warning)}</h3>
                <p>Expiring Within 90 Days</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Expired Certifications
        if not expired.empty:
            st.markdown("### ⛔ Expired Certifications")
            for _, cert in expired.iterrows():
                employee = st.session_state.employees[
                    st.session_state.employees['employee_id'] == cert['employee_id']
                ].iloc[0]
                st.markdown(f"""
                <div class="alert-card">
                    <strong>{employee['name']}</strong> - {cert['cert_name']}<br>
                    Expired: {cert['expiry_date']} ({abs(cert['days_until_expiry'])} days ago)<br>
                    Issuing Org: {cert['issuing_organization']}<br>
                    📧 {employee['email']} | 📞 {employee['phone']}
                </div>
                """, unsafe_allow_html=True)
        
        # Expiring Soon (30 days)
        if not expiring_soon.empty:
            st.markdown("### ⚠️ Expiring Within 30 Days")
            for _, cert in expiring_soon.iterrows():
                employee = st.session_state.employees[
                    st.session_state.employees['employee_id'] == cert['employee_id']
                ].iloc[0]
                st.markdown(f"""
                <div class="warning-card">
                    <strong>{employee['name']}</strong> - {cert['cert_name']}<br>
                    Expires: {cert['expiry_date']} ({cert['days_until_expiry']} days)<br>
                    Issuing Org: {cert['issuing_organization']}<br>
                    📧 {employee['email']} | 📞 {employee['phone']}
                </div>
                """, unsafe_allow_html=True)
        
        # Expiring Warning (30-90 days)
        if not expiring_warning.empty:
            st.markdown("### 📅 Expiring Within 90 Days")
            expiring_warning_display = expiring_warning.merge(
                st.session_state.employees[['employee_id', 'name', 'email']], on='employee_id', how='left'
            )
            st.dataframe(
                expiring_warning_display[['name', 'cert_name', 'expiry_date', 'days_until_expiry', 'issuing_organization', 'email']],
                use_container_width=True,
                hide_index=True
            )
        
        st.markdown("---")
        
        # Add new certification
        st.subheader("➕ Add New Certification")
        
        with st.form("add_certification_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                cert_employee = st.selectbox(
                    "Select Employee",
                    st.session_state.employees['employee_id'].tolist(),
                    format_func=lambda x: st.session_state.employees[
                        st.session_state.employees['employee_id'] == x
                    ]['name'].iloc[0]
                )
                cert_name = st.text_input("Certification Name")
                cert_org = st.text_input("Issuing Organization")
            
            with col2:
                cert_issue_date = st.date_input("Issue Date", datetime.now())
                cert_expiry_date = st.date_input("Expiry Date", datetime.now() + timedelta(days=365))
                cert_status = st.selectbox("Status", ['Active', 'Expired', 'Suspended'])
            
            submit_cert = st.form_submit_button("💾 Add Certification", type="primary")
            
            if submit_cert:
                if cert_name and cert_org:
                    new_cert = pd.DataFrame({
                        'cert_id': [f'C{str(len(st.session_state.certifications) + 1).zfill(3)}'],
                        'employee_id': [cert_employee],
                        'cert_name': [cert_name],
                        'issue_date': [cert_issue_date.strftime('%Y-%m-%d')],
                        'expiry_date': [cert_expiry_date.strftime('%Y-%m-%d')],
                        'status': [cert_status],
                        'issuing_organization': [cert_org]
                    })
                    
                    st.session_state.certifications = pd.concat(
                        [st.session_state.certifications, new_cert],
                        ignore_index=True
                    )
                    
                    st.success("✅ Certification added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields")
        
        st.markdown("---")
        
        # Bulk Email Alert
        st.subheader("📧 Send Renewal Reminders")
        col1, col2 = st.columns([3, 1])
        with col1:
            alert_type = st.selectbox(
                "Select Alert Type",
                ["Expired Certifications", "Expiring Within 30 Days", "Expiring Within 90 Days"]
            )
        with col2:
            if st.button("Send Alerts", type="primary"):
                if alert_type == "Expired Certifications":
                    recipients = len(expired)
                elif alert_type == "Expiring Within 30 Days":
                    recipients = len(expiring_soon)
                else:
                    recipients = len(expiring_warning)
                
                st.success(f"✅ Renewal reminders sent to {recipients} employees!")
    
    # TRAINING MANAGEMENT
    elif page == "📚 Training Management":
        st.header("📚 Training Management")
        
        tab1, tab2, tab3 = st.tabs(["Assign Training", "Track Progress", "Manage Trainings"])
        
        with tab1:
            st.subheader("Assign Training to Employees")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Individual Assignment")
                selected_employee = st.selectbox(
                    "Select Employee",
                    st.session_state.employees['employee_id'].tolist(),
                    format_func=lambda x: st.session_state.employees[
                        st.session_state.employees['employee_id'] == x
                    ]['name'].iloc[0]
                )
                
                employee_role = st.session_state.employees[
                    st.session_state.employees['employee_id'] == selected_employee
                ]['role'].iloc[0]
                
                # Show mandatory trainings for role
                mandatory = assign_training_by_role(employee_role)
                
                st.info(f"**Role:** {employee_role}")
                st.write("**Mandatory Trainings:**")
                for _, training in mandatory.iterrows():
                    st.write(f"• {training['training_name']}")
                
                selected_training = st.selectbox(
                    "Select Training",
                    st.session_state.trainings['training_id'].tolist(),
                    format_func=lambda x: st.session_state.trainings[
                        st.session_state.trainings['training_id'] == x
                    ]['training_name'].iloc[0]
                )
                
                due_date = st.date_input("Due Date", datetime.now() + timedelta(days=30))
                
                if st.button("Assign Training", type="primary"):
                    # Check if already assigned
                    existing = st.session_state.training_assignments[
                        (st.session_state.training_assignments['employee_id'] == selected_employee) &
                        (st.session_state.training_assignments['training_id'] == selected_training)
                    ]
                    
                    if not existing.empty:
                        st.warning("⚠️ This training is already assigned to this employee")
                    else:
                        new_assignment = pd.DataFrame({
                            'assignment_id': [f'A{str(len(st.session_state.training_assignments) + 1).zfill(3)}'],
                            'employee_id': [selected_employee],
                            'training_id': [selected_training],
                            'assigned_date': [datetime.now().strftime('%Y-%m-%d')],
                            'due_date': [due_date.strftime('%Y-%m-%d')],
                            'completion_date': [None],
                            'status': ['Not Started'],
                            'score': [None]
                        })
                        st.session_state.training_assignments = pd.concat(
                            [st.session_state.training_assignments, new_assignment],
                            ignore_index=True
                        )
                        st.success("✅ Training assigned successfully!")
                        st.rerun()
            
            with col2:
                st.markdown("#### Role-Based Bulk Assignment")
                selected_role = st.selectbox(
                    "Select Role",
                    st.session_state.employees['role'].unique()
                )
                
                role_employees = st.session_state.employees[
                    st.session_state.employees['role'] == selected_role
                ]
                st.info(f"**{len(role_employees)} employees** in this role")
                
                bulk_training = st.selectbox(
                    "Select Training for Bulk Assignment",
                    st.session_state.trainings['training_id'].tolist(),
                    format_func=lambda x: st.session_state.trainings[
                        st.session_state.trainings['training_id'] == x
                    ]['training_name'].iloc[0],
                    key="bulk_training"
                )
                
                bulk_due_date = st.date_input(
                    "Due Date for All",
                    datetime.now() + timedelta(days=30),
                    key="bulk_due"
                )
                
                if st.button("Assign to All in Role", type="primary"):
                    new_assignments = []
                    skipped = 0
                    
                    for _, emp in role_employees.iterrows():
                        # Check if already assigned
                        existing = st.session_state.training_assignments[
                            (st.session_state.training_assignments['employee_id'] == emp['employee_id']) &
                            (st.session_state.training_assignments['training_id'] == bulk_training)
                        ]
                        
                        if existing.empty:
                            new_assignment = {
                                'assignment_id': f'A{str(len(st.session_state.training_assignments) + len(new_assignments) + 1).zfill(3)}',
                                'employee_id': emp['employee_id'],
                                'training_id': bulk_training,
                                'assigned_date': datetime.now().strftime('%Y-%m-%d'),
                                'due_date': bulk_due_date.strftime('%Y-%m-%d'),
                                'completion_date': None,
                                'status': 'Not Started',
                                'score': None
                            }
                            new_assignments.append(new_assignment)
                        else:
                            skipped += 1
                    
                    if new_assignments:
                        st.session_state.training_assignments = pd.concat(
                            [st.session_state.training_assignments, pd.DataFrame(new_assignments)],
                            ignore_index=True
                        )
                        st.success(f"✅ Training assigned to {len(new_assignments)} employees!" + 
                                 (f"\n⚠️ {skipped} already had this training" if skipped > 0 else ""))
                        st.rerun()
                    else:
                        st.warning("⚠️ All employees in this role already have this training assigned")
        
        with tab2:
            st.subheader("Training Progress Tracking")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.multiselect(
                    "Filter by Status",
                    st.session_state.training_assignments['status'].unique(),
                    default=st.session_state.training_assignments['status'].unique()
                )
            with col2:
                dept_filter = st.multiselect(
                    "Filter by Department",
                    st.session_state.employees['department'].unique(),
                    default=st.session_state.employees['department'].unique()
                )
            with col3:
                search = st.text_input("Search Employee")
            
            # Display assignments
            assignments_display = st.session_state.training_assignments.copy()
            assignments_display = assignments_display[assignments_display['status'].isin(status_filter)]
            
            # Merge with employee and training data
            assignments_display = assignments_display.merge(
                st.session_state.employees[['employee_id', 'name', 'department']],
                on='employee_id',
                how='left'
            )
            assignments_display = assignments_display.merge(
                st.session_state.trainings[['training_id', 'training_name']],
                on='training_id',
                how='left'
            )
            
            assignments_display = assignments_display[assignments_display['department'].isin(dept_filter)]
            
            if search:
                assignments_display = assignments_display[
                    assignments_display['name'].str.contains(search, case=False, na=False)
                ]
            
            st.dataframe(
                assignments_display[[
                    'assignment_id', 'name', 'department', 'training_name', 'assigned_date',
                    'due_date', 'completion_date', 'status', 'score'
                ]],
                use_container_width=True,
                hide_index=True
            )
            
            # Update status section
            st.markdown("---")
            st.subheader("Update Training Status")
            
            if not assignments_display.empty:
                col1, col2, col3 = st.columns(3)
                with col1:
                    update_assignment = st.selectbox(
                        "Select Assignment to Update",
                        assignments_display['assignment_id'].tolist(),
                        format_func=lambda x: f"{assignments_display[assignments_display['assignment_id']==x]['name'].iloc[0]} - {assignments_display[assignments_display['assignment_id']==x]['training_name'].iloc[0]}"
                    )
                
                with col2:
                    new_status = st.selectbox(
                        "New Status",
                        ['Not Started', 'In Progress', 'Completed', 'Overdue']
                    )
                
                with col3:
                    score = st.number_input("Score (if completed)", 0, 100, 0)
                
                if st.button("Update Status", type="primary"):
                    idx = st.session_state.training_assignments[
                        st.session_state.training_assignments['assignment_id'] == update_assignment
                    ].index[0]
                    
                    st.session_state.training_assignments.at[idx, 'status'] = new_status
                    if new_status == 'Completed':
                        st.session_state.training_assignments.at[idx, 'completion_date'] = datetime.now().strftime('%Y-%m-%d')
                        st.session_state.training_assignments.at[idx, 'score'] = float(score)
                    
                    st.success("✅ Status updated successfully!")
                    st.rerun()
            else:
                st.info("No assignments match the current filters")
        
        with tab3:
            st.subheader("Manage Training Catalog")
            
            # Display existing trainings
            st.dataframe(
                st.session_state.trainings,
                use_container_width=True,
                hide_index=True
            )
            
            # Add new training
            st.markdown("---")
            st.subheader("Add New Training")
            
            col1, col2 = st.columns(2)
            with col1:
                new_training_name = st.text_input("Training Name")
                new_description = st.text_area("Description")
                new_duration = st.number_input("Duration (hours)", 1, 40, 4)
            
            with col2:
                new_required_roles = st.multiselect(
                    "Required for Roles",
                    ['All'] + st.session_state.employees['role'].unique().tolist()
                )
                new_frequency = st.selectbox(
                    "Frequency",
                    ['Once', 'Annual', 'Semi-Annual', 'Quarterly', 'Monthly']
                )
                new_compliance_type = st.selectbox(
                    "Compliance Type",
                    ['OSHA', 'Legal', 'Professional', 'Internal', 'Industry Standard']
                )
            
            if st.button("Add Training", type="primary"):
                if new_training_name:
                    new_training = pd.DataFrame({
                        'training_id': [f'T{str(len(st.session_state.trainings) + 1).zfill(3)}'],
                        'training_name': [new_training_name],
                        'description': [new_description],
                        'duration_hours': [new_duration],
                        'required_for_roles': [','.join(new_required_roles)],
                        'frequency': [new_frequency],
                        'compliance_type': [new_compliance_type]
                    })
                    st.session_state.trainings = pd.concat(
                        [st.session_state.trainings, new_training],
                        ignore_index=True
                    )
                    st.success("✅ Training added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a training name")
    
    # COMPLIANCE REPORTING (continuing from previous sections)
    elif page == "📈 Compliance Reporting":
        st.header("📈 Regulatory Compliance Reporting")
        
        tab1, tab2, tab3 = st.tabs(["Overview Report", "Detailed Analytics", "Export Reports"])
        
        with tab1:
            st.subheader("Compliance Overview")
            
            # Overall compliance metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_assignments = len(st.session_state.training_assignments)
            completed = len(st.session_state.training_assignments[
                st.session_state.training_assignments['status'] == 'Completed'
            ])
            overdue = len(st.session_state.training_assignments[
                st.session_state.training_assignments['status'] == 'Overdue'
            ])
            in_progress = len(st.session_state.training_assignments[
                st.session_state.training_assignments['status'] == 'In Progress'
            ])
            
            with col1:
                st.metric("Total Assignments", total_assignments)
            with col2:
                st.metric("Completed", completed, f"{completed/total_assignments*100:.1f}%" if total_assignments > 0 else "0%")
            with col3:
                st.metric("Overdue", overdue, f"{overdue/total_assignments*100:.1f}%" if total_assignments > 0 else "0%")
            with col4:
                st.metric("In Progress", in_progress, f"{in_progress/total_assignments*100:.1f}%" if total_assignments > 0 else "0%")
            
            st.markdown("---")
            
            # Compliance by type
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Compliance by Type")
                compliance_data = st.session_state.training_assignments.merge(
                    st.session_state.trainings[['training_id', 'compliance_type']],
                    on='training_id'
                )
                
                type_compliance = []
                for comp_type in compliance_data['compliance_type'].unique():
                    type_data = compliance_data[compliance_data['compliance_type'] == comp_type]
                    total = len(type_data)
                    completed = len(type_data[type_data['status'] == 'Completed'])
                    compliance_rate = (completed / total * 100) if total > 0 else 0
                    
                    type_compliance.append({
                        'Type': comp_type,
                        'Total': total,
                        'Completed': completed,
                        'Compliance Rate': compliance_rate
                    })
                
                type_df = pd.DataFrame(type_compliance)
                fig = px.bar(
                    type_df,
                    x='Type',
                    y='Compliance Rate',
                    color='Compliance Rate',
                    color_continuous_scale='RdYlGn',
                    text='Compliance Rate'
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Employee Compliance Scores")
                employee_scores = []
                for emp_id in st.session_state.employees['employee_id']:
                    score = calculate_compliance_score(emp_id)
                    name = st.session_state.employees[
                        st.session_state.employees['employee_id'] == emp_id
                    ]['name'].iloc[0]
                    employee_scores.append({'Employee': name, 'Score': score})
                
                scores_df = pd.DataFrame(employee_scores).sort_values('Score', ascending=True)
                fig = px.bar(
                    scores_df,
                    y='Employee',
                    x='Score',
                    orientation='h',
                    color='Score',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table
            st.markdown("---")
            st.subheader("Detailed Compliance Status")
            
            detailed_report = st.session_state.training_assignments.merge(
                st.session_state.employees[['employee_id', 'name', 'role', 'department']],
                on='employee_id'
            ).merge(
                st.session_state.trainings[['training_id', 'training_name', 'compliance_type']],
                on='training_id'
            )
            
            st.dataframe(
                detailed_report[[
                    'name', 'role', 'department', 'training_name', 'compliance_type',
                    'assigned_date', 'due_date', 'status', 'score'
                ]],
                use_container_width=True,
                hide_index=True
            )
        
        with tab2:
            st.subheader("Detailed Analytics")
            
            # Time series analysis
            st.markdown("#### Training Completion Trend")
            
            completed_trainings = st.session_state.training_assignments[
                st.session_state.training_assignments['status'] == 'Completed'
            ].copy()
            
            if not completed_trainings.empty and 'completion_date' in completed_trainings.columns:
                completed_trainings = completed_trainings[completed_trainings['completion_date'].notna()]
                if not completed_trainings.empty:
                    completed_trainings['completion_date'] = pd.to_datetime(
                        completed_trainings['completion_date']
                    )
                    completed_trainings['month'] = completed_trainings['completion_date'].dt.to_period('M').astype(str)
                    
                    monthly_completions = completed_trainings.groupby('month').size().reset_index(name='Completions')
                    
                    fig = px.line(
                        monthly_completions,
                        x='month',
                        y='Completions',
                        markers=True,
                        title="Monthly Training Completions"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No completed trainings to display")
            else:
                st.info("No completed trainings to display")
            
            # Department comparison
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Average Scores by Department")
                dept_scores_df = st.session_state.training_assignments[
                    st.session_state.training_assignments['score'].notna()
                ].merge(
                    st.session_state.employees[['employee_id', 'department']],
                    on='employee_id'
                )
                
                if not dept_scores_df.empty:
                    dept_scores = dept_scores_df.groupby('department')['score'].mean().reset_index()
                    fig = px.bar(dept_scores, x='department', y='score', color='score',
                               color_continuous_scale='Viridis',
                               title="Average Training Scores by Department")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No score data available")
            
            with col2:
                st.markdown("#### Training Hours by Employee")
                training_hours = st.session_state.training_assignments[
                    st.session_state.training_assignments['status'] == 'Completed'
                ].merge(
                    st.session_state.employees[['employee_id', 'name']],
                    on='employee_id'
                ).merge(
                    st.session_state.trainings[['training_id', 'duration_hours']],
                    on='training_id'
                )
                
                if not training_hours.empty:
                    training_hours_summary = training_hours.groupby('name')['duration_hours'].sum().reset_index()
                    fig = px.bar(training_hours_summary, x='name', y='duration_hours',
                               labels={'duration_hours': 'Total Hours'},
                               title="Total Training Hours Completed")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No completed training hours to display")
        
        with tab3:
            st.subheader("Export Compliance Reports")
            
            report_type = st.selectbox(
                "Select Report Type",
                [
                    "Full Compliance Report",
                    "Employee Training Summary",
                    "Certification Status Report",
                    "Department Compliance Report",
                    "Overdue Trainings Report"
                ]
            )
            
            date_range = st.date_input(
                "Report Date Range",
                [datetime.now() - timedelta(days=90), datetime.now()]
            )
            
            if st.button("Generate Report", type="primary"):
                if report_type == "Full Compliance Report":
                    report_data = st.session_state.training_assignments.merge(
                        st.session_state.employees,
                        on='employee_id'
                    ).merge(
                        st.session_state.trainings,
                        on='training_id'
                    )
                
                elif report_type == "Employee Training Summary":
                    report_data = st.session_state.training_assignments.merge(
                        st.session_state.employees[['employee_id', 'name', 'department']],
                        on='employee_id'
                    ).merge(
                        st.session_state.trainings[['training_id', 'training_name']],
                        on='training_id'
                    )
                
                elif report_type == "Certification Status Report":
                    report_data = st.session_state.certifications.merge(
                        st.session_state.employees[['employee_id', 'name', 'department']],
                        on='employee_id'
                    )
                    report_data['days_until_expiry'] = report_data['expiry_date'].apply(
                        calculate_days_until_expiry
                    )
                
                elif report_type == "Department Compliance Report":
                    report_data = st.session_state.training_assignments.merge(
                        st.session_state.employees[['employee_id', 'name', 'department']],
                        on='employee_id'
                    )
                    
                elif report_type == "Overdue Trainings Report":
                    report_data = st.session_state.training_assignments[
                        st.session_state.training_assignments['status'] == 'Overdue'
                    ].merge(
                        st.session_state.employees[['employee_id', 'name', 'email', 'department']],
                        on='employee_id'
                    ).merge(
                        st.session_state.trainings[['training_id', 'training_name']],
                        on='training_id'
                    )
                
                # Display preview
                st.markdown("### Report Preview")
                st.dataframe(report_data, use_container_width=True)
                
                # Download options
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    # CSV export
                    csv = report_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name=f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        type="primary"
                    )
                
                with col2:
                    # Excel export
                    try:
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            report_data.to_excel(writer, index=False, sheet_name='Report')
                        output.seek(0)
                        
                        st.download_button(
                            label="📥 Download as Excel",
                            data=output,
                            file_name=f"{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            type="primary"
                        )
                    except ImportError:
                        st.warning("Excel export requires 'xlsxwriter'. Install with: pip install xlsxwriter")
    
    # TRAINING TRANSCRIPTS
    elif page == "📜 Training Transcripts":
        st.header("📜 Training Transcripts")
        
        # Select employee
        selected_employee = st.selectbox(
            "Select Employee",
            st.session_state.employees['employee_id'].tolist(),
            format_func=lambda x: st.session_state.employees[
                st.session_state.employees['employee_id'] == x
            ]['name'].iloc[0]
        )
        
        employee, transcript = generate_transcript(selected_employee)
        
        # Employee Information Header
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"**Name:** {employee['name']}")
            st.markdown(f"**Employee ID:** {employee['employee_id']}")
        with col2:
            st.markdown(f"**Role:** {employee['role']}")
            st.markdown(f"**Department:** {employee['department']}")
        with col3:
            compliance_score = calculate_compliance_score(selected_employee)
            st.markdown(f"**Compliance Score:** {compliance_score}%")
            st.markdown(f"**Hire Date:** {employee['hire_date']}")
        with col4:
            st.markdown(f"**Email:** {employee['email']}")
            st.markdown(f"**Phone:** {employee['phone']}")
        
        st.markdown("---")
        
        # Training History
        st.subheader("Completed Training History")
        
        if not transcript.empty:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Trainings", len(transcript))
            with col2:
                avg_score = transcript['score'].mean()
                st.metric("Average Score", f"{avg_score:.1f}" if pd.notna(avg_score) else "N/A")
            with col3:
                total_hours = transcript['duration_hours'].sum()
                st.metric("Total Hours", f"{total_hours}h")
            with col4:
                latest = transcript['completion_date'].max()
                st.metric("Latest Completion", latest)
            
            st.markdown("---")
            
            # Detailed transcript
            display_transcript = transcript[[
                'training_name', 'description', 'completion_date', 'score',
                'duration_hours', 'compliance_type'
            ]].copy()
            display_transcript.columns = [
                'Training', 'Description', 'Completion Date', 'Score',
                'Hours', 'Compliance Type'
            ]
            
            st.dataframe(display_transcript, use_container_width=True, hide_index=True)
            
            # Certifications
            st.markdown("---")
            st.subheader("Certifications")
            
            employee_certs = st.session_state.certifications[
                st.session_state.certifications['employee_id'] == selected_employee
            ].copy()
            
            if not employee_certs.empty:
                employee_certs['days_until_expiry'] = employee_certs['expiry_date'].apply(
                    calculate_days_until_expiry
                )
                st.dataframe(
                    employee_certs[['cert_name', 'issue_date', 'expiry_date', 'status', 'issuing_organization', 'days_until_expiry']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No certifications on record")
            
            # Export transcript
            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                if st.button("📥 Download as PDF", type="primary"):
                    st.info("PDF generation feature coming soon!")
            with col3:
                try:
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        # Employee info sheet
                        emp_info = pd.DataFrame([{
                            'Name': employee['name'],
                            'Employee ID': employee['employee_id'],
                            'Role': employee['role'],
                            'Department': employee['department'],
                            'Compliance Score': f"{compliance_score}%",
                            'Generated Date': datetime.now().strftime('%Y-%m-%d')
                        }])
                        emp_info.to_excel(writer, sheet_name='Employee Info', index=False)
                        
                        # Training history
                        display_transcript.to_excel(writer, sheet_name='Training History', index=False)
                        
                        # Certifications
                        if not employee_certs.empty:
                            employee_certs.to_excel(writer, sheet_name='Certifications', index=False)
                    
                    output.seek(0)
                    
                    st.download_button(
                        label="📄 Download Excel",
                        data=output,
                        file_name=f"Training_Transcript_{employee['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary"
                    )
                except ImportError:
                    csv_data = display_transcript.to_csv(index=False)
                    st.download_button(
                        label="📄 Download CSV",
                        data=csv_data,
                        file_name=f"Training_Transcript_{employee['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        type="primary"
                    )
        else:
            st.info("No completed trainings for this employee")
            
            # Show pending trainings
            st.markdown("---")
            st.subheader("Pending Trainings")
            pending = st.session_state.training_assignments[
                (st.session_state.training_assignments['employee_id'] == selected_employee) &
                (st.session_state.training_assignments['status'] != 'Completed')
            ].merge(
                st.session_state.trainings[['training_id', 'training_name', 'due_date']],
                on='training_id',
                how='left'
            )
            
            if not pending.empty:
                st.dataframe(
                    pending[['training_name', 'assigned_date', 'due_date_y', 'status']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No pending trainings")
    
    # SKILLS GAP ANALYSIS
    elif page == "🎯 Skills Gap Analysis":
        st.header("🎯 Skills Gap Analysis")
        
        tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Team Analysis", "Skills Matrix"])
        
        with tab1:
            st.subheader("Individual Skills Gap Analysis")
            
            selected_employee = st.selectbox(
                "Select Employee",
                st.session_state.employees['employee_id'].tolist(),
                format_func=lambda x: st.session_state.employees[
                    st.session_state.employees['employee_id'] == x
                ]['name'].iloc[0],
                key="gap_employee"
            )
            
            employee = st.session_state.employees[
                st.session_state.employees['employee_id'] == selected_employee
            ].iloc[0]
            
            st.markdown(f"**Name:** {employee['name']} | **Role:** {employee['role']} | **Department:** {employee['department']}")
            
            gap_analysis = analyze_skills_gap(selected_employee)
            
            if not gap_analysis.empty:
                # Visualization
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Skills Overview")
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        name='Current Level',
                        x=gap_analysis['skill_name'],
                        y=gap_analysis['current_level_num'],
                        marker_color='lightblue'
                    ))
                    
                    fig.add_trace(go.Bar(
                        name='Required Level',
                        x=gap_analysis['skill_name'],
                        y=gap_analysis['required_level_num'],
                        marker_color='darkblue'
                    ))
                    
                    fig.update_layout(barmode='group', yaxis_title='Proficiency Level (1-4)')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### Gap Magnitude")
                    gap_data = gap_analysis[['skill_name', 'gap']].copy()
                    gap_data['gap_status'] = gap_data['gap'].apply(
                        lambda x: 'Exceeds' if x < 0 else ('Meets' if x == 0 else 'Gap')
                    )
                    
                    fig = px.bar(
                        gap_data,
                        x='skill_name',
                        y='gap',
                        color='gap_status',
                        color_discrete_map={
                            'Exceeds': '#51cf66',
                            'Meets': '#ffd43b',
                            'Gap': '#ff6b6b'
                        }
                    )
                    fig.update_layout(yaxis_title='Gap Level')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detaile
                # Detailed table
                st.markdown("---")
                st.subheader("Detailed Skills Assessment")
                
                display_gap = gap_analysis[[
                    'skill_name', 'current_level', 'required_level', 'last_assessed', 'gap'
                ]].copy()
                display_gap['status'] = display_gap['gap'].apply(
                    lambda x: '✅ Exceeds' if x < 0 else ('✅ Meets' if x == 0 else '⚠️ Needs Improvement')
                )
                
                st.dataframe(display_gap, use_container_width=True, hide_index=True)
                
                # Recommendations
                gaps = gap_analysis[gap_analysis['gap'] > 0]
                if not gaps.empty:
                    st.markdown("---")
                    st.subheader("📋 Development Recommendations")
                    
                    for _, skill in gaps.iterrows():
                        priority = '🔴 High' if skill['gap'] > 1 else '🟡 Medium'
                        st.markdown(f"""
                        <div class="warning-card">
                            <strong>{skill['skill_name']}</strong> - Priority: {priority}<br>
                            Current: {skill['current_level']} → Target: {skill['required_level']}<br>
                            Gap: {skill['gap']} level(s)<br>
                            Last Assessed: {skill['last_assessed']}<br>
                            <em>Recommended Action: Assign relevant training programs and schedule reassessment</em>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ All skills meet or exceed requirements!")
            else:
                st.info("No skills data available for this employee")
                st.markdown("---")
                st.subheader("Add Initial Skills Assessment")
                
                with st.form("add_initial_skills"):
                    available_skills = st.session_state.skills_matrix['skill_id'].tolist()
                    selected_skill = st.selectbox(
                        "Select Skill",
                        available_skills,
                        format_func=lambda x: st.session_state.skills_matrix[
                            st.session_state.skills_matrix['skill_id'] == x
                        ]['skill_name'].iloc[0]
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        current = st.selectbox("Current Level", ['Beginner', 'Intermediate', 'Advanced', 'Expert'])
                    with col2:
                        required = st.selectbox("Required Level", ['Beginner', 'Intermediate', 'Advanced', 'Expert'])
                    
                    if st.form_submit_button("Add Skill Assessment", type="primary"):
                        new_skill = pd.DataFrame({
                            'employee_id': [selected_employee],
                            'skill_id': [selected_skill],
                            'current_level': [current],
                            'required_level': [required],
                            'last_assessed': [datetime.now().strftime('%Y-%m-%d')]
                        })
                        
                        st.session_state.employee_skills = pd.concat(
                            [st.session_state.employee_skills, new_skill],
                            ignore_index=True
                        )
                        st.success("✅ Skill assessment added!")
                        st.rerun()
        
        with tab2:
            st.subheader("Team Skills Gap Analysis")
            
            # Select department or role
            col1, col2 = st.columns(2)
            with col1:
                analysis_type = st.radio("Analyze by:", ["Department", "Role"])
            
            with col2:
                if analysis_type == "Department":
                    selected_group = st.selectbox(
                        "Select Department",
                        st.session_state.employees['department'].unique()
                    )
                    team_employees = st.session_state.employees[
                        st.session_state.employees['department'] == selected_group
                    ]['employee_id'].tolist()
                else:
                    selected_group = st.selectbox(
                        "Select Role",
                        st.session_state.employees['role'].unique()
                    )
                    team_employees = st.session_state.employees[
                        st.session_state.employees['role'] == selected_group
                    ]['employee_id'].tolist()
            
            # Aggregate team skills
            team_gaps = []
            for emp_id in team_employees:
                emp_skills = st.session_state.employee_skills[
                    st.session_state.employee_skills['employee_id'] == emp_id
                ]
                if not emp_skills.empty:
                    team_gaps.append(emp_skills)
            
            if team_gaps:
                team_skills = pd.concat(team_gaps)
                team_skills = team_skills.merge(
                    st.session_state.skills_matrix[['skill_id', 'skill_name']],
                    on='skill_id'
                )
                
                # Define proficiency levels
                levels = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Expert': 4}
                team_skills['current_level_num'] = team_skills['current_level'].map(levels)
                team_skills['required_level_num'] = team_skills['required_level'].map(levels)
                team_skills['gap'] = team_skills['required_level_num'] - team_skills['current_level_num']
                
                # Average gap by skill
                skill_summary = team_skills.groupby('skill_name').agg({
                    'gap': 'mean',
                    'current_level_num': 'mean',
                    'required_level_num': 'mean',
                    'employee_id': 'count'
                }).reset_index()
                skill_summary.columns = ['skill_name', 'avg_gap', 'avg_current', 'avg_required', 'employee_count']
                
                # Visualization
                st.markdown(f"#### Skills Gap Summary - {selected_group}")
                st.markdown(f"*Analysis of {len(team_employees)} employees | {len(skill_summary)} skills assessed*")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        name='Average Current Level',
                        x=skill_summary['skill_name'],
                        y=skill_summary['avg_current'],
                        marker_color='lightblue'
                    ))
                    
                    fig.add_trace(go.Bar(
                        name='Required Level',
                        x=skill_summary['skill_name'],
                        y=skill_summary['avg_required'],
                        marker_color='darkblue'
                    ))
                    
                    fig.update_layout(
                        barmode='group', 
                        yaxis_title='Average Proficiency Level',
                        title="Current vs Required Skills"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.bar(
                        skill_summary,
                        x='skill_name',
                        y='avg_gap',
                        color='avg_gap',
                        color_continuous_scale='RdYlGn_r',
                        title="Average Skills Gap"
                    )
                    fig.update_layout(yaxis_title='Gap Level')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Gap distribution
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Gap Distribution by Status")
                    gap_distribution = team_skills['gap'].value_counts().reset_index()
                    gap_distribution.columns = ['Gap Level', 'Count']
                    gap_distribution['Status'] = gap_distribution['Gap Level'].apply(
                        lambda x: 'Exceeds' if x < 0 else ('Meets' if x == 0 else 'Needs Development')
                    )
                    
                    status_summary = gap_distribution.groupby('Status')['Count'].sum().reset_index()
                    
                    fig = px.pie(
                        status_summary,
                        values='Count',
                        names='Status',
                        color='Status',
                        color_discrete_map={
                            'Exceeds': '#51cf66',
                            'Meets': '#ffd43b',
                            'Needs Development': '#ff6b6b'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### Skills Assessment Coverage")
                    total_possible = len(team_employees) * len(st.session_state.skills_matrix)
                    total_assessed = len(team_skills)
                    coverage = (total_assessed / total_possible * 100) if total_possible > 0 else 0
                    
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=coverage,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Assessment Coverage"},
                        delta={'reference': 100},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "gray"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detailed table
                st.markdown("---")
                st.subheader("Detailed Skills Summary")
                st.dataframe(skill_summary, use_container_width=True, hide_index=True)
                
                # Recommendations
                st.markdown("---")
                st.subheader("🎯 Team Development Priorities")
                
                priority_skills = skill_summary[skill_summary['avg_gap'] > 0.5].sort_values('avg_gap', ascending=False)
                
                if not priority_skills.empty:
                    for _, skill in priority_skills.iterrows():
                        priority = '🔴 High' if skill['avg_gap'] > 1.5 else ('🟡 Medium' if skill['avg_gap'] > 1 else '🟢 Low')
                        st.markdown(f"""
                        <div class="warning-card">
                            <strong>{skill['skill_name']}</strong> - Priority: {priority}<br>
                            Average Gap: {skill['avg_gap']:.2f} levels<br>
                            Current Avg: {skill['avg_current']:.1f} | Target: {skill['avg_required']:.1f}<br>
                            Employees Assessed: {skill['employee_count']}<br>
                            <em>Recommended Action: Develop training program for {selected_group}</em>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ Team meets all required skill levels!")
                
                # Export team analysis
                st.markdown("---")
                csv = skill_summary.to_csv(index=False)
                st.download_button(
                    label="📥 Export Team Analysis",
                    data=csv,
                    file_name=f"Skills_Gap_Analysis_{selected_group.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No skills data available for this team")
                st.warning("Please add skill assessments for employees in this group")
        
        with tab3:
            st.subheader("Skills Matrix Management")
            
            # Display current skills matrix
            st.markdown("#### Defined Skills")
            st.dataframe(
                st.session_state.skills_matrix,
                use_container_width=True,
                hide_index=True
            )
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Skills", len(st.session_state.skills_matrix))
            with col2:
                assessments = len(st.session_state.employee_skills)
                st.metric("Total Assessments", assessments)
            with col3:
                avg_assessments = assessments / len(st.session_state.employees) if len(st.session_state.employees) > 0 else 0
                st.metric("Avg per Employee", f"{avg_assessments:.1f}")
            with col4:
                levels_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Expert': 4}
                if not st.session_state.employee_skills.empty:
                    avg_level = st.session_state.employee_skills['current_level'].map(levels_map).mean()
                    st.metric("Avg Skill Level", f"{avg_level:.1f}/4")
                else:
                    st.metric("Avg Skill Level", "N/A")
            
            # Add new skill
            st.markdown("---")
            st.subheader("Add New Skill")
            
            with st.form("add_skill_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_skill_name = st.text_input("Skill Name *")
                    new_skill_roles = st.multiselect(
                        "Required for Roles *",
                        ['All'] + st.session_state.employees['role'].unique().tolist(),
                        key="new_skill_roles"
                    )
                
                with col2:
                    st.markdown("**Default Proficiency Levels:**")
                    st.info("• Beginner\n• Intermediate\n• Advanced\n• Expert")
                
                if st.form_submit_button("Add Skill", type="primary"):
                    if new_skill_name and new_skill_roles:
                        new_skill = pd.DataFrame({
                            'skill_id': [f'S{str(len(st.session_state.skills_matrix) + 1).zfill(3)}'],
                            'skill_name': [new_skill_name],
                            'required_for_roles': [','.join(new_skill_roles)],
                            'proficiency_levels': ['Beginner,Intermediate,Advanced,Expert']
                        })
                        st.session_state.skills_matrix = pd.concat(
                            [st.session_state.skills_matrix, new_skill],
                            ignore_index=True
                        )
                        st.success(f"✅ Skill '{new_skill_name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields")
            
            # Assess employee skills
            st.markdown("---")
            st.subheader("Assess Employee Skills")
            
            with st.form("assess_skills_form"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    assess_employee = st.selectbox(
                        "Select Employee",
                        st.session_state.employees['employee_id'].tolist(),
                        format_func=lambda x: st.session_state.employees[
                            st.session_state.employees['employee_id'] == x
                        ]['name'].iloc[0],
                        key="assess_employee"
                    )
                
                with col2:
                    assess_skill = st.selectbox(
                        "Select Skill",
                        st.session_state.skills_matrix['skill_id'].tolist(),
                        format_func=lambda x: st.session_state.skills_matrix[
                            st.session_state.skills_matrix['skill_id'] == x
                        ]['skill_name'].iloc[0]
                    )
                
                with col3:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        current_level = st.selectbox(
                            "Current Level",
                            ['Beginner', 'Intermediate', 'Advanced', 'Expert']
                        )
                    with col_b:
                        required_level = st.selectbox(
                            "Required Level",
                            ['Beginner', 'Intermediate', 'Advanced', 'Expert'],
                            index=2  # Default to Advanced
                        )
                
                if st.form_submit_button("Save Assessment", type="primary"):
                    # Check if assessment exists
                    existing = st.session_state.employee_skills[
                        (st.session_state.employee_skills['employee_id'] == assess_employee) &
                        (st.session_state.employee_skills['skill_id'] == assess_skill)
                    ]
                    
                    if not existing.empty:
                        # Update existing
                        idx = existing.index[0]
                        st.session_state.employee_skills.at[idx, 'current_level'] = current_level
                        st.session_state.employee_skills.at[idx, 'required_level'] = required_level
                        st.session_state.employee_skills.at[idx, 'last_assessed'] = datetime.now().strftime('%Y-%m-%d')
                        st.success("✅ Assessment updated!")
                    else:
                        # Add new
                        new_assessment = pd.DataFrame({
                            'employee_id': [assess_employee],
                            'skill_id': [assess_skill],
                            'current_level': [current_level],
                            'required_level': [required_level],
                            'last_assessed': [datetime.now().strftime('%Y-%m-%d')]
                        })
                        st.session_state.employee_skills = pd.concat(
                            [st.session_state.employee_skills, new_assessment],
                            ignore_index=True
                        )
                        st.success("✅ Assessment saved!")
                    st.rerun()
            
            # Bulk assessment
            st.markdown("---")
            st.subheader("Bulk Skills Assessment")
            
            with st.expander("📊 Assess Multiple Employees"):
                bulk_skill = st.selectbox(
                    "Select Skill for Bulk Assessment",
                    st.session_state.skills_matrix['skill_id'].tolist(),
                    format_func=lambda x: st.session_state.skills_matrix[
                        st.session_state.skills_matrix['skill_id'] == x
                    ]['skill_name'].iloc[0],
                    key="bulk_skill"
                )
                
                bulk_employees = st.multiselect(
                    "Select Employees",
                    st.session_state.employees['employee_id'].tolist(),
                    format_func=lambda x: st.session_state.employees[
                        st.session_state.employees['employee_id'] == x
                    ]['name'].iloc[0]
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    bulk_current = st.selectbox(
                        "Current Level (same for all)",
                        ['Beginner', 'Intermediate', 'Advanced', 'Expert'],
                        key="bulk_current"
                    )
                with col2:
                    bulk_required = st.selectbox(
                        "Required Level (same for all)",
                        ['Beginner', 'Intermediate', 'Advanced', 'Expert'],
                        index=2,
                        key="bulk_required"
                    )
                
                if st.button("Apply Bulk Assessment", type="primary"):
                    if bulk_employees:
                        added = 0
                        updated = 0
                        
                        for emp_id in bulk_employees:
                            existing = st.session_state.employee_skills[
                                (st.session_state.employee_skills['employee_id'] == emp_id) &
                                (st.session_state.employee_skills['skill_id'] == bulk_skill)
                            ]
                            
                            if not existing.empty:
                                idx = existing.index[0]
                                st.session_state.employee_skills.at[idx, 'current_level'] = bulk_current
                                st.session_state.employee_skills.at[idx, 'required_level'] = bulk_required
                                st.session_state.employee_skills.at[idx, 'last_assessed'] = datetime.now().strftime('%Y-%m-%d')
                                updated += 1
                            else:
                                new_assessment = pd.DataFrame({
                                    'employee_id': [emp_id],
                                    'skill_id': [bulk_skill],
                                    'current_level': [bulk_current],
                                    'required_level': [bulk_required],
                                    'last_assessed': [datetime.now().strftime('%Y-%m-%d')]
                                })
                                st.session_state.employee_skills = pd.concat(
                                    [st.session_state.employee_skills, new_assessment],
                                    ignore_index=True
                                )
                                added += 1
                        
                        st.success(f"✅ Bulk assessment complete!\nAdded: {added} | Updated: {updated}")
                        st.rerun()
                    else:
                        st.warning("Please select at least one employee")

if __name__ == "__main__":
    main()