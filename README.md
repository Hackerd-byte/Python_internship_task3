# Python_internship_task3
# 📊 PDF Report Generator - Internship Task 3

This project generates an automated PDF report from a CSV dataset using Python. It includes summary statistics, data visualizations (bar charts), and tabular insights, suitable for real-world reporting needs.

## 🔧 Features

- ✅ Reads data from `electronics.csv`
- 📈 Generates bar charts using `matplotlib`
  - **Brands vs Sales**
  - **Category vs Sales**
- 📋 Calculates summary statistics:
  - Mean, Median, Min, Max, Standard Deviation
- 🧾 Compiles everything into a professional `Report.pdf`
- 🐍 Virtual environment included (`env/`)

---

## 📁 Project Structure

```
pdfreportgenerator/
│
├── env/ # Python virtual environment
├── images/ # Auto-generated charts saved here
├── electronics.csv # Input dataset (electronics sales)
├── report_generator.py # Main script to generate PDF
├── Report.pdf # Final generated report
└── README.md # This file
```


---

## 📦 Requirements

- Python 3.x
- matplotlib
- pandas
- fpdf

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## 🚀 How to Run
Activate virtual environment:
```
.\env\Scripts\activate  # Windows
```
Run the script:
```
python report_generator.py
```
Your Report.pdf will be generated with visualizations and stats.



