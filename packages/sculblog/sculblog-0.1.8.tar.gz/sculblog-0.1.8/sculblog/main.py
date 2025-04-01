import sqlite3
import os
from bs4 import BeautifulSoup
from datetime import datetime
import markdown
import re
import html
from contextlib import contextmanager
import sys
import traceback

from sculblog.diego_flavored_markdown import DiegoFlavoredMarkdown, count_markdown_words
from sculblog.db import DbConn

#===============================
# Configuration and Utilities
#===============================

db_path = os.path.abspath(os.path.join('/', 'var', 'www', 'html', 'database', 'db.db'))

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def remove_extension(filename):
    return os.path.splitext(filename)[0]


#===============================
# HTML and Content Management
#===============================


def write_page_html(markdown_content: str):
    try:
        soup = BeautifulSoup("", 'html.parser')
        md = markdown.Markdown(extensions=[DiegoFlavoredMarkdown(), 'footnotes'])
        # If markdown_content is a file object, read it first
        if hasattr(markdown_content, 'read'):
            markdown_content = markdown_content.read()
        html_content = md.convert(markdown_content)
        soup.append(BeautifulSoup(html_content, 'html.parser'))
        return str(soup)
    except Exception as e:
        print(f"Error in write_page_html: {str(e)}")
        raise

def write_preview_html(html_content: str, char_len: int):
    try:
        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Convert link tags to spans
        for a_tag in soup.find_all('a'):
            span_tag = soup.new_tag('span', **{'class': 'false-external-link'})
            span_tag.string = a_tag.get_text()
            a_tag.replace_with(span_tag)
        
        # Convert header tags to spans
        for h_tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            span_tag = soup.new_tag('span', **{'class': 'preview-header'})
            span_tag.string = h_tag.get_text()
            h_tag.replace_with(span_tag)
        
        # Unwrap any tags that aren't spans, sup or sub
        for tag in soup.find_all():
            if tag.name not in ['span', 'sup', 'sub']:
                tag.unwrap()
        
        # Get all text content to check length
        text_content = soup.get_text()
        
        # If text is longer than char_len, truncate
        if len(text_content) > char_len:
            # Find all text nodes and accumulate up to char_len
            text_nodes = []
            current_count = 0
            
            for element in soup.descendants:
                if isinstance(element, str) and current_count < char_len:
                    if current_count + len(element) <= char_len:
                        text_nodes.append((element, element))
                        current_count += len(element)
                    else:
                        # Truncate this text node
                        truncated = element[:char_len - current_count] + "..."
                        text_nodes.append((element, truncated))
                        current_count = char_len
                        break
            
            # Replace text nodes with truncated versions
            for original, truncated in text_nodes:
                if original != truncated:
                    original.replace_with(truncated)
        
        # Get final HTML with all tags properly closed
        clean_html = ''.join(str(tag) for tag in soup.contents)
        return clean_html
        
    except Exception as e:
        print(f"Error in write_preview_html: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        raise

#===============================
# Main Functions
#===============================

def process(category, file_path):
    try:
        db = DbConn(db_path)
        
        with open(os.path.abspath(file_path), "r") as file:
            markdown_content = file.read()
        
        page_html = write_page_html(markdown_content)
        
        post_data = {
            "text": page_html,
            "preview_html": write_preview_html(page_html, 1500),
            "word_count": count_markdown_words(markdown_content), 
        }
        
        file_name = os.path.splitext(file_path)[0]
        
        if not db.value_in_column(category, "file_name", file_name):
            post_data["header"] = input("what is the header of the page? ")
            post_data["file_name"] = file_name
            
            if db.insert_row(category, post_data):
                print("Data inserted successfully.")
            else:
                print("Failed to insert data.")
        else:
            db.update_row(category, "file_name", file_name, post_data)
            
    except Exception as e:
        print(f"An error of Exception type {type(e).__name__} occurred: {e}")

def hide(category, file_path):
    file_name = remove_extension(file_path)
    DbConn(db_path).update_row(category, "file_name", file_name, {"hide": "0"})

def unhide(category, file_path):
    file_name = remove_extension(file_path)
    DbConn(db_path).update_row(category, "file_name", file_name, {"hide": ""})

def date(category, file_path, date_splash):
    file_name = remove_extension(file_path)
    DbConn(db_path).update_row(category, "file_name", file_name, {"date_splash": date_splash})

def main():
    if len(sys.argv) < 3:
        print("Usage: sculblog <command> <category> <postname> (command: process | hide | unhide )")
        sys.exit(1)

    command, category, file_path = sys.argv[1], sys.argv[2], sys.argv[3]

    if command == "process": 
        process(category, file_path)
    elif command == "hide": 
        hide(category, file_path)
    elif command == "unhide":
        unhide(category, file_path)
    elif command == "date":
        date_splash = sys.argv[3]
        date(category, file_path, date_splash)
    else: 
        print('invalid command. command must be either "process", "hide", or "unhide"')
        sys.exit(1)

if __name__ == "__main__":
    main()
