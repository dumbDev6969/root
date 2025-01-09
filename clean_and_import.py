import codecs

def clean_sql_file(input_file, output_file):
    try:
        # Try different encodings
        encodings = ['utf-8-sig', 'latin1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                with codecs.open(input_file, 'r', encoding=encoding) as f:
                    content = f.read()
                    print(f"Successfully read with {encoding} encoding")
                    break
            except UnicodeDecodeError:
                continue
        
        if content:
            # Remove BOM and special characters
            content = content.replace('\ufeff', '')
            # Remove any byte order marks
            content = content.replace('\xff\xfe', '')
            # Clean up line endings
            content = content.replace('\r\n', '\n')
            # Remove null bytes
            content = content.replace('\x00', '')
            
            # Write cleaned content
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned SQL written to {output_file}")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if clean_sql_file('export-01-09-24.sql', 'cleaned_export.sql'):
        print("SQL file cleaned successfully")
    else:
        print("Failed to clean SQL file")