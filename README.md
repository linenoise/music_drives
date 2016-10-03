Make Music Drives
=================

Copies tracks within a specific genre tag from your Native Instruments Traktor library to any USB drive that's currently plugged in and has enough space to hold it. Prepends target files with open key and tempo for easy sorting and identification on Pioneer equipment.

Usage
-----

    python make_music_drives.pl [genre_key]

Example
-------

    $ python make_music_drives.pl techno
    Building techno USB drives...
    Using index found in /Users/linenoise/Documents/Native Instruments/Traktor 
    2.10.1/collection.nml
    Parsing Native Instruments XML...
    Indexing Traktor metadata...
    Calculating necessary USB drive size...
       16674904 bytes
    Finding available USB drives with enough free space that linenoise can 
    write to...
       Using /Volumes/LINENOISE C
       Using /Volumes/LINENOISE D
    Copying tracks to /Volumes/LINENOISE C...
    /Volumes/LINENOISE C/(05m,133) Absorbed - Intrude (Original Mix).flac
    ...


Notes
-----

* If you have Traktor running and can't see updates you've made in your NML file, right click on "Track Collection" and click on "Save Collection".
* You'll need to install Element Tree first by `pip install elementtree`

Questions
---------

Danne Stayskal <danne@stayskal.com>
