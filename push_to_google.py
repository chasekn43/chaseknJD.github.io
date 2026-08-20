"""
Google Indexing & Search Console Automation Suite

This script submits sitemaps and individual URLs directly to Google's Indexing API
and Google Search Console API.

Prerequisites:
- Service Account credentials in google_credentials.json
- Add `google-indexer@regulatory-archive-2026.iam.gserviceaccount.com` as Owner in Google Search Console
"""

import os
import sys
import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "google_credentials.json")
if not os.path.exists(KEY_FILE):
    KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "google_credentials.json")

SITEMAP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitemap.xml")
SITE_URL = "https://kinslow-regulatory-archive.org/"
SCOPES = [
    'https://www.googleapis.com/auth/indexing',
    'https://www.googleapis.com/auth/webmasters'
]

def parse_sitemap():
    urls = []
    if not os.path.exists(SITEMAP_FILE):
        print(f"[-] Sitemap file not found at {SITEMAP_FILE}")
        return urls
    try:
        tree = ET.parse(SITEMAP_FILE)
        root = tree.getroot()
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url_node in root.findall('ns:url', ns):
            loc = url_node.find('ns:loc', ns)
            if loc is not None and loc.text:
                urls.append(loc.text.strip())
    except Exception as e:
        print(f"[-] Error parsing sitemap: {e}")
    return urls

def publish_to_google_indexing_api():
    if not os.path.exists(KEY_FILE):
        print(f"[-] Credentials file not found: {KEY_FILE}")
        return

    urls = parse_sitemap()
    print(f"[+] Loaded {len(urls)} URLs from sitemap for Google Indexing API push.")

    try:
        credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
        indexing_service = build('indexing', 'v3', credentials=credentials)
    except Exception as e:
        print(f"[-] Failed to initialize Google API client: {e}")
        return

    success_count = 0
    permission_needed = False

    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] Pushing URL to Google Indexing API: {url}")
        try:
            content = {
                'url': url,
                'type': 'URL_UPDATED'
            }
            res = indexing_service.urlNotifications().publish(body=content).execute()
            print(f"  [SUCCESS] Notified Google: {res.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('notifyTime')}")
            success_count += 1
            time.sleep(0.5)
        except Exception as e:
            err_str = str(e)
            if "Permission denied" in err_str:
                permission_needed = True
                print(f"  [-] Permission Denied: Service account needs Owner permissions in GSC.")
                break
            else:
                print(f"  [-] Error: {e}")

    if permission_needed:
        print("\n" + "="*70)
        print(" ACTION REQUIRED FOR GOOGLE SEARCH CONSOLE / INDEXING API:")
        print(f" 1. Go to Google Search Console (https://search.google.com/search-console)")
        print(f" 2. Select property: {SITE_URL} (or sc-domain:kinslow-regulatory-archive.org)")
        print(f" 3. Go to Settings -> Users and permissions -> Add user")
        print(f" 4. Add email: google-indexer@regulatory-archive-2026.iam.gserviceaccount.com")
        print(f" 5. Set Permission to: Owner")
        print("="*70 + "\n")
    else:
        print(f"\n[+] Successfully pushed {success_count} URLs to Google Indexing API.")

if __name__ == "__main__":
    print("=== Google Search Console & Indexing API Instant Pusher ===")
    publish_to_google_indexing_api()
