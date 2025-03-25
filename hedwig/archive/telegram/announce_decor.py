from time												import sleep
from typing												import Any
from typing												import Callable
from requests											import Response
from requests											import get		as GET
from pygwarts.magical.philosophers_stone				import Transmutable
from pygwarts.magical.philosophers_stone.transmutations	import ControlledTransmutation








class Announcer(ControlledTransmutation):

	"""
		Accepts bot token and chats to announce to
	"""

	def nlsetneg(self, wrapped_layer : Transmutable) -> Callable :

		"""
			Process message as new line separated set to remove duplicate
			Returning value is negatives responses summary
		"""

		self.current_preproc = lambda query : "\n".join(set( NL for NL in query.split("\n") if NL ))
		self.current_posproc = self.sum_negative_responses


		return self.__call__(wrapped_layer)


	def strneg(self, wrapped_layer : Transmutable) -> Callable :

		"""
			Process message as it is
			Returning value is negatives responses summary
		"""

		self.current_posproc = self.sum_negative_responses
		return self.__call__(wrapped_layer)




	def __init__(self, token :str, *chats :str):

		assert type(token)	== str,						f"Token must be type string, got {type(token)}"
		assert len(chats)	>= 1,						"At least one chat id must be provided"
		assert all( type(C)	== str for C in chats ),	"Chats id must be strings"


		self.TOKEN		= token
		self.CHATS		= chats


	def __call__(self, chained_layer :Transmutable) -> Callable[[Transmutable],Transmutable] :

		chained = super().__call__(chained_layer)
		token	= self.TOKEN
		chats	= self.CHATS
		handler	= self.current_handler if hasattr(self, "current_handler") else self.send_string
		preproc	= self.current_preproc if hasattr(self, "current_preproc") else lambda query : str(query)
		posproc	= self.current_posproc if hasattr(self, "current_posproc") else lambda total : str(total)




		def transmutation(upper_layer :Transmutable) -> Transmutable :
			class Transmute(chained(upper_layer)):

				def deliver(self, query :str) -> Any :

					"""
						Any "hanlder" must implement such interface, that it will return
						a list of Response objects.
					"""

					current = list()
					message = preproc(query)


					for chat_id in chats : current.extend(handler(message, chat_id))


					return	posproc(current)
			return	Transmute




		# Completing controlled transmutation
		transmutation._CHAIN_OVER_HOOK = True
		self._CHAIN_LAYER_HOOK = transmutation


		return	transmutation








	def sum_negative_responses(self, responses :[ Response, ]) -> str or None :

		"""
			Summarizes the list of messages of Response object's which code are not 200.
			Return string with number of responses, every response number in order they appear,
			code and message, or None if every code is 200.

			It is assumed, that "handler" will produce list of Response objects!
		"""

		summary = str()


		for i,response in enumerate(responses):

			if (code := response.status_code) != 200 :
				summary += f"{i}-{code} : {response.text}\n"


		if len(summary):

			return "out of %s responses:\n%s" % (len(responses), summary.rstrip("\n"))




	def sum_positive_responses(self, responses :[ Response, ]) -> str | None :

		"""
			Summarizes the list of messages of Response object's which code are exactly 200.
			Return string with number of responses and every response number in order they appear,
			or None if there no 200 code responses.

			It is assumed, that "handler" will produce list of Response objects!
		"""

		summary = str()


		for i,response in enumerate(responses):

			if (code := response.status_code) == 200 :
				summary += f"{i}-{code} : {response.text}\n"


		if len(summary):

			return "out of %s responses:\n%s" % (len(responses), summary.rstrip("\n"))








	def send_string(	self,
						message			:str,
						chat_id			:str,
					)->	[ Response, ]	:

		"""
			Apply string slicing to produce legit message portions for sending via HTTP API

			Current implementation is a simple predelay
		"""

		delay = 1
		responses = list()


		for i in range(0, len(message), 4096):

			sleep(delay); delay += 1
			responses.append(

				GET(

					f"https://api.telegram.org/bot{self.TOKEN}/sendMessage",
					{
						"chat_id":	chat_id,
						"text":		message[i:i+4096],
					}
				)
			)


		return responses







