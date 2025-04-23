from typing												import List
from typing												import Dict
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
			/path/to/file : { air :air, mtime :int }
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


					last	= self.Navshelf[str(file)] or dict()
					mtime	= last.get("mtime",0)
					fname	= file.name
					buffer	= list()


					if	int(file.stat().st_mtime) <= mtime:

						self.loggy.debug(f"No modification made on \"{file}\"")
						self.Navshelf(str(file), last, silent=True)

						continue


					# At this point "mtime" is either zero or less than actual file, so analyzing proceed.
					# "is_new" flag will be derived as either zero "mtime" or "air" inequality. If both
					# "air" mappings are None, the "state" must be zero with corresponding handling.
					current	= self.analyzer.with_mapping(file)
					is_new	= not mtime or current.get("air") != last.get("air")
					state	= current["state"]


					# Zero "state" might mean two cases:
					# 1 - "byte_scan" discovered non utf-8 symbols in "file", so "current" will
					# content censored message text as "message" mapping.
					# 2 - "file" contents no alphanumerical symbols, it might be a text with
					# whitespace characters only; in this case "current" will not have "message"
					# mapping, any other processing is redundant.
					if	not state:
						if	(msg := current.get("message")) is not None:

							self.loggy.buffer_insert("corrupted message:\n")
							self.loggy.buffer_insert(msg)
							self.loggy.buffer_insert("\n\n* must be checked in original message\n\n")
							self.loggy.info(f"Message \"{file}\" is corrupted")

						else:

							self.loggy.buffer_insert(f"Message \"{file}\" is invalid")
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


					# Maintaining creation datetime check. It is assumed, that once message is
					# created by coordinator and delivered to operator, it is analyzed once.
					if	isinstance(CDT := current["analysis"].get("cdt"), datetime):
						if	TimeTurner(CDT).mdY_aspath != TimeTurner().mdY_aspath:

							buffer.append(f"{fname} message is outdated")


					self.process_analysis(current, buffer)
					self.Navshelf(str(file),{ "air": current["air"], "mtime": int(file.stat().st_mtime) })


					if	is_new : self.loggy.buffer_insert("new message:\n\n")
					if	is_new or buffer:

						self.loggy.buffer_insert("\n".join( " ",join(line) for line in current["air"] ))
					self.loggy.buffer_insert("\n\n""\n".join(buffer))


				super().__call__(*plant, **kwargs)




			def format(self, name :str, item :str, count :int, line :int) -> str :

				""" Helper method that serves as an analysis stats formatter. """

				return "%s%s %s at line %s"%(f"{count} " if 1 <count else "", name, item, line)




			def process_analysis(self, stats :Dict[int,Dict[str,int]], buffer :List[str]):

				"""
					Helper method that processes all lines in "stats"
				"""

				line = 1
				done = False

				while not done:

					done = True

					if	(coords := stats["coords"].get(line)) and not (done := False):
						for coordinate,count in coords.items():

							self.loggy.info(self.format("coordinatal", coordinate, count, line))

					if	(alnums := stats["alnums"].get(line)) and not (done := False):
						for alnum,count in alnums.items():

							self.loggy.info(self.format("alphanumerical", alnum, count, line))

					if	(nums := stats["nums"].get(line)) and not (done := False):
						for numeric,count in nums.items():

							self.loggy.info(self.format("numerical", numeric, count, line))

					if	(known := stats["known"].get(line)) and not (done := False):
						for word,count in known.items():

							self.loggy.info(self.format("known", word, count, line))

					if	(unknown := stats["unknown"].get(line)) and not (done := False):
						for word,count in unknown.items():

							msg = self.format("unknown", word, count, line)
							self.loggy.info(msg)
							buffer.append(msg)

					if	(pendings := stats["pending"].get(line)) and not (done := False):
						for word,count in pendings.items():

							msg = self.format("pending", word, count, line)
							self.loggy.info(msg)
							buffer.append(msg)

					if	(puncts := stats["punct"].get(line)) and not (done := False):
						for char,count in pendings.items():

							msg = self.format("unmatched", char, count, line)
							self.loggy.info(msg)
							buffer.append(msg)

					line += 1




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







