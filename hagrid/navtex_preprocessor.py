from typing												import List
from typing												import Tuple
from typing												import Literal
from typing												import Optional
from pathlib											import Path
from pygwarts.magical.philosophers_stone				import Transmutable
from pygwarts.magical.philosophers_stone.transmutations	import Transmutation
from pygwarts.magical.spells							import patronus
from pygwarts.magical.spells							import flagrate
from pygwarts.magical.spells							import geminio
from pygwarts.irma.shelve								import LibraryShelf
from pygwarts.hagrid.cultivation.sifting				import SiftingController
from credistr											import link_navbow_receiver
from requests											import post as POST








class NavtexPreprocessor(Transmutation):

	"""
		Decorator, that serves as a planting dispatching interceptor for files preprocessing purposes.
		This class is designed to process Navtex messages in the way that comply with UDK2 (3744) station.
		The processing relies on Navanalyzer (https://github.com/longdeer/NavtexBoWAnalyzer).
		In mutable chain acts as a mutation - takes decorated planting dispatching class and extends it by
		declaring meta __call__ to invoke decorated __call__. Meta __call__ will act as a planting
		dispatching in terms of accepting "plant", processing it and pass it to the decorated dispatcher.
		It is assumed, that this dispatching layer will have it's own SiftingController "Navfiles" to
		assure only Navtex files will be processed. During processing, source files will have structure
		check and might be rewritten.
	"""

	def _mutable_chain_injection(self, layer :Transmutable) -> Transmutable :
		class Preprocessor(geminio(layer)):


			Navshelf	:LibraryShelf
			Navfiles	:SiftingController
			MSG_SEP		:Optional[str]


			def __call__(self, *plant :Tuple[str, Path, List[Path], List[Path]], **kwargs):

				# Assuming "plant" is valid and "unplantable" check in dispatcher will suffice.
				# Assuming "Navfiles" is reachable "SiftingController" that will ensure only
				# Navtex messages will be handled. This is crucial cause current preprocessing
				# goes before "Flourish" main sifting.
				if not plant : return
				*_, navtex_files = plant
				navtex_files = self.Navfiles(navtex_files)


				raws = dict()
				fl = len(navtex_files)
				self.loggy.debug(f"Considering {fl} file{flagrate(fl)}")


				for file in navtex_files:


					ltime = self.Navshelf[str(file)] or 0
					ntime = int(file.stat().st_mtime)
					fname = file.name


					if	ntime == ltime:

						self.loggy.debug(f"No modification made on \"{file}\"")
						self.Navshelf(str(file), ltime, silent=True)

						continue


					# At this point "ltime" is either zero or less than actual file, so analyzing proceed.
					with open(file,"rb") as raw_file: raws[str(file)] = raw_file.read()
					self.Navshelf(str(file), ntime)


				if	raws:

					try:	response = POST(link_navbow_receiver(),files=raws).json()
					except	Exception as E: self.loggy.error(f"Navtex analyze failed due to {patronus(E)}")
					else:

						buffer = str()

						for file,analysis in response.items():

							buffer += analysis.get("view") + "\n\n"
							current = analysis.get("analysis",dict())

							self.loggy.debug(f"{file} analysis: {current}")

							state = current.get("state")
							raw_lines = current.get("raw")

							if	state &2 or self.is_unstructured(raw_lines):
								if	self.rewrite_source(file, current.get("air")):

									self.Navshelf(file, int(Path(file).stat().st_mtime))
								else:
									self.loggy.warning(f"Message \"{file}\" not structured")


						self.process_buffer(buffer)


				super().__call__(*plant, **kwargs)




			def process_buffer(self, buffer :str):

				"""
					Helper method to actually hoist information via Telegram, by ContribInterceptor.
					If "buffer" is not empty, hoists it.
				"""

				if	callable(hoist := getattr(self.loggy, "buffer_insert", None)):
					if not buffer.isspace(): self.loggy.buffer_insert(buffer.strip("\n"))

					else:	self.loggy.debug("Buffer is empty")
				else:		self.loggy.debug("Buffer not hoisted")




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
					by "MSG_SEP" string. Hard coded to add "MSG_SEP" as header and footer.
					Returns True in case of success, None in any other cases.
				"""

				try:

					text = self.MSG_SEP.join( " ".join(line) for line in message )
					Path(path).write_text(f"{self.MSG_SEP}{text}{self.MSG_SEP}")

					self.loggy.info(f"Source file \"{path}\" rewritten")
					return True

				except Exception as E : self.loggy.info(f"Falid to rewrite \"{path}\" due to {patronus(E)}")




		return	Preprocessor







