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
        karat = float(entry_karat.get())
        sum_value = int(entry_sum.get())
        mili_per_rati = float(entry_mil_fi_rati.get())

        # Validate customer name
        if not customer_name:
            messagebox.showerror("Input Error", "Please enter the customer's name.")
            return

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
        create_pdf(receipt_filename, customer_name, current_datetime, given_gold_weight, karat, sum_value, mili_per_rati)

        messagebox.showinfo("Success", f"Receipt has been saved at '{receipt_filename}'.")
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter numeric values for all fields.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


def create_pdf(receipt_filename, customer_name, current_datetime, given_gold_weight, karat, sum_value, mili_per_rati):
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
        ["Sum ", f"{sum_value:.0f} mg"],
        ["Karat", f"{karat:.3f}"],
        ["Mil kam sona fi Rati", f"{mili_per_rati:.3f} g"]
    ]

    # Create the table with adjusted column widths
    table = Table(data, colWidths=[7 * cm, 3 * cm])  # Increase the width of the first column
    
   # Updated table creation with increased font size and row height
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),  # Left-align header
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'), # Right-align the second column
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Increased font size to 12
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Increased bottom padding for header
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),  # Increased bottom padding for rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        # Bold styling for specific rows
        ('FONTNAME', (0, 4), (1, 4), 'Helvetica-Bold'),  # "Mil kam sona fi Tola" row
        ('FONTNAME', (0, 5), (1, 5), 'Helvetica-Bold'),  # "Mil kam sona fi Rati" row
        ('TEXTCOLOR', (0, 4), (1, 4), colors.black),  # Make text black for bold rows
        ('TEXTCOLOR', (0, 5), (1, 5), colors.black),
    ]))

    # Recalculate the vertical positioning of the table
    table.wrapOn(c, width, height)
    table.drawOn(c, 1 * cm, height - 12 * cm)  # Adjusted vertical position to accommodate larger table
    # Footer message at the bottom
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 0.5 * cm, "© 2024 Nadeem Gold Testing Lab. All Rights Reserved.")

    # Save the PDF
    c.save()
    
# Create the main application window
root = tk.Tk()
root.title("Gold Testing Receipt 2.0")  # Set window title
root.geometry("700x500")  # Initial size
root.minsize(600, 400)  # Minimum size for responsiveness

# Fonts and colors
default_font = ("Helvetica", 12)
header_font = ("Helvetica", 16, "bold")
footer_font = ("Helvetica", 9)
entry_font = ("Helvetica", 14)
highlight_color = "#f0f8ff"  # Light blue for the input frame

# Styling with ttk
style = ttk.Style()
style.configure("TLabel", font=default_font)
style.configure("TEntry", font=entry_font, padding=(5, 5, 5, 5))
style.configure("Header.TLabel", font=header_font, foreground="darkblue")
style.configure("Highlight.TFrame", background=highlight_color, borderwidth=2, relief="solid")

# Header Section
header = ttk.Label(root, text="Gold Testing Lab Receipt 2.0 ", style="Header.TLabel")
header.grid(row=0, column=0, columnspan=2, pady=(20, 10))

# Input Form Frame
form_frame = ttk.Frame(root, style="Highlight.TFrame", padding=(20, 20))  # Highlighted frame
form_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")

# Input Fields
ttk.Label(form_frame, text="Customer Name:").grid(row=0, column=0, padx=10, pady=15, sticky="e")
entry_customer_name = ttk.Entry(form_frame, width=35, font=entry_font)
entry_customer_name.grid(row=0, column=1, padx=10, pady=15, sticky="w")

ttk.Label(form_frame, text="Given Gold Weight (grams):").grid(row=1, column=0, padx=10, pady=15, sticky="e")
entry_gold_weight = ttk.Entry(form_frame, width=35, font=entry_font)
entry_gold_weight.grid(row=1, column=1, padx=10, pady=15, sticky="w")

ttk.Label(form_frame, text="Enter Karat:").grid(row=2, column=0, padx=10, pady=15, sticky="e")
entry_karat = ttk.Entry(form_frame, width=35, font=entry_font)
entry_karat.grid(row=2, column=1, padx=10, pady=15, sticky="w")

ttk.Label(form_frame, text="Enter Sum:").grid(row=3, column=0, padx=10, pady=15, sticky="e")
entry_sum = ttk.Entry(form_frame, width=35, font=entry_font)
entry_sum.grid(row=3, column=1, padx=10, pady=15, sticky="w")

ttk.Label(form_frame, text="Enter Mil fi Rati:").grid(row=4, column=0, padx=10, pady=15, sticky="e")
entry_mil_fi_rati = ttk.Entry(form_frame, width=35, font=entry_font)
entry_mil_fi_rati.grid(row=4, column=1, padx=10, pady=15, sticky="w")

# Generate Receipt Button (Placed above the footer)
generate_button = ttk.Button(root, text="Generate Receipt", command=generate_receipt)
generate_button.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")

# Footer Section
footer = ttk.Label(root, text="© 2024 Nadeem Gold Testing Lab. All Rights Reserved.", font=footer_font)
footer.grid(row=3, column=0, columnspan=2, pady=(10, 10))

# Make the columns and rows dynamically resizable
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
form_frame.grid_columnconfigure(1, weight=1)

# Run the application
root.mainloop()