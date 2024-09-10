import	unittest
from	pathlib							import Path
from	time							import sleep
from	shutil							import rmtree
from	pygwarts.irma.contrib			import LibraryContrib
from	pygwarts.irma.contrib.default	import NullContrib
from	pygwarts.irma.shelve			import LibraryShelf
from	pygwarts.tests					import PygwartsTestCase
from	navbow							import NavbowController








# Uncomment below statement to provide custom testing folder as a string
# PygwartsTestCase._PygwartsTestCase__WFOLDER = 








class NavbowTest(PygwartsTestCase):

	"""
		Testing cases for Navtex Bag of Words object
	"""

	NAVBOW_SHELF	= Path(PygwartsTestCase._PygwartsTestCase__WFOLDER) /"Navbow" /"navbow.Shelf"
	NAVBOW_LOGGY	= Path(PygwartsTestCase._PygwartsTestCase__WFOLDER) /"Navbow" /"navbow.loggy"


	@classmethod
	def setUpClass(cls):
		class TestShelf(LibraryShelf):

			class loggy(NullContrib):	pass
			grabbing	= str(cls.NAVBOW_SHELF)
			reclaiming	= True

		if	cls.NAVBOW_SHELF.parent.is_dir() : rmtree(cls.NAVBOW_SHELF.parent)

		test_Shelf = TestShelf()
		test_Shelf["OOH"]	= 0
		test_Shelf["EEH"]	= 0
		test_Shelf["AAH"]	= 0
		test_Shelf["TING"]	= 0
		test_Shelf["TANG"]	= 0
		test_Shelf["WALLA"]	= 0
		test_Shelf["BING"]	= 0
		test_Shelf["BANG"]	= 0
		test_Shelf.produce(strict_mode=False)

		cls.make_loggy_file(cls, cls.NAVBOW_LOGGY)




	def test_A_conversion(self):

		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(
				init_name="A_conversion",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("A_conversion", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			for word,state in self.test_case.NavbowShelve:
				with self.subTest(word=word, state=state): self.assertEqual(state,0)

			result = self.test_case("ooh", "EEH", mode=1)
			self.test_case.NavbowShelve.produce(str(self.NAVBOW_SHELF))


		self.assertIn("DEBUG:A_conversion:Converted \"OOH\" to known", case_loggy.output)
		self.assertIn("DEBUG:A_conversion:Converted \"EEH\" to known", case_loggy.output)
		self.assertIn("INFO:A_conversion:Done conversion for 2 words", case_loggy.output)
		self.assertIn(
			f"INFO:A_conversion:Shelf \"{self.NAVBOW_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertIsNotNone(result.get("converted"))
		self.assertIsInstance(result["converted"], list)
		self.assertEqual(result["converted"], [ "OOH", "EEH" ])
		self.assertIsNotNone(result.get("skipped"))
		self.assertIsInstance(result["skipped"], list)
		self.assertFalse(result["skipped"])
		self.assertIsNotNone(result.get("unknown"))
		self.assertIsInstance(result["unknown"], list)
		self.assertFalse(result["unknown"])


		for word,state in self.test_case.NavbowShelve:
			with self.subTest(word=word, state=state):

				if		word in ( "OOH","EEH" ): self.assertEqual(state,1)
				else:	self.assertEqual(state,0)








	def test_B_conversion(self):

		sleep(1)
		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(
				init_name="B_conversion",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("B_conversion", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			for word,state in self.test_case.NavbowShelve:
				with self.subTest(word=word, state=state):

					if		word in ( "OOH","EEH" ): self.assertEqual(state,1)
					else:	self.assertEqual(state,0)

			result = self.test_case("he", "Said", "OOH", "eeh", "ooh", "AaH", "aAh", mode=1)
			self.test_case.NavbowShelve.produce(str(self.NAVBOW_SHELF))


		self.assertIn("DEBUG:B_conversion:Converted \"AAH\" to known", case_loggy.output)
		self.assertIn("DEBUG:B_conversion:Duplicate word \"ooh\" skipped", case_loggy.output)
		self.assertIn("DEBUG:B_conversion:Duplicate word \"aAh\" skipped", case_loggy.output)
		self.assertIn("INFO:B_conversion:Done conversion for 1 words", case_loggy.output)
		self.assertIn(
			f"INFO:B_conversion:Shelf \"{self.NAVBOW_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertIsNotNone(result.get("converted"))
		self.assertIsInstance(result["converted"], list)
		self.assertEqual(result["converted"], [ "AAH" ])
		self.assertIsNotNone(result.get("skipped"))
		self.assertIsInstance(result["skipped"], list)
		self.assertEqual(result["skipped"], [ "OOH", "EEH" ])
		self.assertIsNotNone(result.get("unknown"))
		self.assertIsInstance(result["unknown"], list)
		self.assertEqual(result["unknown"], [ "HE", "SAID" ])


		for word,state in self.test_case.NavbowShelve:
				with self.subTest(word=word, state=state):

					if		word in ( "OOH","EEH", "AAH" ): self.assertEqual(state,1)
					else:	self.assertEqual(state,0)








	def test_C_conversion(self):

		sleep(1)
		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(
				init_name="C_conversion",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("C_conversion", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			for word,state in self.test_case.NavbowShelve:
				with self.subTest(word=word, state=state):

					if		word in ( "OOH","EEH", "AAH" ): self.assertEqual(state,1)
					else:	self.assertEqual(state,0)

			result = self.test_case(
				"OOH", "eeh", "ooh", "AaH", "aAh", "ting", "TANG", "WALLA", "WALLA", "Bing", "BANg", mode=0
			)
			self.test_case.NavbowShelve.produce(str(self.NAVBOW_SHELF))


		self.assertIn("DEBUG:C_conversion:Converted \"OOH\" to unknown", case_loggy.output)
		self.assertIn("DEBUG:C_conversion:Converted \"EEH\" to unknown", case_loggy.output)
		self.assertIn("DEBUG:C_conversion:Duplicate word \"ooh\" skipped", case_loggy.output)
		self.assertIn("DEBUG:C_conversion:Converted \"AAH\" to unknown", case_loggy.output)
		self.assertIn("DEBUG:C_conversion:Duplicate word \"aAh\" skipped", case_loggy.output)
		self.assertIn("DEBUG:C_conversion:Duplicate word \"WALLA\" skipped", case_loggy.output)
		self.assertIn("INFO:C_conversion:Done conversion for 3 words", case_loggy.output)
		self.assertIn(
			f"INFO:C_conversion:Shelf \"{self.NAVBOW_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertIsNotNone(result.get("converted"))
		self.assertIsInstance(result["converted"], list)
		self.assertEqual(result["converted"], [ "OOH", "EEH", "AAH" ])
		self.assertIsNotNone(result.get("skipped"))
		self.assertIsInstance(result["skipped"], list)
		self.assertEqual(result["skipped"], [ "TING", "TANG", "WALLA", "BING", "BANG" ])
		self.assertIsNotNone(result.get("unknown"))
		self.assertIsInstance(result["unknown"], list)
		self.assertFalse(result["unknown"])


		for word,state in self.test_case.NavbowShelve:
			with self.subTest(word=word, state=state): self.assertEqual(state,0)








if	__name__ == "__main__" : unittest.main(verbosity=2)







