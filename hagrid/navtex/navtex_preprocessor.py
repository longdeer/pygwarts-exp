import	re
from	typing												import Tuple
from	typing												import List
from	typing												import Callable
from	typing												import Literal
from	pathlib												import Path
from	pygwarts.magical.philosophers_stone					import Transmutable
from	pygwarts.magical.philosophers_stone.transmutations	import ControlledTransmutation
from	pygwarts.magical.patronus							import CAST
from	pygwarts.magical.time_turner						import TimeTurner
from	pygwarts.irma.shelve								import LibraryShelf
from	pygwarts.hagrid.planting							import unplantable
from	NavtexBoWAnalyzer.navtex_analyzer					import Navanalyzer








class Navpreprocessor(ControlledTransmutation):

	"""
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
	"""


	def __init__(self, station :str, categories :str | List[str] =None, separator :str ="\n"):


		self.separator	= separator
		self.station	= station
		self.categories	= categories


	def __call__(self, chained_layer :Transmutable) -> Callable[Transmutable, Transmutable] :


		chained		= super().__call__(chained_layer)
		separator	= self.separator
		analyzer	= Navanalyzer(self.station, self.categories)


		# Modifying Navtex message structure regex to comply UDK2
		analyzer.TEXT_MSG_STRUCT = re.compile(r"^\n(?:[ =!\"'\(\)\+,\-\./0-9:;A-Z]+\n)+$")




		def transmutation(upper_layer :Transmutable) -> Transmutable :
			class Preprocessor(chained(upper_layer)):


				def __call__(self, *plant :Tuple[str, Path, List[Path], List[Path]], **kwargs):


					processed	= list()
					Navshelf	= getattr(self, "Navshelf", None)
					Navbow		= getattr(self, "Navbow", dict())
					dispatcher	= str()


					if	not isinstance(Navshelf, LibraryShelf):
						self.loggy.warning(f"No previous NAVTEX watch records found")


					if	plant:
						if	isinstance(reason := unplantable(*plant), str): self.loggy.warning(reason)
						else:


							*_, nav_files = plant
							self.loggy.debug(f"Received files: {len(nav_files)}")




							# Preprocessor files filter, that must be tuned to only allow certain files
							# with NAVTEX messages texts. For a single NAVTEX files flourish might
							# be sufficient sifting for all sprouts, so this SiftingController has a
							# special name that help in isolation from any other "sifters".
							if	callable((Navfiles := getattr(self, "Navfiles", None))):

								sifted_files = Navfiles(nav_files)
								Navfiles.loggy.debug(f"Files after sifting: {len(sifted_files)}")
							else:
								sifted_files = nav_files




							if	not len(sifted_files): self.loggy.debug(f"No NAVTEX files at \"{sprout}\"")
							for file in sifted_files:


								CDT = None
								shelved_CDT = None
								repr_name = file.name
								is_new_message = False
								current_dispatch = str()
								self.loggy.debug(f"Considering NAVTEX file \"{file}\"")




								if	isinstance(Navshelf, LibraryShelf):
									if	isinstance((current_shelf := Navshelf[str(file)]), dict):
										shelved_CDT = current_shelf.get("CDT")


										if	current_shelf.get("FMT") == file.stat().st_mtime:


											self.loggy.debug(f"No modification made on \"{file}\"")
											Navshelf(str(file), current_shelf, silent=True)

											continue

									else:

										is_new_message = True
										self.loggy.debug(f"No records for \"{file}\", marked as new")
								else:	self.loggy.debug("Navshelf was not found")




								try:

									with open(file) as raw_message:

										current_check	= analyzer(raw_message.read(), Navbow, separator)
										proper_lines	= current_check["proper_lines"]
										proper_message	= current_check["proper_message"]
										is_structured	= current_check["is_structured"]
										is_sanitized	= current_check["is_sanitized"]
										header_id		= current_check["header_id"]
										header_issue	= current_check["header_issue"]
										message_CDT		= current_check["message_CDT"]
										CDT_issues		= current_check["CDT_issues"]
										body_issues		= current_check["body_issues"]
										EOS_issue		= current_check["EOS_issue"]
								except	Exception as E:

									self.loggy.warning(f"Failed to analyze \"{file}\" due to {CAST(E)}")
									continue

								else:
									repr_name = header_id or repr_name
									raw_count = len(current_check["raw_message"])

									self.loggy.debug(f"{repr_name} raw message symbols: {raw_count}")




								# Section of decision wether source file must be rewritten or not.
								if	not is_structured:	self.loggy.info(f"{repr_name} failed structure check")
								if	is_sanitized:		self.loggy.info(f"{repr_name} failed layout check")
								if	is_sanitized or not is_structured:
									if	self.rewrite_source(

										file,
										proper_message,
										header=separator,
										footer=separator,

									)	is None: continue




								if	header_issue is not None:

									self.loggy.info(f"{header_issue} in {repr_name}")
									current_dispatch += f"{header_issue} in {repr_name}\n"




								# Ignoring all "issues" that might be generated by "analyzer" about CDT,
								# but using fetched date and time strings to process message CDT.
								# Technically it is better to wrap actual "CDT" obtaining in try-except,
								# but if "message_CDT" is not None it must means it was already validated.
								if	message_CDT is not None:
									if(

										isinstance(message_CDT, tuple)			and
										len(message_CDT) == 3					and
										isinstance((D := message_CDT[1]), str)	and
										isinstance((T := message_CDT[2]), str)

									):

										try:	CDT = TimeTurner(D,T)
										except	Exception as E:

											self.loggy.info(f"Failed to convert CDT for {repr_name}")
										else:
											self.loggy.debug(f"{repr_name} created by {CDT}")
											self.loggy.debug(f"shelved CDT is {shelved_CDT}")


											if	shelved_CDT is not None and shelved_CDT <CDT:


												is_new_message = True
												self.loggy.debug(f"Younger CDT found, marked as new")
									else:		self.loggy.info(f"CDT obtaining problem in {repr_name}")
								else:

									# As Navtex manual doesn't assumes CDT is mandatory line, user must
									# be notified CDT wether absent or incorrect.
									self.loggy.info(f"CDT not found in {repr_name}")
									current_dispatch += f"CDT not found in {repr_name}\n"


								if	CDT_issues is not None:
									for issue in CDT_issues:


										self.loggy.info(f"{issue} in {repr_name}")
										current_dispatch += f"{issue} in {repr_name}\n"




								if	body_issues is not None:
									for level,N,item,message in body_issues:

										if	20 <level:

											current_dispatch += f"{message} in {repr_name} line {N}\n"
										Navbow.loggy.log(level, f"{message} in {repr_name} line {N}")




								if	EOS_issue is not None:

									self.loggy.info(f"{EOS_issue} in {repr_name}")
									current_dispatch += f"{EOS_issue} in {repr_name}\n"




								if	current_dispatch or is_new_message:
									if		is_new_message: message_pool = f"new message {repr_name}\n"
									else:	message_pool = f"{repr_name}\n"


									for L,line in enumerate(proper_lines, 1):
										message_pool += f"{str(L).ljust(5)}{line}\n"


									dispatcher += "%s\n%s%s"%(

										message_pool,
										current_dispatch,

										# NL indents multiplications means 1 if "current_dispatch" is empty,
										# so no troubles just a new message notification, otherwise 2 NL
										# to ensure proper space between neighbor messages.
										"\n" *(int(bool(current_dispatch)) +1)
									)




								if	Navshelf is not None:
									Navshelf(

										str(file),
										{
											"FMT": file.stat().st_mtime,
											"CDT": CDT
										}
									)




								self.loggy.debug(f"Processed {repr_name}")
					else:		self.loggy.debug(f"No plants to flourish")




					if	callable(pool := getattr(self.loggy, "pool", None)):

						# All NL that wrapps final message over top and bottom must be stripped
						# before message will be pushed to the pool.
						if	dispatcher : pool(("\n%s\n"%dispatcher).strip("\n"))




					# Passing inner shelf so every new word will be stored in both shelfs and "modified"
					# flag will be successfully triggered for LibraryShelf object. The "produce" method for
					# NavBow must be invoked with from_outer flag set to True to maintain only new words.
					analyzer.update_BoW(Navbow)




					# As all processing serves just for sanytaizing and checking for messages, all received
					# "plant" as it is must be passed to the dispatcher with all possible key-word flags.
					super().__call__(*plant, **kwargs)




				def rewrite_source(	self,
									file_path			:Path,
									message				:str,
									header				:str	="",
									footer				:str	="",
								)-> Literal[True] | None:

					"""
						Rewrites sanitaized source message file.

						This is the place, where source file is claimed to have a special structure.
						As Navtex message transmitting automation require two new lines between
						messages, and some modems might have wrong pre/post key settings, tath may lead
						to very first message header corruption, current implementation maintains
						the structure like first new line in the beggining -----and second at the end
						of message. The argument "wrapper" must be a new line, that is to be provided
						as a decorator argument.-----must satisfy both NAVTEX manual conditions and
						keying issues. Arguments "header" and "footer" allows to place it wherever.

						None must be returned only if write to file failed.
					"""

					try:	file_path.write_text(f"{header}{message}{footer}")
					except	Exception as E:

						self.loggy.warning(f"Failed to rewrite \"{file_path}\" due to {CAST(E)}")
					else:
						self.loggy.info(f"Source file \"{file_path}\" rewritten")

						return	True




			return	Preprocessor




		# Completing controlled transmutation
		transmutation.CHAIN_OVER_HOOK = True
		self.CHAIN_LAYER_HOOK = transmutation


		return	transmutation







