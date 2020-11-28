#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import argparse

def printer(*msg): print(*msg, file = sys.stderr)

def is_float_with_dot(str):
    try:
        float(str)
        return "." in str
    except:
        return False

class Placemark:
    
    def __init__(self, lat, lon, name="", description=""):
        self.latitude = lat
        self.longtitude = lon
        self.name = name
        self.description = description
    
    def flush(self):
        print("  <Placemark>")
        print("    <name>{:}</name>".format(self.name))
        print("    <description>{:}</description>".format(self.description))
        print("    <Point><coordinates>{:},{:},0.0</coordinates></Point>".
          format(self.longtitude, self.latitude))
        print("  </Placemark>")
        return

def parse_line(line, names_w_spaces=False, description_col=None):
    l = line.split()
    if len(l) < 3:
        ermsg = ("[ERROR] Number of fields in line \"{:}\" < 3".format(
          line.strip()))
        # printer(ermsg)
        raise RuntimeError(ermsg)
    ##  resolve point name
    if names_w_spaces:
        lat_str = ""
        for idx, colstr in enumerate(l):
            if is_float_with_dot(colstr):
                lat_str = colstr
                break
        if idx > len(l) - 2:
            ermsg = ("[ERROR] Failed to resolve line \"{:}\"."
              "Cannot find lat/lon after name".format(line.strip()))
            # printer(ermsg)
            raise RuntimeError(ermsg)
        name = line[0:line.find("{:}".format(lat_str))-1]
    else:
        name = l[0]
        idx = 0
    ##  resolve latitude/longtitude
    assert(len(l)>=idx+2)
    try:
      lat, lon = [ float(x) for x in [l[idx], l[idx+1]] ]
    except:
          ermsg = ("[ERROR] Failed to resolve lat/lon fields in line \"{:}\"".
            format(line.strip()))
          # printer(ermsg)
          raise RuntimeError(ermsg)
    ##  resolve description
    if description_col and len(l) > description_col+idx:
      description_col += idx-1
      description = line[line.find(" {:} "
        .format(l[description_col]))+1:].rstrip()
    else:
      description = ""
    ##  return Placemark
    return Placemark(lat, lon, name, description)

def flush_placemark(lat, lon, name="", description=""):
    print("  <Placemark>")
    print("    <name>{:}</name>".format(name))
    print("    <description>{:}</description>".format(description))
    print("    <Point><coordinates>{:},{:},0.0</coordinates></Point>"
      .format(lon, lat))
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
    description=('Read in points (on the earth\'s surface) and transform them '
      'to Placemarks in a valid KML document.'),
    epilog=('National Technical University of Athens\n'
      'Dionysos Satellite Observatory\n'
      'Send bug reports to:\n'
      'Xanthos Papanikolaou, xanthos@mail.ntua.gr'
      'Dimitris Anastasiou,danast@mail.ntua.gr\n'
      'November, 2020'))

parser.add_argument('--document-name',
    default='sample.kml',
    metavar='DOCUMENT_NAME',
    dest='doc_name',
    required=False,
    help=('The name of the \"Document\" tag, inside the kml file; note that '
      'this is not the output filename.'))

parser.add_argument('--name-w-spaces',
    dest='names_w_spaces',
    action='store_true',
    help=('If set then the station/point names can include whitespace/tab '
      'characters. That means, that the name of each point will start from the '
      'begining of the line and stop untill we reach a column that can be '
      'interpreted as float (i.e. the latitude).'))

parser.add_argument('--description-after-col',
    default=None,
    metavar='DESCRIPTION_COL',
    dest='description_col',
    type=int,
    required=False,
    help=('If given, then the text starting at column DESCRIPTION_COL and '
      'ending at the EndOfLine (for each line) will be interpreted as '
      'description text and added to the kml file. Note that column indexing '
      'starts at 0! If the point name includes whitespace characters (aka is '
      'longer than 1 cols) it will only be counted as one column (given that '
      'the \'--name-w-spaces\' switch is used). That is, for the line '
      '\'Name2 With  Big Name 37.694930591 22.717623263 a description!\' the '
      'name string \'Name2 With  Big Name\' is counted as one column and thus '
      'users should use \'--description-after-col=3\''))

parser.add_argument('--ignore-error-lines',
    dest='ignore_error_lines',
    action='store_true',
    help=('By default the program will stop if it encounters a line it cannot '
      'resolve. With this switch, the program will not stop but only ignore '
      'erronuous lines and keep on reading.'))

##  parse cmd
args  = parser.parse_args()

if args.description_col: assert(args.description_col>=3)

##  read ascii lines from STDIN
open_kml(args.doc_name)
for line in sys.stdin:
    if not line.lstrip().startswith('#'):
        try:
            placemark = parse_line(line, args.names_w_spaces, args.description_col)
            placemark.flush()
        except Exception as exc:
            if args.ignore_error_lines:
                pass
            else:
                printer(*exc.args)
                sys.exit(1)
close_kml()
