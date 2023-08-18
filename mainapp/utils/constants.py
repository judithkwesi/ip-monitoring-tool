class Urls:
    """
        This contains the URLS of the various databases/sites
    """
    BLOCKLISTDE = "https://lists.blocklist.de/lists/all.txt"
    CINS = "http://cinsscore.com/list/ci-badguys.txt"
    SPAMHAUS = "https://www.spamhaus.org/drop/drop.txt"
    SPAMHAUSV6 = "https://www.spamhaus.org/drop/dropv6.txt"


class OutputFile:
    """
        This contains the paths to the output files of the databases/sites
    """
    BLOCKLIST= "./mainapp/sites/blocklist.txt"
    CINS= "./mainapp/sites/cins.txt"
    SPAMHAUS= "./mainapp/sites/spamhaus.txt"
    SPAMHAUSV6= "./mainapp/sites/spamhausv6.txt"
    ABUSEIPDB= "./mainapp/sites/abuseIPDB.txt"
    BLACKLIST= "./mainapp/sites/blacklist.json"