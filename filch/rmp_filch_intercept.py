import	re
from	typing							import List
from	time							import sleep
from	requests						import get as GET
from	pygwarts.irma.contrib.intercept	import PoolHoist
from	pygwarts.magical.spells			import patronus
from	goperator_credistr				import gmdssA2mrmENGbot
from	goperator_credistr				import mrma2tech








class TelegramTechHoist(PoolHoist):
	def __call__(self):


		class Interceptor(super().__call__()):

			def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)

				if	isinstance(getattr(self, "watchdog", None), tuple):
					self.watchdog_map = { re.compile(P.replace("*",".*")) for P in self.watchdog }

			def warning(self, message :str):

				self.buffer_insert(f"{self.handover_name} WARNING: {message}")
				return super().warning(message)

			def error(self, message :str):

				self.buffer_insert(f"{self.handover_name} ERROR: {message}")
				return super().error(message)

			def critical(self, message :str):

				self.buffer_insert(f"{self.handover_name} CRITICAL: {message}")
				return super().critical(message)

			def buffer_release(self, *args, **kwargs) -> List[str] :

				buffer_dump = super().buffer_release(*args, **kwargs)
				dump_message = "\n".join(buffer_dump)
				delay = 0

				try:

					for i in range(0, len(dump_message), 4096):
						sleep(delay)

						GET(

							f"https://api.telegram.org/bot{gmdssA2mrmENGbot()}/sendMessage",
							{
								"chat_id":	mrma2tech(),
								"text":		dump_message[i:i+4096],
							}
						)

						delay += 1


				except	Exception as E : self.pool_debug(f"Buffer chunk {delay} failed due to {patronus(E)}")
				return	buffer_dump


		return	Interceptor








class BroadHoist(TelegramTechHoist):
	def __call__(self):


		class Interceptor(super().__call__()):
			def info(self, message :str):

				if	isinstance(getattr(self, "watchdog_map", None), set):
					for pattern in self.watchdog_map:

						if	isinstance(pattern, re.Pattern):
							if	pattern.fullmatch(self.handover_name):

								self.buffer_insert(f"broadwatch: {message}")

				return super().info(message)


		return	Interceptor








class DiscoveryHoist(TelegramTechHoist):
	def __call__(self):


		class Interceptor(super().__call__()):
			def info(self, message :str):

				if	isinstance(getattr(self, "watchdog_map", None), set):
					for pattern in self.watchdog_map:

						if	isinstance(pattern, re.Pattern):
							if	pattern.fullmatch(self.handover_name):

								self.buffer_insert(f"discoverywatch: {message}")

				return super().info(message)


		return	Interceptor








class SNMPHoist(TelegramTechHoist):
	def __call__(self):


		class Interceptor(super().__call__()):
			def info(self, message :str):

				if	isinstance(getattr(self, "watchdog_map", None), set):
					for pattern in self.watchdog_map:

						if	isinstance(pattern, re.Pattern):
							if	pattern.fullmatch(self.handover_name):

								self.buffer_insert(f"snmpwatch: {message}")

				return super().info(message)


		return	Interceptor







