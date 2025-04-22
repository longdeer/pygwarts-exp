from typing												import List
from typing												import Tuple
from typing												import Literal
from typing												import Optional
from pathlib											import Path
from datetime											import datetime
from pygwarts.magical.philosophers_stone				import Transmutable
from pygwarts.magical.philosophers_stone.transmutations	import Transmutation
from pygwarts.magical.time_turner						import TimeTurner
from pygwarts.magical.spells							import patronus
from pygwarts.magical.spells							import flagrate
from pygwarts.magical.spells							import geminio
from pygwarts.irma.shelve								import LibraryShelf
from pygwarts.hagrid.cultivation.sifting				import SiftingController
from NavtexBoWAnalyzer									import Navanalyzer








class NavtexPreprocessor(Transmutation):

	"""
		old:
		pygwarts.hagrid utility decorator, that serves as a planting dispatching interceptor for files
		preprocessing purposes.
		This class is designed to process NAVTEX messages in the way that comply with UDK2 station.
		The processing relies on Navanalyzer class tool (https://github.com/longdeer/NavtexBoWAnalyzer).
		As ControlledTransmutation class, accepts following arguments:
			"station"	-	positional argument that is used by Navanalyzer class;
			"categories"-	key-word argument that is used by Navanalyzer class (defaulted to None);
			"separator"	-	key-word argument that in used by preprocessor to reconstruct messages.
		In mutable chain acts as a mutation - takes decorated planting dispatching class and extends it by
		declaring meta __call__ to invoke decorated __call__. Meat __call__ will act as a planting dispatching
		in terms of accepting "plant", processing it and pass it to the decorated dispatcher.
		It is assumed, that this dispatching layer will only receive NAVTEX messages files, which are to be
		filtered out before processing start. The preprocessing may result source file rewriting and some sort
		of report message sending via "loggy.pool" tool.

		Navshelf:
			/path/to/file : mtime
	"""

	def _mutable_chain_injection(self, layer :Transmutable) -> Transmutable :
		class Preprocessor(geminio(layer)):


			NavBoW		:LibraryShelf
			Navshelf	:LibraryShelf
			Navfiles	:SiftingController
			MSG_SEP		:Optional[str]


			def __init__(self, *args, **kwargs):

				super().__init__(*args, **kwargs)
				self.analyzer = Navanalyzer("K")

			def __call__(self, *plant :Tuple[str, Path, List[Path], List[Path]], **kwargs):

				# Assuming "plant" is valid and "unplantable" check in dispatcher will suffice.
				# Assuming "Navfiles" is reachable "SiftingController" that will ensure only
				# Navtex messages will be handled. This is crucial cause current preprocessing
				# goes before "Flourish" main sifting.
				*_, navtex_files = plant
				navtex_files = self.Navfiles(navtex_files)

				fl = len(navtex_files)
				self.loggy.debug(f"Considering {len(fl)} file{flagrate(len(fl))}")


				for file in navtex_files:


					if	isinstance(last := self.Navshelf[str(file)], int):
						if	int(file.stat().st_mtime) <= last:

							self.loggy.debug(f"No modification made on \"{file}\"")
							self.Navshelf(str(file), last, silent=True)

							continue


					current	= self.analyzer.with_mapping(file)
					state	= current["state"]
					fname	= file.name
					buffer	= list()


					# Zero "state" might mean two cases:
					# 1 - "byte_scan" discovered non utf-8 symbols in "file", so "current" will
					# content censored message text as "message" mapping.
					# 2 - "file" contents no alphanumerical symbols, it might be a text with
					# whitespace characters only; in this case "current" will not have "message"
					# mapping, any other processing is redundant.
					if	not state:
						if	(msg := current.get("message")) is not None:
							if	callable(pool := getattr(self.loggy, "buffer_insert", None)):

								self.loggy.buffer_insert("corrupted message:\n")
								self.loggy.buffer_insert(msg)
								self.loggy.buffer_insert("\n\n* must be checked in original message\n\n")


							self.loggy.info(f"Message \"{file}\" is corrupted")
						else:
							self.loggy.info(f"Message \"{file}\" is invalid")


						continue


					# Further processing suggests "state" is not zero so "current" is "Navanalyzer"
					# long variant dictionary with "raw", "air" and "analysis".
					if	state &2 or self.is_unstructured(current["raw"]):
						if	not self.rewrite_source(file, current["air"]):
							buffer.append(f"{fname} message not structured")


					if not state &8 : buffer.append(f"{fname} invalid EoS (NNNN)")
					if not state &4 : buffer.append(f"{fname} invalid header (ZCZC)")
					elif not self.is_numerated(current["analysis"].get("header")):

						buffer.append(f"{fname} abnormal message numeration")


					# Maintaining creation datetime
					if	state &64:
						if	isinstance(CDT := current["analysis"].get("cdt"), datetime):
							if	TimeTurner(CDT).mdY_aspath != TimeTurner().mdY_aspath:
								buffer.append(f"{fname} message is outdated")


					# Maintaining unkown words
					if	state &32:

						unknowns = current["analysis"]["unknowns"]


					for coordinatal in current[""]




			def is_numerated(self, SSN :Tuple[str,str,str]) -> bool :

				"""
					Helper method to verify some unofficial rules about messages numeration,
					such as B and D subjects must only be 00, and E perhaps never be 00. Returns
					True for every other Station Subject Number combination.
				"""

				match SSN:

					case ( _, "B", number ): return number == "00"
					case ( _, "D", number ): return number == "00"
					case ( _, "E", number ): return number != "00"

					case None:	return False
					case _:		return True




			def is_unstructured(self, lines :List[str]) -> bool :

				"""
					Helper method to verify original message is structured the universal proper way:
						NL
						MESSAGE
						NL
				"""

				try:	header,*body,eos = lines
				except	ValueError : return True
				else:	return not (header == eos == "")




			def rewrite_source(self, path : Path, message :List[List[str]])-> Literal[True] | None :

				"""
					Helper method that takes message structure, which is two-dimensional list of strings,
					and writes it to the "path" file. Relies on "path" is a Path object. Joins "message"
					y "MSG_SEP" string, if provided, or with \\n by default. Hardcoded to add \\n as
					header and footer. Returns True in case of success, None in any other cases.
				"""

				try:

					text = getattr(self, "MSG_SEP", "\n").join( " ".join(lin) for line in message )
					path.write_text(f"\n{text}\n")

					self.loggy.info(f"Source file \"{path}\" rewritten")
					return True

				except Exception as E : self.loggy.info(f"Falid to write \"{file}\" due to {patronus(E)}")




		return	Preprocessor