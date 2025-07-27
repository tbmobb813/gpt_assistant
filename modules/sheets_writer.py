import os
import time
import functools
import logging
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'gsheets_service_account.json')

logger = logging.getLogger(__name__)

def retry(exceptions, tries=3, delay=1, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"{e}, retrying in {mdelay}s...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapped
    return decorator

@retry((APIError,), tries=3, delay=1, backoff=2)
def connect_to_sheet(sheet_name, worksheet_name="Sheet1"):
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    logger.info(f"Connected to Google Sheet '{sheet_name}'")
    return sheet

def append_post(sheet_name, content, platform="Instagram", tags=None, status="Idea"):
    try:
        sheet = connect_to_sheet(sheet_name)
        sheet.append_row([
            content,
            platform,
            ", ".join(tags or []),
            status
        ])
        logger.info(f"Appended post to sheet '{sheet_name}'")
        return f"✅ Post sent to '{sheet_name}'!"
    except APIError as e:
        logger.error(f"Google Sheets API error: {e}")
        return f"❌ Google Sheets API error: {e}"
    except Exception as e:
        logger.error(f"Unexpected error sending to sheet: {e}")
        return f"❌ Failed to send to sheet: {str(e)}"
        
def get_all_posts(sheet_name, worksheet_name="Sheet1"):
    try:
        sheet = connect_to_sheet(sheet_name, worksheet_name)
        data = sheet.get_all_values()
        headers = data[0]
        rows = data[1:]

        posts = []
        for row in rows:
            entry = dict(zip(headers, row))
            posts.append(entry)
        logger.info(f"Fetched {len(posts)} posts from sheet '{sheet_name}'")
        return posts
    except APIError as e:
        logger.error(f"Google Sheets API error: {e}")
        return f"❌ Google Sheets API error: {e}"
    except Exception as e:
        logger.error(f"Unexpected error fetching posts: {e}")
        return f"❌ Failed to fetch posts: {str(e)}"


