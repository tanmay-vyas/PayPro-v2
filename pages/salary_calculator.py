import streamlit as st
from datetime import datetime
import random
import pymysql
from pymysql.cursors import DictCursor
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


class SlipIDGenerator:
    @staticmethod
    def generate():
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"SLIP-{timestamp}-{random_num}"


class EmployeeSalary:
    def __init__(self, employee_id, gross_salary, present_days,
                 total_days, username,):
        self.employee_id = employee_id
        self.gross_salary = gross_salary
        self.present_days = present_days
        self.total_days = total_days
        self.username = username
        self.calculation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.slip_id = SlipIDGenerator.generate()

        self.proportional_salary = None
        self.pf = None
        self.hra = None
        self.tax = None
        self.da = None
        self.medical_insurance = 1000  # fixed
        self.transport_allowance = None
        self.bonus = None
        self.attendance_pct = None
        self.total_deductions = None
        self.take_home = None

    def calculate(self):
        self.proportional_salary = (
            self.gross_salary * self.present_days) / self.total_days
        self.pf = self.proportional_salary * 0.12
        self.hra = self.proportional_salary * 0.10
        self.tax = self.proportional_salary * 0.15
        self.da = self.proportional_salary * 0.08
        self.transport_allowance = self.proportional_salary * 0.02
        self.attendance_pct = (self.present_days / self.total_days) * 100
        self.bonus = self.proportional_salary * 0.05 if self.attendance_pct >= 75 else 0
        self.total_deductions = self.pf + self.tax
        self.take_home = self.proportional_salary - self.total_deductions + self.bonus

    def to_dict(self):
        return {
            "slip_id": self.slip_id,
            "employee_id": self.employee_id,
            "username": self.username,
            "calculation_date": self.calculation_date,
            "present_days": self.present_days,
            "total_days": self.total_days,
            "gross_salary": round(self.gross_salary, 2),
            "proportional_salary": round(self.proportional_salary, 2),
            "pf_deduction": round(self.pf, 2),
            "tax_deduction": round(self.tax, 2),
            "hra": round(self.hra, 2),
            "da": round(self.da, 2),
            "medical_insurance": round(self.medical_insurance, 2),
            "transport_allowance": round(self.transport_allowance, 2),
            "bonus": round(self.bonus, 2),
            "attendance_percentage": round(self.attendance_pct, 2),
            "total_deductions": round(self.total_deductions, 2),
            "take_home_salary": round(self.take_home, 2),
        }


class EmployeeDataStorageMySQL:
    def __init__(self, host='localhost', user="root", password='root', database='employee_salary_data_db'):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='employee_salary_data_db',
            cursorclass=DictCursor,
            autocommit=True
        )

    def save_employee_data(self, employee_data: dict):
        with self.connection.cursor() as cursor:
            sql = """
            INSERT  INTO salary_slips (
                slip_id, employee_id, username, calculation_date,
                present_days, total_days, gross_salary, proportional_salary,
                pf_deduction, tax_deduction, hra, da, medical_insurance,
                transport_allowance, bonus, attendance_percentage,
                total_deductions, take_home_salary
            ) VALUES (
                %(slip_id)s, %(employee_id)s, %(username)s, %(calculation_date)s,
                %(present_days)s, %(total_days)s, %(gross_salary)s, %(proportional_salary)s,
                %(pf_deduction)s, %(tax_deduction)s, %(hra)s, %(da)s, %(medical_insurance)s,
                %(transport_allowance)s, %(bonus)s, %(attendance_percentage)s,
                %(total_deductions)s, %(take_home_salary)s
            )
            """
            cursor.execute(sql, employee_data)

    def close(self):
        self.connection.close()


class SalaryCalculatorApp:
    def __init__(self):
        self.username = st.session_state.get("username", "User")
        self.logged_in = st.session_state.get("logged_in", False)
        self.salary_slip_data = None
        # Initialize MySQL storage (update credentials accordingly)
        self.storage = EmployeeDataStorageMySQL(
            host='localhost',
            user='admin',
            password='password',
            database='employee_salary_data_db'
        )

    def add_custom_css(self):
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
            margin-bottom: 1rem;
        }

        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin: 0.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .success-alert {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }

        .error-alert {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }

        .info-box {
            background: #e8f4f8;
            border-left: 4px solid #17a2b8;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 5px;
            color: #333;
        }

        .info-box strong {
            color: #2c3e50;
        }

        .info-box small {
            color: #6c757d;
        }

        .stButton > button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        .sidebar .stSelectbox > div > div {
            background: #f8f9fa;
            border-radius: 8px;
        }

        .attendance-gauge {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)

    def display_header(self):
        st.markdown(f"""
        <div class="main-header">
            <h1>💰 Employee Salary Calculator</h1>
            <p>Welcome back, <strong>{self.username}</strong>! Let's calculate your salary details.</p>
        </div>
        """, unsafe_allow_html=True)

    def create_salary_form(self):
        st.markdown("### 📋 Employee Information")

        # Create columns for better layout
        col1, col2 = st.columns(2)

        with col1:
            employee_id = st.text_input(
                "👤 Employee ID",
                placeholder="e.g., EMP001",
                help="Enter your unique employee identification number"
            )

            gross_salary = st.number_input(
                "💵 Gross Salary (₹)",
                min_value=0.0,
                step=1000.0,
                max_value=100000000.0,
                help="Enter your monthly gross salary"
            )

        with col2:
            present_days = st.number_input(
                "📅 Present Days",
                min_value=0,
                max_value=31,
                step=1,
                help="Number of days you were present this month"
            )

            total_days = st.number_input(
                "📊 Total Working Days",
                min_value=0,
                max_value=31,
                step=1,
                value=30,
                help="Total working days in the month"
            )

        # Real-time validation feedback
        if employee_id and gross_salary > 0 and present_days >= 0 and total_days > 0:
            if present_days <= total_days:
                attendance_pct = (present_days / total_days) * 100

                # Attendance status indicator
                if attendance_pct >= 90:
                    status_color = "green"
                    status_text = "Excellent"
                elif attendance_pct >= 75:
                    status_color = "orange"
                    status_text = "Good"
                else:
                    status_color = "red"
                    status_text = "Needs Improvement"

                st.markdown(f"""
                <div class="info-box">
                    <strong>📊 Attendance Status:</strong>
                    <span style="color: {status_color}; font-weight: bold;">{attendance_pct:.1f}% ({status_text})</span>
                    <br>
                    <small>💡 Tip: Maintain >75% attendance for bonus eligibility!</small>
                </div>
                """, unsafe_allow_html=True)

        return employee_id, gross_salary, present_days, total_days

    def validate_inputs(self, employee_id, gross_salary, present_days, total_days):
        if not employee_id:
            st.error("🚫 Employee ID is required!")
            return False
        if gross_salary <= 0:
            st.error("🚫 Gross salary must be greater than 0!")
            return False
        if present_days < 0:
            st.error("🚫 Present days cannot be negative!")
            return False
        if total_days <= 0:
            st.error("🚫 Total working days must be greater than 0!")
            return False
        if present_days > total_days:
            st.error("🚫 Present days cannot exceed total working days!")
            return False
        return True

    def create_salary_breakdown_chart(self, emp_salary):
        # Create a pie chart for salary breakdown
        labels = ['Take Home', 'PF Deduction', 'Tax Deduction']
        values = [emp_salary.take_home, emp_salary.pf, emp_salary.tax]
        colors = ['#28a745', '#dc3545', '#ffc107']

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
            textinfo='label+percent',
            textfont=dict(size=14, color='white'))
        ])

        fig.update_layout(
            title={
                'text': "💰 Salary Distribution",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 18, 'color': 'white'}
            },
            font=dict(size=12),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=80, b=80, l=50, r=50),
            height=400
        )

        return fig

    def create_allowances_chart(self, emp_salary):
        # Create a bar chart for allowances and deductions
        categories = ['HRA', 'DA', 'Transport',
                      'Medical', 'Bonus', 'PF', 'Tax']
        values = [emp_salary.hra, emp_salary.da, emp_salary.transport_allowance,
                  emp_salary.medical_insurance, emp_salary.bonus, -emp_salary.pf, -emp_salary.tax]
        colors = ['#28a745', '#28a745', '#28a745',
                  '#17a2b8', '#ffc107', '#dc3545', '#dc3545']

        fig = go.Figure(data=[go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f'₹{abs(v):,.0f}' for v in values],
            textposition='auto',
        )])

        fig.update_layout(
            title={
                'text': "📊 Allowances & Deductions Breakdown",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 18, 'color': 'white'}
            },
            xaxis_title="Components",
            yaxis_title="Amount (₹)",
            font=dict(size=12),
            margin=dict(t=80, b=80, l=50, r=50),
            height=400
        )

        return fig

    def display_salary_metrics(self, emp_salary):
        st.markdown("### 📈 Salary Metrics")

        # Create metric cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="💰 Take Home Salary",
                value=f"₹{emp_salary.take_home:,.0f}",
                delta=f"₹{emp_salary.bonus:,.0f} bonus"
            )

        with col2:
            st.metric(
                label="📊 Attendance",
                value=f"{emp_salary.attendance_pct:.1f}%",
                delta="Good" if emp_salary.attendance_pct >= 75 else "Needs Improvement"
            )

        with col3:
            st.metric(
                label="💸 Total Deductions",
                value=f"₹{emp_salary.total_deductions:,.0f}",
                delta=f"{(emp_salary.total_deductions/emp_salary.proportional_salary)*100:.1f}% of gross"
            )

        with col4:
            st.metric(
                label="🏠 HRA + DA",
                value=f"₹{emp_salary.hra + emp_salary.da:,.0f}",
                delta=f"18% of gross"
            )

    def display_interactive_breakdown(self, emp_salary):
        st.markdown("### 📊 Interactive Salary Analysis")

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(
            ["📈 Distribution", "📊 Components", "📋 Details"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(self.create_salary_breakdown_chart(
                    emp_salary), use_container_width=True)
            with col2:
                st.markdown("#### 💡 Key Insights")
                st.markdown(f"""
                - **Effective Salary Rate**: ₹{emp_salary.take_home/emp_salary.present_days:,.0f} per day
                - **Deduction Percentage**: {(emp_salary.total_deductions/emp_salary.proportional_salary)*100:.1f}%
                - **Bonus Eligibility**: {'✅ Eligible' if emp_salary.attendance_pct >= 75 else '❌ Not Eligible'}
                - **Attendance Impact**: {emp_salary.attendance_pct:.1f}% attendance
                """)

        with tab2:
            st.plotly_chart(self.create_allowances_chart(
                emp_salary), use_container_width=True)

        with tab3:
            # Detailed breakdown table
            data = {
                "Component": ["Gross Salary", "Proportional Salary", "HRA (10%)", "DA (8%)",
                              "Transport (2%)", "Medical Insurance", "Bonus (5%)", "PF (12%)",
                              "Tax (15%)", "Take Home"],
                "Amount (₹)": [
                    f"{emp_salary.gross_salary:,.2f}",
                    f"{emp_salary.proportional_salary:,.2f}",
                    f"{emp_salary.hra:,.2f}",
                    f"{emp_salary.da:,.2f}",
                    f"{emp_salary.transport_allowance:,.2f}",
                    f"{emp_salary.medical_insurance:,.2f}",
                    f"{emp_salary.bonus:,.2f}",
                    f"-{emp_salary.pf:,.2f}",
                    f"-{emp_salary.tax:,.2f}",
                    f"{emp_salary.take_home:,.2f}"
                ],
                "Type": ["Base", "Calculated", "Allowance", "Allowance", "Allowance",
                         "Insurance", "Incentive", "Deduction", "Deduction", "Final"]
            }

            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

    def display_salary_slip_preview(self, emp_salary):
        with st.expander("📄 View Salary Slip Preview", expanded=False):
            # Header section
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 1rem;">
                <h2>💰 SALARY SLIP</h2>
                <p>Pay Period: """ + datetime.now().strftime('%B %Y') + """</p>
            </div>
            """, unsafe_allow_html=True)

            # Employee details
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **👤 Employee Information:**
                - **Employee ID:** {emp_salary.employee_id}
                - **Employee Name:** {emp_salary.username}
                - **Slip ID:** {emp_salary.slip_id}
                """)

            with col2:
                st.markdown(f"""
                **📅 Calculation Details:**
                - **Calculation Date:** {emp_salary.calculation_date}
                - **Present Days:** {emp_salary.present_days}/{emp_salary.total_days}
                - **Attendance:** {emp_salary.attendance_pct:.1f}%
                """)

            st.markdown("---")

            # Create earnings and deductions data
            earnings_data = {
                "Component": ["Proportional Salary", "HRA (10%)", "DA (8%)", "Transport Allowance (2%)", "Medical Insurance", "Bonus (5%)"],
                "Amount (₹)": [
                    f"{emp_salary.proportional_salary:,.2f}",
                    f"{emp_salary.hra:,.2f}",
                    f"{emp_salary.da:,.2f}",
                    f"{emp_salary.transport_allowance:,.2f}",
                    f"{emp_salary.medical_insurance:,.2f}",
                    f"{emp_salary.bonus:,.2f}"
                ]
            }

            deductions_data = {
                "Component": ["PF (12%)", "Tax (15%)"],
                "Amount (₹)": [
                    f"{emp_salary.pf:,.2f}",
                    f"{emp_salary.tax:,.2f}"
                ]
            }

            # Display earnings table
            st.markdown("### 💰 **EARNINGS**")
            earnings_df = pd.DataFrame(earnings_data)
            st.dataframe(earnings_df, use_container_width=True,
                         hide_index=True)

            # Display deductions table
            st.markdown("### 💸 **DEDUCTIONS**")
            deductions_df = pd.DataFrame(deductions_data)
            st.dataframe(deductions_df, use_container_width=True,
                         hide_index=True)

            # Net pay
            st.markdown("---")
            st.markdown(f"""
            <div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 1rem; border-radius: 8px; text-align: center;">
                <h3 style="color: #155724; margin: 0;">🎉 NET PAY (Take Home)</h3>
                <h2 style="color: #28a745; margin: 0.5rem 0;">₹{emp_salary.take_home:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

    def salary_page(self):
        if not self.logged_in:
            st.switch_page("main.py")

        # Apply custom CSS
        self.add_custom_css()

        # Display header
        self.display_header()

        # Create form
        with st.form("salary_form", clear_on_submit=False):
            employee_id, gross_salary, present_days, total_days = self.create_salary_form()

            st.markdown("---")
            calculate = st.form_submit_button(
                "🧮 Calculate Salary", use_container_width=True)

        if calculate:
            if self.validate_inputs(employee_id, gross_salary, present_days, total_days):
                with st.spinner("🔄 Calculating your salary..."):
                    emp_salary = EmployeeSalary(
                        employee_id, gross_salary, present_days, total_days, self.username)
                    emp_salary.calculate()

                    # Save to MySQL
                    try:
                        self.storage.save_employee_data(emp_salary.to_dict())
                        st.success(
                            "✅ Salary calculated and saved successfully!")
                    except Exception as e:
                        st.warning(
                            f"⚠️ Salary calculated but couldn't save to database: {str(e)}")

                    self.salary_slip_data = emp_salary.to_dict()
                    st.session_state['salary_slip_data'] = self.salary_slip_data

                    # Display results
                    self.display_salary_metrics(emp_salary)
                    self.display_interactive_breakdown(emp_salary)
                    self.display_salary_slip_preview(emp_salary)

        # Action buttons
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.session_state.get('salary_slip_data'):
                if st.button("🖨️ Print Slip", use_container_width=True):
                    st.switch_page("pages/slip_generator.py")

        with col2:
            if st.button("🔄 Calculate Again", use_container_width=True):
                st.rerun()

        with col3:
            if st.button("📊 View History", use_container_width=True):
                st.info("📋 Feature coming soon!")

        with col4:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.clear()
                st.rerun()

    def close(self):
        self.storage.close()


if __name__ == "__main__":
    app = SalaryCalculatorApp()
    app.salary_page()
