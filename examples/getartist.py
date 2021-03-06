#! /usr/bin/env python
#
# Retrieve an artist by ID and display all official albums.
#
# Usage:
#	python getartist.py artist-id
#
# $Id: getartist.py 11853 2009-07-21 09:26:50Z luks $
#
import sys
import logging
import musicbrainz2.webservice as ws
import musicbrainz2.model as m

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


if len(sys.argv) < 2:
	print "Usage: getartist.py artist-id"
	sys.exit(1)

q = ws.Query()

try:
	# The result should include all official albums.
	#
	inc = ws.ArtistIncludes(
		releases=(m.Release.TYPE_OFFICIAL, m.Release.TYPE_ALBUM),
		tags=True, releaseGroups=True)
	artist = q.getArtistById(sys.argv[1], inc)
except ws.WebServiceError, e:
	print 'Error:', e
	sys.exit(1)


print "Id         :", artist.id
print "Name       :", artist.name
print "SortName   :", artist.sortName
print "UniqueName :", artist.getUniqueName()
print "Type       :", artist.type
print "BeginDate  :", artist.beginDate
print "EndDate    :", artist.endDate
print "Tags       :", ', '.join([t.value for t in artist.tags])
print

if len(artist.getReleases()) == 0:
	print "No releases found."
else:
	print "Releases:"

for release in artist.getReleases():
	print
	print "Id        :", release.id
	print "Title     :", release.title
	print "ASIN      :", release.asin
	print "Text      :", release.textLanguage, '/', release.textScript
	print "Types     :", release.types

print

if len(artist.getReleaseGroups()) == 0:
	print
	print "No release groups found."
else:
	print
	print "Release groups:"

for rg in artist.getReleaseGroups():
	print
	print "Id        :", rg.id
	print "Title     :", rg.title
	print "Type      :", rg.type

print

#
# Using the release IDs and Query.getReleaseById(), you could now request 
# those releases, including the tracks, release events, the associated
# DiscIDs, and more. The 'getrelease.py' example shows how this works.
#

# EOF
