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

    
    
    


class GetVals(object):
    
    def __init__(self,source, fields, extent, sumlevel):
        
        self.sumlevels = ['state','county','place','tract','bg','block']
        self.sumlevelurls = {}
        self.sumlevelurls['state'] = "for=state:{istate}"
        self.sumlevelurls['county'] = "for=county:{icounty}&in=state:{istate}"
        self.sumlevelurls['place'] = "for=place:{iplace}&in=state:{istate}"
        self.sumlevelurls['tract'] = "for=tract:{itract}&in=state:{istate}+county:{icounty}"
        self.sumlevelurls['bg'] = "for=block+group:{ibg}&in=state:{istate}+county:{icounty}+tract:{itract}"
        self.sumlevelurls['block'] = "for=block:{iblock}&in=state:{istate}+county:{icounty}+tract:{itract}"
        
        self.sources = ['sf1_2010','sf1_2000','sf3_2000','sf1_1990','sf3_1990','acs_2010_5','acs_2011_5']
        self.sourceurls ={}
        self.sourceurls['sf1_2010'] = "http://api.census.gov/data/2010/sf1?key={ikey}"
        self.sourceurls['sf1_2000'] = "http://api.census.gov/data/2000/sf1?key={ikey}"
        self.sourceurls['sf3_2000'] = "http://api.census.gov/data/2000/sf3?key={ikey}"
        self.sourceurls['sf1_1990'] = "http://api.census.gov/data/1990/sf1?key={ikey}"
        self.sourceurls['sf3_1990'] = "http://api.census.gov/data/1990/sf3?key={ikey}"
        self.sourceurls['acs_2010_5'] = "http://api.census.gov/data/2010/acs5?key={ikey}"
        self.sourceurls['acs_2011_5'] = "http://api.census.gov/data/2011/acs5?key={ikey}"
        
        
        if self.CheckSource(source):
            self.source = source
        else:
            raise Exception("Failed to register source")
        self.fields = fields
        self.extent = extent
        if self.CheckSumLevel(sumlevel): 
            self.sumlevel = sumlevel
        else:
            raise Exception("Failed to register summary level")

        
    def CheckSumLevel(self,sumlevel):
        if sumlevel in self.sumlevels:
            return True
        else:
            return False
    
    def CheckSource(self,source):
        if source in self.sources:
            return True
        else:
            return False
        
   
    def GetState(self,extent,fields):
        return json.load(urllib2.urlopen("&".join([self.sourceurls[self.source],self.sumlevelurls['state'].format(istate=",".join(extent)),'get='+",".join(fields+['NAME'])])))


#metadata
#key (sumlevel, extent, source)
#val1
#val2

#Datatables (source_sumlevel)
#geoid (varchar25)
#Val(name, numeric)


