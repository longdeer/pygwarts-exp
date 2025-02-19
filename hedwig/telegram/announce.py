from time		import sleep
from requests	import get	as GET
from requests	import Response








class ChannelAnnouncer:

	def __init__(self, token :str, channel_id :str):

		self.TOKEN		= token
		self.CHANNEL	= channel_id









	# def print_check(self):

	# 	if hasattr(self.caller.loggy, "dispatch"):

	# 		print(self.caller.loggy.dispatch.strip())
	# 	else:
	# 		print(f"No dispatch for {self.caller}")









	def _post(self, message :str) -> Response :

		return GET(

			f"https://api.telegram.org/bot{self.TOKEN}/sendMessage",
			{
				"chat_id":	self.CHANNEL,
				"text":		message,
			}
		)


		# if response.status_code == 200:

		# 	if self.caller:	self.caller.loggy.info(f"Posted {len(message)} symbols")
		# 	else:			print(f"Posted {len(message)} symbols")
		# else:
		# 	if self.caller:	self.caller.loggy.warning(f"Response: \"{response.text}\"")
		# 	else:			print(f"Response: \"{response.text}\"")




	def from_string(self, message :str) -> [ Response, ] :

		delay = 1
		responses = list()

		for i in range(0, len(message), 4096):
				
			responses.append(self._post(message[i:i+4096]))
			sleep(delay)
			delay += 1


		return responses




	def as_nlset(self, message :str) -> [ Response, ] :

		_message = set( NL for NL in message.split("\n") if NL )
		return self.from_string("\n".join(_message))








	def sumneg(self, responses :[ Response, ]) -> str or None :

		"""
			Summarizes the list of messages of Response object's which code are not 200.
			Return string with number of responses, every response number in order they appear,
			code and message, or None if every code is 200.
		"""

		summary = str()


		for I,response in enumerate(responses):
			if (code := response.status_code) != 200 : summary += f"{I}-{code} : {response.text}\n"


		if len(summary) : return "%s responses:\n %s" % (len(responses), summary.rstrip("\n"))




	def sumpos(self, responses :[ Response, ]) -> str or None :

		"""
			Summarizes the list of messages of Response object's which code are exactly 200.
			Return string with number of responses and every response number in order they appear,
			or None if there no 200 code responses.
		"""

		summary = ", ".join( I for I,R in responses if R.status_code == 200 )
		if len(summary) : return f"{len(responses)} 200 responses: {summary}"







	# def from_dispatch(self) -> str or None :

	# 	if hasattr(self.caller.loggy, "dispatch"):

	# 		message = self.caller.loggy.dispatch
	# 		if message: return self.from_string(message)




	# def from_buffer(self) -> str or None :

	# 	if hasattr(self.caller.loggy, "buffer"):

	# 		# As buffer is not sanitized by WATHCDOG, it is shrinked to unique messages
	# 		message = self.caller.loggy.buffer
	# 		message = set(( M for M in message.split("\n\n") if M ))
	# 		message = "\n\n".join(message)


	# 		if message: return self.from_string(message)







