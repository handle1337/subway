import requests
import sys
import tempfile
import colorama
from bs4 import BeautifulSoup
from argparse import *
from configparser import ConfigParser
import os



BANNER = """
   ___            _                        _  _  
  / __|   _  _   | |__   __ __ __ __ _    | || | 
  \__ \  | +| |  | '_ \  \ V  V // _` |    \_, | 
  |___/   \_,_|  |_.__/   \_/\_/ \__,_|   _|__/  
_|\"\"\"\"\"\|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_| \"\"\"\"| 
\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'

"""

config = ConfigParser.read('config.ini')


def config_init():
    config = ConfigParser.read('config.ini')
    config.read('config.ini')
    if not config.has_section(main):
        config.add_section('main')


URL = ""

msrecursive = False
rdrecursive = False
msdepth = 0
rddepth = 0

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')

def fuzz(file):
    with open(file, 'r') as f:
        for line in f:
            check_status(URL + "/" + line)


def recursive_fuzz(file, tmpfile):
    url = URL
    for i in range(rddepth):
        for line in file:
            if check_status(url):
                tmpfile.write(check_status[1] + "\n")
                


def check_status(subdomain, directory):
    url = subdomain + URL + "/" + directory
    r = requests.get(url)
    r_unicode = r.text
    title = r_unicode[r_unicode.find('<title>') + 7 : r_unicode.find('</title>')]
    if r.status_code < 400:
        print(f"[{title}][{r.status_code}] {url}")
        return [subdomain, directory]
    return None
        
def main():
    config_init()
    config.getboolean("banner")
    
    print(BANNER) #make this optional


    with open("config.ini", "w") as configfile:
        config.write(configfile)

    parser = ArgumentParser(description="Enumerate subdomains and URLs",
                            usage="use '%(prog)s --help' for more information",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("--banner", "-b", default=False, description="Print banner at program startup")
    parser.add_argument("--url", "-u", required=True, description="Target URL")
    parser.add_argument("--output", "-o", nargs='?', default=sys.stdout, description="Output file")
    parser.add_argument("--dwordlist", "-dw", nargs='?', default=sys.stdin, type=FileType('r'),
                        description="Directory wordlist")
    parser.add_argument("--swordlist", "-sw", nargs='?', default=sys.stdin, type=FileType('r'),
                        description="Subdomain wordlist")
    parser.add_argument("--multisub", "-ms", description="Multilevel subdomain enumeration")
    parser.add_argument("--msdepth", "-msd", description="Multilevel subdomain enumeration depth")
    parser.add_argument("--recdir", "-rd", description="Recurisve directory fuzzing")
    parser.add_argument("--rddepth", "-rdd", description="Recurisve directory fuzzing depth")
    parser.add_argument("--crawl", "-c", type=str2bool, description="Crawl")
    parser.add_argument("--outurl", "-ou", type=str2bool, description="Output ALL found URLs")
    parser.add_argument("--inurl", "-iu", type=str2bool, default="True",
                        description="[SUBDOMAIN ENUMERATION] Include URLs that belong to the site")
    parser.add_argument("--inaurl", "-iau", type=str2bool, default="False",
                        description="[SUBDOMAIN ENUMERATION] Include ALL found URLs")
    args = parser.parse_args()
    
    if args.banner:
        config.set("banner", args.banner[0])
    if args.url:
        URL = args.url[0]
    if args.output:
        pass

    if args.multisub:
        ms = tempfile.mkstemp()
        with os.fdopen(ms, 'w') as mtmp:
                with open(args.swordlist) as tmp:
                    pass
        os.remove(ms)

    if args.recdir:
        dd = tempfile.mkstemp()
        with os.fdopen(dd, 'w') as rtmp:
            with open(args.dwordlist) as dlist:
                recursive_fuzz(dlist, rtmp)
        os.remove(dd)

    if args.crawl:
        pass
    if args.outurl:
        pass
    if args.inurl:
        pass
    if args.inaurl:
        pass

if __name__ == "__main__":
    main()