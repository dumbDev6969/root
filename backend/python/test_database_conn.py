import pymysql
import codecs
import re

def clean_sql_content(content):
    # Remove BOM and special characters
    content = content.replace('\ufeff', '')
    # Remove any non-printable characters
    content = ''.join(char for char in content if ord(char) >= 32 or char == '\n')
    # Remove any byte order marks
    content = content.replace('\xff\xfe', '')
    # Clean up line endings
    content = content.replace('\r\n', '\n')
    # Remove comments
    content = re.sub(r'--.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return content

def split_sql_statements(content):
    # Split on semicolons but preserve those within quotes
    statements = []
    current_statement = []
    in_string = False
    string_char = None
    
    for char in content:
        if char in ["'", '"'] and not in_string:
            in_string = True
            string_char = char
        elif char == string_char and in_string:
            in_string = False
        
        if char == ';' and not in_string:
            current_statement.append(char)
            stmt = ''.join(current_statement).strip()
            if stmt and not stmt.isspace():
                statements.append(stmt)
            current_statement = []
        else:
            current_statement.append(char)
    
    # Add the last statement if it exists
    last_stmt = ''.join(current_statement).strip()
    if last_stmt and not last_stmt.isspace():
        statements.append(last_stmt)
    
    return statements

def execute_sql_file(cursor, sql_content):
    # Clean the content
    sql_content = clean_sql_content(sql_content)
    
    # Split into statements
    statements = split_sql_statements(sql_content)
    
    success_count = 0
    for statement in statements:
        # Skip empty statements
        if statement.strip():
            try:
                cursor.execute(statement)
                success_count += 1
                print(f"Successfully executed statement {success_count}")
            except Exception as e:
                print(f"Error executing statement: {e}")
                print(f"Failed statement: {statement[:100]}...")  # Print first 100 chars of failed statement

timeout = 10
connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db="jobsearc",
    host="jobsearach-mysql-server-jobs.h.aivencloud.com",
    password="AVNS_ro5gQNnPaH3uQNf_sw7",
    read_timeout=timeout,
    port=16459,
    user="avnadmin",
    write_timeout=timeout,
)

try:
    cursor = connection.cursor()
    
    # Try different encodings
    encodings = ['utf-8-sig', 'latin1', 'cp1252']
    sql_content = None
    
    for encoding in encodings:
        try:
            with codecs.open('export-01-09-24.sql', 'r', encoding=encoding) as file:
                sql_content = file.read()
                print(f"Successfully read file with {encoding} encoding")
                break
        except UnicodeDecodeError:
            continue
    
    if sql_content:
        # Execute the SQL
        execute_sql_file(cursor, sql_content)
        # Commit the changes
        connection.commit()
        print("SQL import completed successfully")
    else:
        print("Could not read the SQL file with any of the attempted encodings")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()