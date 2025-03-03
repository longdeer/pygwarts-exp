import	os
import	unittest
import	socket
from	typing								import Any
from	telnetlib							import Telnet
from	threading							import Thread
from	pygwarts.tests.filch				import FilchTestCase
from	pygwarts.irma.contrib				import LibraryContrib
from	pygwarts.filch.apppuf.telnet		import TelnetDialog








class ApppufCase(FilchTestCase):

	"""
		Testing L5 instruments
	"""

	@classmethod
	def tearDownClass(cls):

		if	cls.clean_up:
			if	os.path.isfile(cls.APPPUF_HANDLER): os.remove(cls.APPPUF_HANDLER)

	@classmethod
	def setUpClass(cls): cls.make_loggy_file(cls, cls.APPPUF_HANDLER)
	def test_TelnetDialog_push_bytes(self):
		class Mock:

			def __init__(self): self.pushed = []
			def write(self, load :Any): self.pushed.append(load)

		class TelnetTest(TelnetDialog):
			class loggy(LibraryContrib):

				handler		= self.APPPUF_HANDLER
				init_name	= "TelnetDialog_push_bytes"
				init_level	= 10

		self.test_case = TelnetTest()
		mock = Mock()

		with self.assertLogs("TelnetDialog_push_bytes", 10) as case_loggy:

			self.assertTrue(self.test_case.push_bytes(mock, "LOAD"))
			self.assertTrue(self.test_case.push_bytes(mock, "LOAD\r"))
			self.assertTrue(self.test_case.push_bytes(mock, "LOAD\n"))
			self.assertTrue(self.test_case.push_bytes(mock, "LOAD\r\n"))
			self.assertTrue(self.test_case.push_bytes(mock, b"LOAD"))
			self.assertTrue(self.test_case.push_bytes(mock, b"LOAD\r"))
			self.assertTrue(self.test_case.push_bytes(mock, b"LOAD\n"))
			self.assertTrue(self.test_case.push_bytes(mock, b"LOAD\r\n"))

		self.assertIn("DEBUG:TelnetDialog_push_bytes:Pushed 6 bytes", case_loggy.output)
		self.assertIn("DEBUG:TelnetDialog_push_bytes:Pushed 7 bytes", case_loggy.output)
		self.assertEqual(case_loggy.output.count("DEBUG:TelnetDialog_push_bytes:Pushed 6 bytes"),4)
		self.assertEqual(case_loggy.output.count("DEBUG:TelnetDialog_push_bytes:Pushed 7 bytes"),4)
		self.assertEqual(

			mock.pushed,
			[
				b"LOAD\r\n",
				b"LOAD\r\r\n",
				b"LOAD\n\r\n",
				b"LOAD\r\n",
				b"LOAD\r\n",
				b"LOAD\r\r\n",
				b"LOAD\n\r\n",
				b"LOAD\r\n"
			]
		)




	def test_TelnetDialog_push_bytes_invalid(self):

		class TelnetTest(TelnetDialog):
			class loggy(LibraryContrib):

				handler		= self.APPPUF_HANDLER
				init_name	= "TelnetDialog_push_bytes_invalid"
				init_level	= 10

		self.test_case = TelnetTest()
		for invalid in (

			42, 69., True, False, None, ..., unittest, LibraryContrib,
			[ "LOAD" ],( "LOAD", ),{ "LOAD" },{ "message": "LOAD" }
		):
			with (
				self.subTest(message=invalid),
				self.assertLogs("TelnetDialog_push_bytes_invalid", 10) as case_loggy
			):
				self.assertIsNone(self.test_case.push_bytes(None, invalid))
			self.assertIn(

				"ERROR:TelnetDialog_push_bytes_invalid:"
				f"{self.test_case} message must be of type string or bytes, not {type(invalid)}",
				case_loggy.output
			)




	def test_TelnetDialog_push_bytes_raise(self):

		class Mock:
			def write(self, load :Any): raise ValueError("Enough of this")

		class TelnetTest(TelnetDialog):
			class loggy(LibraryContrib):

				handler		= self.APPPUF_HANDLER
				init_name	= "TelnetDialog_push_bytes_raise"
				init_level	= 10

		self.test_case = TelnetTest()
		mock = Mock()

		with self.assertLogs("TelnetDialog_push_bytes_raise", 10) as case_loggy:

			self.assertIsNone(self.test_case.push_bytes(mock, "LOAD"))
		self.assertIn(

			"ERROR:TelnetDialog_push_bytes_raise:TelnetTest failed to push with ValueError: Enough of this",
			case_loggy.output
		)








	def test_TelnetDialog_fetch_bytes(self):

		class Mock:
			def read_until(self, load :Any, timeout): return load

		class TelnetTest(TelnetDialog):
			class loggy(LibraryContrib):

				handler		= self.APPPUF_HANDLER
				init_name	= "TelnetDialog_fetch_bytes"
				init_level	= 10

		self.test_case = TelnetTest()
		mock = Mock()

		with self.assertLogs("TelnetDialog_fetch_bytes", 10) as case_loggy:

			self.assertTrue(self.test_case.fetch_bytes(mock, "LOAD"), "LOAD")
			self.assertTrue(self.test_case.fetch_bytes(mock, "LOAD\r"), "LOAD")
			self.assertTrue(self.test_case.fetch_bytes(mock, "LOAD\n"), "LOAD")
			self.assertTrue(self.test_case.fetch_bytes(mock, "LOAD\r\n"), "LOAD")
			self.assertTrue(self.test_case.fetch_bytes(mock, b"LOAD"), "LOAD")
			self.assertTrue(self.test_case.fetch_bytes(mock, b"LOAD\r"), "LOAD")
			self.assertTrue(self.test_case.fetch_bytes(mock, b"LOAD\n"), "LOAD")
			self.assertTrue(self.test_case.fetch_bytes(mock, b"LOAD\r\n"), "LOAD")

		self.assertIn("DEBUG:TelnetDialog_fetch_bytes:Fetched 6 bytes", case_loggy.output)
		self.assertIn("DEBUG:TelnetDialog_fetch_bytes:Fetched 7 bytes", case_loggy.output)
		self.assertEqual(case_loggy.output.count("DEBUG:TelnetDialog_fetch_bytes:Fetched 6 bytes"),4)
		self.assertEqual(case_loggy.output.count("DEBUG:TelnetDialog_fetch_bytes:Fetched 7 bytes"),4)




	def test_TelnetDialog_fetch_bytes_invalid(self):

		class TelnetTest(TelnetDialog):
			class loggy(LibraryContrib):

				handler		= self.APPPUF_HANDLER
				init_name	= "TelnetDialog_fetch_bytes_invalid"
				init_level	= 10

		self.test_case = TelnetTest()
		for invalid in (

			42, 69., True, False, None, ..., unittest, LibraryContrib,
			[ "LOAD" ],( "LOAD", ),{ "LOAD" },{ "message": "LOAD" }
		):
			with (
				self.subTest(message=invalid),
				self.assertLogs("TelnetDialog_fetch_bytes_invalid", 10) as case_loggy
			):
				self.assertIsNone(self.test_case.fetch_bytes(None, invalid))
			self.assertIn(

				"ERROR:TelnetDialog_fetch_bytes_invalid:"
				f"{self.test_case} expect must be of type string or bytes, not {type(invalid)}",
				case_loggy.output
			)




	def test_TelnetDialog_fetch_bytes_raise(self):

		class Mock:
			def read_until(self, load :Any, timeout): raise ValueError("Enough of this")

		class TelnetTest(TelnetDialog):
			class loggy(LibraryContrib):

				handler		= self.APPPUF_HANDLER
				init_name	= "TelnetDialog_fetch_bytes_raise"
				init_level	= 10

		self.test_case = TelnetTest()
		mock = Mock()

		with self.assertLogs("TelnetDialog_fetch_bytes_raise", 10) as case_loggy:

			self.assertIsNone(self.test_case.fetch_bytes(mock, "LOAD"))
		self.assertIn(

			"ERROR:TelnetDialog_fetch_bytes_raise:TelnetTest failed to fetch with ValueError: Enough of this",
			case_loggy.output
		)








	def test_TelnetDialog(self):

		# Telnet connection example. Will open a socket and bind it to provided "HOST" on "PORT"
		# to listen for incomming connection. The TelnetDialog object will connect to socket and
		# write some bytes that will be echoed back. The writing methods must demostrate the idea
		# of implementation such "dialog" callables for TelnetDialog. However results of test to
		# be checked manually in loggy file. It is tested manually, that "fetch_bytes" after timeout
		# will return "read_until" fetched bytes.

		try:

			HOST = None
			PORT = None

			class TelnetTest(TelnetDialog):
				class loggy(LibraryContrib):

					handler		= self.APPPUF_HANDLER
					init_name	= "TelnetDialog"
					init_level	= 10

				def send1(self, connection :Telnet):

					self.push_bytes(connection, "OOH")
					self.fetch_bytes(connection, "OOH")

				def send2(self, connection :Telnet):

					self.push_bytes(connection, "EEH")
					self.fetch_bytes(connection, "EEH")

				def exit(self, connection :Telnet): self.push_bytes(connection, "exit")

			self.test_case = TelnetTest()

			class EchoClient(Thread):
				def __init__(self, client :TelnetDialog):

					super().__init__()
					self.client = client

				def run(self):
					self.client(

						HOST,
						self.client.send1,
						self.client.send2,
						self.client.exit,
						port=PORT,
					)

			class EchoServer(Thread):
				def run(self):

					with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:

						srv.bind(( HOST,PORT ))
						srv.listen()
						session,_ = srv.accept()

						with session:

							while	(data := session.recv(1024)):
								if	data == b"exit\r\n" : break

								session.sendall(data)

			if	isinstance(HOST, str) and isinstance(PORT, int):

				EchoServer().start()
				EchoClient(self.test_case).start()
		except:	self.assertFalse("Test caused troubles")








	def test_TelnetDialog_invalid_target(self):

		class TelnetTest(TelnetDialog):
			class loggy(LibraryContrib):

				handler		= self.APPPUF_HANDLER
				init_name	= "TelnetDialog_invalid_target"
				init_level	= 10

		self.test_case = TelnetTest()

		for invalid in (

			"target", 42, 69., True, False, None, ..., unittest, LibraryContrib,
			[ "10.10.10.10" ],( "10.10.10.10", ),{ "10.10.10.10" },{ "target": "10.10.10.10" }
		):
			with (
				self.subTest(target=invalid),
				self.assertLogs("TelnetDialog_invalid_target", 10) as case_loggy
			):
				self.assertIsNone(self.test_case(invalid))
			self.assertIn(f"INFO:TelnetDialog_invalid_target:Invalid host \"{invalid}\"", case_loggy.output)




	def test_TelnetDialog_connection_raise(self):

		class TelnetTest(TelnetDialog):
			class loggy(LibraryContrib):

				handler		= self.APPPUF_HANDLER
				init_name	= "TelnetDialog_connection_raise"
				init_level	= 10

		self.test_case = TelnetTest()

		with self.assertLogs("TelnetDialog_connection_raise", 10) as case_loggy:
			self.test_case("10.10.10.10", None, spanish_inquisition=True)

		self.assertIn(

			"ERROR:TelnetDialog_connection_raise:Connection to 10.10.10.10 failed due to "
			"TypeError: Telnet.open() got an unexpected keyword argument 'spanish_inquisition'",
			case_loggy.output
		)








if	__name__ == "__main__" : unittest.main(verbosity=2)







