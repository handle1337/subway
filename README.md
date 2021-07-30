# This tool is under development
It still isn't finished and I wouldn't recommend using it as of now.

# Features
1. Subdomain discovery using wordlists
2. (In development) Subdomain discovery using APIs
3. (In development) CNAME discovery
4. (In development) Endpoints discovery maybe?

# Usage
This tool is very simple to use, you can see what flags are available by using the -h/--help flags. <br>
```
└──╼ $./subway.py -h
usage: use 'subway.py --help' for more information

Enumerate subdomains and URLs

optional arguments:
  -h, --help            show this help message and exit
  --banner, -b          disable banner
  --url URL, -u URL     Target URL
  --output OUTPUT, -o OUTPUT
                        Output file
  --wordlist WORDLIST, -w WORDLIST
                        Subdomain wordlist
  --multisub MULTISUB, -ms MULTISUB
                        multilevel subdomain enumeration
  --crawl, -c           crawl source for URLs
  --outurl, -ou         output ALL found URLs
  --inurl, -iu          include URLs that are found inside the site's source [href]
  --inaurl, -iau        include ALL found URLs in the site's source [href]

```
## Examples
+ Subdomain discovery using wordlist:
`./subway.py -u https://target.com/ -w /opt/SecLists/Discovery/DNS/bitquark-subdomains-top100000.txt -o output.txt`
