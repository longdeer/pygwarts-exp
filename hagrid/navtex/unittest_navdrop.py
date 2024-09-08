import	os
import	unittest
from	pathlib								import Path
from	time								import sleep
from	shutil								import rmtree
from	pygwarts.magical.time_turner		import TimeTurner
from	pygwarts.irma.contrib				import LibraryContrib
from	pygwarts.irma.shelve				import LibraryShelf
from	pygwarts.hagrid.thrivables			import Tree
from	pygwarts.hagrid.thrivables			import Copse
from	pygwarts.hagrid.sprouts				import fssprout
from	pygwarts.hagrid.planting			import Flourish
from	pygwarts.hagrid.bloom.leafs			import Rejuvenation
from	pygwarts.hagrid.bloom.weeds			import Efflorescence
from	pygwarts.hagrid.planting.leafs		import LeafGrowth
from	pygwarts.hagrid.planting.peeks		import DraftPeek
from	pygwarts.hagrid.planting.weeds		import SprigTrimmer
from	pygwarts.hagrid.cultivation.sifting	import SiftingController
from	pygwarts.tests						import PygwartsTestCase
from	navtex_preprocessor					import Navpreprocessor








# Uncomment below statement to provide custom testing folder as a string
# ATTENTION!
# After root directory change there might be some FAIL because of fs file sorting.
# Pay attention for the "pool" messages order!
# PygwartsTestCase._PygwartsTestCase__WFOLDER = 








class NavdropTest(PygwartsTestCase):

	"""
		Testing cases for large Navtex processing object
	"""

	MESSAGES_SRC	= Path(PygwartsTestCase._PygwartsTestCase__WFOLDER) /"Navdrop" /"messages_src"
	MESSAGES_DST1	= Path(PygwartsTestCase._PygwartsTestCase__WFOLDER) /"Navdrop" /"messages_dst1"
	MESSAGES_DST2	= Path(PygwartsTestCase._PygwartsTestCase__WFOLDER) /"Navdrop" /"messages_dst2"
	NAVDROP_LOGGY	= Path(PygwartsTestCase._PygwartsTestCase__WFOLDER) /"Navdrop" /"navdrop.loggy"
	NAVDROP_SHELF	= Path(PygwartsTestCase._PygwartsTestCase__WFOLDER) /"Navdrop" /"navdrop.Shelf"
	NAVDROP_BOW		= Path(PygwartsTestCase._PygwartsTestCase__WFOLDER) /"Navdrop" /"navbow.Shelf"


	@classmethod
	def setUpClass(cls):

		cls.maxDiff = None
		cls.now = TimeTurner(timepoint="0420")

		# All messages are well structured (for UDK2) and actual at the first place
		cls.text_1 = str(

			"\n"
			"ZCZC KE42\n"
			f"{cls.now.dHM_asjoin} UTC {cls.now.b.upper()}\n"
			"MURMANSK WEATHER FORECAST\n"
			"ON MURMAN COAST AT 06 UTC\n"
			"TO 18 UTC 01 SEP WIND NORTH-WESTERN\n"
			"WESTERN 8-13 M/S VISIBILITY GOOD\n"
			"IN TO MIST 1-2 KM SEAS 1,5-2,0 M\n"
			"NNNN\n"
		)


		cls.text_2 = str(

			"\n"
			"ZCZC KA69\n"
			f"{cls.now.dHM_asjoin} UTC {cls.now.b.upper()} {cls.now.y}\n"
			"COASTAL WARNING MURMANSK 270\n"
			"WEST OF NOVAYA ZEMLYA ISLANDS\n"
			"1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
			"NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
			"DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
			"76-00.0N 056-30.0E\n"
			"76-00.0N 058-00.0E\n"
			"75-23.0N 056-00.0E\n"
			"75-12.0N 055-05.0E\n"
			"73-45.0N 052-58.0E\n"
			"72-45.0N 051-45.0E\n"
			"72-00.0N 050-50.0E\n"
			"72-00.0N 050-00.0E\n"
			"74-00.0N 050-00.0E\n"
			"75-25.0N 052-45.0E\n"
			"2. CANCEL THIS MESSAGE 302200 SEP 24\n"
			"NNNN\n"
		)


		cls.text_3 = str(

			"\n"
			"ZCZC KB00\n"
			f"{cls.now.dHM_asjoin} UTC {cls.now.b.upper()}\n"
			"GALE WARNING MURMANSK NR85\n"
			"ON MURMAN COAST 01 MAR 17-21 UTC\n"
			"WIND NORTH-EASTERN NORTHERN GUST\n"
			"15-20 M/S\n"
			"NNNN\n"
		)


		# Precleaning root directory
		if(root := Path(PygwartsTestCase._PygwartsTestCase__WFOLDER) /"Navdrop").is_dir(): rmtree(root)


		cls.MESSAGE_1 = cls.MESSAGES_SRC /"KE42.TLX"
		cls.MESSAGE_2 = cls.MESSAGES_SRC /"KA69.TLX"
		cls.MESSAGE_3 = cls.MESSAGES_SRC /"KB00.TLX"


		cls.DST1_MESSAGE_1 = cls.MESSAGES_DST1 /"KE42.TLX"
		cls.DST1_MESSAGE_2 = cls.MESSAGES_DST1 /"KA69.TLX"
		cls.DST1_MESSAGE_3 = cls.MESSAGES_DST1 /"KB00.TLX"


		cls.DST2_MESSAGE_1 = cls.MESSAGES_DST2 /"KE42.TLX"
		cls.DST2_MESSAGE_2 = cls.MESSAGES_DST2 /"KA69.TLX"
		cls.DST2_MESSAGE_3 = cls.MESSAGES_DST2 /"KB00.TLX"


		cls.fmake(cls, cls.MESSAGE_1, cls.text_1)
		cls.fmake(cls, cls.MESSAGE_2, cls.text_2)
		cls.fmake(cls, cls.MESSAGE_3, cls.text_3)


		cls.make_loggy_file(cls, cls.NAVDROP_LOGGY)




	def setUp(self):

		class Navdrop(Copse):
			class loggy(LibraryContrib):

				init_level		= 10
				init_name		= "Navdrop"
				handler			= str(self.NAVDROP_LOGGY)
				force_warning	= "*.outer_shelf", "*.inner_shelf",

				# Dummy method that must verify "pool" receive correct message
				def pool(self, message :str): self.current_pool = message

			class Targets(Copse):
				class one(Tree):	bough = self.MESSAGES_DST1
				class two(Tree):	bough = self.MESSAGES_DST2
				class leafs(SiftingController):
					include = (

						rf".+{os.sep}[Kk][A-Za-z]\d\d\.[Tt][Ll][Xx]",
						rf"{self.MESSAGES_DST1}{os.sep}.+",
						rf"{self.MESSAGES_DST2}{os.sep}.+",
					)
				class twigs(SiftingController):
					include = (

						rf"{self.MESSAGES_DST1}{os.sep}.+",
						rf"{self.MESSAGES_DST2}{os.sep}.+",
					)

			@DraftPeek(renew=False, cache=False)
			class grow(LeafGrowth):		pass
			class rejuve(Rejuvenation):	pass

			class trim(SprigTrimmer):	pass
			class effloresce(Efflorescence):
				branches = {

					str(self.MESSAGES_DST1):	( str(self.MESSAGES_SRC), ),
					str(self.MESSAGES_DST2):	( str(self.MESSAGES_SRC), ),
				}

			@fssprout(str(self.MESSAGES_SRC))
			@Navpreprocessor("K")
			class perform(Flourish):

				class Navfiles(SiftingController):	include = r".+/[Kk][A-Za-z]\d\d\.[tT][lL][xX]",
				class Navbow(LibraryShelf):

					grabbing	= str(self.NAVDROP_BOW)
					reclaiming	= True

				class Navshelf(LibraryShelf):

					grabbing	= str(self.NAVDROP_SHELF)
					reclaiming	= True


		self.case_object = Navdrop








	def test_A_strict_init(self):

		self.case_object.loggy.init_name = "A_strict_init"
		self.assertFalse(self.MESSAGES_DST1.is_dir())
		self.assertFalse(self.MESSAGES_DST2.is_dir())
		self.assertFalse(self.NAVDROP_SHELF.is_file())
		self.assertFalse(self.NAVDROP_BOW.is_file())


		with self.assertLogs("A_strict_init", 10) as case_loggy:

			self.test_case = self.case_object()
			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),48)
			self.assertEqual(len(self.test_case.perform.Navshelf),0)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.assertTrue(hasattr(self.test_case.loggy, "current_pool"))
		self.assertEqual(

			self.test_case.loggy.current_pool,
			str(
				"new message KB00\n"
				"1    ZCZC KB00\n"
				f"2    {self.now.dHM_asjoin} UTC {self.now.b.upper()}\n"
				"3    GALE WARNING MURMANSK NR85\n"
				"4    ON MURMAN COAST 01 MAR 17-21 UTC\n"
				"5    WIND NORTH-EASTERN NORTHERN GUST\n"
				"6    15-20 M/S\n"
				"7    NNNN\n"
				"\n"
				"Unknown word \"UTC\" in KB00 line 2\n"
				"Unknown word \"SEP\" in KB00 line 2\n"
				"Unknown word \"GALE\" in KB00 line 3\n"
				"Unknown word \"WARNING\" in KB00 line 3\n"
				"Unknown word \"MURMANSK\" in KB00 line 3\n"
				"Unknown word \"ON\" in KB00 line 4\n"
				"Unknown word \"MURMAN\" in KB00 line 4\n"
				"Unknown word \"COAST\" in KB00 line 4\n"
				"Unknown word \"MAR\" in KB00 line 4\n"
				"Unknown word \"UTC\" in KB00 line 4\n"
				"Unknown word \"WIND\" in KB00 line 5\n"
				"Unknown word \"NORTH-EASTERN\" in KB00 line 5\n"
				"Unknown word \"NORTHERN\" in KB00 line 5\n"
				"Unknown word \"GUST\" in KB00 line 5\n"
				"Unknown word \"M/S\" in KB00 line 6\n"
				"\n\n"
				"new message KE42\n"
				"1    ZCZC KE42\n"
				f"2    {self.now.dHM_asjoin} UTC {self.now.b.upper()}\n"
				"3    MURMANSK WEATHER FORECAST\n"
				"4    ON MURMAN COAST AT 06 UTC\n"
				"5    TO 18 UTC 01 SEP WIND NORTH-WESTERN\n"
				"6    WESTERN 8-13 M/S VISIBILITY GOOD\n"
				"7    IN TO MIST 1-2 KM SEAS 1,5-2,0 M\n"
				"8    NNNN\n"
				"\n"
				"Unknown word \"UTC\" in KE42 line 2\n"
				"Unknown word \"SEP\" in KE42 line 2\n"
				"Unknown word \"MURMANSK\" in KE42 line 3\n"
				"Unknown word \"WEATHER\" in KE42 line 3\n"
				"Unknown word \"FORECAST\" in KE42 line 3\n"
				"Unknown word \"ON\" in KE42 line 4\n"
				"Unknown word \"MURMAN\" in KE42 line 4\n"
				"Unknown word \"COAST\" in KE42 line 4\n"
				"Unknown word \"AT\" in KE42 line 4\n"
				"Unknown word \"UTC\" in KE42 line 4\n"
				"Unknown word \"TO\" in KE42 line 5\n"
				"Unknown word \"UTC\" in KE42 line 5\n"
				"Unknown word \"SEP\" in KE42 line 5\n"
				"Unknown word \"WIND\" in KE42 line 5\n"
				"Unknown word \"NORTH-WESTERN\" in KE42 line 5\n"
				"Unknown word \"WESTERN\" in KE42 line 6\n"
				"Unknown word \"M/S\" in KE42 line 6\n"
				"Unknown word \"VISIBILITY\" in KE42 line 6\n"
				"Unknown word \"GOOD\" in KE42 line 6\n"
				"Unknown word \"IN\" in KE42 line 7\n"
				"Unknown word \"TO\" in KE42 line 7\n"
				"Unknown word \"MIST\" in KE42 line 7\n"
				"Unknown word \"KM\" in KE42 line 7\n"
				"Unknown word \"SEAS\" in KE42 line 7\n"
				"Unknown word \"M\" in KE42 line 7\n"
				"\n\n"
				"new message KA69\n"
				"1    ZCZC KA69\n"
				f"2    {self.now.dHM_asjoin} UTC {self.now.b.upper()} {self.now.y}\n"
				"3    COASTAL WARNING MURMANSK 270\n"
				"4    WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"5    1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"6    NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"7    DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"8    76-00.0N 056-30.0E\n"
				"9    76-00.0N 058-00.0E\n"
				"10   75-23.0N 056-00.0E\n"
				"11   75-12.0N 055-05.0E\n"
				"12   73-45.0N 052-58.0E\n"
				"13   72-45.0N 051-45.0E\n"
				"14   72-00.0N 050-50.0E\n"
				"15   72-00.0N 050-00.0E\n"
				"16   74-00.0N 050-00.0E\n"
				"17   75-25.0N 052-45.0E\n"
				"18   2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"19   NNNN\n"
				"\n"
				"Unknown word \"UTC\" in KA69 line 2\n"
				"Unknown word \"SEP\" in KA69 line 2\n"
				"Unknown word \"COASTAL\" in KA69 line 3\n"
				"Unknown word \"WARNING\" in KA69 line 3\n"
				"Unknown word \"MURMANSK\" in KA69 line 3\n"
				"Unknown word \"WEST\" in KA69 line 4\n"
				"Unknown word \"OF\" in KA69 line 4\n"
				"Unknown word \"NOVAYA\" in KA69 line 4\n"
				"Unknown word \"ZEMLYA\" in KA69 line 4\n"
				"Unknown word \"ISLANDS\" in KA69 line 4\n"
				"Unknown word \"SPECIAL\" in KA69 line 5\n"
				"Unknown word \"ACTIVITIES\" in KA69 line 5\n"
				"Unknown word \"AUG\" in KA69 line 5\n"
				"Unknown word \"TO\" in KA69 line 5\n"
				"Unknown word \"SEP\" in KA69 line 5\n"
				"Unknown word \"NAVIGATION\" in KA69 line 6\n"
				"Unknown word \"PROHIBITED\" in KA69 line 6\n"
				"Unknown word \"IN\" in KA69 line 6\n"
				"Unknown word \"TERRITORIAL\" in KA69 line 6\n"
				"Unknown word \"WATERS\" in KA69 line 6\n"
				"Unknown word \"DANGEROUS\" in KA69 line 7\n"
				"Unknown word \"OUTSIDE\" in KA69 line 7\n"
				"Unknown word \"IN\" in KA69 line 7\n"
				"Unknown word \"AREA\" in KA69 line 7\n"
				"Unknown word \"BOUNDED\" in KA69 line 7\n"
				"Unknown word \"BY\" in KA69 line 7\n"
				"Unknown word \"CANCEL\" in KA69 line 18\n"
				"Unknown word \"THIS\" in KA69 line 18\n"
				"Unknown word \"MESSAGE\" in KA69 line 18\n"
				"Unknown word \"SEP\" in KA69 line 18"
			)
		)


		self.assertIn(f"INFO:A_strict_init:Bough \"{self.MESSAGES_DST1}\" is invalid", case_loggy.output)
		self.assertIn(f"INFO:A_strict_init:Bough \"{self.MESSAGES_DST2}\" is invalid", case_loggy.output)


		self.assertIn(
			f"DEBUG:A_strict_init:No records for \"{self.MESSAGE_3}\", marked as new", case_loggy.output
		)
		self.assertIn(f"DEBUG:A_strict_init:KB00 created by {self.now}", case_loggy.output)
		self.assertNotIn("INFO:A_strict_init:KB00 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:A_strict_init:KB00 failed layout check", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"GALE\" in KB00 line 3", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"MAR\" in KB00 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"NORTH-EASTERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"NORTHERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"GUST\" in KB00 line 5", case_loggy.output)
		self.assertNotIn(f"INFO:A_strict_init:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:A_strict_init:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)


		self.assertIn(
			f"DEBUG:A_strict_init:No records for \"{self.MESSAGE_1}\", marked as new", case_loggy.output
		)
		self.assertIn(f"DEBUG:A_strict_init:KE42 created by {self.now}", case_loggy.output)
		self.assertNotIn("INFO:A_strict_init:KE42 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:A_strict_init:KE42 failed layout check", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"WEATHER\" in KE42 line 3", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"FORECAST\" in KE42 line 3", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"ON\" in KE42 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"MURMAN\" in KE42 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"COAST\" in KE42 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"AT\" in KE42 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"WIND\" in KE42 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"NORTH-WESTERN\" in KE42 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"WESTERN\" in KE42 line 6", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"M/S\" in KE42 line 6", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"VISIBILITY\" in KE42 line 6", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"GOOD\" in KE42 line 6", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"MIST\" in KE42 line 7", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"KM\" in KE42 line 7", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"SEAS\" in KE42 line 7", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"M\" in KE42 line 7", case_loggy.output)
		self.assertNotIn(f"INFO:A_strict_init:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:A_strict_init:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)


		self.assertIn(
			f"DEBUG:A_strict_init:No records for \"{self.MESSAGE_2}\", marked as new", case_loggy.output
		)
		self.assertNotIn("INFO:A_strict_init:KA69 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:A_strict_init:KA69 failed layout check", case_loggy.output)
		self.assertIn(f"DEBUG:A_strict_init:KA69 created by {self.now}", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"UTC\" in KA69 line 2", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"COASTAL\" in KA69 line 3", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"WARNING\" in KA69 line 3", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"MURMANSK\" in KA69 line 3", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"WEST\" in KA69 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"OF\" in KA69 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"NOVAYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"ZEMLYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"ISLANDS\" in KA69 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"SPECIAL\" in KA69 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"ACTIVITIES\" in KA69 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"AUG\" in KA69 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"TO\" in KA69 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"NAVIGATION\" in KA69 line 6", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"PROHIBITED\" in KA69 line 6", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"TERRITORIAL\" in KA69 line 6", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"WATERS\" in KA69 line 6", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"DANGEROUS\" in KA69 line 7", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"OUTSIDE\" in KA69 line 7", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"IN\" in KA69 line 7", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"AREA\" in KA69 line 7", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"BOUNDED\" in KA69 line 7", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"BY\" in KA69 line 7", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"CANCEL\" in KA69 line 18", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"THIS\" in KA69 line 18", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"MESSAGE\" in KA69 line 18", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"SEP\" in KA69 line 18", case_loggy.output)
		self.assertNotIn(f"INFO:A_strict_init:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:A_strict_init:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(
			f"INFO:A_strict_init:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)
		self.assertIn(
			f"INFO:A_strict_init:Shelf \"{self.NAVDROP_BOW}\" successfully produced", case_loggy.output
		)


		self.assertFalse(self.MESSAGES_DST1.is_dir())
		self.assertFalse(self.MESSAGES_DST2.is_dir())
		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_B_notouch_boughs(self):
		sleep(1)

		self.assertFalse(self.MESSAGES_DST1.is_dir())
		self.assertFalse(self.MESSAGES_DST2.is_dir())

		self.MESSAGES_DST1.mkdir()
		self.MESSAGES_DST2.mkdir()

		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "B_notouch_boughs"
		with self.assertLogs("B_notouch_boughs", 10) as case_loggy:

			self.test_case = self.case_object()
			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			# Navshelf.outer_shelf will always have all of them cause silent put.
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertFalse(hasattr(self.test_case.loggy, "current_pool"))


		self.assertNotIn(
			f"INFO:B_notouch_boughs:Bough \"{self.MESSAGES_DST1}\" is invalid", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:B_notouch_boughs:Bough \"{self.MESSAGES_DST2}\" is invalid", case_loggy.output
		)


		# No modification made means message was not processed, just skipped.
		self.assertIn(
			f"DEBUG:B_notouch_boughs:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertIn(
			f"DEBUG:B_notouch_boughs:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output
		)
		self.assertIn(
			f"DEBUG:B_notouch_boughs:No modification made on \"{self.MESSAGE_2}\"", case_loggy.output
		)


		# Despite messages were not processed due to Navshelf didn't find mtime difference
		# from the last time, DraftPeek will see target files don't exist, so grow will occur.
		self.assertIn(f"INFO:B_notouch_boughs:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertIn(f"INFO:B_notouch_boughs:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)
		self.assertIn(f"INFO:B_notouch_boughs:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertIn(f"INFO:B_notouch_boughs:Grown leaf \"{self.DST2_MESSAGE_2}\"", case_loggy.output)
		self.assertIn(f"INFO:B_notouch_boughs:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertIn(f"INFO:B_notouch_boughs:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)


		self.assertIn(f"DEBUG:B_notouch_boughs:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:B_notouch_boughs:Shelf was not modified"),2)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_C_simple_touch(self):
		sleep(1)

		self.fmake(self.MESSAGE_1, self.text_1)

		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "C_simple_touch"
		with self.assertLogs("C_simple_touch", 10) as case_loggy:

			self.test_case = self.case_object()
			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertFalse(hasattr(self.test_case.loggy, "current_pool"))


		self.assertIn(f"DEBUG:C_simple_touch:KE42 created by {self.now}", case_loggy.output)
		self.assertNotIn("INFO:C_simple_touch:KE42 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:C_simple_touch:KE42 failed layout check", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"WEATHER\" in KE42 line 3", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"FORECAST\" in KE42 line 3", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"ON\" in KE42 line 4", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"MURMAN\" in KE42 line 4", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"COAST\" in KE42 line 4", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"AT\" in KE42 line 4", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"WIND\" in KE42 line 5", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"NORTH-WESTERN\" in KE42 line 5", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"WESTERN\" in KE42 line 6", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"M/S\" in KE42 line 6", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"VISIBILITY\" in KE42 line 6", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"GOOD\" in KE42 line 6", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"MIST\" in KE42 line 7", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"KM\" in KE42 line 7", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"SEAS\" in KE42 line 7", case_loggy.output)
		self.assertIn("INFO:C_simple_touch:Pending word \"M\" in KE42 line 7", case_loggy.output)
		self.assertIn(f"INFO:C_simple_touch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertIn(f"INFO:C_simple_touch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(f"DEBUG:C_simple_touch:No modification made on \"{self.MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:C_simple_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:C_simple_touch:Grown leaf \"{self.DST2_MESSAGE_2}\"", case_loggy.output)

		self.assertIn(f"DEBUG:C_simple_touch:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:C_simple_touch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:C_simple_touch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)

		self.assertIn(f"DEBUG:C_simple_touch:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:C_simple_touch:Shelf was not modified"),1)
		self.assertIn(
			f"INFO:C_simple_touch:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_D_knowns_touch(self):
		sleep(1)

		self.fmake(self.MESSAGE_2, self.text_2)

		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "D_knowns_touch"
		with self.assertLogs("D_knowns_touch", 10) as case_loggy:

			self.test_case = self.case_object()
			for word,_ in self.test_case.perform.Navbow : self.test_case.perform.Navbow[word] = 1
			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),48)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertFalse(hasattr(self.test_case.loggy, "current_pool"))


		self.assertIn(f"DEBUG:D_knowns_touch:KA69 created by {self.now}", case_loggy.output)
		self.assertNotIn("INFO:D_knowns_touch:KA69 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:D_knowns_touch:KA69 failed layout check", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"UTC\" in KA69 line 2", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"COASTAL\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"WARNING\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"MURMANSK\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"WEST\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"OF\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"NOVAYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"ZEMLYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"ISLANDS\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"SPECIAL\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"ACTIVITIES\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"AUG\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"TO\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"NAVIGATION\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"PROHIBITED\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"TERRITORIAL\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"WATERS\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"DANGEROUS\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"OUTSIDE\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"IN\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"AREA\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"BOUNDED\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"BY\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"CANCEL\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"THIS\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"MESSAGE\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:D_knowns_touch:Known word \"SEP\" in KA69 line 18", case_loggy.output)
		self.assertIn(f"INFO:D_knowns_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertIn(f"INFO:D_knowns_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(f"DEBUG:D_knowns_touch:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:D_knowns_touch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:D_knowns_touch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(f"DEBUG:D_knowns_touch:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:D_knowns_touch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:D_knowns_touch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)


		self.assertIn(
			f"INFO:D_knowns_touch:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)
		self.assertIn(
			f"INFO:D_knowns_touch:Shelf \"{self.NAVDROP_BOW}\" successfully produced", case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_E_knowns_notouch(self):
		sleep(1)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "E_knowns_notouch"
		with self.assertLogs("E_knowns_notouch", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertFalse(hasattr(self.test_case.loggy, "current_pool"))


		self.assertIn(
			f"DEBUG:E_knowns_notouch:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertIn(
			f"DEBUG:E_knowns_notouch:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output
		)
		self.assertIn(
			f"DEBUG:E_knowns_notouch:No modification made on \"{self.MESSAGE_2}\"", case_loggy.output
		)


		self.assertNotIn(f"INFO:E_knowns_notouch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:E_knowns_notouch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:E_knowns_notouch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:E_knowns_notouch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:E_knowns_notouch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:E_knowns_notouch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(f"DEBUG:E_knowns_notouch:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:E_knowns_notouch:Shelf was not modified"),2)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_F_sanitize_touch(self):
		sleep(1)

		# Now message will have extra spaces to be trimmed
		self.fmake(

			self.MESSAGE_3,
			str(

				"\n"
				"ZCZC KB00\n"
				f"{self.now.dHM_asjoin} UTC {self.now.b.upper()}\n"
				" GALE WARNING MURMANSK NR85\n"
				"ON MURMAN COAST  01 MAR 17-21 UTC\n"
				"WIND  NORTH-EASTERN NORTHERN GUST\n"
				"15-20 M/S\n"
				"NNNN\n"
			)
		)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "F_sanitize_touch"
		with self.assertLogs("F_sanitize_touch", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertFalse(hasattr(self.test_case.loggy, "current_pool"))


		self.assertIn(f"DEBUG:F_sanitize_touch:KB00 created by {self.now}", case_loggy.output)
		self.assertNotIn("INFO:F_sanitize_touch:KB00 failed structure check", case_loggy.output)
		self.assertIn("INFO:F_sanitize_touch:KB00 failed layout check", case_loggy.output)


		self.assertIn("DEBUG:F_sanitize_touch:Known word \"GALE\" in KB00 line 3", case_loggy.output)
		self.assertIn("DEBUG:F_sanitize_touch:Known word \"MAR\" in KB00 line 4", case_loggy.output)
		self.assertIn("DEBUG:F_sanitize_touch:Known word \"NORTH-EASTERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("DEBUG:F_sanitize_touch:Known word \"NORTHERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("DEBUG:F_sanitize_touch:Known word \"GUST\" in KB00 line 5", case_loggy.output)


		self.assertIn(f"INFO:F_sanitize_touch:Source file \"{self.MESSAGE_3}\" rewritten", case_loggy.output)
		self.assertIn(f"INFO:F_sanitize_touch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertIn(f"INFO:F_sanitize_touch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)

		self.assertIn(f"DEBUG:F_sanitize_touch:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:F_sanitize_touch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:F_sanitize_touch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(f"DEBUG:F_sanitize_touch:No modification made on \"{self.MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:F_sanitize_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:F_sanitize_touch:Grown leaf \"{self.DST2_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(f"DEBUG:F_sanitize_touch:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:F_sanitize_touch:Shelf was not modified"),1)
		self.assertIn(
			f"INFO:F_sanitize_touch:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_G_structure_touch(self):
		sleep(1)

		# Now message will have structure that will no match regex
		self.fmake(

			self.MESSAGE_1,
			str(

				"ZCZC KE42\n"
				f"{self.now.dHM_asjoin} UTC {self.now.b.upper()}\n"
				"MURMANSK WEATHER FORECAST\n"
				"ON MURMAN COAST AT 06 UTC\n"
				"TO 18 UTC 01 SEP WIND NORTH-WESTERN\n"
				"WESTERN 8-13 M/S VISIBILITY GOOD\n"
				"IN TO MIST 1-2 KM SEAS 1,5-2,0 M\n"
				"NNNN"
			)
		)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "G_structure_touch"
		with self.assertLogs("G_structure_touch", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertFalse(hasattr(self.test_case.loggy, "current_pool"))


		self.assertIn(f"DEBUG:G_structure_touch:KE42 created by {self.now}", case_loggy.output)
		self.assertIn("INFO:G_structure_touch:KE42 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:G_structure_touch:KE42 failed layout check", case_loggy.output)


		self.assertIn("DEBUG:G_structure_touch:Known word \"WEATHER\" in KE42 line 3", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"FORECAST\" in KE42 line 3", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"ON\" in KE42 line 4", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"MURMAN\" in KE42 line 4", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"COAST\" in KE42 line 4", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"AT\" in KE42 line 4", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"WIND\" in KE42 line 5", case_loggy.output)
		self.assertIn(
			"DEBUG:G_structure_touch:Known word \"NORTH-WESTERN\" in KE42 line 5", case_loggy.output
		)
		self.assertIn("DEBUG:G_structure_touch:Known word \"WESTERN\" in KE42 line 6", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"M/S\" in KE42 line 6", case_loggy.output)
		self.assertIn(
			"DEBUG:G_structure_touch:Known word \"VISIBILITY\" in KE42 line 6", case_loggy.output
		)
		self.assertIn("DEBUG:G_structure_touch:Known word \"GOOD\" in KE42 line 6", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"MIST\" in KE42 line 7", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"KM\" in KE42 line 7", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"SEAS\" in KE42 line 7", case_loggy.output)
		self.assertIn("DEBUG:G_structure_touch:Known word \"M\" in KE42 line 7", case_loggy.output)


		self.assertIn(f"INFO:G_structure_touch:Source file \"{self.MESSAGE_1}\" rewritten", case_loggy.output)
		self.assertIn(f"INFO:G_structure_touch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertIn(f"INFO:G_structure_touch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(
			f"DEBUG:G_structure_touch:No modification made on \"{self.MESSAGE_2}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:G_structure_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:G_structure_touch:Grown leaf \"{self.DST2_MESSAGE_2}\"", case_loggy.output)

		self.assertIn(
			f"DEBUG:G_structure_touch:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:G_structure_touch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:G_structure_touch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)


		self.assertIn(f"DEBUG:G_structure_touch:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:G_structure_touch:Shelf was not modified"),1)
		self.assertIn(
			f"INFO:G_structure_touch:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_H_header_touch(self):
		sleep(1)

		self.fmake(

			self.MESSAGE_2,
			str(

				"\n"
				"ZC KA69\n"
				f"{self.now.dHM_asjoin} UTC {self.now.b.upper()} {self.now.y}\n"
				"COASTAL WARNING MURMANSK 270\n"
				"WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"76-00.0N 056-30.0E\n"
				"76-00.0N 058-00.0E\n"
				"75-23.0N 056-00.0E\n"
				"75-12.0N 055-05.0E\n"
				"73-45.0N 052-58.0E\n"
				"72-45.0N 051-45.0E\n"
				"72-00.0N 050-50.0E\n"
				"72-00.0N 050-00.0E\n"
				"74-00.0N 050-00.0E\n"
				"75-25.0N 052-45.0E\n"
				"2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"NNNN\n"
			)
		)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "H_header_touch"
		with self.assertLogs("H_header_touch", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertTrue(hasattr(self.test_case.loggy, "current_pool"))
		self.assertEqual(

			self.test_case.loggy.current_pool,
			str(
				"KA69.TLX\n"
				"1    ZC KA69\n"
				f"2    {self.now.dHM_asjoin} UTC {self.now.b.upper()} {self.now.y}\n"
				"3    COASTAL WARNING MURMANSK 270\n"
				"4    WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"5    1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"6    NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"7    DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"8    76-00.0N 056-30.0E\n"
				"9    76-00.0N 058-00.0E\n"
				"10   75-23.0N 056-00.0E\n"
				"11   75-12.0N 055-05.0E\n"
				"12   73-45.0N 052-58.0E\n"
				"13   72-45.0N 051-45.0E\n"
				"14   72-00.0N 050-50.0E\n"
				"15   72-00.0N 050-00.0E\n"
				"16   74-00.0N 050-00.0E\n"
				"17   75-25.0N 052-45.0E\n"
				"18   2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"19   NNNN\n"
				"\n"
				"Incorrect NAVTEX header \"ZC KA69\" in KA69.TLX"
			)
		)


		self.assertIn(f"DEBUG:H_header_touch:KA69.TLX created by {self.now}", case_loggy.output)
		self.assertNotIn("INFO:H_header_touch:KA69.TLX failed structure check", case_loggy.output)
		self.assertNotIn("INFO:H_header_touch:KA69.TLX failed layout check", case_loggy.output)


		self.assertIn("DEBUG:H_header_touch:Known word \"UTC\" in KA69.TLX line 2", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"COASTAL\" in KA69.TLX line 3", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"WARNING\" in KA69.TLX line 3", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"MURMANSK\" in KA69.TLX line 3", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"WEST\" in KA69.TLX line 4", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"OF\" in KA69.TLX line 4", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"NOVAYA\" in KA69.TLX line 4", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"ZEMLYA\" in KA69.TLX line 4", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"ISLANDS\" in KA69.TLX line 4", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"SPECIAL\" in KA69.TLX line 5", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"ACTIVITIES\" in KA69.TLX line 5", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"AUG\" in KA69.TLX line 5", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"TO\" in KA69.TLX line 5", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"NAVIGATION\" in KA69.TLX line 6", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"PROHIBITED\" in KA69.TLX line 6", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"TERRITORIAL\" in KA69.TLX line 6", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"WATERS\" in KA69.TLX line 6", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"DANGEROUS\" in KA69.TLX line 7", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"OUTSIDE\" in KA69.TLX line 7", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"IN\" in KA69.TLX line 7", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"AREA\" in KA69.TLX line 7", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"BOUNDED\" in KA69.TLX line 7", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"BY\" in KA69.TLX line 7", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"CANCEL\" in KA69.TLX line 18", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"THIS\" in KA69.TLX line 18", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"MESSAGE\" in KA69.TLX line 18", case_loggy.output)
		self.assertIn("DEBUG:H_header_touch:Known word \"SEP\" in KA69.TLX line 18", case_loggy.output)


		self.assertIn(f"INFO:H_header_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertIn(f"INFO:H_header_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(
			f"DEBUG:H_header_touch:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:H_header_touch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:H_header_touch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(
			f"DEBUG:H_header_touch:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:H_header_touch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:H_header_touch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)


		self.assertIn(f"DEBUG:H_header_touch:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:H_header_touch:Shelf was not modified"),1)
		self.assertIn(
			f"INFO:H_header_touch:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_I_header_repeat(self):
		sleep(1)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "I_header_repeat"
		with self.assertLogs("I_header_repeat", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertFalse(hasattr(self.test_case.loggy, "current_pool"))


		self.assertIn(
			f"DEBUG:I_header_repeat:No modification made on \"{self.MESSAGE_2}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:I_header_repeat:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:I_header_repeat:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(
			f"DEBUG:I_header_repeat:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:I_header_repeat:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:I_header_repeat:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(
			f"DEBUG:I_header_repeat:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:I_header_repeat:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:I_header_repeat:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)


		self.assertIn(f"DEBUG:I_header_repeat:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:I_header_repeat:Shelf was not modified"),2)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_J_CDT_touch(self):
		sleep(1)


		self.fmake(

			self.MESSAGE_2,
			str(

				"\n"
				"ZCZC KA69\n"
				f"{self.now.dHM_asjoin} {self.now.b.upper()} {self.now.y}\n"
				"COASTAL WARNING MURMANSK 270\n"
				"WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"76-00.0N 056-30.0E\n"
				"76-00.0N 058-00.0E\n"
				"75-23.0N 056-00.0E\n"
				"75-12.0N 055-05.0E\n"
				"73-45.0N 052-58.0E\n"
				"72-45.0N 051-45.0E\n"
				"72-00.0N 050-50.0E\n"
				"72-00.0N 050-00.0E\n"
				"74-00.0N 050-00.0E\n"
				"75-25.0N 052-45.0E\n"
				"2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"NNNN\n"
			)
		)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "J_CDT_touch"
		with self.assertLogs("J_CDT_touch", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertTrue(hasattr(self.test_case.loggy, "current_pool"))
		self.assertEqual(

			self.test_case.loggy.current_pool,
			str(
				"KA69\n"
				"1    ZCZC KA69\n"
				f"2    {self.now.dHM_asjoin} {self.now.b.upper()} {self.now.y}\n"
				"3    COASTAL WARNING MURMANSK 270\n"
				"4    WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"5    1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"6    NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"7    DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"8    76-00.0N 056-30.0E\n"
				"9    76-00.0N 058-00.0E\n"
				"10   75-23.0N 056-00.0E\n"
				"11   75-12.0N 055-05.0E\n"
				"12   73-45.0N 052-58.0E\n"
				"13   72-45.0N 051-45.0E\n"
				"14   72-00.0N 050-50.0E\n"
				"15   72-00.0N 050-00.0E\n"
				"16   74-00.0N 050-00.0E\n"
				"17   75-25.0N 052-45.0E\n"
				"18   2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"19   NNNN\n"
				"\n"
				"CDT not found in KA69\n"
				"No line looks like message creation timestamp in KA69"
			)
		)


		self.assertIn(f"INFO:J_CDT_touch:CDT not found in KA69", case_loggy.output)
		self.assertIn(
			f"INFO:J_CDT_touch:No line looks like message creation timestamp in KA69", case_loggy.output
		)


		self.assertNotIn("INFO:J_CDT_touch:KA69 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:J_CDT_touch:KA69 failed layout check", case_loggy.output)


		self.assertIn("DEBUG:J_CDT_touch:Known word \"COASTAL\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"WARNING\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"MURMANSK\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"WEST\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"OF\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"NOVAYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"ZEMLYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"ISLANDS\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"SPECIAL\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"ACTIVITIES\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"AUG\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"TO\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"NAVIGATION\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"PROHIBITED\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"TERRITORIAL\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"WATERS\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"DANGEROUS\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"OUTSIDE\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"IN\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"AREA\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"BOUNDED\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"BY\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"CANCEL\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"THIS\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"MESSAGE\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:J_CDT_touch:Known word \"SEP\" in KA69 line 18", case_loggy.output)


		self.assertIn(f"INFO:J_CDT_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertIn(f"INFO:J_CDT_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(
			f"DEBUG:J_CDT_touch:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:J_CDT_touch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:J_CDT_touch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(
			f"DEBUG:J_CDT_touch:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:J_CDT_touch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:J_CDT_touch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)


		self.assertIn(f"DEBUG:J_CDT_touch:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:J_CDT_touch:Shelf was not modified"),1)
		self.assertIn(
			f"INFO:J_CDT_touch:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_K_CDT_out_touch(self):

		sleep(1)
		before = self.now.sight(months=-1)


		self.fmake(

			self.MESSAGE_2,
			str(

				"\n"
				"ZCZC KA69\n"
				f"{before.dHM_asjoin} UTC {before.b.upper()} {before.y}\n"
				"COASTAL WARNING MURMANSK 270\n"
				"WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"76-00.0N 056-30.0E\n"
				"76-00.0N 058-00.0E\n"
				"75-23.0N 056-00.0E\n"
				"75-12.0N 055-05.0E\n"
				"73-45.0N 052-58.0E\n"
				"72-45.0N 051-45.0E\n"
				"72-00.0N 050-50.0E\n"
				"72-00.0N 050-00.0E\n"
				"74-00.0N 050-00.0E\n"
				"75-25.0N 052-45.0E\n"
				"2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"NNNN\n"
			)
		)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "K_CDT_out_touch"
		with self.assertLogs("K_CDT_out_touch", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertTrue(hasattr(self.test_case.loggy, "current_pool"))
		self.assertEqual(

			self.test_case.loggy.current_pool,
			str(
				"KA69\n"
				"1    ZCZC KA69\n"
				f"2    {before.dHM_asjoin} UTC {before.b.upper()} {before.y}\n"
				"3    COASTAL WARNING MURMANSK 270\n"
				"4    WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"5    1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"6    NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"7    DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"8    76-00.0N 056-30.0E\n"
				"9    76-00.0N 058-00.0E\n"
				"10   75-23.0N 056-00.0E\n"
				"11   75-12.0N 055-05.0E\n"
				"12   73-45.0N 052-58.0E\n"
				"13   72-45.0N 051-45.0E\n"
				"14   72-00.0N 050-50.0E\n"
				"15   72-00.0N 050-00.0E\n"
				"16   74-00.0N 050-00.0E\n"
				"17   75-25.0N 052-45.0E\n"
				"18   2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"19   NNNN\n"
				"\n"
				f"CDT line \"{before.dHM_asjoin} UTC {before.b.upper()} {before.y}\" "
				"doesn't match current date in KA69"
			)
		)


		self.assertIn(f"DEBUG:K_CDT_out_touch:KA69 created by {before}", case_loggy.output)
		self.assertIn(

			f"INFO:K_CDT_out_touch:CDT line \"{before.dHM_asjoin} UTC {before.b.upper()} {before.y}\" "
			"doesn't match current date in KA69",
			case_loggy.output
		)


		self.assertNotIn("INFO:K_CDT_out_touch:KA69 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:K_CDT_out_touch:KA69 failed layout check", case_loggy.output)


		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"UTC\" in KA69 line 2", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"COASTAL\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"WARNING\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"MURMANSK\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"WEST\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"OF\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"NOVAYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"ZEMLYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"ISLANDS\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"SPECIAL\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"ACTIVITIES\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"AUG\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"TO\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"NAVIGATION\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"PROHIBITED\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"TERRITORIAL\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"WATERS\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"DANGEROUS\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"OUTSIDE\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"IN\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"AREA\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"BOUNDED\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"BY\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"CANCEL\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"THIS\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"MESSAGE\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:K_CDT_out_touch:Known word \"SEP\" in KA69 line 18", case_loggy.output)


		self.assertIn(f"INFO:K_CDT_out_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertIn(f"INFO:K_CDT_out_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(
			f"DEBUG:K_CDT_out_touch:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:K_CDT_out_touch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:K_CDT_out_touch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(
			f"DEBUG:K_CDT_out_touch:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(f"INFO:K_CDT_out_touch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertNotIn(f"INFO:K_CDT_out_touch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)


		self.assertIn(f"DEBUG:K_CDT_out_touch:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:K_CDT_out_touch:Shelf was not modified"),1)
		self.assertIn(
			f"INFO:K_CDT_out_touch:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_L_CDT_out_repeat_touch(self):

		sleep(1)
		before = self.now.sight(months=-1, days=-1)


		# Same message but even more earlier timestamp
		self.fmake(

			self.MESSAGE_2,
			str(

				"\n"
				"ZCZC KA69\n"
				f"{before.dHM_asjoin} UTC {before.b.upper()} {before.y}\n"
				"COASTAL WARNING MURMANSK 270\n"
				"WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"76-00.0N 056-30.0E\n"
				"76-00.0N 058-00.0E\n"
				"75-23.0N 056-00.0E\n"
				"75-12.0N 055-05.0E\n"
				"73-45.0N 052-58.0E\n"
				"72-45.0N 051-45.0E\n"
				"72-00.0N 050-50.0E\n"
				"72-00.0N 050-00.0E\n"
				"74-00.0N 050-00.0E\n"
				"75-25.0N 052-45.0E\n"
				"2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"NNNN\n"
			)
		)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "L_CDT_out_repeat_touch"
		with self.assertLogs("L_CDT_out_repeat_touch", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertTrue(hasattr(self.test_case.loggy, "current_pool"))
		self.assertEqual(

			self.test_case.loggy.current_pool,
			str(
				"KA69\n"
				"1    ZCZC KA69\n"
				f"2    {before.dHM_asjoin} UTC {before.b.upper()} {before.y}\n"
				"3    COASTAL WARNING MURMANSK 270\n"
				"4    WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"5    1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"6    NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"7    DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"8    76-00.0N 056-30.0E\n"
				"9    76-00.0N 058-00.0E\n"
				"10   75-23.0N 056-00.0E\n"
				"11   75-12.0N 055-05.0E\n"
				"12   73-45.0N 052-58.0E\n"
				"13   72-45.0N 051-45.0E\n"
				"14   72-00.0N 050-50.0E\n"
				"15   72-00.0N 050-00.0E\n"
				"16   74-00.0N 050-00.0E\n"
				"17   75-25.0N 052-45.0E\n"
				"18   2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"19   NNNN\n"
				"\n"
				f"CDT line \"{before.dHM_asjoin} UTC {before.b.upper()} {before.y}\" "
				"doesn't match current date in KA69"
			)
		)


		self.assertIn(f"DEBUG:L_CDT_out_repeat_touch:KA69 created by {before}", case_loggy.output)
		self.assertIn(

			f"INFO:L_CDT_out_repeat_touch:CDT line \"{before.dHM_asjoin} UTC {before.b.upper()} {before.y}\" "
			"doesn't match current date in KA69",
			case_loggy.output
		)


		self.assertNotIn("INFO:L_CDT_out_repeat_touch:KA69 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:L_CDT_out_repeat_touch:KA69 failed layout check", case_loggy.output)


		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"UTC\" in KA69 line 2", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"COASTAL\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"WARNING\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"MURMANSK\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"WEST\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"OF\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"NOVAYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"ZEMLYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"ISLANDS\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"SPECIAL\" in KA69 line 5", case_loggy.output)
		self.assertIn(
			"DEBUG:L_CDT_out_repeat_touch:Known word \"ACTIVITIES\" in KA69 line 5", case_loggy.output
		)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"AUG\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"TO\" in KA69 line 5", case_loggy.output)
		self.assertIn(
			"DEBUG:L_CDT_out_repeat_touch:Known word \"NAVIGATION\" in KA69 line 6", case_loggy.output
		)
		self.assertIn(
			"DEBUG:L_CDT_out_repeat_touch:Known word \"PROHIBITED\" in KA69 line 6", case_loggy.output
		)
		self.assertIn(
			"DEBUG:L_CDT_out_repeat_touch:Known word \"TERRITORIAL\" in KA69 line 6", case_loggy.output
		)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"WATERS\" in KA69 line 6", case_loggy.output)
		self.assertIn(
			"DEBUG:L_CDT_out_repeat_touch:Known word \"DANGEROUS\" in KA69 line 7", case_loggy.output
		)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"OUTSIDE\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"IN\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"AREA\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"BOUNDED\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"BY\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"CANCEL\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"THIS\" in KA69 line 18", case_loggy.output)
		self.assertIn(
			"DEBUG:L_CDT_out_repeat_touch:Known word \"MESSAGE\" in KA69 line 18", case_loggy.output
		)
		self.assertIn("DEBUG:L_CDT_out_repeat_touch:Known word \"SEP\" in KA69 line 18", case_loggy.output)


		self.assertIn(f"INFO:L_CDT_out_repeat_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertIn(f"INFO:L_CDT_out_repeat_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(
			f"DEBUG:L_CDT_out_repeat_touch:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:L_CDT_out_repeat_touch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:L_CDT_out_repeat_touch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output
		)

		self.assertIn(
			f"DEBUG:L_CDT_out_repeat_touch:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:L_CDT_out_repeat_touch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:L_CDT_out_repeat_touch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output
		)


		self.assertIn(f"DEBUG:L_CDT_out_repeat_touch:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:L_CDT_out_repeat_touch:Shelf was not modified"),1)
		self.assertIn(

			f"INFO:L_CDT_out_repeat_touch:Shelf \"{self.NAVDROP_SHELF}\" successfully produced",
			case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_M_CDT_back_touch(self):

		sleep(1)
		self.fmake(self.MESSAGE_2, self.text_2)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "M_CDT_back_touch"
		with self.assertLogs("M_CDT_back_touch", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertTrue(hasattr(self.test_case.loggy, "current_pool"))
		self.assertEqual(

			self.test_case.loggy.current_pool,
			str(
				"new message KA69\n"
				"1    ZCZC KA69\n"
				f"2    {self.now.dHM_asjoin} UTC {self.now.b.upper()} {self.now.y}\n"
				"3    COASTAL WARNING MURMANSK 270\n"
				"4    WEST OF NOVAYA ZEMLYA ISLANDS\n"
				"5    1. SPECIAL ACTIVITIES 312100 AUG TO 302100 SEP\n"
				"6    NAVIGATION PROHIBITED IN TERRITORIAL WATERS\n"
				"7    DANGEROUS OUTSIDE IN AREA BOUNDED BY\n"
				"8    76-00.0N 056-30.0E\n"
				"9    76-00.0N 058-00.0E\n"
				"10   75-23.0N 056-00.0E\n"
				"11   75-12.0N 055-05.0E\n"
				"12   73-45.0N 052-58.0E\n"
				"13   72-45.0N 051-45.0E\n"
				"14   72-00.0N 050-50.0E\n"
				"15   72-00.0N 050-00.0E\n"
				"16   74-00.0N 050-00.0E\n"
				"17   75-25.0N 052-45.0E\n"
				"18   2. CANCEL THIS MESSAGE 302200 SEP 24\n"
				"19   NNNN"
			)
		)



		self.assertIn(f"DEBUG:M_CDT_back_touch:KA69 created by {self.now}", case_loggy.output)
		self.assertNotIn("INFO:M_CDT_back_touch:KA69 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:M_CDT_back_touch:KA69 failed layout check", case_loggy.output)


		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"UTC\" in KA69 line 2", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"COASTAL\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"WARNING\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"MURMANSK\" in KA69 line 3", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"WEST\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"OF\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"NOVAYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"ZEMLYA\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"ISLANDS\" in KA69 line 4", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"SPECIAL\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"ACTIVITIES\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"AUG\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"TO\" in KA69 line 5", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"NAVIGATION\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"PROHIBITED\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"TERRITORIAL\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"WATERS\" in KA69 line 6", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"DANGEROUS\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"OUTSIDE\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"IN\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"AREA\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"BOUNDED\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"BY\" in KA69 line 7", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"CANCEL\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"THIS\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"MESSAGE\" in KA69 line 18", case_loggy.output)
		self.assertIn("DEBUG:M_CDT_back_touch:Known word \"SEP\" in KA69 line 18", case_loggy.output)


		self.assertIn(f"INFO:M_CDT_back_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertIn(f"INFO:M_CDT_back_touch:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(
			f"DEBUG:M_CDT_back_touch:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:M_CDT_back_touch:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:M_CDT_back_touch:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output
		)

		self.assertIn(
			f"DEBUG:M_CDT_back_touch:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:M_CDT_back_touch:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:M_CDT_back_touch:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output
		)


		self.assertIn(f"DEBUG:M_CDT_back_touch:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:M_CDT_back_touch:Shelf was not modified"),1)
		self.assertIn(

			f"INFO:M_CDT_back_touch:Shelf \"{self.NAVDROP_SHELF}\" successfully produced",
			case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_N_one_src_out(self):
		sleep(1)


		self.assertTrue(self.MESSAGE_3.is_file())
		self.MESSAGE_3.unlink()
		self.assertFalse(self.MESSAGE_3.is_file())


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "N_one_src_out"
		with self.assertLogs("N_one_src_out", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),2)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertFalse(hasattr(self.test_case.loggy, "current_pool"))


		self.assertIn(
			f"DEBUG:N_one_src_out:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:N_one_src_out:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:N_one_src_out:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output
		)


		self.assertIn(
			f"DEBUG:N_one_src_out:No modification made on \"{self.MESSAGE_2}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:N_one_src_out:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:N_one_src_out:Grown leaf \"{self.DST2_MESSAGE_2}\"", case_loggy.output
		)


		self.assertNotIn(
			f"DEBUG:N_one_src_out:No modification made on \"{self.MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:N_one_src_out:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output
		)
		self.assertNotIn(
			f"INFO:N_one_src_out:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output
		)
		self.assertIn(
			f"INFO:N_one_src_out:Trimmed leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output
		)
		self.assertIn(
			f"INFO:N_one_src_out:Trimmed leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output
		)


		self.assertIn(f"DEBUG:N_one_src_out:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:N_one_src_out:Shelf was not modified"),1)
		self.assertIn(

			f"INFO:N_one_src_out:Shelf \"{self.NAVDROP_SHELF}\" successfully produced",
			case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertFalse(self.MESSAGE_3.is_file())
		self.assertFalse(self.DST1_MESSAGE_3.is_file())
		self.assertFalse(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_O_src_back_EOS(self):
		sleep(1)


		# No EOS (NNNN)
		self.fmake(

			self.MESSAGE_3,
			str(

				"\n"
				"ZCZC KB00\n"
				f"{self.now.dHM_asjoin} UTC {self.now.b.upper()}\n"
				"GALE WARNING MURMANSK NR85\n"
				"ON MURMAN COAST 01 MAR 17-21 UTC\n"
				"WIND NORTH-EASTERN NORTHERN GUST\n"
				"15-20 M/S\n"
			)
		)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "O_src_back_EOS"
		with self.assertLogs("O_src_back_EOS", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),2)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertTrue(hasattr(self.test_case.loggy, "current_pool"))
		self.assertEqual(

			self.test_case.loggy.current_pool,
			str(

				"new message KB00\n"
				"1    ZCZC KB00\n"
				f"2    {self.now.dHM_asjoin} UTC {self.now.b.upper()}\n"
				"3    GALE WARNING MURMANSK NR85\n"
				"4    ON MURMAN COAST 01 MAR 17-21 UTC\n"
				"5    WIND NORTH-EASTERN NORTHERN GUST\n"
				"6    15-20 M/S\n"
				"\n"
				"Incorrect EOS line \"15-20 M/S\" in KB00"
			)
		)


		self.assertIn(
			f"DEBUG:O_src_back_EOS:No records for \"{self.MESSAGE_3}\", marked as new", case_loggy.output
		)
		self.assertNotIn("INFO:O_src_back_EOS:KB00 failed structure check", case_loggy.output)
		self.assertNotIn("INFO:O_src_back_EOS:KB00 failed layout check", case_loggy.output)
		self.assertIn(f"DEBUG:O_src_back_EOS:KB00 created by {self.now}", case_loggy.output)


		self.assertIn("DEBUG:O_src_back_EOS:Known word \"GALE\" in KB00 line 3", case_loggy.output)
		self.assertIn("DEBUG:O_src_back_EOS:Known word \"MAR\" in KB00 line 4", case_loggy.output)
		self.assertIn("DEBUG:O_src_back_EOS:Known word \"NORTH-EASTERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("DEBUG:O_src_back_EOS:Known word \"NORTHERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("DEBUG:O_src_back_EOS:Known word \"GUST\" in KB00 line 5", case_loggy.output)


		self.assertIn("INFO:O_src_back_EOS:Incorrect EOS line \"15-20 M/S\" in KB00", case_loggy.output)


		self.assertIn(f"INFO:O_src_back_EOS:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertIn(f"INFO:O_src_back_EOS:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)

		self.assertIn(f"DEBUG:O_src_back_EOS:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:O_src_back_EOS:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:O_src_back_EOS:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(f"DEBUG:O_src_back_EOS:No modification made on \"{self.MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:O_src_back_EOS:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:O_src_back_EOS:Grown leaf \"{self.DST2_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(f"DEBUG:O_src_back_EOS:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:O_src_back_EOS:Shelf was not modified"),1)
		self.assertIn(
			f"INFO:O_src_back_EOS:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








	def test_P_EOS_sanit(self):
		sleep(1)


		self.fmake(

			self.MESSAGE_3,
			str(

				"\n"
				"ZCZC  KB00\n"
				f"{self.now.dHM_asjoin} UTC {self.now.b.upper()}\n"
				"\n"
				"GALE WARNING MURMANSK NR85\n"
				"ON MURMAN COAST 01 MAR 17-21 UTC\n"
				"	WIND NORTH-EASTERN NORTHERN GUST\n"
				" 15-20 M/S\n"
				"NNNN\n"
			)
		)


		self.assertTrue(self.MESSAGES_DST1.is_dir())
		self.assertTrue(self.MESSAGES_DST2.is_dir())

		self.assertTrue(self.NAVDROP_SHELF.is_file())
		self.assertTrue(self.NAVDROP_BOW.is_file())


		self.case_object.loggy.init_name = "P_EOS_sanit"
		with self.assertLogs("P_EOS_sanit", 10) as case_loggy:

			self.test_case = self.case_object()

			for word,_ in self.test_case.perform.Navbow:
				with self.subTest(word=word): self.assertEqual(self.test_case.perform.Navbow[word],1)

			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow),48)
			self.assertEqual(len(self.test_case.perform.Navbow()),0)
			self.assertEqual(len(self.test_case.perform.Navshelf),3)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(self.test_case.perform.Navshelf.diff)
			)


		self.no_loggy_levels(case_loggy.output, 30,40,50)
		self.assertFalse(hasattr(self.test_case.loggy, "current_pool"))


		self.assertIn("INFO:P_EOS_sanit:KB00 failed structure check", case_loggy.output)
		self.assertIn("INFO:P_EOS_sanit:KB00 failed layout check", case_loggy.output)
		self.assertIn(f"DEBUG:P_EOS_sanit:KB00 created by {self.now}", case_loggy.output)


		self.assertIn("DEBUG:P_EOS_sanit:Known word \"GALE\" in KB00 line 3", case_loggy.output)
		self.assertIn("DEBUG:P_EOS_sanit:Known word \"MAR\" in KB00 line 4", case_loggy.output)
		self.assertIn("DEBUG:P_EOS_sanit:Known word \"NORTH-EASTERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("DEBUG:P_EOS_sanit:Known word \"NORTHERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("DEBUG:P_EOS_sanit:Known word \"GUST\" in KB00 line 5", case_loggy.output)


		self.assertIn(f"INFO:P_EOS_sanit:Source file \"{self.MESSAGE_3}\" rewritten", case_loggy.output)
		self.assertIn(f"INFO:P_EOS_sanit:Grown leaf \"{self.DST1_MESSAGE_3}\"", case_loggy.output)
		self.assertIn(f"INFO:P_EOS_sanit:Grown leaf \"{self.DST2_MESSAGE_3}\"", case_loggy.output)

		self.assertIn(f"DEBUG:P_EOS_sanit:No modification made on \"{self.MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:P_EOS_sanit:Grown leaf \"{self.DST1_MESSAGE_1}\"", case_loggy.output)
		self.assertNotIn(f"INFO:P_EOS_sanit:Grown leaf \"{self.DST2_MESSAGE_1}\"", case_loggy.output)

		self.assertIn(f"DEBUG:P_EOS_sanit:No modification made on \"{self.MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:P_EOS_sanit:Grown leaf \"{self.DST1_MESSAGE_2}\"", case_loggy.output)
		self.assertNotIn(f"INFO:P_EOS_sanit:Grown leaf \"{self.DST2_MESSAGE_2}\"", case_loggy.output)


		self.assertIn(f"DEBUG:P_EOS_sanit:Shelf was not modified", case_loggy.output)
		self.assertEqual(case_loggy.output.count(f"DEBUG:P_EOS_sanit:Shelf was not modified"),1)
		self.assertIn(
			f"INFO:P_EOS_sanit:Shelf \"{self.NAVDROP_SHELF}\" successfully produced", case_loggy.output
		)


		self.assertTrue(self.MESSAGE_1.is_file())
		self.assertTrue(self.DST1_MESSAGE_1.is_file())
		self.assertTrue(self.DST2_MESSAGE_1.is_file())

		self.assertTrue(self.MESSAGE_2.is_file())
		self.assertTrue(self.DST1_MESSAGE_2.is_file())
		self.assertTrue(self.DST2_MESSAGE_2.is_file())

		self.assertTrue(self.MESSAGE_3.is_file())
		self.assertTrue(self.DST1_MESSAGE_3.is_file())
		self.assertTrue(self.DST2_MESSAGE_3.is_file())

		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








if	__name__ == "__main__" : unittest.main(verbosity=2)







