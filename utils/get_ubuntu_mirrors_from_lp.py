import sys
import feedparser

d = feedparser.parse("https://launchpad.net/ubuntu/+archivemirrors-rss")
#d = feedparser.parse(open("+archivemirrors-rss"))

countries = {}

for entry in d.entries:
    countrycode = entry.mirror_countrycode
    if countrycode not in countries:
        countries[countrycode] = set()
    for link in entry.links:
        countries[countrycode].add(link.href)


keys = sorted(countries)

if len(keys) == 0:
    sys.stderr.write("E: Could not read the mirror list due to some issue"
                     " -- status code: %s\n" % d.status)
    sys.exit(1)

print("mirror://mirrors.ubuntu.com/mirrors.txt")
for country in keys:
    print("#LOC:%s" % country)
    print("\n".join(sorted(countries[country])))
