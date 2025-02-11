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

def fetch_doc_and_parse_metadata(file_id: str):
    """
    Export doc as HTML and attempt to parse top lines for metadata.
    Returns (metadata_dict, full_html).
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

    # 3. Extract the first ~5 paragraphs
    paragraphs = re.split(r"</p>\s*<p[^>]*>", exported, maxsplit=5)

    text_lines = []
    for p in paragraphs[:6]:
        # remove remaining HTML tags
        clean_line = re.sub(r"<.*?>", "", p)
        # split on line breaks
        for line in clean_line.strip().splitlines():
            text_lines.append(line.strip())

    # 4. Match each line
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

    return metadata, exported