from typing									import Dict
from typing									import List
from typing									import Tuple
from typing									import Literal
from pygwarts.magical.philosophers_stone	import Transmutable
from pygwarts.irma.shelve					import LibraryShelf








class NavbowController(Transmutable):

	"""
		Transmutable object that serves as a maintainer for Navtex Bag of Words LibraryShelf produced files.
		Provides such operations as conversion of words between two states and inspection of any word or
		corresponding state for Shelf file.
		It is important that none of the methods, that actually alter "NavbowShelve" in place, does not
		perform "produce" for the Shelf, so no changes takes affect for the end Shelf file. This is up
		to user to perform "produce" manually.
	"""

	class NavbowShelve(LibraryShelf):	pass
	def inspect_state(self, state :int | str) -> Dict[str,List[str]] :

		"""
			Inspection of certain state words.
			Accepts "state" integer or string that represents:
				1 - "known" state words;
				0 - "unknown" state words.
			Every word that is string obtained from "NavbowShelve" that mapped to "state" will be
			gathered to a list and returned in dictionary with corresponding mapping. If no words found
			empty dictionary will be returned.
		"""

		counter		= 0
		current		= list()
		inspection	= {

			"known":		list(),
			"unknown":		list(),
		}

		try:	state = int(state)
		except	Exception as E : self.loggy.info(f"State \"{state}\" not an integer or numeric string")
		else:
			if	state == 1 or state == 0:

				words = self.NavbowShelve.keysof(state)
				original = len(words)


				if	original:
					for word in words:


						if	isinstance(word, str):

							counter += 1
							current.append(word)
						else:
							self.loggy.warning(f"Invalid key \"{word}\" in {self.NavbowShelve}")
					else:

						self.loggy.info(f"Done state inspection for {counter}/{original} words")
						inspection[f"{'' if state else 'un'}known"] = current

				else:	self.loggy.info(f"No words with {'' if state else 'un'}known state")
			else:		self.loggy.info(f"Improper state \"{state}\" for inspection")


		return	inspection








	def inspect(self, *words :Tuple[str,]) -> Dict[str,List[str]] :

		"""
			Inspection of words.
			Accepts "words" strings, that must represent words with states to be checked. The result of
			inspection is a dictionary with corresponding keys.
			Every word that is string will be searched in Shelf by the "NavbowShelve" object, and placed
			to the list mapped with:
				"known" if current word state is 1 in Shelf,
				"unknown" if current word state is 0 in Shelf,
				"undefined" if Shelf doesn't content such word as a key mapping.
			Returns populated or empty empty-lists values dictionary.
		"""

		original	= len(words)
		processed	= set()
		counter		= 0
		inspection	= {

			"known":		list(),
			"unknown":		list(),
			"undefined":	list(),
		}


		if	original:
			for word in words:


				if	isinstance(word, str):
					if	(current := word.upper()) not in processed:


						counter += 1
						processed.add(current)
						target	= self.NavbowShelve[current]


						if		target is None:	inspection["undefined"].append(current)
						elif	target == 0:	inspection["unknown"].append(current)
						elif	target == 1:	inspection["known"].append(current)


						else:	self.loggy.warning(f"Invalid state for word \"{word}\"")
					else:		self.loggy.debug(f"Duplicate word \"{word}\" skipped")
				else:			self.loggy.info(f"Incorrect word \"{word}\" for inspection")
			else:				self.loggy.info(f"Done inspection for {counter}/{original} words")
		else:					self.loggy.info("No words provided for inspection")


		return	inspection








	def erase_state(self, state :int | str) -> Dict[str,List[str]] :

		"""
			Erasion of certain state words.
			Accepts "state" integer or string that represents:
				1 - "known erased" state words;
				0 - "unknown erased" state words.
			Every word that is string obtained from "NavbowShelve" that mapped to "state" will be deleted
			from "NavbowShelve", gathered to a list and returned in dictionary with corresponding mapping.
			If no words found empty dictionary will be returned.
		"""

		counter	= 0
		current	= list()
		erasion	= {

			"known erased":		list(),
			"unknown erased":	list(),
		}


		try:	state = int(state)
		except	Exception as E : self.loggy.info(f"State \"{state}\" not an integer or numeric string")
		else:
			if	state == 1 or state == 0:

				words = self.NavbowShelve.keysof(state)
				original = len(words)


				if	original:
					for word in words:


						if	isinstance(word, str):

							counter += 1
							current.append(word)
							del self.NavbowShelve[word]
						else:
							self.loggy.warning(f"Invalid key \"{word}\" in {self.NavbowShelve}")
					else:

						self.loggy.info(f"Done state erasion for {counter}/{original} words")
						erasion[f"{'' if state else 'un'}known erased"] = current

				else:	self.loggy.info(f"No words with {'' if state else 'un'}known state")
			else:		self.loggy.info(f"Improper state \"{state}\" for erasion")


		return	erasion








	def erase(self, *words :Tuple[str,]) -> Dict[str,List[str]] :

		"""
			Erasion of words.
			Accepts "words" strings, that must represent words to be erased. The result of erasion is a
			dictionary with corresponding keys. Every word that is string will be searched in Shelf by the
			"NavbowShelve" object, every valid state word will be deleted, every word found will be placed
			to the list mapped with:
				"known erased" if current word state is 1 in Shelf,
				"unknown erased" if current word state is 0 in Shelf,
				"undefined" if Shelf doesn't content such word as a key mapping.
			Returns populated or empty empty-lists values dictionary.
		"""

		original	= len(words)
		processed	= set()
		counter		= 0
		erasion		= {

			"known erased":		list(),
			"unknown erased":	list(),
			"undefined":		list(),
		}


		if	original:
			for word in words:


				if	isinstance(word, str):
					if	(current := word.upper()) not in processed:


						counter += 1
						processed.add(current)
						target	= self.NavbowShelve[current]
						del self.NavbowShelve[current]


						if		target is None:	erasion["undefined"].append(current)
						elif	target == 0:	erasion["unknown erased"].append(current)
						elif	target == 1:	erasion["known erased"].append(current)


						else:	self.loggy.warning(f"Invalid state for word \"{word}\"")
					else:		self.loggy.debug(f"Duplicate word \"{word}\" skipped")
				else:			self.loggy.info(f"Incorrect word \"{word}\" for erasion")
			else:				self.loggy.info(f"Done erasion for {counter}/{original} words")
		else:					self.loggy.info("No words provided for erasion")


		return	erasion








	def convert(self, *words :Tuple[str,], state :int | str) -> Dict[str,List[str]] :

		"""
			Conversion of words.
			Accepts "words", that must represent words to be converted, and final state for every word
			"state". The result of conversion is a dictionary with corresponding keys.
			Every word that is string will be searched in Shelf by "NavbowShelve" object, the "state"
			will be set if possible and word will be placed to the list mapped with:
				"converted" if current word was in opposite state, so current state was actually changed,
				"skipped" if current word state is already set to the "state" and no conversion done,
				"undefined" if Shelf doesn't content such word as a key mapping.
			Returns populated or empty-lists values dictionary.
		"""

		original	= len(words)
		processed	= set()
		counter		= 0
		conversion	= {

			"converted":	list(),
			"skipped":		list(),
			"undefined":	list(),
		}


		try:	state = int(state)
		except	Exception as E : self.loggy.info(f"State \"{state}\" not an integer or numeric string")
		else:
			if	original:
				if	state == 1 or state == 0:


					for word in words:


						if	isinstance(word, str):
							if	(current := word.upper()) not in processed:


								processed.add(current)
								prestate= int(not state)
								target	= self.NavbowShelve[current]


								if		target is None:		conversion["undefined"].append(current)
								elif	target == state:	conversion["skipped"].append(current)
								elif	target == prestate:

									counter	+= 1
									self.NavbowShelve[current] = state

									conversion_string = f"{current} -> {'' if state else 'un'}known"
									conversion["converted"].append(conversion_string)

									self.loggy.debug(
										f"Converted \"{current}\" to {'' if state else 'un'}known"
									)


								else:	self.loggy.warning(f"Invalid state for word \"{word}\"")
							else:		self.loggy.debug(f"Duplicate word \"{word}\" skipped")
						else:			self.loggy.info(f"Incorrect word \"{word}\" for conversion")
					else:				self.loggy.info(f"Done conversion for {counter}/{original} words")
				else:					self.loggy.info(f"Improper conversion state \"{state}\"")
			else:						self.loggy.info("No words provided for conversion")


		return	conversion








	def add(self, *words :Tuple[str,], state :int | str) -> Dict[str,List[str]] :

		"""
			Addition of words.
			Accepts "words", that must represent words to be added, and corresponding state for every word
			"state". The result of addition is a dictionary with corresponding keys.
			Every word that is string will be searched in Shelf beforehand. Every word that already in Shelf,
			but in opposite "state" will be converted, in same state will be skipped. Every absent word will
			be mapped with "state". The result output mapping will as follow:
				"added to known" if current word was absent and was now mapped with state == 1,
				"added to unknown" if current word was absent and was now mapped with state == 0,
				"skipped" if current word already in Shelf mapped with any valid state.
			Returns populated or empty-lists values dictionary.
		"""

		original	= len(words)
		processed	= set()
		counter		= 0
		addition	= {

			"added to known":	list(),
			"added to unknown":	list(),
			"skipped":			list(),
		}


		try:	state = int(state)
		except	Exception as E : self.loggy.info(f"State \"{state}\" not an integer or numeric string")
		else:
			if	original:
				if	state == 1 or state == 0:


					for word in words:


						if	isinstance(word, str):
							if	(current := word.upper()) not in processed:


								processed.add(current)
								prestate= int(not state)
								target	= self.NavbowShelve[current]


								if	target is None:

									counter	+= 1
									self.NavbowShelve[current] = state
									addition[f"added to {'' if state else 'un'}known"].append(current)


								else:	addition["skipped"].append(current)
							else:		self.loggy.debug(f"Duplicate word \"{word}\" skipped")
						else:			self.loggy.info(f"Incorrect word \"{word}\" for addition")
					else:				self.loggy.info(f"Done addition for {counter}/{original} words")
				else:					self.loggy.info(f"Improper addition state \"{state}\"")
			else:						self.loggy.info("No words provided for addition")


		return	addition








	def __call__(self) -> Dict[str,List[str]] :

		"""
			Inspection of every single word in Shelf and it's corresponding state.
			Accepts no arguments. The result of inspection is a dictionary with corresponding keys.
			Every word that is string found in Shelf by the "NavbowShelve" object, will be placed
			to the list mapped with:
				"known" if current word state is 1 in Shelf,
				"unknown" if current word state is 0 in Shelf,
				"undefined" if current word state neither 0 nor 1 in Shelf.
			Returns populated or empty-lists values dictionary.
		"""

		original	= len(self.NavbowShelve)
		counter		= 0
		total		= {

			"known":		list(),
			"unknown":		list(),
			"undefined":	list(),
		}


		if	original:
			for word,state in self.NavbowShelve:


				if	isinstance(word, str):
					match state:

						case 1:
							total["known"].append(word)
							counter += 1

						case 0:
							total["unknown"].append(word)
							counter += 1

						case _: total["undefined"].append(word)


				else:	self.loggy.warning(f"Incorrect word \"{word}\" encountered")
			else:		self.loggy.info(f"Total {counter}/{original} stated words")
		else:			self.loggy.info("No words in total")


		return	total







