from flask import Flask, request, redirect, Response
import twilio.twiml
import urllib2
import os.path
import flask
 
application = Flask(__name__)
#application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']
#app = Flask(__name__)
#TEMP_PATH="/tmp/"
# Try adding your own number to this list!
callers = {
    "+16825832250": "Mr Riby",
    "+14089871135": "Mr Bansal",
    "+13474817269": "Mr Sadhoo",
}
def pullData(stock):
	fileLine=stock+".txt"
	urltoget='http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1m/csv'
	data=urllib2.urlopen(urltoget)
	dblock=data.read().decode('utf-8')
	splitdblock=dblock.split('\n')
	
	for eachLine in splitdblock:
		splitLine=eachLine.split(',')
		if 'values' not in eachLine:
			saveFile=open(fileLine,'a')
			linetoWrite=eachLine+'\n'
			saveFile.write(linetoWrite)

def printData(stock):
	if(os.path.isfile(stock+".txt")==False):
		pullData(stock)
	f=open(stock+".txt",'r')
	l=f.readlines()
	
	last=l[-2]
	last=last.replace('\n','')
	last=last.split(',')
	#DATE,CLOSE,HIGH,LOW,OPEN,VOLUME
	msg="Last Close:"+last[1]+" High:"+last[2]+" Low:"+last[3]
	return msg

@application.route("/", methods=['GET', 'POST'])
def mob_con():
	"""Respond and greet the caller by name."""
	stock="AMD"
	req=request.values.get('Body',None).decode('utf-8')
	if "stock" in req:
		req=req.split()
		stock=req[1]
		stock=stock.upper()
	else:
		stock="GOOG"
	
		
	msg=printData(stock)
	#msg=str(stock)
	from_number = request.values.get('From', None)
	if from_number in callers:
		message = callers[from_number] + ", requested quotes!"+msg
	else:
		message = "Riby, thanks for the message!"+msg
	resp = twilio.twiml.Response()
	resp.message(message)
	return str(resp)

@application.route("/stock/<string:stock>", methods=['GET', 'POST'])
def web_con(stock):
	"""Respond and greet the caller by name."""
		
	msg=printData(stock)
	from_number = request.values.get('From', None)
	if from_number in callers:
		message = callers[from_number] + ", requested quotes!"+msg
	else:
		message = "Riby, thanks for the message!"+msg
	resp = twilio.twiml.Response()
	resp.message(message)
	return str(resp)
	
if __name__ == '__main__':
	application.run(host='0.0.0.0')
