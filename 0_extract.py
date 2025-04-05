import os
import subprocess
from PyPDF2 import PdfReader, PdfWriter


def pdf_to_images_gs(pdf_path, output_dir, image_format="png", dpi=300):
    """
    Convert PDF pages to images using Ghostscript directly.

    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save the images
        image_format (str): Image format (png, jpg, etc.)
        dpi (int): Resolution in dots per inch
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get base filename without extension
    base_filename = os.path.basename(pdf_path).rsplit(".", 1)[0]

    # Open the PDF to get page count
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    print(f"Converting {total_pages} pages to {image_format} images...")

    for page_num in range(total_pages):
        # Create temporary PDF with single page
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])

        temp_pdf = f"{output_dir}/temp_page_{page_num + 1}.pdf"
        with open(temp_pdf, "wb") as f:
            writer.write(f)

        # Output image path
        output_file = f"{output_dir}/{base_filename}_page_{page_num + 1}.{image_format}"

        # Use Ghostscript to convert PDF to image
        device = "png16m" if image_format == "png" else image_format
        gs_command = [
            "gs",
            "-q",  # Quiet mode
            "-dNOPAUSE",
            "-dBATCH",
            "-dSAFER",
            f"-sDEVICE={device}",
            f"-r{dpi}",
            "-dTextAlphaBits=4",
            "-dGraphicsAlphaBits=4",
            f"-sOutputFile={output_file}",
            temp_pdf,
        ]

        print(f"Converting page {page_num + 1}/{total_pages}")
        subprocess.run(gs_command)

        # Remove temporary PDF
        os.remove(temp_pdf)

    print(f"All pages converted successfully. Images saved to {output_dir}/")


# Example usage
if __name__ == "__main__":
    pdf_to_images_gs("raw/Pfanzagl_1982.pdf", "./pdf_images")
