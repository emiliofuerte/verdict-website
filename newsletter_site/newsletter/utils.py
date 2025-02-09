import logging
from django.conf import settings
from googleapiclient.discovery import build
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

def fetch_google_doc_as_html(file_id: str) -> str:
    """
    Given a Google Drive file ID for a Google Doc, returns the HTML content.
    Requires the Drive API to be enabled and the doc to be accessible
    by the service account.
    """
    # Load the service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=settings.GOOGLE_API_SCOPES
    )

    # Build the Drive service
    drive_service = build('drive', 'v3', credentials=credentials)

    try:
        # 'text/html' is the MIME type for exporting Google Docs to HTML
        exported = drive_service.files().export(fileId=file_id, mimeType='text/html').execute()
        # If returned type is bytes, decode to str
        if isinstance(exported, bytes):
            exported = exported.decode('utf-8', errors='replace')
        return exported
    except Exception as e:
        logger.error(f"Failed to fetch doc {file_id} as HTML: {e}")
        return ""