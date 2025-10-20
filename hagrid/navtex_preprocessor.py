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
		Decorator, that serves as a planting dispatching interceptor for files preprocessing purposes.
		This class is designed to process Navtex messages in the way that comply with UDK2 (3744) station.
		The processing relies on Navanalyzer class tool (https://github.com/longdeer/NavtexBoWAnalyzer).
		In mutable chain acts as a mutation - takes decorated planting dispatching class and extends it by
		declaring meta __call__ to invoke decorated __call__. Meat __call__ will act as a planting
		dispatching in terms of accepting "plant", processing it and pass it to the decorated dispatcher.
		It is assumed, that this dispatching layer will have it's own SiftingController "Navfiles" to
		assure only Navtex files will be processed. During processing, source files will have structure
		check and might be rewritten. Also "Navshelf" will maintain files state, peeking and inspecting
		the content. As a "Bag of Words" for Navanalyzer the "Navbow" LibraryShelf will be used.
	"""

	def _mutable_chain_injection(self, layer :Transmutable) -> Transmutable :
		class Preprocessor(geminio(layer)):


			Navbow		:LibraryShelf
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
				if not plant : return
				*_, navtex_files = plant
				navtex_files = self.Navfiles(navtex_files)


				fl = len(navtex_files)
				self.loggy.debug(f"Considering {fl} file{flagrate(fl)}")


				for file in navtex_files:


					last	= self.Navshelf[str(file)] or dict()
					ltime	= last.get("mtime",0)
					ntime	= int(file.stat().st_mtime)
					fname	= file.name
					buffer	= list()


					if	ntime <= ltime:

						self.loggy.debug(f"No modification made on \"{file}\"")
						self.Navshelf(str(file), last, silent=True)

						continue


					# At this point "ltime" is either zero or less than actual file, so analyzing proceed.
					# "is_new" flag will be derived as either zero "ltime" or "air" inequality. If both
					# "air" mappings are None, the "state" must be zero with corresponding handling.
					current	= self.analyzer.with_mapping(file, self.Navbow)
					is_new	= not ltime or current.get("air") != last.get("air")
					state	= current["state"]


					# Zero "state" might mean two cases:
					# 1 - "byte_scan" discovered non utf-8 symbols in "file", so "current" will
					# content censored message text as "message" mapping.
					# 2 - "file" contents no alphanumerical symbols, it might be a text with
					# whitespace characters only; in this case "current" will not have "message"
					# mapping, any other processing is redundant.
					if	not state:
						if	(msg := current.get("message")) is not None:

							self.Navshelf(str(file),{ "air": msg, "mtime": ntime })
							self.loggy.info(f"Message \"{file}\" is corrupted")
							self.loggy.buffer_insert(

								f"\ncorrupted message {fname}\n"
								+ msg.strip("\n") +
								"\n\n* must be checked in original file"
							)

						else:

							self.Navshelf(str(file),{ "air": None, "mtime": ntime })
							self.loggy.info(f"Message \"{file}\" is invalid")
							self.loggy.buffer_insert(f"\nfile \"{file}\" is invalid")

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
					if	isinstance(DTG := current["analysis"].get("DTG"), datetime):
						if	TimeTurner(DTG).mdY_aspath != TimeTurner().mdY_aspath:

							buffer.append(f"{fname} message is outdated")


					self.process_analysis(fname, current["analysis"], buffer)
					self.process_buffer(fname, is_new, buffer, current["air"])
					self.Navshelf(str(file),{ "air": current["air"], "mtime": int(file.stat().st_mtime) })


				super().__call__(*plant, **kwargs)




			def format(self, file :str, name :str, item :str, count :int, line :int) -> str :

				"""
					Helper method that serves as an analysis stats formatter.
					Returns string that represents how many items found at which line.
				"""

				return "%s %s%s %s at line %s"%(file, f"{count} " if 1 <count else "", name, item, line)




			def process_buffer(self, file :str, flag :bool, buffer :List[str], message :List[List[str]]):

				"""
					Helper method to actually hoist information via Telegram, by ContribInterceptor.
					If "flag" is True, which is "is_new", hoists the message, marked as new, and
					"buffer" content. Otherwise, if "buffer" is not empty, hoists message and
					"buffer" content.
				"""

				if	callable(hoist := getattr(self.loggy, "buffer_insert", None)) and not (send := str()):

					if	flag:	send += f"\nnew message {file}\n\n"
					if	flag or buffer:

						for i,line in enumerate(message,1):

							send += str(i).ljust(5)
							send += " ".join(line)
							send += "\n"


					send += "\n"
					send += "\n".join(buffer)


					if		send != "\n" : self.loggy.buffer_insert(send)
					else:	self.loggy.debug("Buffer is empty")
				else:		self.loggy.debug("Buffer not hoisted")




			def process_analysis(self, file :str, stats :Dict[int,Dict[str,int]], buffer :List[str]):

				"""
					Helper method that processes all lines in "stats", inspecting it line by line.
					Logs at INFO level:
						- coordinates;
						- numerical;
						- alphanumerical;
						- known words;
						- unknown words;
						- pending words;
						- unmatched punctuation;
					Also hoists:
						- unknown words;
						- unmatched punctuation;
				"""

				line = 1
				done = False

				while not done:

					done = True

					if	(coords := stats["coords"].get(line)) and not (done := False):
						for coordinate,count in coords.items():

							self.loggy.info(self.format(file, "coordinatal", coordinate, count, line +1))

					if	(alnums := stats["alnums"].get(line)) and not (done := False):
						for alnum,count in alnums.items():

							self.loggy.info(self.format(file, "alphanumerical", alnum, count, line +1))

					if	(nums := stats["nums"].get(line)) and not (done := False):
						for numeric,count in nums.items():

							self.loggy.info(self.format(file, "numerical", numeric, count, line +1))

					if	(known := stats["known"].get(line)) and not (done := False):
						for word,count in known.items():

							self.loggy.info(
								self.format(file, f"known word{flagrate(count)}", word, count, line +1)
							)

					if	(pendings := stats["pending"].get(line)) and not (done := False):
						for word,count in pendings.items():

							self.loggy.info(
								self.format(file, f"pending word{flagrate(count)}", word, count, line +1)
							)

					if	(unknown := stats["unknown"].get(line)) and not (done := False):
						for word,count in unknown.items():

							msg = self.format(file, f"unknown word{flagrate(count)}", word, count, line +1)
							self.loggy.info(msg)
							buffer.append(msg)

					if	(puncts := stats["punct"].get(line)) and not (done := False):
						for char,count in puncts.items():

							msg = self.format(file, "unmatched", char, count, line +1)
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
				else:	return header != "" or eos != "" or body[0] == "" or body[-1] == ""




			def rewrite_source(self, path : Path, message :List[List[str]])-> Literal[True] | None :

				"""
					Helper method that takes message structure, which is two-dimensional list of strings,
					and writes it to the "path" file. Relies on "path" is a Path object. Joins "message"
					y "MSG_SEP" string, if provided, or with \\n by default. Hardcoded to add \\n as
					header and footer. Returns True in case of success, None in any other cases.
				"""

				try:

					text = "\r\n".join( " ".join(line) for line in message )
					path.write_text(f"\r\n{text}\r\n")

					self.loggy.info(f"Source file \"{path}\" rewritten")
					return True

				except Exception as E : self.loggy.info(f"Falid to rewrite \"{path}\" due to {patronus(E)}")




		return	Preprocessor







