from apscheduler.schedulers.background import BackgroundScheduler
import subprocess


# Constants for URLs and output file paths
BLOCKLIST_URL = "https://lists.blocklist.de/lists/all.txt"
CINS_URL = "http://cinsscore.com/list/ci-badguys.txt"
SPAMHAUS_URL = "https://www.spamhaus.org/drop/drop.txt"
SPAMHAUSV6_URL = "https://www.spamhaus.org/drop/dropv6.txt"

BLOCKLIST_OUTPUT_FILE = "./mainapp/sites/blocklist.txt"
CINS_OUTPUT_FILE = "./mainapp/sites/cins.txt"
SPAMHAUS_OUTPUT_FILE = "./mainapp/sites/spamhaus.txt"
SPAMHAUSV6_OUTPUT_FILE = "./mainapp/sites/spamhausv6.txt"


def schedule_site_downloads():
    scheduler = BackgroundScheduler()
    scheduler.add_job(download_sites_file, 'interval', hours=12)
    scheduler.start()


def download_sites_file():
    # Use wget to download the files
    try:
        subprocess.call(f"wget -O {BLOCKLIST_OUTPUT_FILE} {BLOCKLIST_URL}")
        subprocess.call(f"wget -O {CINS_OUTPUT_FILE} {CINS_URL}")
        subprocess.call(f"wget -O {SPAMHAUS_OUTPUT_FILE} {SPAMHAUS_URL}")
        subprocess.call(f"wget -O {SPAMHAUSV6_OUTPUT_FILE} {SPAMHAUSV6_URL}")
    except Exception as e:
        print(f"Error occurred during download: {e}")

    return "Done"
