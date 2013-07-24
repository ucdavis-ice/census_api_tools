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

import sys,urllib2,json,datetime,time
time.clock()
print str(datetime.datetime.now()),"|Starting"
key = "<key goes here>" #Your API key goes here. get one at: http://www.census.gov/developers/tos/key_request.html
fields = ['P0010001','H0040001','H0050001']
instatelist = "*" # "06" for california
tracts = []
bgs = []
try:
    statesurl = "http://api.census.gov/data/2010/sf1?key={ikey}&get=NAME&for=state:{istatelist}".format(ikey=key,istatelist=instatelist)
    stateresult = urllib2.urlopen(statesurl)
    statelist = json.load(stateresult)
    for state in statelist[1:]:
        countiesurl = "http://api.census.gov/data/2010/sf1?key={ikey}&get=NAME&for=county:*&in=state:{istate}".format(ikey=key,istate=state[1])
        cntyresult = urllib2.urlopen(countiesurl)
        countylist = json.load(cntyresult)
        for cnty in countylist[1:]:
            print str(datetime.datetime.now()),"|Working on: {icounty},{istate}".format(ikey=key,icounty=cnty[0],istate=state[0])
            tracturl = "http://api.census.gov/data/2010/sf1?key={ikey}&get={ifields}&for=tract:*&in=state:{istate}+county:{icounty}".format(ikey=key,istate=state[1],icounty=cnty[2],ifields=",".join(fields))
            tractresult = urllib2.urlopen(tracturl)
            tractlist = json.load(tractresult)
            tractkey = tractlist[0]
            for tract in tractlist[1:]:
                tracts.append(tract) # create a list of the JSON items for each tract
#                bgurl = "http://api.census.gov/data/2010/sf1?key={ikey}&get=P0010001,H0040001,H0050001&for=block+group:*&in=state:06+county:{icounty}+tract:{itract}".format(ikey=key,icounty=cnty[2], itract = tract[5])
#                bgresult = urllib2.urlopen(bgurl)
#                bglist = json.load(bgresult)
#                bgkey = bglist[0]
#                for bg in bglist[1:]:
#                    bgs.append(bg) # create a list of the JSON items for each block group.
    
    print str(datetime.datetime.now()),"|Finished"
    print "Number of tracts:" + str(len(tracts))
    print "Number of block groups:" + str(len(bgs))
    print "Total size of tracts in memory (bytes):", sys.getsizeof(tracts)
    print "Total Time:",str(time.clock())
except urllib2.URLError, e:
    print "URLError:",str(e)
except Exception, e:
    print "Error:", str(e)