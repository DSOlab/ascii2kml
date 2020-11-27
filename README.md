# ascii2kml
Transform plain ascii files to kml format

This is a dead simple python script to transform plain ascii files to kml format. It reads points (aka code, latitude, longtitude) from STDIN and transforms them to kml Placemarks inside a kml document. For a description of the input file format, see the file sample.ascii; the output of the script for this file is presented in the file sample.kml.

For more information and usage, type:
``` $>./ascii2kml.py -h ```
to display the help message.

Example:
```
$> cat sample.ascii
046006 38.305266755 22.553844827
047007 39.023304923 23.246122441 This   is       a      description for the point  with code "047007"
048052 37.594930591 22.617623263
# this is a comment line, no problem!
        # this is also a comment line
046007 37.305266755 21.553844827

$> cat sample.ascii | ./ascii2kml.py --document-name=foobar --description-after-col=3
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>foobar</name>
  <Placemark>
    <name>046006</name>
    <description></description>
    <Point><coordinates>22.553844827,38.305266755,0.0</coordinates></Point>
  </Placemark>
  <Placemark>
    <name>047007</name>
    <description>This   is       a      description for the point  with code "047007"
</description>
    <Point><coordinates>23.246122441,39.023304923,0.0</coordinates></Point>
  </Placemark>
  <Placemark>
    <name>048052</name>
    <description></description>
    <Point><coordinates>22.617623263,37.594930591,0.0</coordinates></Point>
  </Placemark>
  <Placemark>
    <name>046007</name>
    <description></description>
    <Point><coordinates>21.553844827,37.305266755,0.0</coordinates></Point>
  </Placemark>
</Document>
</kml>
```
