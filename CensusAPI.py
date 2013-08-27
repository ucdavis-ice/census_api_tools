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
time.clock()
print str(datetime.datetime.now()),"|Starting"
key = api_key.api_key #Your API key goes here. get one at: http://www.census.gov/developers/tos/key_request.html

#geolevel = "tract" #not implemented yet


# Source defines the data source
source = 'sf1_2010'
#source = 'acs_2011_5'


# Fields defines what data you're going to request
fields = ['P0010001','H0040001','H0050001'] # test values for the sf1_2010
#fields = ['B01001_002E','B01001_002M','B01001_026E','B01001_026M'] # test for ACS_2011_5

# Limit the data by state
instatelist = ["06"] # "06" for california "*" for all states

# output csv
outfile = "output.csv"

dobg = False #Do you want to run the block group, if not run tract

#open output
try:
    ofile = open(outfile,'w')
    csvwriter = csv.writer(ofile,lineterminator='\n')
except:
    raise Exception('Unable to open csv for writing.')

sources = ['sf1_2010','sf1_2000','sf3_2000','sf1_1990','sf3_1990','acs_2010_5','acs_2011_5']
baseurls ={}
baseurls['sf1_2010'] = "http://api.census.gov/data/2010/sf1?key={ikey}"
baseurls['sf1_2000'] = "http://api.census.gov/data/2000/sf1?key={ikey}"
baseurls['sf3_2000'] = "http://api.census.gov/data/2000/sf3?key={ikey}"
baseurls['sf1_1990'] = "http://api.census.gov/data/1990/sf1?key={ikey}"
baseurls['sf3_1990'] = "http://api.census.gov/data/1990/sf3?key={ikey}"
baseurls['acs_2010_5'] = "http://api.census.gov/data/2010/acs5?key={ikey}"
baseurls['acs_2011_5'] = "http://api.census.gov/data/2011/acs5?key={ikey}"


#geolevels = ['county','tract','bg','block','place','state']
#geolevelurls = {}
#geolevelurls['state'] = "&for=state:{istate}"
#geolevelurls['county'] = "&for=county:{icounty}&in=state:{istate}"
#geolevelurls['place'] = "&for=place:{iplace}&in=state:{istate}"
#geolevelurls['tract'] = "&for=tract:{itract}&in=state:{istate}+county:{icounty}"
#geolevelurls['bg'] = "&for=block+group:{ibg}&in=state:{istate}+county:{icounty}+tract:{itract}"
#geolevelurls['block'] = "&for=block:{iblock}&in=state:{istate}+county:{icounty}+tract:{itract}"
#
#if geolevel not in geolevels: raise
if source not in sources: raise Exception("Source is not one of the allowable options.")

def get_val(inlist,val):
    try: 
        i = inlist.index(val)
        return i
    except:
        raise Exception("Unable to return list index.")
        
    



tracts = []
bgs = []
try:
    statesurl = baseurls[source].format(ikey=key)+"&get=NAME&for=state:{istatelist}".format(ikey=key,istatelist=",".join(instatelist))
    stateresult = urllib2.urlopen(statesurl)
    statelist = json.load(stateresult)
    stateidx = get_val(statelist[0],"state")
    for state in statelist[1:]:
        countiesurl = baseurls[source].format(ikey=key)+"&get=NAME&for=county:*&in=state:{istate}".format(ikey=key,istate=state[stateidx])
        cntyresult = urllib2.urlopen(countiesurl)
        countylist = json.load(cntyresult)
        cntyidx = get_val(countylist[0],'county')
        for cnty in countylist[1:]:
            print str(datetime.datetime.now()),"|Working on: {icounty},{istate}".format(ikey=key,icounty=cnty[cntyidx],istate=state[stateidx])
            tracturl = baseurls[source].format(ikey=key)+"&get={ifields}&for=tract:*&in=state:{istate}+county:{icounty}".format(ikey=key,istate=state[stateidx],icounty=cnty[cntyidx],ifields=",".join(fields))
            tractresult = urllib2.urlopen(tracturl)
            tractlist = json.load(tractresult)
            tractkey = tractlist[0]
            tractidx = get_val(tractkey,'tract')
            for tract in tractlist[1:]:
                tracts.append(tract) # create a list of the JSON items for each tract
                if dobg == True:
                    bgurl = baseurls[source].format(ikey=key)+"&get={ifields}&for=block+group:*&in=state:{istate}+county:{icounty}+tract:{itract}".format(ikey=key,istate=state[stateidx],icounty=cnty[cntyidx], itract = tract[tractidx],ifields=",".join(fields))
                    bgresult = urllib2.urlopen(bgurl)
                    bglist = json.load(bgresult)
                    bgkey = bglist[0]
                    bgidx = get_val(bgkey,'block group')
                    for bg in bglist[1:]:
                        bgs.append(bg) # create a list of the JSON items for each block group.
    if bgs != []:
        # write bgs
        csvwriter.writerow(bgkey)
        csvwriter.writerows(bgs)
        
    else:
        # write tracts
        csvwriter.writerow(tractkey)
        csvwriter.writerows(tracts)
    try:
        ofile.close()
    except:
        raise Exception("Failed to close output csv.")
    
    
    
    print str(datetime.datetime.now()),"|Finished"
    print "Number of tracts:" + str(len(tracts))
    print "Number of block groups:" + str(len(bgs))
    print "Total size of tracts in memory (bytes):", sys.getsizeof(tracts)
    print "Total Time:",str(time.clock())
except urllib2.URLError, e:
    print "URLError:",str(e)
except Exception, e:
    print "Error:", str(e)