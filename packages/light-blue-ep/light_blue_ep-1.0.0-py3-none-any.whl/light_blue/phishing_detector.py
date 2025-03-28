import time
import sys
import os
import requests
from utils import green, red, yellow
from utils import loader  # if loader is defined in a separate file


API_KEY = os.getenv('VT_API_KEY')  # Replace with your real key

def detect_phishing():
    url = input("\n🔗 Enter a URL to scan with VirusTotal: ").strip()

    if not url.startswith("http"):
        print(red("❌ Please enter a valid URL (starting with http or https)."))
        return

    # Spinner animation
    loading = loader()
    for _ in range(20):
        sys.stdout.write(next(loading))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")

    print(yellow(f"\n🔍 Scanning URL with VirusTotal: {url}"))

    try:
        headers = {
            "x-apikey": API_KEY
        }

        # Submit the URL to get a scan ID
        scan_resp = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )
        scan_resp.raise_for_status()
        scan_id = scan_resp.json()["data"]["id"]

        # Wait for analysis to complete with a timeout
        status = "queued"
        max_attempts = 10
        attempts = 0

        while status != "completed" and attempts < max_attempts:
            print(yellow("⏳ Waiting for analysis to complete..."))
            time.sleep(2)
            report_resp = requests.get(
                f"https://www.virustotal.com/api/v3/analyses/{scan_id}",
                headers=headers
            )
            report_resp.raise_for_status()
            report_data = report_resp.json()
            status = report_data["data"]["attributes"].get("status")
            attempts += 1

        if status != "completed":
            print(red("❌ Analysis timed out. Try again later or check manually."))
            return

        stats = report_data["data"]["attributes"].get("stats", {})
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        harmless = stats.get("harmless", 0)

        if malicious > 0 or suspicious > 0:
            print(red(f"\n⚠️ This URL is flagged as suspicious or malicious by {malicious + suspicious} engines!"))
        else:
            print(green("\n✅ This URL appears clean according to VirusTotal."))

        print(yellow(f"\nEngines flagged: {malicious} malicious, {suspicious} suspicious, {harmless} harmless"))

    except requests.exceptions.RequestException as e:
        print(red(f"\n❌ Network/API error: {e}"))
    except Exception as e:
        print(red(f"\n❌ Unexpected error: {e}"))
