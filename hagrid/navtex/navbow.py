from typing									import List
from typing									import Tuple
from typing									import Dict
from pygwarts.magical.philosophers_stone	import Transmutable
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.irma.shelve					import LibraryShelf








class NavbowController(Transmutable):
	class NavbowShelve(LibraryShelf):	pass


	def __call__(self, *words :Tuple[str,], mode :int) -> Dict[str,List[str]] :

		"""
			Convert words arguments, that must be 
		"""

		original	= len(words)
		processed	= set()
		counter		= 0
		conversion	= {

			"converted":	list(),
			"skipped":		list(),
			"undefined":	list(),
		}


		if	original:
			if	mode == 1 or mode == 0:


				for word in words:


					if	isinstance(word, str):
						if	(current := word.upper()) not in processed:


							processed.add(current)
							state1	= int(not mode)
							target	= self.NavbowShelve[current]


							if		target is None:		conversion["undefined"].append(current)
							elif	target == mode:		conversion["skipped"].append(current)
							elif	target == state1:

								counter	+= 1
								self.NavbowShelve[current] = mode
								conversion["converted"].append(current)
								self.loggy.debug(f"Converted \"{current}\" to {'' if mode else 'un'}known")


							else:	self.loggy.warning(f"Invalid state for word \"{word}\"")
						else:		self.loggy.debug(f"Duplicate word \"{word}\" skipped")
					else:			self.loggy.info(f"Incorrect word \"{word}\" for conversion")
				else:				self.loggy.info(f"Done conversion for {counter}/{original} words")
			else:					self.loggy.info(f"Improper conversion mode {mode}")
		else:						self.loggy.info("No words provided for conversion")


		return	conversion




	def inspect(self, *words :Tuple[str,]) -> Dict[str,List[str]] :

		"""
			Inspection of some words
		"""

		original	= len(words)
		processed	= set()
		counter		= 0
		conversion	= {

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


						if		target is None:		conversion["undefined"].append(current)
						elif	target == 0:		conversion["unknown"].append(current)
						elif	target == 1:		conversion["known"].append(current)


						else:	self.loggy.warning(f"Invalid state for word \"{word}\"")
					else:		self.loggy.debug(f"Duplicate word \"{word}\" skipped")
				else:			self.loggy.info(f"Incorrect word \"{word}\" for inspection")
			else:				self.loggy.info(f"Done inspection for {counter}/{original} words")
		else:					self.loggy.info("No words provided for inspection")


		return	conversion







