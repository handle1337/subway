#!/usr/bin/env python3

import requests
import sys
import os
import threading
import tempfile
import colorama
from bs4 import BeautifulSoup
from argparse import *




BANNER = """
   ___            _                        _  _  
  / __|   _  _   | |__   __ __ __ __ _    | || | 
  \__ \  | +| |  | '_ \  \ V  V // _` |    \_, | 
  |___/   \_,_|  |_.__/   \_/\_/ \__,_|   _|__/  
_|\"\"\"\"\"\|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_| \"\"\"\"| 
\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'

"""


url = ""



def fuzz(file, output="output_enum.txt"):
	with open(file, 'r') as f:
		for line in f:
			data = check_status(URL + "/" + line)
			if output:
				save_output(output, data[1])


# TODO: make this pull subdomains from the virustotal api
def enum(file, output="output_enum.txt"):
	pass



def recursive_fuzz(file, tmpfile, depth):
	url_l = url
	for i in range(depth):
		for line in file:
			if check_status(url_l + "/" + line):
				tmpfile.write(check_status[1] + "\n")
				url_l = url_l + "/" + line
				file = tmpfile



def recursive_enum(file, tmpfile, depth):
	url_l = url
	for i in range(depth):
		for line in file:
			url_l = line + "." + url_l
			if check_status(url_l):
				tmpfile.write(check_status[1] + "\n")
				url_l = url_l + "/" + line
				file = tmpfile
				#Theres a massive logic flaw in this function i need to test it



def save_output(file, data):
	with open(file, 'w') as f:
		f.write(data + "\n")



def s_request(url_l):
	r = requests.get(url_l)
	return r.text



def check_status(subdomain, directory):
	url_l = subdomain + URL + "/" + directory
	r_unicode = s_request(url_l)
	title = r_unicode[r_unicode.find('<title>') + 7 : r_unicode.find('</title>')]
	if r.status_code < 400:
		print(f"[{title}][{r.status_code}] {url_l}")
		return [subdomain, directory]
	return None


def main():

	#TODO: ???
	parser = ArgumentParser(description="Enumerate subdomains and URLs",
							usage="use '%(prog)s --help' for more information",
							formatter_class=RawTextHelpFormatter)
	parser.add_argument("--banner", "-b", default=False, help="Print banner at program startup")
	parser.add_argument("--url", "-u", required=True, help="Target URL")
	parser.add_argument("--output", "-o", nargs='+', dest="output", help="Output file", type=FileType('w'))
	parser.add_argument("--dwordlist", "-dw", nargs='?', default=sys.stdin, type=FileType('r'),
						help="Directory wordlist")
	parser.add_argument("--swordlist", "-sw", nargs='?', default=sys.stdin, type=FileType('r'),
						help="Subdomain wordlist")
	parser.add_argument("--multisub", "-ms", help="Multilevel subdomain enumeration")
	parser.add_argument("--recdir", "-rd", help="Recurisve directory fuzzing")
	parser.add_argument("--crawl", "-c", help="Crawl source for URLs")
	parser.add_argument("--outurl", "-ou", help="Output ALL found URLs")
	parser.add_argument("--inurl", "-iu", default="True",
						help="[SUBDOMAIN ENUMERATION] Include URLs that belong to the site")
	parser.add_argument("--inaurl", "-iau", default="False",
						help="[SUBDOMAIN ENUMERATION] Include ALL found URLs")
	args = parser.parse_args()
	
	
	if args.banner:
		print(banner)
	if args.url:
		url = args.url
	# ======================================================================
	# The purpose of this code is to save time by fuzzing directories and
	# subdomains recursively by using process of elimination to create
	# a new wordlist to be used in the next iteration/depth
	# ======================================================================
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
				recursive_fuzz(dlist, rtmp, args.recdir[1])
		os.remove(dd)

	# ======================================================================

	if args.crawl:
		#ok i actually gotta loop through all dirs and subdomains and then their dirs, this code is gonna be extra fucky
		r = s_request(url)
		for link in BeautifulSoup(r, parse_only=SoupStrainer('a')):
			if link.has_attr('href'):
				print(link['href'])
				if args.outurl:
					pass
				if args.inurl:
					pass
				if args.inaurl:
					pass

	#TODO: multithread this shit
	fuzz(args.dwordlist[0], args.output[0])
	enum(args.swordlist[0], args.output[1])

if __name__ == "__main__":
	main()