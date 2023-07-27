from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

def updater():
    scheduler = BackgroundScheduler()
    scheduler.add_job(download_sites_file, 'interval', hours=12)
    scheduler.start()

def download_sites_file():
    # Sites url
    block_url = "https://lists.blocklist.de/lists/all.txt"
    cins_url = "http://cinsscore.com/list/ci-badguys.txt"
    spam_url = "https://www.spamhaus.org/drop/drop.txt"
    
		# Output path
    block_output_file = "./mainapp/sites/blocklist.txt"
    cins_output_file = "./mainapp/sites/cins.txt"
    spam_output_file = "./mainapp/sites/spamhaus.txt"

    print(block_url)

    # Use wget to download the file
    download_block = f"wget -O {block_output_file} {block_url}"
    download_cins_url = f"wget -O {cins_output_file} {cins_url}"
    download_spamhaus = f"wget -O {spam_output_file} {spam_url}"

    subprocess.call(download_spamhaus, shell=True)
    subprocess.call(download_block, shell=True)
    subprocess.call(download_cins_url, shell=True)

    return "Done"