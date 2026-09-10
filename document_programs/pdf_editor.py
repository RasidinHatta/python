import os
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
    print("        ✂️  PDF Page Remover Tool")
    print("=" * 60)
    
    pdf_path = input("\nEnter PDF file path: ").strip()
    
    if not os.path.exists(pdf_path) or not pdf_path.lower().endswith('.pdf'):
        print(f"❌ File not found or not a PDF: {pdf_path}")
        return

    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"\nTotal pages: {total_pages}")
        
        exclude_input = input("Enter pages to REMOVE (e.g., '1, 3-5') or press Enter to cancel: ").strip()
        if not exclude_input:
            print("Operation cancelled.")
            return
            
        excluded_pages = parse_pages_to_exclude(exclude_input)
        if not excluded_pages:
            print("No valid pages selected for removal. Exiting.")
            return

        writer = PdfWriter()
        
        pages_kept = 0
        for i in range(total_pages):
            if i not in excluded_pages:
                writer.add_page(reader.pages[i])
                pages_kept += 1
            else:
                print(f"Removed page {i + 1}")
                
        print(f"\nPages kept: {pages_kept} / {total_pages}")
        
        replace_choice = input("\nReplace the original file? (Y/n): ").strip().lower()
        if replace_choice == 'n':
            output_filename = input("Enter name for the new PDF (without .pdf): ").strip()
            if not output_filename:
                output_filename = "edited_output"
            output_dir = 'documents'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_path = os.path.join(output_dir, f"{output_filename}.pdf")
        else:
            # Overwrite original
            output_path = pdf_path
            
        # Write to a temporary file first if replacing
        temp_path = output_path + ".tmp"
        with open(temp_path, "wb") as f:
            writer.write(f)
            
        # Replace
        if os.path.exists(output_path):
            os.replace(temp_path, output_path)
        else:
            os.rename(temp_path, output_path)
            
        print(f"\n✅ Successfully updated PDF!")
        print(f"📁 Saved to: {output_path}")

    except Exception as e:
        print(f"\n❌ Error processing PDF: {e}")
        # Clean up temp file if exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

if __name__ == "__main__":
    main()
