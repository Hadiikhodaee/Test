from crawler import *
import sys
    
   
if __name__ == '__main__':
    switch = sys.argv[1]
    if switch == 'find_links':
        crawler = LinkCrawler(['london', 'albany'])
        crawler.start()
    elif switch == 'extract_pages':
        crawler = DataCrawler()
        crawler.start()