from scrapy.cmdline import execute
import sys
import os

dirpath = os.path.dirname(os.path.abspath(__file__))
print(dirpath)

sys.path.append(dirpath)

execute(['scrapy','crawl','itslawspider'])