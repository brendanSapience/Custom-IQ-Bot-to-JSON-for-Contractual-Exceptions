#######################################
#
# Nano Service CSV to Json
#
# Prerequisites:
# Install Python 3.7+ (make sure to add python to your PATH, the installer has an option for it)
#
#
########################################
DESCRIPTION = "CSV To Json Service"
VERSION = 0.1
#
#######################################
import json,os,csv,re
from flask import Flask,request,jsonify

def IsLineMainException(myline,regexp):
    match = re.search(regexp, myline)
    if(match):
        return True
    else:
        return False

def RemoveFirstPhrase(myarray,regexexp):
    FoundFirstPhrase = False
    #LineStartRegex = regexexp
    RawLinesWIthoutHeader = []
    for s in myarray:
        if(not FoundFirstPhrase):
            match = re.search(regexexp, s)
            if(match):
                FoundFirstPhrase = True
                RawLinesWIthoutHeader.append(s)
        else:
            RawLinesWIthoutHeader.append(s)
    return RawLinesWIthoutHeader

def RemoveLastPhrase(myarray,regexexp):

    #LineStartRegex = regexexp
    RelevantLines = []
    for s in myarray:
        match = re.search(regexexp, s)
        if(match):
            RelevantLines.append(s)
    return RelevantLines


def ReformatBrokenLines(myarray,regexp):
    #idx = 0
    Lines = []
    for s in myarray:
        #print("Debug: "+s)
        match = re.search(regexp, s)
        #print("processing:"+s)
        if(match):
            #print("MATCH")
            Lines.append(s)
            #idx=idx+1

        if(not match):
            #print("NO MATCH")
            #print ("Lines[-1] Before:"+Lines[-1])
            Lines[-1]=Lines[-1]+" "+s
            #print ("Lines[-1] After:"+Lines[-1])
            #idx=idx+1
    return Lines

def IsNumEven(num):
    if num % 2 == 0:
        return True
    else:
        return False


def DetectAndExtractLines(myarray,regexp):

    Lines = []
    for s in myarray:

        match = re.search(regexp, s)
        if(match):
            #print("Match found..")
            tokens = re.split(regexp, s)
            #print(tokens)
            #["4. Notes and 80A, being as follows: ", 'i. ', 'Fifty (50) Cooperative. ', 'ii. ', 'Public sewer line in southeast corner of parcel in question. ', 'iii. ', 'Easement for rodeo clown migration path across south half of quarter-section.']
            for i, token in enumerate(tokens):
                if(i>0):
                    if(not IsNumEven(i)):
                        myException = tokens[i]+tokens[i+1]
                        #print("Debug:"+myException)
                        Lines.append(myException)
                else:
                    Lines.append(tokens[i])

        if(not match):
            Lines.append(s)

    return Lines

def ConvertCsvToJson(inputcsvfile,columnNum):

    with open(inputcsvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        RawLines = []
        RawLinesWIthoutHeader = []
        ColumnNumber = columnNum
        for row in csv_reader:
            line = row[ColumnNumber]
            RawLines.append(line)

        #For Simple Exceptions, this is enough
        FilteredLines = RemoveFirstPhrase(RawLines,r"^\d+\.")

        ConsolidatedLines = ReformatBrokenLines(FilteredLines,r"^\d{1,3}\.|^[a-z]\)")
        SplitLines = DetectAndExtractLines(ConsolidatedLines,r"(i+\.[ ]+|iv\.|v\.|vi\.|vii\.|viii\.|ix.|x\.|xi\.|xii\.|xiii\.|xiv\.|xv\.|xvi\.|xvii\.|xviii\.|xix\.|xx\.)")
        FinalLines = SplitLines #RemoveLastPhrase(SplitLines,r"^\d\.|^[a-z]\)")
        #For medium Exceptions:

        FormattedOutput = []
        #check each line, if it starts with a number, check the next Done#if the next one is a number, add to list of subexception
        #etc
        MainExcPattern = r"^\d+\."
        for i, line in enumerate(FinalLines):
            if (IsLineMainException(line,MainExcPattern)):
                SubExceptions = []
                for f in FinalLines[i+1:]:
                    if(not IsLineMainException(f,MainExcPattern)):
                        SubExceptions.append(f)
                    else:
                        break

                #print(SubExceptions)

                FormattedOutput.append({"exception":line,"subexceptions":SubExceptions})




        JSON = {
        "exceptions":FormattedOutput
        }
        return jsonify(JSON)



app = Flask(__name__)
app.secret_key = 'Oh what a big secret this is!!'

# Done, returns the list of folders under the IQ Bot output folder (List of Learning Instances)
@app.route('/convert', methods = ['GET', 'POST'])
def ConvertCall ():
    content = request.get_json()
    if 'input_file' not in content:
        return jsonify({"Status" : "Error","Message":"Missing input_file parameter"})
    if 'exception_column' not in content:
        return jsonify({"Status" : "Error","Message":"Missing exception_column parameter"})

    InputFile = content['input_file']
    ColumnNumber = content['exception_column']
    JsonOutput = ConvertCsvToJson(InputFile,ColumnNumber)
    return JsonOutput
