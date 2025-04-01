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
from sculblog.db import db_connection,  execute_single_query, insert_row, update_row, execute_query, value_in_column 

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

def write_preview_html(html_content: str):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for a_tag in soup.find_all('a'):
            span_tag = soup.new_tag('span', **{'class': 'false-external-link'})
            span_tag.string = a_tag.get_text()
            a_tag.replace_with(span_tag)

        for h_tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            span_tag = soup.new_tag('span', **{'class': 'preview-header'})
            span_tag.string = h_tag.get_text()
            h_tag.replace_with(span_tag)
        
        for tag in soup.find_all():
            if tag.name not in ['span', 'sup', 'sub']:
                tag.unwrap()
        
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

def process(file_path):
    try:
        db = DbConn(db_path)
        
        with open(os.path.abspath(file_path), "r") as file:
            markdown_content = file.read()
        
        page_html = write_page_html(markdown_content)
        
        post_data = {
            "text": page_html,
            "preview_html": write_preview_html(page_html)[:1500],
            "word_count": count_markdown_words(markdown_content), 
        }
        
        file_name = os.path.splitext(file_path)[0]
        
        if not db.value_in_column("blog", "file_name", file_name):
            post_data["header"] = input("what is the header of the page? ")
            post_data["file_name"] = file_name
            
            if db.insert_row("blog", post_data):
                print("Data inserted successfully.")
            else:
                print("Failed to insert data.")
        else:
            db.update_row("blog", "file_name", file_name, post_data)
            
    except Exception as e:
        print(f"An error of Exception type {type(e).__name__} occurred: {e}")

def hide(file_path):
    file_name = remove_extension(file_path)
    DbConn(db_path).update_row("blog", "file_name", file_name, {"hide": "0"})

# Example: Unhide a post
def unhide(file_path):
    file_name = remove_extension(file_path)
    DbConn(db_path).update_row("blog", "file_name", file_name, {"hide": ""})

def main():
    if len(sys.argv) < 3:
        print("Usage: sculblog <command> <postname> (command: process | hide | unhide )")
        sys.exit(1)

    command, file_path = sys.argv[1], sys.argv[2]

    if command == "process": 
        process(file_path)
    elif command == "hide": 
        hide(file_path)
    elif command == "unhide":
        unhide(file_path)
    else: 
        print('invalid command. command must be either "process", "hide", or "unhide"')
        sys.exit(1)

if __name__ == "__main__":
    main()
