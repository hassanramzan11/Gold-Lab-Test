import os
import platform
import subprocess
from tkinter import Tk, Label, Entry, Button, messagebox
import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter.filedialog import asksaveasfilename
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime


# Function to generate a receipt and save it as a PDF
def generate_receipt():
    try:
        # Get inputs from the GUI
        customer_name = entry_customer_name.get().strip()
        given_gold_weight = float(entry_gold_weight.get())
        taken_gold = float(entry_taken_gold.get())
        pure_gold = float(entry_pure_gold.get())
        gold_prize = float(entry_gold_price.get())

        # Validate customer name
        if not customer_name:
            messagebox.showerror("Input Error", "Please enter the customer's name.")
            return

        # Constants
        masha = 0.041666

        # Calculations
        sum_value = pure_gold / taken_gold
        karat = sum_value / masha
        mili_per_tola = (1 - sum_value) * 11.664
        mili_per_rati = mili_per_tola / 0.121
        gold_valu_NNN = given_gold_weight * sum_value
        gold_valu_NNO = (gold_valu_NNN * 1000) / 990

        # Get current date and time for the receipt
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdffilename=datetime.now().strftime("%Y-%m-%d___%H-%M-%S")
        # Ask user where to save the file
        receipt_filename = asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Receipt As",
            initialfile=f"{pdffilename+" ("+customer_name}).pdf"  # Default filename
        )

        if not receipt_filename:  # If the user cancels the save dialog
            messagebox.showwarning("Save Cancelled", "You did not select a file to save.")
            return

        # PDF creation
        create_pdf(receipt_filename, customer_name, current_datetime, given_gold_weight, taken_gold, pure_gold, 
                   sum_value, karat, mili_per_tola, mili_per_rati, gold_valu_NNN, 
                   gold_valu_NNO, gold_prize)

        messagebox.showinfo("Success", f"Receipt has been saved at '{receipt_filename}'.")
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter numeric values for all fields.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


def create_pdf(receipt_filename, customer_name, current_datetime, given_gold_weight, taken_gold, pure_gold, sum_value, karat, mili_per_tola, mili_per_rati, gold_valu_NNN, gold_valu_NNO, gold_prize):
    # Define the new paper size (12 cm x 15 cm)
    small_paper = (12 * cm, 15 * cm)  # Width x Height in cm
    c = canvas.Canvas(receipt_filename, pagesize=small_paper)
    width, height = small_paper

    # Title and branding
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 2 * cm, "NADEEM GOLD TESTING LAB")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 3 * cm, "Receipt")

    # Line separator
    c.setLineWidth(0.5)
    c.setStrokeColor(colors.black)
    c.line(1 * cm, height - 4 * cm, width - 1 * cm, height - 4 * cm)

    # Name and Date
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1 * cm, height - 5 * cm, "Customer Name: ")
    c.setFont("Helvetica", 10)
    c.drawString(4 * cm, height - 5 * cm, customer_name.upper())  # Display customer name in uppercase
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1 * cm, height - 6 * cm, "Date & Time: ")
    c.setFont("Helvetica", 10)
    c.drawString(4 * cm, height - 6 * cm, current_datetime)  # Displaying Date & Time

    # Receipt details in a table format
    data = [
        ["Field", "Value"],
        ["Original Gold Weight", f"{given_gold_weight:.3f} g"],
        ["Sum (in grams)", f"{sum_value:.3f} g"],
        ["Karat", f"{karat:.3f}"],
        ["Mil kam sona fi Tola", f"{mili_per_tola:.3f} g"],
        ["Mil kam sona fi Rati", f"{mili_per_rati:.3f} g"],
        ["Pure Gold 999", f"{gold_valu_NNN:.3f} g"],
        ["Pure Gold 990", f"{gold_valu_NNO:.3f} g"],
        ["Labor Charges+Test Fee as Gold Weight", f"{(given_gold_weight * 40 + 300) * 11.664 / gold_prize:.3f} g"],
        ["Total Gold Weight", f"{gold_valu_NNO - (given_gold_weight * 40 + 300) * 11.664 / gold_prize:.3f} g"],
        ["Labor Charges+Test Fee (300)", f"{(given_gold_weight * 40 + 300):.2f} Rs"]
    ]

    # Create the table with adjusted column widths
    table = Table(data, colWidths=[7 * cm, 3 * cm])  # Increase the width of the first column

    # Set the style to ensure left alignment for the first column and right alignment for the second column
    table.setStyle(TableStyle([ 
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),  # Left-align header
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'), # Right-align the second column
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        # Bold styling for specific rows
        ('FONTNAME', (0, 4), (1, 4), 'Helvetica-Bold'),  # "Mil kam sona fi Tola" row
        ('FONTNAME', (0, 5), (1, 5), 'Helvetica-Bold'),  # "Mil kam sona fi Rati" row
        ('TEXTCOLOR', (0, 4), (1, 4), colors.black),  # Make text black for bold rows
        ('TEXTCOLOR', (0, 5), (1, 5), colors.black),
    ])) 

    # Position the table further down from the previous position
    table.wrapOn(c, width, height)
    table.drawOn(c, 1 * cm, height - 13.7 * cm)  # Adjusted to 5 cm further down

    # Footer message at the bottom
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 0.5 * cm, "© 2024 Nadeem Gold Testing Lab. All Rights Reserved.")

    # Save the PDF
    c.save()
    
    
    
    
# Create the main application window
root = tk.Tk()
root.title("Gold Testing Receipt 1.0")
root.geometry("700x540")  # Initial window size
root.minsize(600, 400)  # Minimum size for responsiveness

# Fonts and colors
header_font = ("Helvetica", 16, "bold")
default_font = ("Helvetica", 12)
entry_font = ("Helvetica", 14)
highlight_color = "#f0f8ff"  # Light blue for the input frame

# Styling with ttk
style = ttk.Style()
style.configure("TLabel", font=default_font)
style.configure("TEntry", font=entry_font, padding=(5, 5, 5, 5))
style.configure("Header.TLabel", font=header_font, foreground="darkblue")
style.configure("TButton", font=default_font, padding=(10, 10))
style.configure("Highlight.TFrame", background=highlight_color, borderwidth=2, relief="solid")

# Header Section
header = ttk.Label(root, text="Gold Testing Lab Receipt 1.0", style="Header.TLabel")
header.grid(row=0, column=0, columnspan=2, pady=(20, 10))

# Input Form Frame
form_frame = ttk.Frame(root, style="Highlight.TFrame", padding=(20, 20))
form_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")

# Input Fields
ttk.Label(form_frame, text="Customer Name:").grid(row=0, column=0, padx=10, pady=15, sticky="e")
entry_customer_name = ttk.Entry(form_frame, width=35)
entry_customer_name.grid(row=0, column=1, padx=10, pady=15, sticky="w")

ttk.Label(form_frame, text="Given Gold Weight (grams):").grid(row=1, column=0, padx=10, pady=15, sticky="e")
entry_gold_weight = ttk.Entry(form_frame, width=35)
entry_gold_weight.grid(row=1, column=1, padx=10, pady=15, sticky="w")

ttk.Label(form_frame, text="Gold Taken (milligrams):").grid(row=2, column=0, padx=10, pady=15, sticky="e")
entry_taken_gold = ttk.Entry(form_frame, width=35)
entry_taken_gold.grid(row=2, column=1, padx=10, pady=15, sticky="w")

ttk.Label(form_frame, text="Pure Gold (milligrams):").grid(row=3, column=0, padx=10, pady=15, sticky="e")
entry_pure_gold = ttk.Entry(form_frame, width=35)
entry_pure_gold.grid(row=3, column=1, padx=10, pady=15, sticky="w")

ttk.Label(form_frame, text="Gold Price (per tola):").grid(row=4, column=0, padx=10, pady=15, sticky="e")
entry_gold_price = ttk.Entry(form_frame, width=35)
entry_gold_price.grid(row=4, column=1, padx=10, pady=15, sticky="w")

# Generate Receipt Button
generate_button = ttk.Button(root, text="Generate Receipt", command=generate_receipt)
generate_button.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")

# Footer Section
footer = ttk.Label(root, text="© 2024 Nadeem Gold Testing Lab. All Rights Reserved..", font=("Helvetica", 9))
footer.grid(row=3, column=0, columnspan=2, pady=(10, 10))

# Make columns and rows dynamically resizable
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
form_frame.grid_columnconfigure(1, weight=1)

# Start the main GUI loop
root.mainloop()