# ascii2kml
Transform plain ascii files to kml format

This is a dead simple python script to transform points recorded in plain ascii 
format to Palcemarks in a valid KML document. The program will read points 
(aka lines of code, latitude, longtitude) from STDIN and transform them to KML 
Placemarks inside a KML document. For a description of the input file format, 
see the file sample.ascii; the output of the script for this file is presented in the file sample.kml.

## input format for data points
The program reads in points from STDIN; every line is considered a new 
individual point. The points should follow the following convention:
```CODE LATITUDE LONGTITUDE DESCRIPTION```
where:

  * CODE is a name for the specific point; it will be interpreted as the 
    Placemark's name tag. In **default mode, CODE must not contain whitespace 
    characters**. If it does (contain whitespaces and or tabs characters), 
    then **use the switch `--name-w-spaces`**; this will trigger a different
    approach where the programm will interpret as CODE all columns starting from 
    the first one up untill it finds a column that contains a float number. The 
    latter is interpreted as latitude; everything before this column is 
    interpreted as the CODE. E.g.
    `046007 37.305266755 21.553844827` is ok, '046007' is interpreted as CODE.
    `Name With   Spaces 37.794930591 22.817623263` is not ok in default mode. If 
    we use the switch `--name-w-spaces` though, the program will interpret the 
    string 'Name With   Spaces` as CODE.

  * LATITUDE is the latitude of the point. It must follow the CODE and follow 
    a floating point format convention. Latitude should be given in decimal 
    degrees.
  
  * LONGTITUDE is the longtitude of the point. It must follow the LATITUDE and follow 
    a floating point format convention. Longtitude should be given in decimal 
    degrees.

  * DESCRIPTION [optional] An optional description of the point which will be 
    written in the Placemark's description tag. Note that you must use the switch 
    `--description-after-col=N` for the program to know that the string starting 
    at column N to the end of line is a description (otherwise columns after 
    LONGTITUDE will be ignored). Note that column numbering starts at column 0 and 
    that if you specify the `--name-w-spaces` switch, the string interpreted as 
    CODE will be counted as one column (whatever number of columns/whitespaces it 
    contains). E.g. the line `Name2 With  Big Name 37.694930591 22.717623263 and it also has a description!` 
    with the command `ascii2kml.py --description-after-col=3 --name-w-spaces` will 
    be interpreted as: `Column[0] = CODE = 'Name2 With  Big Name'`, `Column[1] = LATITUDE = 37.694930591`, 
    `Column[2] = LONGTITUDE = 22.717623263` and everything after column 3 is a 
    description, `Column[3 to EOL] = DESCRIPTION = 'and it also has a description!'`.


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
Name With   Spaces 37.794930591 22.817623263
Name2 With  Big Name 37.694930591 22.717623263 and it also has a description!
This is an erronuous line
Also an erronuous line 37.594930591
# the following is also an erronuous line
37.594930591 22.617623263

$> cat sample.ascii | ./ascii2kml.py \ 
  --document-name=foobar --description-after-col=3 \
  --name-w-spaces --ignore-error-lines
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
    <description>This   is       a      description for the point  with code "047007"</description>
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
  <Placemark>
    <name>Name With   Spaces</name>
    <description></description>
    <Point><coordinates>22.817623263,37.794930591,0.0</coordinates></Point>
  </Placemark>
  <Placemark>
    <name>Name2 With  Big Name</name>
    <description>and it also has a description!</description>
    <Point><coordinates>22.717623263,37.694930591,0.0</coordinates></Point>
  </Placemark>
</Document>
</kml>
```
