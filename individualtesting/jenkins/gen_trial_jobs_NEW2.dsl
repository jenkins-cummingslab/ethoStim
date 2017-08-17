import groovy.json.JsonSlurper

//**********************************************************************
// Define constants
//**********************************************************************
def DAYS2KEEP = 30
def NUM2KEEP = 100
def TIMEOUT = 90

def NUM_DAYS = 11

//**********************************************************************
// Define parameters with default settings
//**********************************************************************
def ci_job_name_root = 'run-single-trial'
def fish = "Harlene"
def thatpistimulus = "0"
def pistimulus = "0.png"
def correctside = "B"
def day = "1"
def session = "1"
def feedside = "both"
def sex = "female"
def proportion = "0"
def species = "gambusia"
def fishstandardlength = "TBD"
def round = "7"
def camera = "FALSE"
def node = "master"
def cam_node = "master"
def which_node = "master"
def cwtime = "3.8"
def ccwtime = "3.8"
def copydelay = "0"

//**********************************************************************
//Read in json files
//**********************************************************************
println("Current dir: " + System.getProperty("user.dir") + "\n")

def slurper = new JsonSlurper()

//Read in H1 schedule
File f = new File('/var/lib/jenkins/workspace/dsl-seed-job/H1.json')
def jsonText = f.getText()
jsonH1 = slurper.parseText(jsonText)
println("H1 schedule: \n" + jsonH1 + "\n")

//Read in H2 schedule
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/H2.json')
jsonText = f.getText()
jsonH2 = slurper.parseText(jsonText)
println("H2 schedule: \n" + jsonH2 + "\n")

//Read in H3 schedule
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/H3.json')
jsonText = f.getText()
jsonH3 = slurper.parseText(jsonText)
println("H3 schedule: \n" + jsonH3 + "\n")

//Read in L1 schedule
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/L1.json')
jsonText = f.getText()
jsonL1 = slurper.parseText(jsonText)
println("L1 schedule: \n" + jsonL1 + "\n")

//Read in L2 schedule
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/L2.json')
jsonText = f.getText()
jsonL2 = slurper.parseText(jsonText)
println("L2 schedule: \n" + jsonL2 + "\n")

//Read in L3 schedule
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/L3.json')
jsonText = f.getText()
jsonL3 = slurper.parseText(jsonText)
println("L3 schedule: \n" + jsonL3 + "\n")

//Read in Fish specific parameters
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/fish.json')
jsonText = f.getText()
jsonFish = slurper.parseText(jsonText)
println("Fish: \n" + jsonFish + "\n")

//Read in Pies specific parameters
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/pies.json')
jsonText = f.getText()
jsonPies = slurper.parseText(jsonText)
println("Pies: \n" + jsonPies + "\n")

//Read in Record-only schedule specific parameters
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/R1.json')
jsonText = f.getText()
jsonR1 = slurper.parseText(jsonText)
println("Record-only schedule: \n" + jsonR1 + "\n")


//Read in top level parameters
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/top_NEW.json')
jsonText = f.getText()
jsonTop = slurper.parseText(jsonText)
println("Top: \n" + jsonTop + "\n")
round = jsonTop."round"
println("round=" + round)
def startDate = jsonTop."startDate"
println("startDate=" + startDate)
def h_schedule = jsonTop."h_schedule"
println("h_schedule=" + h_schedule)
def l_schedule = jsonTop."l_schedule"
println("l_schedule=" + l_schedule)
String hfish1 = jsonTop."mapping"."H"."fish1"
println("hfish1=" + hfish1)
String hfish2 = jsonTop."mapping"."H"."fish2"
println("hfish2=" + hfish2)
String hfish3 = jsonTop."mapping"."H"."fish3"
println("hfish3=" + hfish3)
String lfish1 = jsonTop."mapping"."L"."fish1"
println("lfish1=" + lfish1)
String lfish2 = jsonTop."mapping"."L"."fish2"
println("lfish2=" + lfish2)
String lfish3 = jsonTop."mapping"."L"."fish3"
println("lfish3=" + lfish3 + "\n")

//Loop through schedules
schedules = [h_schedule, l_schedule]
for (schedule in schedules) {
	println("\n*****************" + schedule + " Schedule *****************")
	if (schedule == "H1") {
		json = jsonH1
	} else if (schedule == "H2") {
		json = jsonH2
	} else if (schedule == "H3") {
		json = jsonH3
	} else if (schedule == "L1") {
		json = jsonL1
	} else if (schedule == "L2") {
		json = jsonL2
	} else if (schedule == "L3") {
		json = jsonL3
	}
	
	if (schedule == "H1" || schedule == "H2" || schedule == "H3") {
	   fishes = [hfish1, hfish2, hfish3]
	} else { // L1 or L2 or L3
	   fishes = [lfish1, lfish2, lfish3]
	}
	
    for (fish in fishes) {
	   println("\nFish: " + fish + ", schedule: " + schedule)
	   
    	if (fish != "null" && fish != "NA") {
    		fishstandardlength = jsonFish.(fish.toString())."fishstandardlength"
    		species = jsonFish.(fish.toString())."species"
    		sex = jsonFish.(fish.toString())."sex"
    		node = jsonFish.(fish.toString())."node"
    		cam_node = jsonFish.(fish.toString())."cam_node"
    		println("fish=" + fish)
    		println("sex=" + sex)
    		println("species=" + species)
    		println("fishstandardlength=" + fishstandardlength)
    		println("node=" + node)
    		println("cam_node=" + cam_node)
    		println("\n")
    		//Loop over each trial and create a CI job
    		for (item in json) {
    			println("\n#######################")
    			println("Trial #" + item.key)
    			println("#######################")
    			day = json.(item.key)."day"
    			time = json.(item.key)."time"
    			thatpistimulus = json.(item.key)."thatpistimulus"
    			pistimulus = json.(item.key)."pistimulus"
    			correctside = json.(item.key)."correctside"
    			session = json.(item.key)."session"
    			feedside = json.(item.key)."feedside"
    			proportion = json.(item.key)."proportion"
    			feed = json.(item.key)."feed"
    			camera = json.(item.key)."camera"
    			println("day=" + day)
    			println("time=" + time)
    			println("thatpistimulus=" + thatpistimulus)
    			println("pistimulus=" + pistimulus)
    			println("correctside=" + correctside)
    			println("session=" + session)
    			println("feedside=" + feedside)
    			println("proportion=" + proportion)
    			println("feed=" + feed)
    			println("camera=" + camera)
    
    			//Build up job name, fish + trial #
    			ci_job_name = ci_job_name_root + "_" + fish + "_" + item.key
    
    			//Decide between node with or without camera
    			if(camera == "TRUE") {
    				which_node = cam_node
    			} else {
    				which_node = node
    			}
    			println("node=" + which_node)
    
    			//Determine cw and ccw times
    			cwtime = jsonPies.(which_node.toString())."cwtime"
    			ccwtime = jsonPies.(which_node.toString())."ccwtime"
    			copydelay = jsonPies.(which_node.toString())."copydelay"
    			println("cwtime=" + cwtime)
    			println("ccwtime=" + ccwtime)
    			println("copydelay=" + copydelay)
    
    			//Create CI job
    			createCiJob(ci_job_name, DAYS2KEEP, NUM2KEEP, TIMEOUT, fish, thatpistimulus, pistimulus, \
    				correctside, day, session, feedside, sex, proportion, species, \
    				fishstandardlength, round, camera, which_node, startDate, cwtime, \
    				ccwtime, feed, copydelay, time)
    		}
    		
    		days = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    		for (d in days) {
    		    for (item in jsonR1) {
                   println("\n#######################")
                   println("Record Only (Day " + d + ", Record "  + item.key + ")")
                   println("#######################")               
                   ci_job_name = "run-record-only_" + fish + "_d" + d + "_r" + item.key
                   time = jsonR1.(item.key)."time"
                   fileExt = ".h264"
                   vidLen = "30"
                   id = item.key
                   
                   createRecordJob(ci_job_name, DAYS2KEEP, NUM2KEEP, TIMEOUT, fish, id, \
                                   round, cam_node, startDate, vidLen, fileExt, d, time)
                }
    		} 
    	} else {
    		println("Not creating jobs for fish=" + fish + ", schedule=" + schedule)
    	}
	}
	println("*****************End of " + schedule + " Schedule *****************")
}

//**********************************************************************
// Function creates CI job with specified parameters
//**********************************************************************
def createCiJob(def ci_job_name, def DAYS2KEEP, def NUM2KEEP, def TIMEOUT, def fish, \
                def thatpistimulus, def pistimulus, def correctside, \
                def day, def session, def feedside, def sex, def proportion, \
                def species, def fishstandardlength, def round, def camera, \
                def node, def startDate, def cwtime, def ccwtime, def feed, \
								def copydelay, def time) {
	job(ci_job_name){
	  logRotator {
		daysToKeep(DAYS2KEEP)
		numToKeep(NUM2KEEP)
	  }

	  wrappers {
		timeout {
		 absolute(TIMEOUT)
		}
	  }

	  //Container job runs on master, sub-job will be executed on NODE specified parameter
	  label("master")

	  //Spec syntax, similar to cron
	  //MINUTE 	Minutes within the hour (0–59)
	  //HOUR 	The hour of the day (0–23)
	  //DOM 	The day of the month (1–31)
	  //MONTH 	The month (1–12)
	  //DOW 	The day of the week (0–7) where 0 and 7 are Sunday.
	  def (HOUR, MINUTE) = time.tokenize( ':' )
	  def (MONTH, DOM) = startDate.tokenize( '/' )

	  //This mapping will be okay until Feb 2020
	  def days_in_month_map  = new HashMap<String,Integer>()
	  days_in_month_map.put("01", 31)
	  days_in_month_map.put("02", 28)
	  days_in_month_map.put("03", 31)
	  days_in_month_map.put("04", 30)
	  days_in_month_map.put("05", 31)
	  days_in_month_map.put("06", 30)
	  days_in_month_map.put("07", 31)
	  days_in_month_map.put("08", 31)
	  days_in_month_map.put("09", 30)
	  days_in_month_map.put("10", 31)
	  days_in_month_map.put("11", 30)
	  days_in_month_map.put("12", 31)

	  //Adjust day/month based on day parameter
	  if(((day.toInteger()-1) + DOM.toInteger()) > days_in_month_map.(MONTH.toString())) {
			orig_month = MONTH
			if(MONTH != "12") {
				if(MONTH == "9" || MONTH == "10" || MONTH == "11") {
					(MONTH.toInteger() + 1).toString()
				} else {
					MONTH = "0" + (MONTH.toInteger() + 1).toString()
				}
			} else {
				MONTH = "01"
			}
			temp1 = (day.toInteger() - 1) + DOM.toInteger()
			temp2 = days_in_month_map.(orig_month.toString())
			DOM = (temp1 - temp2).toString()
	  } else {
			DOM = (DOM.toInteger() + day.toInteger() - 1).toString()
	  }

	  starttime = HOUR + ":" + MINUTE

	  //Trigger build based on startDate, date, and time parameters
	  println("Triggering build on MONTH=" + MONTH + ", DAY=" + DOM + ", HOUR=" + HOUR + ", MINUTE=" + MINUTE)
	  triggers {
				timerTrigger{
							 spec(MINUTE + " " + HOUR + " " + DOM + " " + MONTH + " *")
				}
	  }

	  //Launch RunSingleTrial (calls trial.py) job with specified parameters
	  steps {
		triggerBuilder {
		  configs {
			  blockableBuildTriggerConfig {
				  projects("RunSingleTrial")
				  block {
					  buildStepFailureThreshold("FAILURE")
					  unstableThreshold("UNSTABLE")
					  failureThreshold("FAILURE")
				  } //block
				  configFactories {}
				  configs {
					  predefinedBuildParameters {
						properties("fish=" + fish +
								   "\nthatpistimulus=" + thatpistimulus +
								   "\npistimulus=" + pistimulus +
								   "\ncorrectside=" + correctside +
								   "\nday=" + day +
								   "\nsession=" + session +
								   "\nfeedside=" + feedside +
								   "\nsex=" + sex +
								   "\nproportion=" + proportion +
								   "\nspecies=" + species +
								   "\nfishstandardlength=" + fishstandardlength +
								   "\nround=" + round +
								   "\ncamera=" + camera +
								   "\nNODE=" + node +
								   "\ncwtime=" + cwtime +
								   "\nccwtime=" + ccwtime +
									 "\nfeed=" + feed +
									 "\nstarttime=" + starttime +
									 "\ncopydelay=" + copydelay)
					  }
				  } //configs
			  } //blockableBuildTriggerConfig
		  } //configs
		}  //triggerBuilder
	  } //steps
	} //job
} //createCiJob

//**********************************************************************
// Function creates CI job with specified parameters
//**********************************************************************
def createRecordJob(def ci_job_name, def DAYS2KEEP, def NUM2KEEP, def TIMEOUT, def fish, \
                def id, def round, def node, def startDate, def vidLen, def fileExt, \
                def day, def time) {
	job(ci_job_name){
	  logRotator {
		daysToKeep(DAYS2KEEP)
		numToKeep(NUM2KEEP)
	  }

	  wrappers {
		timeout {
		 absolute(TIMEOUT)
		}
	  }

	  //Container job runs on master, sub-job will be executed on NODE specified parameter
	  label("master")

	  //Spec syntax, similar to cron
	  //MINUTE 	Minutes within the hour (0–59)
	  //HOUR 	The hour of the day (0–23)
	  //DOM 	The day of the month (1–31)
	  //MONTH 	The month (1–12)
	  //DOW 	The day of the week (0–7) where 0 and 7 are Sunday.
	  def (HOUR, MINUTE) = time.tokenize( ':' )
	  def (MONTH, DOM) = startDate.tokenize( '/' )

	  //This mapping will be okay until Feb 2020
	  def days_in_month_map  = new HashMap<String,Integer>()
	  days_in_month_map.put("01", 31)
	  days_in_month_map.put("02", 28)
	  days_in_month_map.put("03", 31)
	  days_in_month_map.put("04", 30)
	  days_in_month_map.put("05", 31)
	  days_in_month_map.put("06", 30)
	  days_in_month_map.put("07", 31)
	  days_in_month_map.put("08", 31)
	  days_in_month_map.put("09", 30)
	  days_in_month_map.put("10", 31)
	  days_in_month_map.put("11", 30)
	  days_in_month_map.put("12", 31)

	  //Adjust day/month based on day parameter
	  if(((day.toInteger()-1) + DOM.toInteger()) > days_in_month_map.(MONTH.toString())) {
			orig_month = MONTH
			if(MONTH != "12") {
				if(MONTH == "9" || MONTH == "10" || MONTH == "11") {
					(MONTH.toInteger() + 1).toString()
				} else {
					MONTH = "0" + (MONTH.toInteger() + 1).toString()
				}
			} else {
				MONTH = "01"
			}
			temp1 = (day.toInteger() - 1) + DOM.toInteger()
			temp2 = days_in_month_map.(orig_month.toString())
			DOM = (temp1 - temp2).toString()
	  } else {
			DOM = (DOM.toInteger() + day.toInteger() - 1).toString()
	  }

	  starttime = HOUR + ":" + MINUTE

	  //Trigger build based on startDate, date, and time parameters
	  println("Triggering build on MONTH=" + MONTH + ", DAY=" + DOM + ", HOUR=" + HOUR + ", MINUTE=" + MINUTE)
	  triggers {
				timerTrigger{
							 spec(MINUTE + " " + HOUR + " " + DOM + " " + MONTH + " *")
				}
	  }

	  //Launch RunRecordOnly (calls record_only.py) job with specified parameters
	  steps {
		triggerBuilder {
		  configs {
			  blockableBuildTriggerConfig {
				  projects("RunRecordOnly")
				  block {
					  buildStepFailureThreshold("FAILURE")
					  unstableThreshold("UNSTABLE")
					  failureThreshold("FAILURE")
				  } //block
				  configFactories {}
				  configs {
					  predefinedBuildParameters {
						properties("fish=" + fish +
								   "\nid=" + id +
								   "\nround=" + round +
								   "\nvid_len_secs=" + vidLen +
								   "\nNODE=" + node +
								   "\nfile_ext=" + fileExt)
					  }
				  } //configs
			  } //blockableBuildTriggerConfig
		  } //configs
		}  //triggerBuilder
	  } //steps
	} //job
} //createRecordJob
