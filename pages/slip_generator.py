import streamlit as st
from fpdf import FPDF
from datetime import datetime


class SalarySlipPDF:
    """Generates a professional PDF salary slip."""

    def __init__(self, slip_data):
        self.slip_data = slip_data
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

    def add_header(self):
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 15, "SALARY SLIP", ln=True, align='C')
        self.pdf.ln(5)

    def add_employee_info(self):
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "EMPLOYEE DETAILS", ln=True)
        self.pdf.set_font("Arial", size=10)

        details = [
            f"Slip ID: {self.slip_data.get('slip_id', 'N/A')}",
            f"Employee ID: {self.slip_data.get('employee_id', 'N/A')}",
            f"Employee Name: {self.slip_data.get('username', 'N/A')}",
            f"Date: {self.slip_data.get('calculation_date', 'N/A')}",
            f"Present Days: {self.slip_data.get('present_days', 0)}/{self.slip_data.get('total_days', 0)}"
        ]

        for detail in details:
            self.pdf.cell(0, 8, detail, ln=True)
        self.pdf.ln(5)

    def add_earnings(self):
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "EARNINGS", ln=True)
        self.pdf.set_font("Arial", size=10)

        earnings = [
            ("Proportional Salary", self.slip_data.get('proportional_salary', 0)),
            ("HRA (10%)", self.slip_data.get('hra', 0)),
            ("DA (8%)", self.slip_data.get('da', 0)),
            ("Medical Insurance", self.slip_data.get('medical_insurance', 0)),
            ("Transport Allowance (2%)", self.slip_data.get('transport_allowance', 0)),
            ("Bonus (5%)", self.slip_data.get('bonus', 0))
        ]

        for label, amount in earnings:
            self.pdf.cell(100, 8, label, 0, 0)
            self.pdf.cell(0, 8, f"Rs. {amount:,.2f}", ln=True, align='R')
        self.pdf.ln(5)

    def add_deductions(self):
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "DEDUCTIONS", ln=True)
        self.pdf.set_font("Arial", size=10)

        deductions = [
            ("PF (12%)", self.slip_data.get('pf_deduction', 0)),
            ("Tax (15%)", self.slip_data.get('tax_deduction', 0)),
            ("Total Deductions", self.slip_data.get('total_deductions', 0))
        ]

        for label, amount in deductions:
            self.pdf.cell(100, 8, label, 0, 0)
            self.pdf.cell(0, 8, f"Rs. {amount:,.2f}", ln=True, align='R')
        self.pdf.ln(5)

    def add_net_pay(self):
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.cell(100, 12, "NET PAY", 0, 0)
        self.pdf.cell(
            0, 12, f"Rs. {self.slip_data.get('take_home_salary', 0):,.2f}", ln=True, align='R')

    def generate(self):
        self.add_header()
        self.add_employee_info()
        self.add_earnings()
        self.add_deductions()
        self.add_net_pay()
        return self.pdf.output(dest='S').encode('latin1')


class SlipGeneratorApp:
    """Clean, modern salary slip display."""

    def __init__(self):
        self.slip_data = st.session_state.get('salary_slip_data')

    def add_styles(self):
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Poppins', sans-serif;
        }
        
        .main-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }
        
        .slip-header {
            text-align: center;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .slip-title {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .slip-subtitle {
            color: #666;
            font-size: 1.2rem;
            font-weight: 400;
        }
        
        .slip-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .slip-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            padding-bottom: 0.5rem;
        }
        
        .card-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 60px;
            height: 3px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 2px;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
            border-radius: 12px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .info-item:hover {
            background: linear-gradient(135deg, #e8ebff 0%, #d4d9ff 100%);
            transform: translateX(5px);
        }
        
        .info-label {
            font-weight: 500;
            color: #555;
            font-size: 0.95rem;
        }
        
        .info-value {
            font-weight: 600;
            color: #333;
            font-size: 1.1rem;
        }
        
        .earnings-card {
            border-left: 4px solid #10b981;
        }
        
        .earnings-card .card-title::after {
            background: linear-gradient(135deg, #10b981, #059669);
        }
        
        .earnings-card .info-item {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-left-color: #10b981;
        }
        
        .earnings-card .info-item:hover {
            background: linear-gradient(135deg, #d1fae5 0%, #bbf7d0 100%);
        }
        
        .deductions-card {
            border-left: 4px solid #ef4444;
        }
        
        .deductions-card .card-title::after {
            background: linear-gradient(135deg, #ef4444, #dc2626);
        }
        
        .deductions-card .info-item {
            background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
            border-left-color: #ef4444;
        }
        
        .deductions-card .info-item:hover {
            background: linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%);
        }
        
        .net-pay-card {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .net-pay-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #f59e0b, #d97706);
        }
        
        .net-pay-card .card-title {
            color: #e5e7eb;
            font-size: 1.3rem;
        }
        
        .net-pay-card .card-title::after {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            left: 50%;
            transform: translateX(-50%);
        }
        
        .net-pay-amount {
            font-size: 3rem;
            font-weight: 700;
            color: #ffffff;
            margin-top: 1rem;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }
        
        .actions-container {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }
        
        .stDownloadButton > button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(16, 185, 129, 0.4);
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
        }
        
        .error-card {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            text-align: center;
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 15px 35px rgba(239, 68, 68, 0.3);
        }
        
        .error-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .error-message {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        @media (max-width: 768px) {
            .slip-title {
                font-size: 2.5rem;
            }
            
            .net-pay-amount {
                font-size: 2.5rem;
            }
            
            .actions-container {
                flex-direction: column;
                align-items: center;
            }
            
            .info-grid {
                grid-template-columns: 1fr;
            }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        </style>
        """, unsafe_allow_html=True)

    def check_auth(self):
        if not st.session_state.get("logged_in"):
            st.switch_page("main.py")

    def show_error(self):
        st.markdown("""
        <div class="main-container">
            <div class="error-card fade-in">
                <div class="error-title">⚠️ No Salary Data Found</div>
                <div class="error-message">Please calculate your salary first to generate a slip.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Go to Calculator", key="error_btn"):
                st.switch_page("pages/salary_calculator.py")

    def show_slip(self):
        slip = self.slip_data

        st.markdown("""
        <div class="main-container">
            <div class="slip-header fade-in">
                <div class="slip-title">SALARY SLIP</div>
                <div class="slip-subtitle">Professional Payroll Statement</div>
            </div>
        """, unsafe_allow_html=True)

        # Employee Information
        st.markdown("""
        <div class="slip-card fade-in">
            <div class="card-title">Employee Information</div>
            <div class="info-grid">
        """, unsafe_allow_html=True)

        employee_info = [
            ("Slip ID", slip.get('slip_id', 'N/A')),
            ("Employee ID", slip.get('employee_id', 'N/A')),
            ("Employee Name", slip.get('username', 'N/A')),
            ("Calculation Date", slip.get('calculation_date', 'N/A')),
            ("Present Days",
             f"{slip.get('present_days', 0)}/{slip.get('total_days', 0)}"),
            ("Gross Salary", f"₹{slip.get('gross_salary', 0):,.2f}")
        ]

        for label, value in employee_info:
            st.markdown(f"""
            <div class="info-item">
                <span class="info-label">{label}</span>
                <span class="info-value">{value}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Earnings
        st.markdown("""
        <div class="slip-card earnings-card fade-in">
            <div class="card-title">💰 Earnings</div>
            <div class="info-grid">
        """, unsafe_allow_html=True)

        earnings = [
            ("Proportional Salary", slip.get('proportional_salary', 0)),
            ("HRA (10%)", slip.get('hra', 0)),
            ("DA (8%)", slip.get('da', 0)),
            ("Medical Insurance", slip.get('medical_insurance', 0)),
            ("Transport Allowance (2%)", slip.get('transport_allowance', 0)),
            ("Bonus (5%)", slip.get('bonus', 0))
        ]

        for label, amount in earnings:
            st.markdown(f"""
            <div class="info-item">
                <span class="info-label">{label}</span>
                <span class="info-value">₹{amount:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Deductions
        st.markdown("""
        <div class="slip-card deductions-card fade-in">
            <div class="card-title">📉 Deductions</div>
            <div class="info-grid">
        """, unsafe_allow_html=True)

        deductions = [
            ("PF (12%)", slip.get('pf_deduction', 0)),
            ("Tax (15%)", slip.get('tax_deduction', 0)),
            ("Total Deductions", slip.get('total_deductions', 0))
        ]

        for label, amount in deductions:
            st.markdown(f"""
            <div class="info-item">
                <span class="info-label">{label}</span>
                <span class="info-value">₹{amount:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Net Pay
        st.markdown(f"""
        <div class="slip-card net-pay-card fade-in">
            <div class="card-title">💵 Net Pay</div>
            <div class="net-pay-amount">₹{slip.get('take_home_salary', 0):,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        # Actions
        st.markdown("""
        <div class="actions-container">
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            pdf_bytes = SalarySlipPDF(slip).generate()
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"salary_slip_{slip.get('employee_id', 'unknown')}.pdf",
                mime='application/pdf'
            )

        with col2:
            if st.button("← Back to Calculator"):
                st.switch_page("pages/salary_calculator.py")

        st.markdown("</div></div>", unsafe_allow_html=True)

    def show(self):
        self.check_auth()
        self.add_styles()

        if not self.slip_data:
            self.show_error()
        else:
            self.show_slip()


if __name__ == "__main__":
    SlipGeneratorApp().show()
