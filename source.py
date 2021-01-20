import http.server
import socketserver
import datetime
import pandas
import pytz
import json
import tzlocal

class HandleRequests(http.server.BaseHTTPRequestHandler):
	def set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()


	def do_GET(self):
		self.set_headers()

		tz = self.path[1:]
		if not tz:
			tz = None
		else:
			try:
				tz = pytz.timezone(tz)
			except pytz.exceptions.UnknownTimeZoneError:
				respond = (bytes('Unknown timezone', 'utf-8'))
				self.wfile.write(respond)
				return respond

		respond = bytes('Time is {0}'.format(datetime.datetime.now(tz)), 'utf-8')
		self.wfile.write(respond)
		return respond
		

	def do_POST(self):		
		self.set_headers()
		data = self.rfile.read(int(self.headers['Content-Length']))
		try:
			data = json.loads(data)
		except json.JSONDecodeError:
			respond = 'Error in json format'
			self.wfile.write(bytes(respond, 'utf-8'))
			return respond

		if (data['type'] == 'time'):
			try:
				tz = pytz.timezone(data['tz'])
			except KeyError:
				tz = None
			if not tz:
				tz = tzlocal.get_localzone()
			respond = json.dumps({'tz': str(tz), 'time': datetime.datetime.now(tz).time().isoformat()})

		elif (data['type'] == 'date'):
			try:
				tz = pytz.timezone(data['tz'])
			except KeyError:
				tz = None
			if not tz:
				tz = tzlocal.get_localzone()
			respond = json.dumps({'tz': str(tz), 'date': datetime.datetime.now(tz = tz).date().isoformat()})
				
		elif (data['type'] == 'datediff'):
			try:
				tz_start = pytz.timezone(data['start']['tz'])
			except KeyError:
				tz_start = None
			if not tz_start:
				tz_start = tzlocal.get_localzone()
			
			try:
				tz_end = pytz.timezone(data['end']['tz'])
			except KeyError:
				tz_end = None
			if not tz_end:
				tz_end = tzlocal.get_localzone()
			
			time_start = data['start']['date']
			time_end = data['end']['date']
			
			time_start = pandas.to_datetime(time_start)
			time_end = pandas.to_datetime(time_end)
			# высчитываем разницу между часовыми поясами
			time_offset = abs(tz_start.localize(time_start) - tz_end.localize(time_start).astimezone(tz_start)).seconds/3600 
			
			# высчитываем delta для исходного времени каждой из дат без разницы часовых поясов 
			delta = (abs(time_start - time_end) - datetime.timedelta(hours = time_offset)).to_pytimedelta()		
			respond = json.dumps({'datediff': delta, 'tz1' : tz_start, 'start': time_start,  'tz2' : tz_end, 'end': time_end}, default=str)

		self.wfile.write(bytes(respond, 'utf-8'))
		return bytes(respond,'utf-8')

			
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(('', PORT), HandleRequests)

print('Serving HTTP on port', PORT)
httpd.serve_forever()
