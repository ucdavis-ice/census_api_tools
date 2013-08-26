'''
Census 2010 SF1 API test example
@author: Nathaniel Roth, neroth@ucdavis.edu

This loops through all states in the instatelist and gets all of the fields in fields. 

This demonstrates a way to recursively loop through all states, counties, tracts, and block groups obtaining data from the census API.
You will need to provide your own Census API key.

Ideas for the future:
1. Rewrite into a class
2. That supports both ACS (by year) and SF1
3. With selectable geographic scale

Copyright (C) 2013  Nathaniel Roth

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


'''

import sys,urllib2,json,datetime,time,api_key,csv


class Setup(object):
    '''
    
    '''
    def __init__(self,connstr,source,extent,level):
        self.connstr = connstr
        self.source = source
        self.extent = extent
        self.level = level
        
        
    def MakeTables(self):
        #