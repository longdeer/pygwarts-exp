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

		counter		= 0
		conversion	= {

			"converted":	list(),
			"skipped":		list(),
			"unknown":		list(),
		}


		if	words:
			if	mode == 1 or mode == 0:


				for word in words:


					if	isinstance(word, str):

						counter	+= 1
						current	= word.upper()
						target	= self.NavbowShelve[current]
						state1	= int(not mode)


						if		target is None:conversion["unknown"].append(word)
						elif	target == mode:conversion["skipped"].append(word)
						elif	target == state1:

							self.NavbowShelve[current] = mode
							conversion["converted"].append(word)
							self.loggy.debug(f"Converted \"{word}\" to {'' if mode else 'un'}known")

						else:

							self.loggy.warning(f"Invalid state for \"{word}\"")
					else:	self.loggy.info(f"Incorrect \"{word}\" for conversion")
				else:		self.loggy.info(f"Done conversion for {counter} words")
			else:			self.loggy.info(f"Improper conversion mode {mode}")
		else:				self.loggy.info("No words provided for conversion")


		return	conversion




	# def convert_120(self, *words :Tuple[str,]) -> Dict[str,List[str]] :

	# 	"""
	# 		Convert words arguments, that must be 
	# 	"""

	# 	counter		= 0
	# 	conversion	= {

	# 		"converted":	list(),
	# 		"skipped":		list(),
	# 		"unknown":		list(),
	# 	}


	# 	if	words:
	# 		for word in words:


	# 			if	isinstance(word, str):

	# 				counter	+= 1
	# 				current = word.upper()


	# 				match self.NavbowShelve[current]:

	# 					case 1:		conversion["skipped"].append(word)
	# 					case None:	conversion["unknown"].append(word)
	# 					case 0:

	# 						self.NavbowShelve[current] = 1
	# 						conversion["converted"].append(word)

	# 						self.loggy.debug(f"Converted \"{wor}d\" to known")
	# 			else:		self.loggy.info(f"Incorrect \"{word}\" for conversion")
	# 		else:			self.loggy.info(f"Done conversion for {coutner} words")
	# 	else:				self.loggy.info("No words provided for conversion")


	# 	return	conversion