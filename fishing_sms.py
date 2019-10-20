from twilio.rest import Client
from lxml import html
import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os

account_sid = os.environ['Twilio_Account_SID']
auth_token = os.environ['Twilio_Auth_Token']
client = Client(account_sid, auth_token)
client.messages.create(
	to=os.environ['MY_PHONE_NUMBER'],
	from_=os.environ['Twilio_Phone_Number'],
	body="Reply with 1 through 3 for the following river flow rates:\n1: Milwuakee River\n2: Black Earth Creek\n3: Root River")


app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
	body = request.values.get('Body', None)

	resp = MessagingResponse()

	if body == '1':
		page1 = requests.get('https://waterdata.usgs.gov/nwis/uv?04087000')
		tree1 = html.fromstring(page1.content)
		flow1 = tree1.xpath('//td[@class="highlight2"]/text()')
		out1 = "Current Flow Milwuakee River (ft^3/s): " + flow1[0]
		resp.message(out1)
	elif body == '2':
		page2 = requests.get('https://waterdata.usgs.gov/nwis/uv?05406500')
		tree2 = html.fromstring(page2.content)
		flow2 = tree2.xpath('//td[@class="highlight2"]/text()')
		out2 = "Current Flow Black Earth Creek (ft^3/s): " + flow2[0]
		resp.message(out2)
	elif body == '3':
		page3 = requests.get('https://waterdata.usgs.gov/nwis/uv?04087240')
		tree3 = html.fromstring(page3.content)
		flow3 = tree3.xpath('//td[@class="highlight2"]/text()')
		out3 = "Current Flow Root River (ft^3/s): " + flow3[0]
		resp.message(out3)
	else:
		resp.message("Unknown request")

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)