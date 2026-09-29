import query_gptj
import csv

#gets standard deviation
def stDev(probList):
    n = len(probList)
    preSum = 0.0
    pTotal = 0.0
    pAverage = 0.0
    
    for val in probList:
        pTotal += float(val)

    pAverage = pTotal/n
    
    for val in probList:
        preSum += ((float(val) - pAverage)*(float(val) - pAverage))
        
    return (preSum/n)**(1/2)
    
     
#this list will eventually be used to host all the old and new data for each prompt 
result_list = []

#dictionaries to accumulate as the most likely major for each prompt
stats = {"b/w":{"Criminal Justice":0,"Studio Art":0,"Computer Science":0,"Political Science":0,"Biochemistry":0,"Art History":0},"w/w":{"Criminal Justice":0,"Studio Art":0,"Computer Science":0,"Political Science":0,"Biochemistry":0,"Art History":0}, "b/m":{"Criminal Justice":0,"Studio Art":0,"Computer Science":0,"Political Science":0,"Biochemistry":0,"Art History":0}, "w/m":{"Criminal Justice":0,"Studio Art":0,"Computer Science":0,"Political Science":0,"Biochemistry":0,"Art History":0},"Neutral":{"Criminal Justice":0,"Studio Art":0,"Computer Science":0,"Political Science":0,"Biochemistry":0,"Art History":0}}

#read from original file
with open("Homework 10 - Sheet1.tsv") as f:
    input_file = csv.reader(f, delimiter="\t")
    
    for line in input_file:
        
        #get top five results for each prompt (1 prompt = 1 line)
        #line = [set #, letter, text, category]
        topResult = query_gptj.word_query(line[2],"Criminal Justice;Studio Art;Computer Science;Political Science;Biochemistry;Art History")
        
        #for calculations
        valList = []
        
        #append topResult tuple
        for key in topResult:
            line.append(topResult[key])
            valList.append(topResult[key])
        
        #adding the standard deviation for each prompt to the sheet
        line.append(stDev(valList))
        
        #gets the major with the highest probabiliy and accumulates value to relevant cat
        topMajor = max(topResult, key=topResult.get)
        currentCat = line[3]
        stats[currentCat][topMajor]+=1
        
        
        
        
        #line.append(topResult[1])
        result_list.append(line)
        

#writing results and original information to new csv file
with open("results.csv", "w") as rF:
    myWriter = csv.writer(rF)
    myWriter.writerow(["Set #","Letter","Text", "Category","Criminal Justice","Studio Art","Computer Science","Political Science","Biochemistry","Art History","Standard Dev"])
    for result in result_list:
        myWriter.writerow(result)
    
    myWriter.writerow([])
    
    #begines to write stats concerning how many times a major is the most likely to be assigned to a category for each prompt
    myWriter.writerow(["Stats"])
    for key in stats:
        print(type(key))
        myWriter.writerow(["","","", key, stats[key]["Criminal Justice"], stats[key]["Studio Art"], stats[key]["Computer Science"], stats[key]["Political Science"], stats[key]["Biochemistry"], stats[key]["Art History"]])

