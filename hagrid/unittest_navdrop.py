import	os
import	unittest
from	pathlib								import Path
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

		cls.now = TimeTurner(timepoint="0420")

		# All messages are well structured (for UDK2) and actual at the first place
		text_1 = str(

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


		text_2 = str(

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


		text_3 = str(

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


		cls.fmake(cls, cls.MESSAGE_1, text_1)
		cls.fmake(cls, cls.MESSAGE_2, text_2)
		cls.fmake(cls, cls.MESSAGE_3, text_3)




		class Navdrop(Copse):
			class loggy(LibraryContrib):

				init_level	= 10
				init_name	= "Navdrop"
				handler		= str(cls.NAVDROP_LOGGY)

			class Boughs(Copse):
				class dst1(Tree):	bough = cls.MESSAGES_DST1
				class dst2(Tree):	bough = cls.MESSAGES_DST2
				class leafs(SiftingController):
					include = (

						rf".+{os.sep}[Kk][A-Za-z]\d\d\.[Tt][Ll][Xx]",
						rf"{cls.MESSAGES_DST1}{os.sep}.+",
						rf"{cls.MESSAGES_DST2}{os.sep}.+",
					)
				class twigs(SiftingController):
					include = (

						rf"{cls.MESSAGES_DST1}{os.sep}.+",
						rf"{cls.MESSAGES_DST2}{os.sep}.+",
					)

			@DraftPeek(renew=False)
			class grow(LeafGrowth):		pass
			class rejuve(Rejuvenation):	pass

			class trim(SprigTrimmer):	pass
			class effloresce(Efflorescence):
				branches = {

					str(cls.MESSAGES_DST1):	str(cls.MESSAGES_SRC),
					str(cls.MESSAGES_DST2):	str(cls.MESSAGES_SRC),
				}

			@fssprout(str(cls.MESSAGES_SRC))
			@Navpreprocessor("K")
			class perform(Flourish):

				class Navfiles(SiftingController):	include = r".+/[Kk][A-Za-z]\d\d\.[tT][lL][xX]",
				class Navbow(LibraryShelf):

					grabbing	= str(cls.NAVDROP_BOW)
					reclaiming	= True

				class Navshelf(LibraryShelf):

					grabbing	= str(cls.NAVDROP_SHELF)
					reclaiming	= True




		cls.make_loggy_file(cls, cls.NAVDROP_LOGGY)
		cls.test_case = Navdrop








	# @classmethod
	# def tearDownClass(cls):

	# 	if	hasattr(cls, "MESSAGE_1") and isinstance(Path, cls.MESSAGE_1) and cls.MESSAGE_1.is_file():
	# 		cls.MESSAGE_1.unlink()

	# 	if	hasattr(cls, "MESSAGE_2") and isinstance(Path, cls.MESSAGE_2) and cls.MESSAGE_2.is_file():
	# 		cls.MESSAGE_2.unlink()

	# 	if	hasattr(cls, "MESSAGE_3") and isinstance(Path, cls.MESSAGE_3) and cls.MESSAGE_3.is_file():
	# 		cls.MESSAGE_3.unlink()







	def test_A_strict_init(self):

		self.test_case.loggy.init_name = "A_strict_init"
		self.assertFalse(self.MESSAGES_DST1.is_dir())
		self.assertFalse(self.MESSAGES_DST2.is_dir())
		self.assertFalse(self.NAVDROP_SHELF.is_file())
		self.assertFalse(self.NAVDROP_BOW.is_file())


		with self.assertLogs("A_strict_init", 10) as case_loggy:

			self.test_case = self.test_case()
			self.test_case.perform()

			self.assertEqual(len(self.test_case.perform.Navbow()),48)
			self.assertEqual(len(self.test_case.perform.Navshelf()),3)

			self.test_case.perform.Navbow.produce(from_outer=True)
			self.test_case.perform.Navshelf.produce(

				from_outer=True,
				rewrite=True,
				ignore_mod=(len(self.test_case.perform.Navshelf) != len(self.test_case.perform.Navshelf()))
			)


		self.assertIn(f"INFO:A_strict_init:Bough \"{self.MESSAGES_DST1}\" is invalid", case_loggy.output)
		self.assertIn(f"INFO:A_strict_init:Bough \"{self.MESSAGES_DST2}\" is invalid", case_loggy.output)

		self.assertIn(
			f"DEBUG:A_strict_init:No records for \"{self.MESSAGE_3}\", marked as new", case_loggy.output
		)
		self.assertIn(f"DEBUG:A_strict_init:KB00 created by {self.now}", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"GALE\" in KB00 line 3", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"MAR\" in KB00 line 4", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"NORTH-EASTERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"NORTHERN\" in KB00 line 5", case_loggy.output)
		self.assertIn("WARNING:A_strict_init:Unknown word \"GUST\" in KB00 line 5", case_loggy.output)

		self.assertIn(
			f"DEBUG:A_strict_init:No records for \"{self.MESSAGE_1}\", marked as new", case_loggy.output
		)
		self.assertIn(f"DEBUG:A_strict_init:KE42 created by {self.now}", case_loggy.output)
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

		self.assertIn(
			f"DEBUG:A_strict_init:No records for \"{self.MESSAGE_2}\", marked as new", case_loggy.output
		)
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

		self.assertFalse(self.MESSAGES_DST1.is_dir())
		self.assertFalse(self.MESSAGES_DST2.is_dir())
		self.assertTrue(self.NAVDROP_BOW.is_file())
		self.assertTrue(self.NAVDROP_SHELF.is_file())








if	__name__ == "__main__":

	# Uncomment below statement to provide custom testing folder as a string
	# PygwartsTestCase._PygwartsTestCase__WFOLDER = 


	unittest.main(verbosity=2)







