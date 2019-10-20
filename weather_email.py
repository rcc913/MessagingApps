from lxml import html
import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

page = requests.get('https://weather.com/weather/today/l/578c23d55e0637e109570d3f6e83ff9ebec6fd69a4e88877fcf6969c27706545')
tree = html.fromstring(page.content)
weather_now = tree.xpath('//div[@class="today_nowcard-temp"]')[0]
nowtemp = weather_now.xpath('.//span/text()')
weather_highlo = tree.xpath('//span[@class="deg-hilo-nowcard"]')
high = weather_highlo[0].xpath('.//span/text()')
low = weather_highlo[1].xpath('.//span/text()')
out1 = "<p>~Madison, WI Weather~</p><p>Currently: " + nowtemp[0] + "F</p>"
out2 = "<p>High for today: " + high[0] + "F</p>" + "<p>Low for today: " + low[0] + "F</p>"

message = Mail(from_email='weather@weathernow.com',
				to_emails=os.environ['MY_EMAIL'],
				subject='Daily Wether for Madison',
				html_content=out1 + out2)
try:
	client = SendGridAPIClient(os.environ['SendGrid_API'])
	weatherout = client.send(message)
	
except Exception as e:
	print(e.message)




