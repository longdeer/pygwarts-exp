from typing									import Callable
from telnetlib								import Telnet
from pygwarts.magical.philosophers_stone	import Transmutable
from pygwarts.magical.spells				import patronus
from pygwarts.magical.spells				import flagrate
from pygwarts.filch.nettherin				import validate_ip4








class TelnetDialog(Transmutable):

	"""
		Application layer class, that represents dialog session via raw socket connection, by telnetlib
		standard library. Implements connection by __call__ the following way:
			1. accepts "target" positional argument, that must represents valid IP4 address. If "target"
		failed validation, no connection proceeding.
			2. creates Telnet object and opens connection to "target", using all keyword arguments,
		provided to __call__ (e.g. port, timeout).
			3. iterates over "dialog", that must be callables, which accepts Telnet object with opened
		connection, and must implement actual communication (e.g. run "read_until" and "write" methods
		of Telnet object). It is recommended to declare "dialog" callables as TelnetDialog members,
		so they will have access to mutable chain.
	"""

	def __call__(self, target :str, *dialog :Callable[[Telnet],None], **kwargs):

		self.host = validate_ip4(target)

		if	self.host is not None:

			with Telnet() as connection:

				try:

					connection.open(self.host, **kwargs)
					self.loggy.info(f"Connection to {self.host} established")
					for k,v in kwargs.items() : self.loggy.debug(f"Using {k}: {v}")


				except Exception as E:
					self.loggy.error(f"Connection to {self.host} failed due to {patronus(E)}")


				else:
					for i,context in enumerate(dialog):

						try:	context(connection)
						except	Exception as E : self.loggy.debug(f"Context {i} failed with {patronus(E)}")

				finally:

					connection.close()
					self.loggy.info(f"Connection to {self.host} closed")
		else:		self.loggy.info(f"Invalid host \"{target}\"")




	def push_bytes(self, session :Telnet, message :str | bytes) -> bool :

		"""
			Helper method to encode string "message" before writing to Telnet session. Accepts "message"
			as both string or bytes, converts it to bytes and adds telnet line termination \\r\\n symbols,
			if needed. Writes to Telnet session and returns True if succeed. Returns None in any other
			cases.
		"""

		match message:

			case str():		load = (f"{message}\r\n" if not message.endswith("\r\n") else message).encode()
			case bytes():	load = message + b"\r\n" if not message.decode().endswith("\r\n") else message
			case _:

				self.loggy.error(f"{self} message must be of type string or bytes, not {type(message)}")
				return


		try:	session.write(load)
		except	Exception as E : self.loggy.error(f"{self} failed to push with {patronus(E)}")
		else:

			self.loggy.debug(f"Pushed {len(load)} byte{flagrate(len(load))}")
			return True




	def fetch_bytes(self, session :Telnet, expect :str | bytes) -> str | None :

		"""
			Helper method that reads from Telnet connection "session" to "expect" bytes and returns it
			Helper method to encode string "expect" and read from Telnet session to that bytes. Accepts
			"expect" as both string or bytes, converts it to bytes and adds telnet line termination \\r\\n
			symbols, if needed. Reads from Telnet session to that bytes and returns it's string
			representation with line termination stripped, if succeed. Returns None in any other cases.
		"""

		match expect:

			case str():		load = (f"{expect}\r\n" if not expect.endswith("\r\n") else expect).encode()
			case bytes():	load = expect + b"\r\n" if not expect.decode().endswith("\r\n") else expect
			case _:

				self.loggy.error(f"{self} expect must be of type string or bytes, not {type(expect)}")
				return


		try:	buffer = session.read_until(load, timeout=5)
		except	Exception as E : self.loggy.error(f"{self} failed to fetch with {patronus(E)}")
		else:

			self.loggy.debug(f"Fetched {len(buffer)} byte{flagrate(len(buffer))}")
			return buffer.decode().rstrip("\r\n")







