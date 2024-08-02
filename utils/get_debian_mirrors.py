from __future__ import print_function
import collections
import sys
import urllib.request
from debian import deb822

mirrors = collections.defaultdict(set)
masterlist = urllib.request.urlopen("https://mirror-master.debian.org/"
                                    "status/Mirrors.masterlist")

for mirror in deb822.Deb822.iter_paragraphs(masterlist):
    if "Country" not in mirror:
        continue
    country = mirror["Country"].split(None, 1)[0]
    site = mirror["Site"]
    for proto in 'http', 'ftp':
        if "Archive-%s" % proto in mirror:
            mirrors[country].add("%s://%s%s" % (proto, site,
                                                mirror["Archive-%s" % proto]))

if len(mirrors) == 0:
    sys.stderr.write("E: Could not read the mirror list due to "
                     "some unknown issue\n")
    sys.exit(1)
for country in sorted(mirrors):
    print("#LOC:%s" % country)
    print("\n".join(sorted(mirrors[country])))
