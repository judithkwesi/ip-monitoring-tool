from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from .models import SyncInterval
import logging


logger = logging.getLogger('ip-monitoring-tool')


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
    sync_query = SyncInterval.objects.all()
    if not sync_query.exists():
        sync = 12
    else:
        sync_query = SyncInterval.objects.all()
        sync_intervals = [ip_obj.sync_interval for ip_obj in sync_query]
        sync = int(sync_intervals[-1])

    scheduler = BackgroundScheduler()
    scheduler.add_job(download_sites_file, 'interval', hours=sync)
    scheduler.start()


def download_sites_file():
    # Use wget to download the files
    try:
        subprocess.run(["wget", "-O", BLOCKLIST_OUTPUT_FILE, BLOCKLIST_URL], check=True)
        logger.info("Blocklist updated successfully.")
        subprocess.run(["wget", "-O", CINS_OUTPUT_FILE, CINS_URL], check=True)
        logger.info("CINS updated successfully.")
        subprocess.run(["wget", "-O", SPAMHAUS_OUTPUT_FILE, SPAMHAUS_URL], check=True)
        logger.info("Spamhaus IPv4 updated successfully.")
        subprocess.run(["wget", "-O", SPAMHAUSV6_OUTPUT_FILE, SPAMHAUSV6_URL], check=True)
        logger.info("Spamhaus IPv6 updated successfully.")
    except Exception as e:
        logger.error(f"Error occurred during download: {e}")

    return "Done"
