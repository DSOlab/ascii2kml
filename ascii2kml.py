#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import argparse

def printer(*msg): print(*msg, file = sys.stderr) 

def flush_placemark(lat, lon, name="", description=""):
    print("  <Placemark>")
    print("    <name>{:}</name>".format(name))
    print("    <description>{:}</description>".format(description))
    print("    <Point><coordinates>{:},{:},0.0</coordinates></Point>".format(lon, lat))
    print("  </Placemark>")
    return

def open_kml(name=""):
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    print("<kml xmlns=\"http://www.opengis.net/kml/2.2\">")
    print("<Document>")
    print("  <name>{:}</name>".format(name))
    return

def close_kml():
    print("</Document>")
    print("</kml>")

class myFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter):
  pass

parser = argparse.ArgumentParser(
    formatter_class=myFormatter,
    description='Ascii files to KML format',
    epilog=('''National Technical University of Athens,
      Dionysos Satellite Observatory\n
      Send bug reports to:
      Xanthos Papanikolaou, xanthos@mail.ntua.gr
      Dimitris Anastasiou,danast@mail.ntua.gr
      November, 2020'''))

parser.add_argument('--document-name',
    default='sample.kml',
    metavar='DOCUMENT_NAME',
    dest='doc_name',
    required=False,
    help='The name of the \"Document\" tag, inside the kml file (note that this is not the output filename).')

parser.add_argument('--description-after-col',
    default=None,
    metavar='DESCRIPTION_COL',
    dest='description_col',
    type=int,
    required=False,
    help='If given, then the text starting at column DESCRIPTION_COL and ending at the EndOfLine (for each line) will be interpreted as description text and added to the kml file. Note that column indexing starts at 0!')

##  parse cmd
args  = parser.parse_args()

if args.description_col: assert(args.description_col>=3)

##  read ascii lines from STDIN
open_kml(args.doc_name)
for line in sys.stdin:
    if not line.lstrip().startswith('#'):
        l = line.split()
        if len(l) < 3:
            printer("[ERROR] Number of fields in line \"{:}\" < 3".format(line))
            sys.exit(1)
        name = l[0]
        try:
          lat, lon = [ float(x) for x in [l[1], l[2]] ]
        except:
            printer("[ERROR] Failed to resolve lat/lon fields in line \"{:}\"".format(line))
            sys.exit(1)
        if args.description_col  and len(l) > args.description_col:
          description = line[line.find(" {:} ".format(l[args.description_col]))+1:]
        else:
          description = ""
        flush_placemark(lat, lon, name, description)
close_kml()
