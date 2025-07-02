BOT_NAME = "mosdac_scraper"

SPIDER_MODULES = ["mosdac_scraper.spiders"]
NEWSPIDER_MODULE = "mosdac_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Be a good web citizen: set a user agent and a download delay
USER_AGENT = "MOSDAC AI Bot Scraper (for academic/demonstration project)"
DOWNLOAD_DELAY = 1

# Increase logging level to reduce noise, show only important messages
LOG_LEVEL = 'INFO'