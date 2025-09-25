import	re
import	json
from	typing							import List
from	time							import sleep
from	requests						import get as GET
from	requests						import post as POST
from	pygwarts.irma.contrib.intercept	import PoolHoist
from	pygwarts.magical.spells			import patronus
from	credistr						import tlg_bot_RMPMRMTECHBOT
from	credistr						import tlg_bot_RMPMRMGMDSSBOT
from	credistr						import tlg_channel_RMPMRMTECH
from	credistr						import tlg_channel_RMPMRMGMDSS
from	credistr						import tlg_channel_RMPMRMGMDSS
from	credistr						import link_overseer_announcer_receiver








class TelegramHoist(PoolHoist):
	def __call__(self):


		class Interceptor(super().__call__()):


			def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)

				if	isinstance(getattr(self, "watchdog", None), tuple):
					self.watchdog_map = { re.compile(P.replace("*",".*")) for P in self.watchdog }

			def warning(self, message :str):

				super().warning(message)
				self.buffer_insert(f"{self.handover_name} WARNING: {message}")

			def error(self, message :str):

				super().error(message)
				self.buffer_insert(f"{self.handover_name} ERROR: {message}")

			def critical(self, message :str):

				super().critical(message)
				self.buffer_insert(f"{self.handover_name} CRITICAL: {message}")


		return	Interceptor








class TelegramTechHoist(TelegramHoist):
	def __call__(self):


		class Interceptor(super().__call__()):
			def info(self, message :str):

				super().info(message)

				if	isinstance(getattr(self, "watchdog_map", None), set):
					for pattern in self.watchdog_map:

						if	isinstance(pattern, re.Pattern):
							if	pattern.fullmatch(self.handover_name):

								self.buffer_insert(f"{self.handover_name}: {message}")


			def buffer_release(self, *args, **kwargs) -> List[str] :


				buffer_dump = super().buffer_release(*args, **kwargs)
				dump_message = "\n".join(buffer_dump)
				delay = 0

				try:

					for i in range(0, len(dump_message), 4096):
						sleep(delay)

						GET(

							f"https://api.telegram.org/bot{tlg_bot_RMPMRMTECHBOT()}/sendMessage",
							{
								"chat_id":	tlg_channel_RMPMRMTECH(),
								"text":		dump_message[i:i+4096],
							}
						)

						delay += 1


				except	Exception as E : self.pool_debug(f"Buffer chunk {delay} failed due to {patronus(E)}")
				return	buffer_dump


		return	Interceptor








class TelegramOperatorHoist(TelegramHoist):
	def __call__(self):


		class Interceptor(super().__call__()):
			def buffer_release(self, *args, **kwargs) -> List[str] :


				buffer_dump = super().buffer_release(*args, **kwargs)
				dump_message = "\n".join(buffer_dump)
				delay = 0

				try:

					POST(

						link_overseer_announcer_receiver(),
						data=json.dumps({ "message": dump_message })
					)

				except	Exception as E : self.pool_debug(f"Overseer delivery failed due to {patronus(E)}")


				try:

					for i in range(0, len(dump_message), 4096):
						sleep(delay)

						GET(

							f"https://api.telegram.org/bot{tlg_bot_RMPMRMGMDSSBOT()}/sendMessage",
							{
								"chat_id":	tlg_channel_RMPMRMGMDSS(),
								"text":		dump_message[i:i+4096],
							}
						)

						delay += 1


				except	Exception as E : self.pool_debug(f"Buffer chunk {delay} failed due to {patronus(E)}")
				return	buffer_dump


		return	Interceptor







