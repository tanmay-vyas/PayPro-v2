PayPro‑v2 💰 Employee Salary Breakdown & PDF Generator

PayPro‑v2 is a Streamlit-based, employee-focused salary analysis tool that provides a complete, dynamic breakdown of an employee’s salary.
Instead of just seeing the credited amount in the bank, employees can view all components — basic pay, HRA, bonuses, transport, taxes, and more — and download a professional PDF pay slip for reference.
This version builds on the original PayPro with polished CSS, better PDF formatting, and a clean object-oriented design, making the tool interactive, modular, and visually appealing.

🧠 Key Features
📊 Complete Salary Breakdown
Input: Package, total working days, present/absent days
Outputs: Base salary, HRA, bonus, transport, tax deductions, net salary
Provides a transparent view of salary components for employees

🖨️ PDF Generation
Download your salary slip in a clean, professional layout
Each PDF adapts to the inputs dynamically

🎨 Polished UI & Streamlit Interface
Responsive, employee-friendly dark/light theme support
CSS-enhanced styling for buttons, inputs, and layout
Organized layout using pages/ for future expansion

🧩 Object-Oriented Design (OOP)
Salary calculation logic encapsulated in classes
Modular design allows easy extension for new allowances or rules

💼 Employee-Centric Design
Eliminates the need to request HR for detailed salary info
Focused on convenience, clarity, and accessibility

📁 Repository Structure
PayPro-v2/
├── .streamlit/          # Streamlit configuration (theme, layout)
├── pages/               # Multi-page app structure (optional extensions)
├── static/              # CSS, images, and other static assets
├── main.py              # Main Streamlit app (inputs, calculation, PDF generation)
├── requirements.txt     # Python dependencies

Install Dependencies
pip install -r requirements.txt

Run the App
streamlit run main.py

Enter salary package, total working days, and present/absent days

Click “Calculate Salary”

View detailed salary breakdown

Download PDF pay slip for reference

🧾 Example Output
Employee: Tanmay Vyas
Total Salary: ₹50,000
- Basic: ₹25,000
- HRA: ₹10,000
- Bonus: ₹5,000
- Transport Allowance: ₹2,000
- Tax Deductions: ₹8,000
Net Salary: ₹44,000

[Download PDF]


Output is dynamic — updates based on user input and calculates all relevant components.

🏷️ Suggested Repo Description & Topics

Description:
Streamlit-based salary breakdown tool that allows employees to analyze their salary components and download professional PDF pay slips. Built with OOP principles and polished CSS interface.

Topics:
python streamlit salary payroll pdf-generator oop employee-tool finance

📌 Future Enhancements

Add multi-currency support
Integrate with HR/payroll APIs for real-time salary processing
Auto-email salary slips
Expand allowances & deductions module
Dashboard visualization for monthly/yearly salary trends
