import groovy.json.JsonSlurper

//**********************************************************************
// Define constants
//**********************************************************************
def DAYS2KEEP = 30
def NUM2KEEP = 100

//**********************************************************************
// Define parameters with default settings
//**********************************************************************
def ci_job_name_root = 'cleanup-job'
def fish = "Harlene"
def node = "master"
def cam_node = "master"
def this_node = "master"

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

//Read in top level parameters
f = new File('/var/lib/jenkins/workspace/dsl-seed-job/top.json')
jsonText = f.getText()
jsonTop = slurper.parseText(jsonText)
println("Top: \n" + jsonTop + "\n")
round = jsonTop."round"
println("round=" + round)
def startDate = jsonTop."startDate"
println("startDate=" + startDate)
String h1_fish = jsonTop."mapping"."H1"
println("h1_fish=" + h1_fish)
String h2_fish = jsonTop."mapping"."H2"
println("h2_fish=" + h2_fish)
String h3_fish = jsonTop."mapping"."H3"
println("h3_fish=" + h3_fish)
String l1_fish = jsonTop."mapping"."L1"
println("l1_fish=" + l1_fish)
String l2_fish = jsonTop."mapping"."L2"
println("l2_fish=" + l2_fish)
String l3_fish = jsonTop."mapping"."L3"
println("l3_fish=" + l3_fish + "\n")

//Loop through schedules
schedules = ["H1", "H2", "H3", "L1", "L2", "L3"]
for (schedule in schedules) {
	println("\n*****************" + schedule + " Schedule *****************")
	if (schedule == "H1") {
		fish = h1_fish
		json = jsonH1
	} else if (schedule == "H2") {
		fish = h2_fish
		json = jsonH2
	} else if (schedule == "H3") {
		fish = h3_fish
		json = jsonH3
	} else if (schedule == "L1") {
		fish = l1_fish
		json = jsonL1
	} else if (schedule == "L2") {
		fish = l2_fish
		json = jsonL2
	} else if (schedule == "L3") {
		fish = l3_fish
		json = jsonL3
	}
	if (fish != "null") {
		node = jsonFish.(fish.toString())."node"
		cam_node = jsonFish.(fish.toString())."cam_node"
		println("node=" + node)
		println("cam_node=" + cam_node)
		println("\n")
		//Loop over each schedule and create a CI job
		for (i = 0; i <2; i++) {
            if (i == 0) {
                this_node = node	      
			} else {
			    this_node = cam_node
			}
			println("\n#######################")
			println("Cleaning up " + this_node)
			println("#######################")
			
			//Build up job name, fish + trial #
			ci_job_name = ci_job_name_root + "_" + this_node
			
			//Create CI job
			createCiJob(ci_job_name, DAYS2KEEP, NUM2KEEP, this_node)
		}
	}	
	println("*******************************************************************")
}

//**********************************************************************
// Function creates CI job with specified parameters
//**********************************************************************
def createCiJob(def ci_job_name, def DAYS2KEEP, def NUM2KEEP, def this_node) {
	job(ci_job_name){
	  logRotator {
		daysToKeep(DAYS2KEEP)
		numToKeep(NUM2KEEP)
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
	  days_in_month_map.put("1", 31)
	  days_in_month_map.put("2", 28)
	  days_in_month_map.put("3", 31)
	  days_in_month_map.put("4", 30)
	  days_in_month_map.put("5", 31)
	  days_in_month_map.put("6", 30)
	  days_in_month_map.put("7", 31)
	  days_in_month_map.put("8", 31)
	  days_in_month_map.put("9", 30)
	  days_in_month_map.put("10", 31)
	  days_in_month_map.put("11", 30)
	  days_in_month_map.put("12", 31)

	  //Adjust day/month based on day parameter
	  //if(((day.toInteger()-1) + DOM.toInteger()) > days_in_month_map.(MONTH.toString())) {
		//if(MONTH != "12") {
			//MONTH =(MONTH.toInteger() + 1).toString()
		//} else {
			//MONTH = "1"
		//}
		//DOM = (((day.toInteger()-1) + DOM.toInteger()) - days_in_month_map.(MONTH.toString())).toString()
	  //} else {
		//DOM = (DOM.toInteger() + day.toInteger() - 1).toString()
	  //}
	  
	  //Trigger build based on startDate, date, and time parameters
	  //println("Triggering build on MONTH=" + MONTH + ", DAY=" + DOM + ", HOUR=" + HOUR + ", MINUTE=" + MINUTE)
	  //triggers {
				//timerTrigger{
							 //spec(MINUTE + " " + HOUR + " " + DOM + " " + MONTH + " *")
				//}
	  //}
	  
	  // run shell that deletes workspace
	  steps {			
		shell { "rm -rf $WORKSPACE/*"
		} //shell
	  } //steps
	} //job
} //createCiJob