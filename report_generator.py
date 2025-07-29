import matplotlib.pyplot as plt
import os
import pandas as pd
from fpdf import FPDF
import io

image_folder ="C:\\progrmming\\pdfreportgenerator\\images"
os.makedirs(image_folder, exist_ok=True)


path = r'C:\\progrmming\\pdfreportgenerator\\electronics.csv'
file = pd.read_csv(path)
df = pd.DataFrame(file)

# Prepare file info
buffer = io.StringIO()
file.info(buf=buffer)
info = buffer.getvalue()

# Create PDF object
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Cover Page
pdf.add_page()
pdf.set_font("Arial", "", size=20)
pdf.cell(200, 10, txt="Stock & Sales Report", align="C", ln=True)
pdf.ln(250)
pdf.set_font("Arial", "I", size=15)
pdf.cell(0, 10, txt="Submitted by Hariprasath", align="R")

# Page: File Info Table
pdf.add_page()
pdf.set_font("Arial", "B", size=12)
pdf.cell(0, 10, txt="Information of File", ln=True)
pdf.set_font("Arial", "B", 10)
pdf.set_fill_color(200, 220, 255)
pdf.cell(60, 10, "Column Name", border=1, fill=True)
pdf.cell(50, 10, "Non-Null Count", border=1, fill=True)
pdf.cell(40, 10, "Data Type", border=1, ln=True, fill=True)

pdf.set_font("Arial", "", 10)
for col in file.columns:
    non_null = file[col].notnull().sum()
    dtype = str(file[col].dtype)
    pdf.cell(60, 10, str(col), border=1)
    pdf.cell(50, 10, str(non_null), border=1)
    pdf.cell(40, 10, dtype, border=1, ln=True)
pdf.ln(10)
# Page: Brands and Product Details
brands = []
total_count = 0
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Brand-wise Product Details", ln=True)

for brand, group in df.groupby("Brand"):
    brands.append(brand)
    count = group["Category"].count()
    categories = ', '.join(group["Category"]) + '.'
    total_count += count

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"{brand} -> ({count})", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, categories)

pdf.ln(5)
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 10, txt=f"Total Products: {total_count}", ln=True)

# Page: Summary Table (from original summary code)
for category, group in df.groupby("Category"):
    brand_stats = {}
    brand_group = group.groupby("Brand")["Price"]

    for brand in brand_group.groups.keys():
        prices = brand_group.get_group(brand)
        brand_stats[brand] = {
            "Average Price (Rs.)": round(prices.mean(), 2),
            "Min Price (Rs.)": round(prices.min(), 2),
            "Max Price (Rs.)": round(prices.max(), 2),
        }

    summary_df = pd.DataFrame.from_dict(brand_stats, orient="index")
    summary_df.index.name = 'Brand'
    summary_df.reset_index(inplace=True)
    summary_df.insert(0, 'S.No', range(1, len(summary_df) + 1))

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Price Summary - {category}", ln=True)

    pdf.set_font("Arial", "B", 10)
    col_widths = [10, 40, 40, 40, 40]
    headers = summary_df.columns.tolist()
    for i in range(len(headers)):
        pdf.cell(col_widths[i], 10, headers[i], border=1)
    pdf.ln(10)

    pdf.set_font("Arial", "", 10)
    for index, row in summary_df.iterrows():
        pdf.cell(col_widths[0], 10, str(row['S.No']), border=1)
        pdf.cell(col_widths[1], 10, str(row['Brand']), border=1)
        pdf.cell(col_widths[2], 10, str(row['Average Price (Rs.)']), border=1)
        pdf.cell(col_widths[3], 10, str(row['Min Price (Rs.)']), border=1)
        pdf.cell(col_widths[4], 10, str(row['Max Price (Rs.)']), border=1)
        pdf.ln(10)

pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Overall Data Summary", ln=True)

total_products = len(df)
total_brands = df["Brand"].nunique()
total_categories = df["Category"].nunique()
total_sales = df["Price"].sum()
price_mean = df["Price"].mean()
price_median = df["Price"].median()
price_min = df["Price"].min()
price_max = df["Price"].max()
price_std = df["Price"].std()

pdf.set_font("Arial", "", 12)
pdf.ln(5)

pdf.cell(0, 10, f"Total Products: {total_products}", ln=True)
pdf.cell(0, 10, f"Total Unique Brands: {total_brands}", ln=True)
pdf.cell(0, 10, f"Total Unique Categories: {total_categories}", ln=True)
pdf.cell(0, 10, f"Total Sales Value: Rs. {total_sales:,.2f}", ln=True)

pdf.ln(5)
pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Price Statistics (All Products)", ln=True)
pdf.set_font("Arial", "", 12)

pdf.cell(0, 10, f"Mean Price: Rs. {price_mean:,.2f}", ln=True)
pdf.cell(0, 10, f"Median Price: Rs. {price_median:,.2f}", ln=True)
pdf.cell(0, 10, f"Minimum Price: Rs. {price_min:,.2f}", ln=True)
pdf.cell(0, 10, f"Maximum Price: Rs. {price_max:,.2f}", ln=True)
pdf.cell(0, 10, f"Standard Deviation: Rs. {price_std:,.2f}", ln=True)


brand_counts = df['Brand'].value_counts()
plt.figure(figsize=(10, 6))
brand_counts.plot(kind='bar', color='skyblue')
plt.title('Brand vs Sales Count')
plt.xlabel('Brand')
plt.ylabel('Number of Products Sold')
plt.xticks(rotation=45)
brand_chart_path = os.path.join(image_folder, 'brand_vs_sales.png')
plt.tight_layout()
plt.savefig(brand_chart_path)
plt.close()

category_counts = df['Category'].value_counts()
plt.figure(figsize=(10, 6))
category_counts.plot(kind='bar', color='orange')
plt.title('Category vs Sales Count')
plt.xlabel('Category')
plt.ylabel('Number of Products Sold')
plt.xticks(rotation=45)
category_chart_path = os.path.join(image_folder, 'category_vs_sales.png')
plt.tight_layout()
plt.savefig(category_chart_path)
plt.close()


pdf.add_page()
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Sales Analysis Charts", ln=True)

pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, "Brand vs Sales", ln=True)
pdf.image(brand_chart_path, x=10, y=None, w=pdf.w - 20)

pdf.ln(10)
pdf.cell(0, 10, "Category vs Sales", ln=True)
pdf.image(category_chart_path, x=10, y=None, w=pdf.w - 20)

# Save PDF
output_path = r"C:\\progrmming\\pdfreportgenerator\\Report.pdf"
pdf.output(output_path)
print(f"Report saved as {output_path}")
