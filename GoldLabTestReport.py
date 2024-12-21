import os
import platform
import subprocess
from tkinter import Tk, Label, Entry, Button, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter.filedialog import asksaveasfilename
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Function to generate a receipt and save it as a PDF
def generate_receipt():
    try:
        # Get inputs from the GUI
        given_gold_weight = float(entry_gold_weight.get())
        taken_gold = float(entry_taken_gold.get())
        pure_gold = float(entry_pure_gold.get())
        gold_prize = float(entry_gold_price.get())

        # Constants
        masha = 0.041666

        # Calculations
        sum_value = pure_gold / taken_gold
        karat = sum_value / masha
        mili_per_tola = (1 - sum_value) * 11.664
        mili_per_rati = mili_per_tola / 0.121
        gold_valu_NNN = given_gold_weight * sum_value
        gold_valu_NNO = (gold_valu_NNN * 1000) / 990

        # Ask user where to save the file
        receipt_filename = asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Receipt As",
            initialfile="gold_testing_receipt.pdf"  # Default filename
        )

        if not receipt_filename:  # If the user cancels the save dialog
            messagebox.showwarning("Save Cancelled", "You did not select a file to save.")
            return

        # PDF creation
        create_pdf(receipt_filename, given_gold_weight, taken_gold, pure_gold, sum_value, karat,
                   mili_per_tola, mili_per_rati, gold_valu_NNN, gold_valu_NNO, gold_prize)

        messagebox.showinfo("Success", f"Receipt has been saved at '{receipt_filename}'.")
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter numeric values for all fields.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")



def create_pdf(receipt_filename, given_gold_weight, taken_gold, pure_gold, sum_value, karat, mili_per_tola, mili_per_rati, gold_valu_NNN, gold_valu_NNO, gold_prize):
    # Define the small paper size
    small_paper = (12 * cm, 15 * cm)  # Width x Height in cm
    c = canvas.Canvas(receipt_filename, pagesize=small_paper)
    width, height = small_paper

    # Title and branding
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 1 * cm, "NADEEM GOLD TESTING LAB")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 2 * cm, "Receipt")

    # Separator line
    c.setLineWidth(0.5)
    c.line(0.5 * cm, height - 2.5 * cm, width - 0.5 * cm, height - 2.5 * cm)

    # Receipt details in a table format
    data = [
        ["Field", "Value"],
        ["Original Gold Weight", f"{given_gold_weight:.3f} g"],
        ["Gold Taken for Test", f"{int(taken_gold)} mg"],
        ["Gold After Test", f"{int(pure_gold)} mg"],
        ["Sum (in grams)", f"{sum_value:.3f} g"],
        ["Karat", f"{karat:.3f}"],
        ["Mil kam sona fi Tola", f"{mili_per_tola:.3f} g"],
        ["Mil kam sona fi Rati", f"{mili_per_rati:.3f} g"],
        ["Pure Gold 999", f"{gold_valu_NNN:.3f} g"],
        ["Pure Gold 990", f"{gold_valu_NNO:.3f} g"],
        ["Labor Charges+Test Fee(300) as gold weight", f"{(given_gold_weight * 40 + 300) * 11.664 / gold_prize:.3f} g"],
        ["Total Gold Weight", f"{gold_valu_NNO - (given_gold_weight * 40 + 300) * 11.664 / gold_prize:.3f} g"],
        ["Labor Charges+Test Fee (300)", f"{(given_gold_weight * 40 + 300):.2f} Rs"]
    ]

    # Create the table with fixed column widths
    table = Table(data, colWidths=[6 * cm, 5 * cm])

    # Set the style to ensure left alignment for the first column and right alignment for the second column
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),  # Left-align header
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Left-align the first column
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'), # Right-align the second column
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    # Position the table dynamically
    table.wrapOn(c, width, height)
    table.drawOn(c, 0.5 * cm, height - 12 * cm)

    # Footer
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 0.5 * cm, "Thank you for using our service!")

    # Save the PDF
    c.save()


# Function to print the receipt directly from input fields
# def print_receipt():
#     try:
#         # Get inputs from the GUI
#         given_gold_weight = float(entry_gold_weight.get())
#         taken_gold = float(entry_taken_gold.get())
#         pure_gold = float(entry_pure_gold.get())
#         gold_prize = float(entry_gold_price.get())

#         # Constants
#         masha = 0.041666

#         # Calculations
#         sum_value = pure_gold / taken_gold
#         karat = sum_value / masha
#         mili_per_tola = (1 - sum_value) * 11.664
#         mili_per_rati = mili_per_tola / 0.121
#         gold_valu_NNN = given_gold_weight * sum_value
#         gold_valu_NNO = (gold_valu_NNN * 1000) / 990

#         # Generate a temporary file
#         temp_filename = "temp_gold_receipt.pdf"
#         create_pdf(temp_filename, given_gold_weight, taken_gold, pure_gold, sum_value, karat,
#                    mili_per_tola, mili_per_rati, gold_valu_NNN, gold_valu_NNO, gold_prize)

#         # Print the temporary PDF
#         system_platform = platform.system()
#         if system_platform == "Windows":
#             os.startfile(temp_filename, "print")
#         elif system_platform in ["Linux", "Darwin"]:
#             subprocess.run(["lp", temp_filename], check=True) 
#         else:
#             messagebox.showerror("Error", "Unsupported operating system for printing.")

#         # Optionally, remove the temporary file
#         os.remove(temp_filename)

#     except ValueError:
#         messagebox.showerror("Input Error", "Please enter numeric values for all fields.")
#     except Exception as e:
#         messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")




# Create the main GUI window using tkinter
root = Tk()
root.title("Gold Testing Receipt Generator")

# Input fields
Label(root, text="Given Gold Weight (grams):").grid(row=0, column=0, padx=10, pady=10)
entry_gold_weight = Entry(root)
entry_gold_weight.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Gold Taken (milligrams):").grid(row=1, column=0, padx=10, pady=10)
entry_taken_gold = Entry(root)
entry_taken_gold.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Pure Gold (milligrams):").grid(row=2, column=0, padx=10, pady=10)
entry_pure_gold = Entry(root)
entry_pure_gold.grid(row=2, column=1, padx=10, pady=10)

Label(root, text="Gold Price (per tola):").grid(row=3, column=0, padx=10, pady=10)
entry_gold_price = Entry(root)
entry_gold_price.grid(row=3, column=1, padx=10, pady=10)

# Buttons
Button(root, text="Generate Receipt", command=generate_receipt).grid(row=4, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

#Button(root, text="Print Receipt", command=print_receipt).grid(row=4, column=1, padx=10, pady=20)

# Start the main GUI loop
root.mainloop()

