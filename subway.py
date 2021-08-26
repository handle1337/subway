#!/usr/bin/env python3

import requests
import re
import sys
import os
import threading
import tempfile
from termcolor import colored
from bs4 import BeautifulSoup
from argparse import *
from datetime import datetime


# TODO: make this pull subdomains from various apis
# TODO: build a DNS zone file based on the information

BANNER = """
   ___            _                        _  _  
  / __|   _  _   | |__   __ __ __ __ _    | || | 
  \__ \  | +| |  | '_ \  \ V  V // _` |    \_, | 
  |___/   \_,_|  |_.__/   \_/\_/ \__,_|   _|__/  
_|\"\"\"\"\"\|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_| \"\"\"\"| 
\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'

"""


def parse_url(url):
    if url.startswith('http'):
        url = re.sub(r'https?://', '', url)
    if url.startswith('www.'):
        url = re.sub(r'www.', '', url)
    return url


def bruteforce(wordlist, output_file, url):
    try:
        url = parse_url(url)
        f_wordlist = open(wordlist, 'r')
        if output_file:
            f_output = open(output_file, 'w')
        lines = f_wordlist.readlines()
        for line in lines:
            sub = check_status(f"{line.strip()}.{url}")
            if sub:
                if output_file:
                    f_output.write(sub + '\n')
        f_wordlist.close()
        f_output.close()
    except Exception as e:
        print(colored(f"[ERROR] {str(e)}", "red"))


"""def recursive_bruteforce(file, tmpfile, depth):
    url_l = url
    for i in range(depth):
        for line in file:
            url_l = line + "." + url_l
            if check_status(url_l):
                tmpfile.write(check_status() + "\n")
                url_l = url_l + "/" + line
                file = tmpfile
                #Theres a massive logic flaw in this function, do not use until fixed
                """


def check_status(url_l):
    try:
        print(f"[*]Currently trying: {url_l}")
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        r = requests.get(f"http://{url_l}", timeout=5)
    except requests.ConnectionError:
        pass
    else:
        r = requests.get(f"http://{url_l}")
        r_unicode = r.text
        title = r_unicode[r_unicode.find('<title>') + 7 : r_unicode.find('</title>')]
        r.close()
        print(f"[{url_l}][{title}][{r.status_code}]")
        return url_l

def print_info(url_l, wordlist_l, output):
    text_break = colored(("="*50), "yellow")

    print(f"""
{text_break}
Started @ [{datetime.now()}]
Hostname: {url_l}
Version: 0.2
Wordlist: {wordlist_l}
Ouput file: {output}
{text_break}
    """)


def main():

    parser = ArgumentParser(description="Enumerate subdomains and URLs",
                            usage="use '%(prog)s --help' for more information",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("--banner", "-b", action='store_true', help="disable banner")
    parser.add_argument("--url", "-u", required=True, help="Target URL")

    parser.add_argument("--output", "-o", dest="output", help="output file")
    parser.add_argument("--wordlist", "-w", default=None,
                        help="Subdomain wordlist")

    parser.add_argument("--multisub", "-m", help="multilevel subdomain enumeration")
    parser.add_argument("--inurl", "-I", action='store_true',
                        help="include URLs that are found inside the site's source and belong to the same domain (html/js files)")
    parser.add_argument("--inaurl", "-A", action='store_true',
                        help="include ALL found URLs in the site's source (html/js)")

    args = parser.parse_args()
    
    
    if not args.banner:
        print(colored(BANNER, "cyan"))

    url = args.url
    wordlist = args.wordlist
    output = args.output
    print_info(url, wordlist, output)

    try:
        bruteforce(wordlist, output, url)
    except KeyboardInterrupt:
        print(f"\n\nYou have exited the program...")
    
    # ======================================================================
    # The purpose of this code is to save time by fuzzing subdomains
    # recursively by using process of elimination to create
    # a new wordlist to be used in the next iteration/depth
    # ======================================================================
    


"""	if args.multisub:
        temp_wordlist = tempfile.mkstemp()
        with os.fdopen(temp_wordlist, 'w') as tmp_f:
                with open(wordlist) as wordlist_f:
                    recursive_bruteforce(wordlist_f, tmp_f, args.multisub[1])
        os.remove(temp_wordlist)

    # ======================================================================

    

    if args.crawl:
        r = s_request(url)
        for link in BeautifulSoup(r, parse_only=SoupStrainer('a')):
            for i in link:
                if link.has_attr('href'):
                    print(link['href'])
                    if args.outurl:
                        pass
                    if args.inurl:
                        pass
                    if args.inaurl:
                        pass
                        """

    #TODO: multithread this shit

if __name__ == "__main__":
    main()
