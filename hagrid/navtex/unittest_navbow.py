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

			result = self.test_case.convert("ooh", "EEH", state=1)
			self.test_case.NavbowShelve.produce(str(self.NAVBOW_SHELF))


		self.assertIn("DEBUG:A_conversion:Converted \"OOH\" to known", case_loggy.output)
		self.assertIn("DEBUG:A_conversion:Converted \"EEH\" to known", case_loggy.output)
		self.assertIn("INFO:A_conversion:Done conversion for 2/2 words", case_loggy.output)
		self.assertIn(
			f"INFO:A_conversion:Shelf \"{self.NAVBOW_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertIsInstance(result, dict)
		self.assertIsInstance(result.get("converted"), list)
		self.assertEqual(result["converted"], [ "OOH", "EEH" ])
		self.assertIsInstance(result.get("skipped"), list)
		self.assertFalse(result["skipped"])
		self.assertIsInstance(result.get("undefined"), list)
		self.assertFalse(result["undefined"])


		for word,state in self.test_case.NavbowShelve:
			with self.subTest(word=word, state=state):

				if		word in ( "OOH","EEH" ): self.assertEqual(state,1)
				else:	self.assertEqual(state,0)








	def test_B_inspection(self):

		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(

				init_name="B_inspection",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("B_inspection", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			for word,state in self.test_case.NavbowShelve:
				with self.subTest(word=word, state=state):

					if		word in ( "OOH","EEH" ): self.assertEqual(state,1)
					else:	self.assertEqual(state,0)

			result = self.test_case.inspect("he", "Said", "OOH", "eeh", "ooh", "AaH", "aAh")


		self.assertIn("DEBUG:B_inspection:Duplicate word \"ooh\" skipped", case_loggy.output)
		self.assertIn("DEBUG:B_inspection:Duplicate word \"aAh\" skipped", case_loggy.output)
		self.assertIn("INFO:B_inspection:Done inspection for 5/7 words", case_loggy.output)


		self.assertIsInstance(result, dict)
		self.assertIsInstance(result.get("known"), list)
		self.assertEqual(result["known"], [ "OOH", "EEH" ])
		self.assertIsInstance(result.get("unknown"), list)
		self.assertEqual(result["unknown"], [ "AAH" ])
		self.assertIsInstance(result.get("undefined"), list)
		self.assertEqual(result["undefined"], [ "HE", "SAID" ])


		for word,state in self.test_case.NavbowShelve:
			with self.subTest(word=word, state=state):

				if		word in ( "OOH","EEH" ): self.assertEqual(state,1)
				else:	self.assertEqual(state,0)








	def test_C_state_inspection(self):

		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(

				init_name="C_state_inspection",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("C_state_inspection", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			result1 = self.test_case.inspect_state(0)
			result2 = self.test_case.inspect_state(1)


		self.assertIn("INFO:C_state_inspection:Done state inspection for 2/2 words", case_loggy.output)
		self.assertIn("INFO:C_state_inspection:Done state inspection for 6/6 words", case_loggy.output)


		self.assertIsInstance(result1, dict)
		self.assertIsInstance(result1.get("unknown"), list)
		self.assertCountEqual(result1["unknown"], [ "AAH", "TING", "TANG", "WALLA", "BING", "BANG" ])
		self.assertIsInstance(result1.get("known"), list)
		self.assertCountEqual(result1["known"], [])
		self.assertIsInstance(result2, dict)
		self.assertIsInstance(result2.get("known"), list)
		self.assertCountEqual(result2["known"], [ "OOH", "EEH" ])
		self.assertIsInstance(result2.get("unknown"), list)
		self.assertCountEqual(result2["unknown"], [])


		with self.assertLogs("C_state_inspection", 10) as case_loggy:

			result1 = self.test_case.inspect_state("0")
			result2 = self.test_case.inspect_state("1")


		self.assertIn("INFO:C_state_inspection:Done state inspection for 2/2 words", case_loggy.output)
		self.assertIn("INFO:C_state_inspection:Done state inspection for 6/6 words", case_loggy.output)


		self.assertIsInstance(result1, dict)
		self.assertIsInstance(result1.get("unknown"), list)
		self.assertCountEqual(result1["unknown"], [ "AAH", "TING", "TANG", "WALLA", "BING", "BANG" ])
		self.assertIsInstance(result1.get("known"), list)
		self.assertCountEqual(result1["known"], [])
		self.assertIsInstance(result2, dict)
		self.assertIsInstance(result2.get("known"), list)
		self.assertCountEqual(result2["known"], [ "OOH", "EEH" ])
		self.assertIsInstance(result2.get("unknown"), list)
		self.assertCountEqual(result2["unknown"], [])








	def test_D_erasion(self):

		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(

				init_name="D_erasion",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("D_erasion", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			for word,state in self.test_case.NavbowShelve:
				with self.subTest(word=word, state=state):

					if		word in ( "OOH","EEH" ): self.assertEqual(state,1)
					else:	self.assertEqual(state,0)

			result = self.test_case.erase("he", "Said", "OOH", "eeh", "ooh", "AaH", "aAh")


		self.assertIn("DEBUG:D_erasion:Duplicate word \"ooh\" skipped", case_loggy.output)
		self.assertIn("DEBUG:D_erasion:Duplicate word \"aAh\" skipped", case_loggy.output)
		self.assertIn("INFO:D_erasion:Done erasion for 5/7 words", case_loggy.output)


		self.assertIsInstance(result, dict)
		self.assertIsNotNone(result.get("known"))
		self.assertEqual(result["known"], [ "OOH", "EEH" ])
		self.assertIsNotNone(result.get("unknown"))
		self.assertEqual(result["unknown"], [ "AAH" ])
		self.assertIsNotNone(result.get("undefined"))
		self.assertEqual(result["undefined"], [ "HE", "SAID" ])


		self.assertEqual(len(self.test_case.NavbowShelve),5)
		self.assertNotIn("OOH", self.test_case.NavbowShelve)
		self.assertNotIn("EEH", self.test_case.NavbowShelve)
		self.assertNotIn("AAH", self.test_case.NavbowShelve)








	def test_E_state_erasion(self):

		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(

				init_name="E_state_erasion",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("E_state_erasion", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			result1 = self.test_case.erase_state(0)
			result2 = self.test_case.erase_state(1)


		self.assertIn("INFO:E_state_erasion:Done state erasion for 2/2 words", case_loggy.output)
		self.assertIn("INFO:E_state_erasion:Done state erasion for 6/6 words", case_loggy.output)


		self.assertIsInstance(result1, dict)
		self.assertIsInstance(result1.get("unknown"), list)
		self.assertCountEqual(result1["unknown"], [ "AAH", "TING", "TANG", "WALLA", "BING", "BANG" ])
		self.assertIsInstance(result1.get("known"), list)
		self.assertCountEqual(result1["known"], [])
		self.assertIsInstance(result2, dict)
		self.assertIsInstance(result2.get("unknown"), list)
		self.assertCountEqual(result2["known"], [ "OOH", "EEH" ])
		self.assertIsInstance(result2.get("known"), list)
		self.assertCountEqual(result2["unknown"], [])


		with self.assertLogs("E_state_erasion", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			result1 = self.test_case.erase_state("0")
			result2 = self.test_case.erase_state("1")


		self.assertIn("INFO:E_state_erasion:Done state erasion for 2/2 words", case_loggy.output)
		self.assertIn("INFO:E_state_erasion:Done state erasion for 6/6 words", case_loggy.output)


		self.assertIsInstance(result1, dict)
		self.assertIsInstance(result1.get("unknown"), list)
		self.assertCountEqual(result1["unknown"], [ "AAH", "TING", "TANG", "WALLA", "BING", "BANG" ])
		self.assertIsInstance(result1.get("known"), list)
		self.assertCountEqual(result1["known"], [])
		self.assertIsInstance(result2, dict)
		self.assertIsInstance(result2.get("unknown"), list)
		self.assertCountEqual(result2["known"], [ "OOH", "EEH" ])
		self.assertIsInstance(result2.get("known"), list)
		self.assertCountEqual(result2["unknown"], [])








	def test_F_call_total(self):

		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(

				init_name="F_call_total",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("F_call_total", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			result = self.test_case()


		self.assertIn("INFO:F_call_total:Total 8/8 stated words", case_loggy.output)
		self.assertIsInstance(result, dict)
		self.assertIsInstance(result.get("known"), list)
		self.assertCountEqual(result["known"], [ "OOH", "EEH" ])
		self.assertIsInstance(result.get("unknown"), list)
		self.assertCountEqual(result["unknown"], [ "AAH", "TING", "TANG", "WALLA", "BING", "BANG" ])
		self.assertIsInstance(result.get("undefined"), list)
		self.assertFalse(result["undefined"])








	def test_G_conversion(self):

		sleep(1)
		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(

				init_name="G_conversion",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("G_conversion", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			for word,state in self.test_case.NavbowShelve:
				with self.subTest(word=word, state=state):

					if		word in ( "OOH","EEH" ): self.assertEqual(state,1)
					else:	self.assertEqual(state,0)

			result = self.test_case.convert("he", "Said", "OOH", "eeh", "ooh", "AaH", "aAh", state=1)
			self.test_case.NavbowShelve.produce(str(self.NAVBOW_SHELF))


		self.assertIn("DEBUG:G_conversion:Converted \"AAH\" to known", case_loggy.output)
		self.assertIn("DEBUG:G_conversion:Duplicate word \"ooh\" skipped", case_loggy.output)
		self.assertIn("DEBUG:G_conversion:Duplicate word \"aAh\" skipped", case_loggy.output)
		self.assertIn("INFO:G_conversion:Done conversion for 1/7 words", case_loggy.output)
		self.assertIn(
			f"INFO:G_conversion:Shelf \"{self.NAVBOW_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertIsInstance(result, dict)
		self.assertIsInstance(result.get("converted"), list)
		self.assertEqual(result["converted"], [ "AAH" ])
		self.assertIsInstance(result.get("skipped"), list)
		self.assertEqual(result["skipped"], [ "OOH", "EEH" ])
		self.assertIsInstance(result.get("undefined"), list)
		self.assertEqual(result["undefined"], [ "HE", "SAID" ])


		for word,state in self.test_case.NavbowShelve:
			with self.subTest(word=word, state=state):

				if		word in ( "OOH","EEH", "AAH" ): self.assertEqual(state,1)
				else:	self.assertEqual(state,0)








	def test_H_conversion(self):

		sleep(1)
		self.assertTrue(self.NAVBOW_SHELF.is_file())
		self.test_case = NavbowController(

			LibraryContrib(

				init_name="H_conversion",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		with self.assertLogs("H_conversion", 10) as case_loggy:

			self.assertEqual(len(self.test_case.NavbowShelve),0)
			self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
			self.assertEqual(len(self.test_case.NavbowShelve),8)

			for word,state in self.test_case.NavbowShelve:
				with self.subTest(word=word, state=state):

					if		word in ( "OOH","EEH", "AAH" ): self.assertEqual(state,1)
					else:	self.assertEqual(state,0)

			result = self.test_case.convert(
				"OOH", "eeh", "ooh", "AaH", "aAh", "ting", "TANG", "WALLA", "WALLA", "Bing", "BANg", state=0
			)
			self.test_case.NavbowShelve.produce(str(self.NAVBOW_SHELF))


		self.assertIn("DEBUG:H_conversion:Converted \"OOH\" to unknown", case_loggy.output)
		self.assertIn("DEBUG:H_conversion:Converted \"EEH\" to unknown", case_loggy.output)
		self.assertIn("DEBUG:H_conversion:Duplicate word \"ooh\" skipped", case_loggy.output)
		self.assertIn("DEBUG:H_conversion:Converted \"AAH\" to unknown", case_loggy.output)
		self.assertIn("DEBUG:H_conversion:Duplicate word \"aAh\" skipped", case_loggy.output)
		self.assertIn("DEBUG:H_conversion:Duplicate word \"WALLA\" skipped", case_loggy.output)
		self.assertIn("INFO:H_conversion:Done conversion for 3/11 words", case_loggy.output)
		self.assertIn(
			f"INFO:H_conversion:Shelf \"{self.NAVBOW_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertIsInstance(result, dict)
		self.assertIsInstance(result.get("converted"), list)
		self.assertEqual(result["converted"], [ "OOH", "EEH", "AAH" ])
		self.assertIsInstance(result.get("skipped"), list)
		self.assertEqual(result["skipped"], [ "TING", "TANG", "WALLA", "BING", "BANG" ])
		self.assertIsInstance(result.get("undefined"), list)
		self.assertFalse(result["undefined"])


		for word,state in self.test_case.NavbowShelve:
			with self.subTest(word=word, state=state): self.assertEqual(state,0)








	def test_I_state_inspect_edge_cases(self):

		self.test_case = NavbowController(

			LibraryContrib(

				init_name="I_state_inspect_edge_cases",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		self.assertEqual(len(self.test_case.NavbowShelve),0)
		self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
		self.assertEqual(len(self.test_case.NavbowShelve),8)


		with self.assertLogs("I_state_inspect_edge_cases", 10) as case_loggy:

			self.test_case.NavbowShelve[42] = 1
			case1 = self.test_case.inspect_state(1)
			case2 = self.test_case.inspect_state("1")

		self.assertIsInstance(case1, dict)
		self.assertIsInstance(case1.get("unknown"), list)
		self.assertCountEqual(case1["unknown"], [])
		self.assertIsInstance(case1.get("known"), list)
		self.assertCountEqual(case1["known"], [])
		self.assertIsInstance(case2, dict)
		self.assertIsInstance(case2.get("unknown"), list)
		self.assertCountEqual(case2["unknown"], [])
		self.assertIsInstance(case2.get("known"), list)
		self.assertCountEqual(case2["known"], [])
		self.assertIn(

			f"WARNING:I_state_inspect_edge_cases:Invalid key \"42\" in {self.test_case.NavbowShelve}",
			case_loggy.output
		)
		self.assertEqual(

			case_loggy.output.count(

				f"WARNING:I_state_inspect_edge_cases:Invalid key \"42\" in {self.test_case.NavbowShelve}"
			),	2
		)


		with self.assertLogs("I_state_inspect_edge_cases", 10) as case_loggy:

			self.test_case.NavbowShelve[42] = 0
			case3 = self.test_case.inspect_state(0)
			case4 = self.test_case.inspect_state("0")

		self.assertIsInstance(case3, dict)
		self.assertIsInstance(case3.get("unknown"), list)
		self.assertCountEqual(
			case3["unknown"], [ "OOH", "EEH", "AAH", "TING", "TANG", "WALLA", "BING", "BANG" ]
		)
		self.assertIsInstance(case3.get("known"), list)
		self.assertCountEqual(case3["known"], [])
		self.assertIsInstance(case4, dict)
		self.assertIsInstance(case4.get("unknown"), list)
		self.assertCountEqual(
			case4["unknown"], [ "OOH", "EEH", "AAH", "TING", "TANG", "WALLA", "BING", "BANG" ]
		)
		self.assertIsInstance(case4.get("known"), list)
		self.assertCountEqual(case4["known"], [])
		self.assertIn(

			f"WARNING:I_state_inspect_edge_cases:Invalid key \"42\" in {self.test_case.NavbowShelve}",
			case_loggy.output
		)
		self.assertEqual(

			case_loggy.output.count(

				f"WARNING:I_state_inspect_edge_cases:Invalid key \"42\" in {self.test_case.NavbowShelve}"
			),	2
		)


		with self.assertLogs("I_state_inspect_edge_cases", 10) as case_loggy:

			case5 = self.test_case.inspect_state(2)
			case6 = self.test_case.inspect_state("2")

		self.assertIsInstance(case5, dict)
		self.assertIsInstance(case5.get("unknown"), list)
		self.assertCountEqual(case5["unknown"], [])
		self.assertIsInstance(case5.get("known"), list)
		self.assertCountEqual(case5["known"], [])
		self.assertIsInstance(case6, dict)
		self.assertIsInstance(case6.get("unknown"), list)
		self.assertCountEqual(case6["unknown"], [])
		self.assertIsInstance(case6.get("known"), list)
		self.assertCountEqual(case6["known"], [])
		self.assertIn(
			f"INFO:I_state_inspect_edge_cases:Improper state \"2\" for inspection", case_loggy.output
		)
		self.assertEqual(

			case_loggy.output.count(

				f"INFO:I_state_inspect_edge_cases:Improper state \"2\" for inspection"
			),	2
		)


		self.test_case.NavbowShelve.unload()
		self.assertEqual(len(self.test_case.NavbowShelve),0)


		with self.assertLogs("I_state_inspect_edge_cases", 10) as case_loggy:

			case7 = self.test_case.inspect_state(1)
			case8 = self.test_case.inspect_state("1")

		self.assertIsInstance(case7, dict)
		self.assertIsInstance(case7.get("unknown"), list)
		self.assertCountEqual(case7["unknown"], [])
		self.assertIsInstance(case7.get("known"), list)
		self.assertCountEqual(case7["known"], [])
		self.assertIsInstance(case8, dict)
		self.assertIsInstance(case8.get("unknown"), list)
		self.assertCountEqual(case8["unknown"], [])
		self.assertIsInstance(case8.get("known"), list)
		self.assertCountEqual(case8["known"], [])
		self.assertIn(
			f"INFO:I_state_inspect_edge_cases:No words with known state", case_loggy.output
		)
		self.assertEqual(
			case_loggy.output.count(f"INFO:I_state_inspect_edge_cases:No words with known state"),2
		)


		with self.assertLogs("I_state_inspect_edge_cases", 10) as case_loggy:

			case9 = self.test_case.inspect_state(0)
			case10= self.test_case.inspect_state("0")

		self.assertIsInstance(case9, dict)
		self.assertIsInstance(case9.get("unknown"), list)
		self.assertCountEqual(case9["unknown"], [])
		self.assertIsInstance(case9.get("known"), list)
		self.assertCountEqual(case9["known"], [])
		self.assertIsInstance(case10, dict)
		self.assertIsInstance(case10.get("unknown"), list)
		self.assertCountEqual(case10["unknown"], [])
		self.assertIsInstance(case10.get("known"), list)
		self.assertCountEqual(case10["known"], [])
		self.assertIn(
			f"INFO:I_state_inspect_edge_cases:No words with unknown state", case_loggy.output
		)
		self.assertEqual(
			case_loggy.output.count(f"INFO:I_state_inspect_edge_cases:No words with unknown state"),2
		)








	def test_J_inspect_edge_cases(self):

		self.test_case = NavbowController(

			LibraryContrib(

				init_name="J_inspect_edge_cases",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		self.assertEqual(len(self.test_case.NavbowShelve),0)
		self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
		self.assertEqual(len(self.test_case.NavbowShelve),8)


		with self.assertLogs("J_inspect_edge_cases", 10) as case_loggy:

			self.test_case.NavbowShelve["OOH"] = 2
			case1 = self.test_case.inspect("OOH", 1)
			case2 = self.test_case.inspect()


		self.assertIn("WARNING:J_inspect_edge_cases:Invalid state for word \"OOH\"", case_loggy.output)
		self.assertIn("INFO:J_inspect_edge_cases:Incorrect word \"1\" for inspection", case_loggy.output)
		self.assertIn("INFO:J_inspect_edge_cases:No words provided for inspection", case_loggy.output)


		self.assertIsInstance(case1, dict)
		self.assertIsInstance(case1.get("known"), list)
		self.assertFalse(case1["known"])
		self.assertIsInstance(case1.get("unknown"), list)
		self.assertFalse(case1["unknown"])
		self.assertIsInstance(case1.get("undefined"), list)
		self.assertFalse(case1["undefined"])


		self.assertIsInstance(case2, dict)
		self.assertIsInstance(case2.get("known"), list)
		self.assertFalse(case2["known"])
		self.assertIsInstance(case2.get("unknown"), list)
		self.assertFalse(case2["unknown"])
		self.assertIsInstance(case2.get("undefined"), list)
		self.assertFalse(case2["undefined"])








	def test_K_state_erase_edge_cases(self):

		self.test_case = NavbowController(

			LibraryContrib(

				init_name="K_state_erase_edge_cases",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		self.assertEqual(len(self.test_case.NavbowShelve),0)
		self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
		self.assertEqual(len(self.test_case.NavbowShelve),8)


		with self.assertLogs("K_state_erase_edge_cases", 10) as case_loggy:

			self.test_case.NavbowShelve[42] = 1
			case1 = self.test_case.erase_state(1)
			case2 = self.test_case.erase_state("1")

		self.assertIsInstance(case1, dict)
		self.assertIsInstance(case1.get("unknown"), list)
		self.assertCountEqual(case1["unknown"], [])
		self.assertIsInstance(case1.get("known"), list)
		self.assertCountEqual(case1["known"], [])
		self.assertIsInstance(case2, dict)
		self.assertIsInstance(case2.get("unknown"), list)
		self.assertCountEqual(case2["unknown"], [])
		self.assertIsInstance(case2.get("known"), list)
		self.assertCountEqual(case2["known"], [])
		self.assertIn(

			f"WARNING:K_state_erase_edge_cases:Invalid key \"42\" in {self.test_case.NavbowShelve}",
			case_loggy.output
		)
		self.assertEqual(

			case_loggy.output.count(

				f"WARNING:K_state_erase_edge_cases:Invalid key \"42\" in {self.test_case.NavbowShelve}"
			),	2
		)


		with self.assertLogs("K_state_erase_edge_cases", 10) as case_loggy:

			self.test_case.NavbowShelve[42] = 0
			case3 = self.test_case.erase_state(0)
			case4 = self.test_case.erase_state("0")

		self.assertIsInstance(case3, dict)
		self.assertIsInstance(case3.get("unknown"), list)
		self.assertCountEqual(
			case3["unknown"], [ "OOH", "EEH", "AAH", "TING", "TANG", "WALLA", "BING", "BANG" ]
		)
		self.assertIsInstance(case3.get("known"), list)
		self.assertCountEqual(case3["known"], [])
		self.assertIsInstance(case4, dict)
		self.assertIsInstance(case4.get("unknown"), list)
		self.assertCountEqual(case4["unknown"], [])
		self.assertIsInstance(case4.get("known"), list)
		self.assertCountEqual(case4["known"], [])
		self.assertIn(

			f"WARNING:K_state_erase_edge_cases:Invalid key \"42\" in {self.test_case.NavbowShelve}",
			case_loggy.output
		)
		self.assertEqual(

			case_loggy.output.count(

				f"WARNING:K_state_erase_edge_cases:Invalid key \"42\" in {self.test_case.NavbowShelve}"
			),	2
		)


		with self.assertLogs("K_state_erase_edge_cases", 10) as case_loggy:

			case5 = self.test_case.erase_state(2)
			case6 = self.test_case.erase_state("2")

		self.assertIsInstance(case5, dict)
		self.assertIsInstance(case5.get("unknown"), list)
		self.assertCountEqual(case5["unknown"], [])
		self.assertIsInstance(case5.get("known"), list)
		self.assertCountEqual(case5["known"], [])
		self.assertIsInstance(case6, dict)
		self.assertIsInstance(case6.get("unknown"), list)
		self.assertCountEqual(case6["unknown"], [])
		self.assertIsInstance(case6.get("known"), list)
		self.assertCountEqual(case6["known"], [])
		self.assertIn(
			f"INFO:K_state_erase_edge_cases:Improper state \"2\" for erasion", case_loggy.output
		)
		self.assertEqual(

			case_loggy.output.count(

				f"INFO:K_state_erase_edge_cases:Improper state \"2\" for erasion"
			),	2
		)


		self.assertEqual(len(self.test_case.NavbowShelve),1)
		self.test_case.NavbowShelve.unload()
		self.assertEqual(len(self.test_case.NavbowShelve),0)


		with self.assertLogs("K_state_erase_edge_cases", 10) as case_loggy:

			case7 = self.test_case.erase_state(1)
			case8 = self.test_case.erase_state("1")

		self.assertIsInstance(case7, dict)
		self.assertIsInstance(case7.get("unknown"), list)
		self.assertCountEqual(case7["unknown"], [])
		self.assertIsInstance(case7.get("known"), list)
		self.assertCountEqual(case7["known"], [])
		self.assertIsInstance(case8, dict)
		self.assertIsInstance(case8.get("unknown"), list)
		self.assertCountEqual(case8["unknown"], [])
		self.assertIsInstance(case8.get("known"), list)
		self.assertCountEqual(case8["known"], [])
		self.assertIn(
			f"INFO:K_state_erase_edge_cases:No words with known state", case_loggy.output
		)
		self.assertEqual(
			case_loggy.output.count(f"INFO:K_state_erase_edge_cases:No words with known state"),2
		)


		with self.assertLogs("K_state_erase_edge_cases", 10) as case_loggy:

			case9 = self.test_case.erase_state(0)
			case10= self.test_case.erase_state("0")

		self.assertIsInstance(case9, dict)
		self.assertIsInstance(case9.get("unknown"), list)
		self.assertCountEqual(case9["unknown"], [])
		self.assertIsInstance(case9.get("known"), list)
		self.assertCountEqual(case9["known"], [])
		self.assertIsInstance(case10, dict)
		self.assertIsInstance(case10.get("unknown"), list)
		self.assertCountEqual(case10["unknown"], [])
		self.assertIsInstance(case10.get("known"), list)
		self.assertCountEqual(case10["known"], [])
		self.assertIn(
			f"INFO:K_state_erase_edge_cases:No words with unknown state", case_loggy.output
		)
		self.assertEqual(
			case_loggy.output.count(f"INFO:K_state_erase_edge_cases:No words with unknown state"),2
		)








	def test_L_erase_edge_cases(self):

		self.test_case = NavbowController(

			LibraryContrib(

				init_name="L_erase_edge_cases",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		self.assertEqual(len(self.test_case.NavbowShelve),0)
		self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
		self.assertEqual(len(self.test_case.NavbowShelve),8)


		with self.assertLogs("L_erase_edge_cases", 10) as case_loggy:

			self.test_case.NavbowShelve["OOH"] = 2
			case1 = self.test_case.erase("OOH", 1)
			case2 = self.test_case.erase()


		self.assertIn("WARNING:L_erase_edge_cases:Invalid state for word \"OOH\"", case_loggy.output)
		self.assertIn("INFO:L_erase_edge_cases:Incorrect word \"1\" for erasion", case_loggy.output)
		self.assertIn("INFO:L_erase_edge_cases:No words provided for erasion", case_loggy.output)


		self.assertIsInstance(case1, dict)
		self.assertIsInstance(case1.get("known"), list)
		self.assertFalse(case1["known"])
		self.assertIsInstance(case1.get("unknown"), list)
		self.assertFalse(case1["unknown"])
		self.assertIsInstance(case1.get("undefined"), list)
		self.assertFalse(case1["undefined"])


		self.assertIsInstance(case2, dict)
		self.assertIsInstance(case2.get("known"), list)
		self.assertFalse(case2["known"])
		self.assertIsInstance(case2.get("unknown"), list)
		self.assertFalse(case2["unknown"])
		self.assertIsInstance(case2.get("undefined"), list)
		self.assertFalse(case2["undefined"])








	def test_M_convert_edge_cases(self):

		self.test_case = NavbowController(

			LibraryContrib(

				init_name="M_convert_edge_cases",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		# RaisesRegex version doesn't work...
		self.assertRaises(TypeError, self.test_case.convert, "OOH", 1)
		self.assertEqual(len(self.test_case.NavbowShelve),0)
		self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
		self.assertEqual(len(self.test_case.NavbowShelve),8)


		with self.assertLogs("M_convert_edge_cases", 10) as case_loggy:

			self.test_case.NavbowShelve["OOH"] = 2
			case1 = self.test_case.convert("OOH", 1, state=1)
			case2 = self.test_case.convert("EEH", state=2)
			case3 = self.test_case.convert(state=0)


		self.assertIn("WARNING:M_convert_edge_cases:Invalid state for word \"OOH\"", case_loggy.output)
		self.assertIn("INFO:M_convert_edge_cases:Incorrect word \"1\" for conversion", case_loggy.output)
		self.assertIn("INFO:M_convert_edge_cases:Improper conversion state \"2\"", case_loggy.output)
		self.assertIn("INFO:M_convert_edge_cases:No words provided for conversion", case_loggy.output)


		self.assertIsNotNone(case1.get("converted"))
		self.assertIsInstance(case1["converted"], list)
		self.assertFalse(case1["converted"])
		self.assertIsNotNone(case1.get("skipped"))
		self.assertIsInstance(case1["skipped"], list)
		self.assertFalse(case1["skipped"])
		self.assertIsNotNone(case1.get("undefined"))
		self.assertIsInstance(case1["undefined"], list)
		self.assertFalse(case1["undefined"])


		self.assertIsNotNone(case2.get("converted"))
		self.assertIsInstance(case2["converted"], list)
		self.assertFalse(case2["converted"])
		self.assertIsNotNone(case2.get("skipped"))
		self.assertIsInstance(case2["skipped"], list)
		self.assertFalse(case2["skipped"])
		self.assertIsNotNone(case2.get("undefined"))
		self.assertIsInstance(case2["undefined"], list)
		self.assertFalse(case2["undefined"])


		self.assertIsNotNone(case3.get("converted"))
		self.assertIsInstance(case3["converted"], list)
		self.assertFalse(case3["converted"])
		self.assertIsNotNone(case3.get("skipped"))
		self.assertIsInstance(case3["skipped"], list)
		self.assertFalse(case3["skipped"])
		self.assertIsNotNone(case3.get("undefined"))
		self.assertIsInstance(case3["undefined"], list)
		self.assertFalse(case3["undefined"])








	def test_N_call_edge_cases(self):

		self.test_case = NavbowController(

			LibraryContrib(

				init_name="N_call_edge_cases",
				init_level=10,
				handler=str(self.NAVBOW_LOGGY)
			)
		)


		# RaisesRegex version doesn't work...
		self.assertRaises(TypeError, self.test_case, "OOH")
		self.assertEqual(len(self.test_case.NavbowShelve),0)
		self.test_case.NavbowShelve.grab(str(self.NAVBOW_SHELF))
		self.assertEqual(len(self.test_case.NavbowShelve),8)


		with self.assertLogs("N_call_edge_cases", 10) as case_loggy:

			self.test_case.NavbowShelve["OOH"] = 2
			self.test_case.NavbowShelve[2] = "OOH"
			case1 = self.test_case()


		self.assertIn("WARNING:N_call_edge_cases:Incorrect word \"2\" encountered", case_loggy.output)
		self.assertIn("INFO:N_call_edge_cases:Total 7/9 stated words", case_loggy.output)
		self.assertIsInstance(case1, dict)
		self.assertIsInstance(case1.get("known"), list)
		self.assertFalse(case1["known"])
		self.assertIsInstance(case1.get("unknown"), list)
		self.assertCountEqual(case1["unknown"], [ "EEH", "AAH", "TING", "TANG", "WALLA", "BING", "BANG" ])
		self.assertIsInstance(case1.get("undefined"), list)
		self.assertEqual(case1["undefined"], [ "OOH" ])


		with self.assertLogs("N_call_edge_cases", 10) as case_loggy:

			self.test_case.NavbowShelve.unload()
			case2 = self.test_case()


		self.assertIn("INFO:N_call_edge_cases:No words in total", case_loggy.output)
		self.assertIsInstance(case2, dict)
		self.assertIsInstance(case2.get("known"), list)
		self.assertFalse(case2["known"])
		self.assertIsInstance(case2.get("unknown"), list)
		self.assertFalse(case2["unknown"])
		self.assertIsInstance(case2.get("undefined"), list)
		self.assertFalse(case2["undefined"])








if	__name__ == "__main__" : unittest.main(verbosity=2)







