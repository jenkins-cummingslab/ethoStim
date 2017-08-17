import json
import os
import sys
import types
import datetime
from itertools import groupby

def checkIfNumber(s):
    if s[0] in ('-','+'):
        return s[1:].isdigit()
    return s.isdigit()  

def respondsToPing(hostname):
    return os.system("ping -c 1 -w2 " + hostname + " > /dev/null 2>&1")

def parseTopJSON():
    with open(os.path.join('top_NEW.json'), 'r') as jsonFile:
        jsonString = jsonFile.read()
        paramsDict = json.loads(jsonString)
        for k,v in paramsDict.iteritems():
            if type(v) == types.UnicodeType:    
                path_elems = v.split('\\')
                newPath = os.path.join(*path_elems)
                paramsDict[k] = newPath
    top_dict = paramsDict
    
    # check error conditions           
    if top_dict is None:
        print 'Tests: Error> Top dictionary is None, problem parsing top.json'
        print 'Tests: Exiting...'
        sys.exit(1)
    
    return top_dict
                  
def parseFishJSON():
    with open(os.path.join('fish.json'), 'r') as jsonFile:
        jsonString = jsonFile.read()
        paramsDict = json.loads(jsonString)
        for k,v in paramsDict.iteritems():
            if type(v) == types.UnicodeType:    
                path_elems = v.split('\\')
                newPath = os.path.join(*path_elems)
                paramsDict[k] = newPath
    fish_dict = paramsDict
    
    # check error conditions           
    if fish_dict is None:
        print 'Tests: Error> Fish dictionary is None, problem parsing fish.json'
        print 'Tests: Exiting...'
        sys.exit(1) 
    
    return fish_dict       
                        
def parsePiesJSON():
    with open(os.path.join('pies.json'), 'r') as jsonFile:
        jsonString = jsonFile.read()
        paramsDict = json.loads(jsonString)
        for k,v in paramsDict.iteritems():
            if type(v) == types.UnicodeType:    
                path_elems = v.split('\\')
                newPath = os.path.join(*path_elems)
                paramsDict[k] = newPath
    pies_dict = paramsDict
    
    # check error conditions           
    if pies_dict is None:
        print 'Tests: Error> Pies dictionary is None, problem parsing pies.json'
        print 'Tests: Exiting...'
        sys.exit(1) 
    
    return pies_dict  
    
def parseTestsJSON():        
    with open(os.path.join('tests.json'), 'r') as jsonFile:
        jsonString = jsonFile.read()
        paramsDict = json.loads(jsonString)
        for k,v in paramsDict.iteritems():
            if type(v) == types.UnicodeType:    
                path_elems = v.split('\\')
                newPath = os.path.join(*path_elems)
                paramsDict[k] = newPath
                
#         key = 'TempStepSize'    
#         if key in paramsDict:
#             if Tests.checkIfNumber(paramsDict[key]):
#                 self.tempStepSize = int(paramsDict[key])
#             else:
#                 print self.me + ': Error> ' + key + ' is not numeric, will use default'
#         else:
#             print self.me + ': Error> ' + key + ' is not in parameters.json, will use default'
                 
    key = 'test_list'  
    test_list = []
    if key in paramsDict:
        tmp_list = eval(paramsDict[key])
        for k in tmp_list:
            if tmp_list[k] is "True":
                test_list.append(k)
    else:
        print 'Tests: Info> ' + key + ' is not in tests.json, NO TESTS WILL BE RUN!'
        print 'Tests: Exiting...'
        sys.exit(0)

    # Check error conditions           
    if not test_list:
        print 'Tests: Info> Test list is empty, NO TESTS WILL BE RUN!'
        print 'Tests: Exiting...'
        sys.exit(0) 
        
    return test_list

class Tests(object):
    
    #DEFAULT_MIN_TEMP = -10

    def __init__(self):
        self.me = 'Tests'
        #self.startTemp = Tests.DEFAULT_MIN_TEMP        
        self.top_dict = parseTopJSON()
        self.fish_dict = parseFishJSON()
        self.test_list = parseTestsJSON()     
        self.pies_dict = parsePiesJSON()
        self.schedules = ["H1", "H2", "H3", "L1", "L2", "L3"]
    
    @staticmethod
    def isFishInFishJson(self, fish):
        if fish in self.fish_dict:
            print self.me + ': ' + fish + ' is valid (in fish.json)'
            return True
        print self.me + ': ERROR> ' + fish + ' is NOT valid (NOT in fish.json)'
        return False
        
    @staticmethod
    def isPiInPiesJson(self, pi):
        if pi in self.pies_dict:
            print self.me + ': ' + pi + ' is valid (in pies.json)'
            return 0
        print self.me + ': ERROR> ' + pi + ' is NOT valid (NOT in pies.json)'
        return 1   

    @staticmethod
    def runPiInPiesTest(self):
        print '\n', '*' * 50
        print '*' * 16, ' Pi In Pies JSON Test ', '*' * 16
        print '*' * 50 
        results = []
        fish_list = []
        hostname_list = []
        fishes = ["fish1", "fish2", "fish3"]
        # Check if mapping is in top.json
        if 'mapping' in self.top_dict:
            # Get a list of  all fish in mapping
            tmp_dict = self.top_dict['mapping']
            if 'H' in tmp_dict:
                tmp_dict2 = tmp_dict['H']
                for fish in fishes:
                    if tmp_dict2[fish] == "NA":
                        print 'Not adding fish=' + tmp_dict2[fish] + ' to fish list'
                    else:
                        fish_list.append(tmp_dict2[fish])    
            else:
                print self.me + ': Error> H is not in top_dict, issue with top.json' 
                print self.me + ': Exiting...'
                sys.exit(1)   
            if 'L' in tmp_dict:
                tmp_dict2 = tmp_dict['L']
                for fish in fishes:
                    if tmp_dict2[fish] == "NA":
                        print 'Not adding fish=' + tmp_dict2[fish] + ' to fish list'
                    else:
                        fish_list.append(tmp_dict2[fish])    
            else:
                print self.me + ': Error> L is not in top_dict, issue with top.json' 
                print self.me + ': Exiting...'
                sys.exit(1)                               
        else:
            print self.me + ': Error> Mapping is not in top_dict, issue with top.json'
            print self.me + ': Exiting...'
            sys.exit(1) 
        
        # Gather list of all hostnames (node and camera node per fish)
        for fish in fish_list:
            if fish in self.fish_dict:
                tmp_dict2 = self.fish_dict[fish]
                hostname_list.append(tmp_dict2['node'])
                hostname_list.append(tmp_dict2['cam_node'])
            else:
                print self.me + ': Error> ' + fish + ' is not in fish_dict, issue with fish.json, make sure fish is in fish.json'
                print self.me + ': Exiting...'
                sys.exit(1) 
        
        for hostname in hostname_list:
            return_code = self.isPiInPiesJson(self, hostname)
            if(return_code == 0):
                result = True
            else:
                result = False
            print self.me + ': Is ' + str(hostname) + ' in pies.json? ' + str(result)
            results.append(result)
                
        # Check if any hostnames are repeated
        #TODO: Add check if hostname is repeated in pies.json
                
        if False in results:
            print '\nPi in Pies JSON Test Result: FAIL'           
            print '*' * 50        
            return False
        print '\nPi in Pies JSON Test Result: PASS'         
        print '*' * 50
        return True
            
    @staticmethod
    def runPiPingerTest(self):
        print '\n', '*' * 50
        print '*' * 16, ' Pi Pinger Test ', '*' * 16
        print '*' * 50 
        results = []
        fish_list = []
        hostname_list = []
        fishes = ["fish1", "fish2", "fish3"]
        # Check if mapping is in top.json
        if 'mapping' in self.top_dict:
            # Get a list of  all fish in mapping
            tmp_dict = self.top_dict['mapping']
            if 'H' in tmp_dict:
                tmp_dict2 = tmp_dict['H']
                for fish in fishes:
                    if tmp_dict2[fish] == "NA":
                        print 'Not adding fish=' + tmp_dict2[fish] + ' to fish list'
                    else:
                        fish_list.append(tmp_dict2[fish])    
            else:
                print self.me + ': Error> H is not in top_dict, issue with top.json' 
                print self.me + ': Exiting...'
                sys.exit(1)   
            if 'L' in tmp_dict:
                tmp_dict2 = tmp_dict['L']
                for fish in fishes:
                    if tmp_dict2[fish] == "NA":
                        print 'Not adding fish=' + tmp_dict2[fish] + ' to fish list'
                    else:
                        fish_list.append(tmp_dict2[fish])    
            else:
                print self.me + ': Error> L is not in top_dict, issue with top.json' 
                print self.me + ': Exiting...'
                sys.exit(1)                               
        else:
            print self.me + ': Error> Mapping is not in top_dict, issue with top.json'
            print self.me + ': Exiting...'
            sys.exit(1) 
        
        # Gather list of all hostnames (node and camera node per fish)
        print 'fish_list=' + str(fish_list)
        print '/n/nfish_dict=' + str(self.fish_dict)
        for fish in fish_list:
            if fish in self.fish_dict:
                tmp_dict2 = self.fish_dict[fish]
                hostname_list.append(tmp_dict2['node'])
                hostname_list.append(tmp_dict2['cam_node'])
            else:
                print self.me + ': Error> ' + fish + ' is not in fish_dict, issue with fish.json, make sure fish is in fish.json'
                print self.me + ': Exiting...'
                sys.exit(1) 
        
        for hostname in hostname_list:
            return_code = respondsToPing(hostname)
            if(return_code == 0):
                result = True
            else:
                result = False
            print self.me + ': Did ' + str(hostname) + ' respond to a ping? ' + str(result)
            results.append(result)
                
        # Check if any hostnames are repeated
        tmp = [len(list(group)) for key, group in groupby(hostname_list)]
        if (all(i == 1 for i in tmp)):
            print self.me + ': All hostnames are assigned to only 1 Pi'
            results.append(True)
        else:
            print self.me + ': ERROR> One or more hostnames are assigned to multiple Pis'
            results.append(False)
                
        if False in results:
            print '\nPi Pinger Test Result: FAIL'           
            print '*' * 50        
            return False
        print '\nPi Pinger Test Result: PASS'         
        print '*' * 50
        return True
        
    @staticmethod
    def runIsFishValidTest(self):
        print '\n', '*' * 50
        print '*' * 14, ' Fish Validity Test ', '*' * 14
        print '*' * 50 
        results = []
        fish_list = []
        fishes = ["fish1", "fish2", "fish3"]
        # Check if mapping is in top.json            
        if 'mapping' in self.top_dict:
            # Get a list of  all fish in mapping
            tmp_dict = self.top_dict['mapping']
            if 'H' in tmp_dict:
                tmp_dict2 = tmp_dict['H']
                for fish in fishes:
                    if tmp_dict2[fish] == "NA":
                        results.append(True)
                        print 'Not adding fish=' + tmp_dict2[fish] + ' to fish list'
                    else:
                        results.append(self.isFishInFishJson(self, tmp_dict2[fish]))
                        fish_list.append(tmp_dict2[fish])    
            else:
                print self.me + ': Error> H is not in top_dict, issue with top.json' 
                print self.me + ': Exiting...'
                sys.exit(1)   
            if 'L' in tmp_dict:
                tmp_dict2 = tmp_dict['L']
                for fish in fishes:
                    if tmp_dict2[fish] == "NA":
                        results.append(True)
                        print 'Not adding fish=' + tmp_dict2[fish] + ' to fish list'
                    else:
                        results.append(self.isFishInFishJson(self, tmp_dict2[fish]))
                        fish_list.append(tmp_dict2[fish])    
            else:
                print self.me + ': Error> L is not in top_dict, issue with top.json' 
                print self.me + ': Exiting...'
                sys.exit(1)                               
        else:
            print self.me + ': Error> Mapping is not in top_dict, issue with top.json'
            print self.me + ': Exiting...'
            sys.exit(1) 
        
        # Check if any fish are assigned to more than 1 schedule
        tmp = [len(list(group)) for key, group in groupby(fish_list)]
        if (all(i == 1 for i in tmp)):
            print self.me + ': All fish are assigned to only 1 schedule'
            results.append(True)
        else:
            print self.me + ': ERROR> One or more fish are assigned to multiple schedules'
            results.append(False)
        
        if False in results:
            print '\nFish Validity Test Result: FAIL'           
            print '*' * 50        
            return False
        print '\nFish Validity Test Result: PASS'         
        print '*' * 50
        return True
    
    @staticmethod
    def runIsDateValidTest(self):
        DAYS_LIMIT = 30
        print '\n', '*' * 50
        print '*' * 14, ' Date Validity Test ', '*' * 14
        print '*' * 50 
        results = []
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # Check if start date is in top.json
        if 'startDate' in self.top_dict:
            # Get today's date
            now = datetime.datetime.now()
            now_month = now.month
            now_day = now.day        
            print self.me + ': Current date/time is ' + str(now)
            start_date = self.top_dict['startDate'].split('/')
            start_month = int(start_date[0])
            start_day = int(start_date[1])
            # Check if start month is this month or next
            if now_month is not 12:
                print self.me + ': Is start month either this month or next? ' + str((start_month == now_month or start_month == now_month + 1))
                results.append(start_month == now_month or start_month == now_month + 1)
            else:
                print self.me + ': Is start month either this month or next? ' + str((start_month == 12 or start_month == 1))
                results.append(start_month == 12 or start_month == 1)
            # Check if within 30 days
            now_days = now_day
            for i in range(1,now_month):
                now_days = now_days + days_in_month[i-1]
            start_days = start_day
            for i in range(1,start_month):
                start_days = start_days + days_in_month[i-1]
            total_days = 0
            for i in range(1,13):
                total_days = total_days + days_in_month[i-1]
            result = False
            if now_days < total_days-30:
                result = (now_days <= start_days and start_days < now_days + DAYS_LIMIT)
            else:
                if(start_month == 12 and now_month == 12):
                    result = True
                else:
                    days_left = total_days - now_days
                    if days_left + start_days < DAYS_LIMIT:
                        result = True
            print self.me + ': Is start date within next 30 days? ' + str(result)
            results.append(result)                            
        else:
            print self.me + ': Error> Start date is not in top_dict, issue with top.json'
            print self.me + ': Exiting...'
            sys.exit(1) 
        
        if False in results:
            print '\nDate Validity Test Result: FAIL'           
            print '*' * 50        
            return False
        print '\nDate Validity Test Result: PASS'         
        print '*' * 50
        return True
        
    def runTests(self):                
        # Print out tests to run
        print '\n', '*' * 50
        print('Tests to run:')
        for test in self.test_list:
            print test
        print '*' * 50, '\n' 
        
        results = []
        
        # Test decode and launch
        for test in self.test_list:
            if test is 'fish_is_valid':
                results.append(self.runIsFishValidTest(self))
            elif test is 'date_is_valid':
                results.append(self.runIsDateValidTest(self))
            elif test is 'pi_pinger':
                results.append(self.runPiPingerTest(self))
            elif test is 'pi_in_pies_json':
                results.append(self.runPiInPiesTest(self))				
            else:
                print 'ERROR> ' + test + ' is NOT a valid test!'
            
        # Determine overall result
        if False in results:
            print '\nOverall Test Result: FAIL\n'          
            return False
        print '\nOverall Test Result: PASS\n' 
        return True
                
                    
if __name__ == '__main__':
    
    test = Tests()
    result = test.runTests()
    if result is False:
        print('Failed Validation!')
        print("Exiting with Error Code 1")
        print '*' * 50, '\n' 
        sys.exit(1)
    
    print('Passed Validation!')
    print("Exiting with Error Code 0")
    print '*' * 50, '\n' 
    sys.exit(0)
