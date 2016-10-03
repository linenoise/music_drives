#!/usr/bin/env python

###
# make_music_drives.py
#
# Usage: python make_music_drives.pl [genre_key]
#
# Copies tracks within a specific genre tag from:
#
#    ~/Documents/Native*/Traktor*/collection.nml 
#
# to any removable drive with enough space. Names target files by open key
# for sorting on CDJs.
#
# Example: $ python make_music_drives.pl techno
#
# Questions:
# * Danne Stayskal <danne@stayskal.com>
###

import re
import os
import sys
import pwd
import glob
import getpass
import subprocess
import xml.etree.ElementTree as ET
from shutil import copyfile

# Musical key translations between NML and Open Key standards
open_key = {
	'0':  '01 ', # C major
	'1':  '08 ', # Db major
	'2':  '03 ', # D major
	'3':  '10 ', # Eb major
	'4':  '05 ', # E major
	'5':  '12 ', # F major
	'6':  '07 ', # Gb major
	'7':  '02 ', # G major
	'8':  '09 ', # Ab major
	'9':  '04 ', # A major
	'10': '11 ', # Bb major
	'11': '06 ', # B major
	'12': '01m', # C minor
	'13': '08m', # Db minor 
	'14': '03m', # D minor
	'15': '10m', # Eb minor
	'16': '05m', # E minor
	'17': '12m', # F minor
	'18': '07m', # Gb minor
	'19': '02m', # G minor
	'20': '09m', # Ab minor
	'21': '04m', # A minor
	'22': '11m', # Bb minor
	'23': '06m' # B minor
}


if len(sys.argv) < 2:
	print "Usage: python make_music_drives.pl [genre_key]"
	print "Example: python make_music_drives.pl techno"
	exit(1)
filter_genre = sys.argv[1]
print "Building " + filter_genre + " USB drives..."


collection_file = subprocess.check_output("ls ~/Documents/Native*/Traktor*/collection.nml", shell=True)
if not collection_file:
	print "Could not find collection.nml file. Exiting."
	exit(1)
print "Using index found in " + collection_file.rstrip();


print "Parsing Native Instruments XML..."
tree = ET.parse(collection_file.rstrip())
root = tree.getroot()


print "Indexing Traktor metadata..."
tracks = {}
path_cleaner = re.compile('/:')
for collection in root.findall('COLLECTION'):
	for entry in collection.findall('ENTRY'):
		location = entry.find('LOCATION')
		info = entry.find('INFO')
		tempo = entry.find('TEMPO')
		musical_key = entry.find('MUSICAL_KEY')
		loudness = entry.find('LOUDNESS')
		
		title = entry.attrib['TITLE']
		artist = entry.attrib['ARTIST']
		genre = info.attrib['GENRE']
		key = 0
		if musical_key is not None:
			key = musical_key.attrib['VALUE']
		if not genre == filter_genre:
			continue
		
		tracks[artist + " - " + title] = {
			'artist': artist,
			'title': title,
			'genre': genre,
			'key': open_key[key],
			'directory': path_cleaner.sub('/', location.attrib['DIR']),
			'filename': location.attrib['FILE'],
			'bitrate': info.attrib['BITRATE'],
			'length': info.attrib['PLAYTIME'],
			'size': info.attrib['FILESIZE'],
			'bpm': tempo.attrib['BPM'],
			'peak': loudness.attrib['PEAK_DB']
		}
track_index = tracks.keys()
track_index.sort()


print "Calculating necessary USB drive size..."
total_size = 0
for track in track_index:
 	total_size += int(tracks[track]['size'])
print "   " + str(total_size) + " bytes"


available_volumes = []
current_user = getpass.getuser()
print "Finding available USB drives with enough free space that " + current_user + " can write to..."
for volume in glob.glob("/Volumes/*"):
	stat_info = os.stat(volume)
	owner = pwd.getpwuid(stat_info.st_uid)[0]
	if current_user == owner:
		stat = os.statvfs(volume)
		available_bytes = (stat.f_bavail * stat.f_frsize) / 1024
		if available_bytes > total_size:
			print "   Using " + volume
			available_volumes.append(volume)
		else:
			print "   Skipping " + volume + ", since it only has " + str(available_bytes) + " bytes free"
			
for volume in available_volumes:
	print "Copying tracks to " + volume + "..."
	for track in track_index:
		source_name = tracks[track]['directory'] + tracks[track]['filename']
		dest_file = volume + '/(' + tracks[track]['key'] + ',' + str(int(float((tracks[track]['bpm'])))) + ') ' + tracks[track]['filename']
		print dest_file
		copyfile(source_name, dest_file)
		
