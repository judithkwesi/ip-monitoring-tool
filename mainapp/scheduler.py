from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from mainapp.utils.get_abuseIPDB import make_abuseipdb_request
from mainapp.utils.constants import Urls, OutputFile
from mainapp.utils.utils import process_and_store_blacklist
from .models import SyncInterval
import logging


logger = logging.getLogger('ip-monitoring-tool')


def schedule_site_downloads():
    sync_query = SyncInterval.objects.all()
    sync = 12
    if sync_query.exists():
        sync_query = SyncInterval.objects.all()
        sync_intervals = [ip_obj.sync_interval for ip_obj in sync_query]
        sync = int(sync_intervals[-1])

    scheduler = BackgroundScheduler()
    scheduler.add_job(download_sites_file, 'interval', hours=sync)
    scheduler.start()


def download_sites_file():
    """
        Downloads files from the databases/sites, currently uses wget
        params: null
        return: string
    """
    try:
        subprocess.run(["wget", "-O", OutputFile.BLOCKLIST, Urls.BLOCKLISTDE], check=True)
        logger.info("Blocklist updated successfully.")
        subprocess.run(["wget", "-O", OutputFile.CINS, Urls.CINS], check=True)
        logger.info("CINS updated successfully.")
        subprocess.run(["wget", "-O", OutputFile.SPAMHAUS, Urls.SPAMHAUS], check=True)
        logger.info("Spamhaus IPv4 updated successfully.")
        subprocess.run(["wget", "-O", OutputFile.SPAMHAUSV6, Urls.SPAMHAUSV6], check=True)
        logger.info("Spamhaus IPv6 updated successfully.")

        make_abuseipdb_request()
    except Exception as e:
        logger.error(f"Error occurred during download: {e}")

    process_and_store_blacklist()

    return "Done"
