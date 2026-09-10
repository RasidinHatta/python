import os
import glob
from pypdf import PdfReader, PdfWriter

def parse_pages_to_exclude(exclude_str):
    """
    Parses a string like "1, 3-5" into a set of 0-indexed page numbers.
    """
    excluded = set()
    if not exclude_str.strip():
        return excluded
    
    parts = exclude_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = part.split('-')
                start = int(start.strip())
                end = int(end.strip())
                # 1-indexed to 0-indexed conversion
                for i in range(start - 1, end):
                    excluded.add(i)
            except ValueError:
                print(f"Warning: Could not parse range '{part}'")
        else:
            try:
                page = int(part)
                excluded.add(page - 1)
            except ValueError:
                print(f"Warning: Could not parse page '{part}'")
    return excluded

def main():
    print("=" * 60)
    print("        📄 PDF Merger Tool")
    print("=" * 60)
    
    # Create output directory
    output_dir = 'documents'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print("\nPlease place your PDF files in the current directory or provide full paths.")
    
    pdfs_to_merge = []
    while True:
        pdf_path = input("Enter PDF file path (or leave empty to stop adding): ").strip()
        if not pdf_path:
            break
        
        # Simple glob expansion or exact match
        if '*' in pdf_path:
            matches = glob.glob(pdf_path)
            for m in matches:
                if m.lower().endswith('.pdf'):
                    pdfs_to_merge.append(m)
                    print(f"Added: {m}")
        else:
            if os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf'):
                pdfs_to_merge.append(pdf_path)
                print(f"Added: {pdf_path}")
            elif not os.path.exists(pdf_path):
                print(f"❌ File not found: {pdf_path}")
            else:
                print(f"❌ Not a PDF file: {pdf_path}")

    if not pdfs_to_merge:
        print("No PDF files selected. Exiting.")
        return

    writer = PdfWriter()
    
    for pdf_path in pdfs_to_merge:
        print(f"\nProcessing: {pdf_path}")
        try:
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)
            print(f"Total pages: {total_pages}")
            
            exclude_input = input("Enter pages to EXCLUDE (e.g., '1, 3-5') or press Enter to include all: ").strip()
            excluded_pages = parse_pages_to_exclude(exclude_input)
            
            for i in range(total_pages):
                if i not in excluded_pages:
                    writer.add_page(reader.pages[i])
                else:
                    print(f"Excluded page {i + 1}")
                    
        except Exception as e:
            print(f"❌ Error processing {pdf_path}: {e}")

    output_filename = input("\nEnter name for the merged PDF (without .pdf): ").strip()
    if not output_filename:
        output_filename = "merged_output"
        
    output_path = os.path.join(output_dir, f"{output_filename}.pdf")
    
    try:
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"\n✅ Successfully merged PDFs!")
        print(f"📁 Output saved to: {output_path}")
    except Exception as e:
        print(f"\n❌ Error saving merged PDF: {e}")

if __name__ == "__main__":
    main()
