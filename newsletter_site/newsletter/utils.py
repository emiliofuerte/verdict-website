# newsletter/utils.py
import logging
import re
from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

logger = logging.getLogger(__name__)

# Basic regex for top lines like:
# Title: ...
# Writer(s): ...
# Date: ...
# Issue: ...
# Type of Article: ...
TITLE_REGEX = re.compile(r"^Title:\s*(.+)$", re.IGNORECASE)
WRITER_REGEX = re.compile(r"^Writer\(s\):\s*(.+)$", re.IGNORECASE)
DATE_REGEX = re.compile(r"^Date:\s*(.+)$", re.IGNORECASE)
ISSUE_REGEX = re.compile(r"^Issue:\s*(\d+)$", re.IGNORECASE)
TYPE_REGEX = re.compile(r"^Type of Article:\s*(.+)$", re.IGNORECASE)

def strip_gdoc_html(raw_html: str) -> str:
    """
    Removes top-level <html>, <head>, <body>, <meta>, and inline style
    attributes from a Google Docs export, so it won't override our
    site's layout. 
    """
    # Remove DOCTYPE if present
    raw_html = re.sub(r'<!DOCTYPE.*?>', '', raw_html, flags=re.IGNORECASE)

    # Remove entire <html> and <head> tags
    raw_html = re.sub(r'</?(html|head)\b[^>]*>', '', raw_html, flags=re.IGNORECASE)

    # Remove <meta ...> tags
    raw_html = re.sub(r'<meta[^>]*>', '', raw_html, flags=re.IGNORECASE)

    # Extract everything inside the <body>...</body>, removing the body tags themselves
    raw_html = re.sub(r'<body\b[^>]*>(.*?)</body>', r'\1', raw_html, flags=re.IGNORECASE|re.DOTALL)

    # Remove inline style attributes (which often force background/width)
    raw_html = re.sub(r'style="[^"]*"', '', raw_html, flags=re.IGNORECASE)

    return raw_html.strip()


def fetch_doc_and_parse_metadata(file_id: str):
    """
    Export a Google Doc as HTML, parse the top lines for metadata,
    and return (metadata_dict, cleaned_html).
    metadata_dict keys: title, writer, date, issue_number, article_type
    """
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=settings.GOOGLE_API_SCOPES
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    # 1. Export as HTML
    try:
        exported = drive_service.files().export(
            fileId=file_id, 
            mimeType='text/html'
        ).execute()
        if isinstance(exported, bytes):
            exported = exported.decode('utf-8', errors='replace')
    except Exception as e:
        logger.error(f"Failed to fetch doc {file_id}: {e}")
        return {}, ""

    # 2. Prepare metadata defaults
    metadata = {
        'title': '',
        'writer': '',
        'date': None,
        'issue_number': None,
        'article_type': ''
    }

    # 3. Extract the first ~5 paragraphs to parse Title, Writer, etc.
    paragraphs = re.split(r"</p>\s*<p[^>]*>", exported, maxsplit=5)
    text_lines = []
    for p in paragraphs[:6]:
        # remove remaining HTML tags
        clean_line = re.sub(r"<.*?>", "", p)
        # split on line breaks
        for line in clean_line.strip().splitlines():
            text_lines.append(line.strip())

    # 4. Match each line against our patterns
    for line in text_lines:
        if TITLE_REGEX.match(line):
            metadata['title'] = TITLE_REGEX.match(line).group(1)
        elif WRITER_REGEX.match(line):
            metadata['writer'] = WRITER_REGEX.match(line).group(1)
        elif DATE_REGEX.match(line):
            dt = DATE_REGEX.match(line).group(1)
            # Attempt to parse date "9/3/24"
            try:
                metadata['date'] = datetime.strptime(dt, "%m/%d/%y").date()
            except ValueError:
                logger.warning(f"Could not parse date '{dt}', storing as raw string.")
                metadata['date'] = dt  # store as string if parse fails
        elif ISSUE_REGEX.match(line):
            metadata['issue_number'] = int(ISSUE_REGEX.match(line).group(1))
        elif TYPE_REGEX.match(line):
            metadata['article_type'] = TYPE_REGEX.match(line).group(1)

    # 5. Strip out unwanted wrapper tags & inline styling 
    cleaned_html = strip_gdoc_html(exported)

    return metadata, cleaned_html