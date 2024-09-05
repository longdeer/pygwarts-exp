from os													import path		as ospath
from os													import remove	as osremove
from re													import compile	as pmake
from typing												import Tuple
from typing												import List
from typing												import Callable
from typing												import Literal
from typing												import Generator
from types												import GeneratorType
from shutil												import copyfile
from pathlib											import Path
from pygwarts.magical.philosophers_stone				import Transmutable
from pygwarts.magical.philosophers_stone.transmutations	import ControlledTransmutation
from pygwarts.magical.patronus							import CAST
from pygwarts.magical.time_turner						import TimeTurner
from pygwarts.hagrid.thrivables							import Tree
from NavtexBoWAnalyzer.navtex_analyzer					import Navanalyzer
from pygwarts.irma.shelve								import LibraryShelf








class Navpreprocessor(ControlledTransmutation):

	"""
		Special navtex version of LeafGrowth
		name pending... LOL! It is absolutle clear now (05/04/2024 v0.6.1.6) that it is terrible idea...
		How dumb might one be to neglect the work done in previous release (0.5.1.8), where it is absolutly
		clear, that navtex processing must take place in dispatching time, and not after, because when
		it designed for two boughs the second bough is out of line... So now it is a decorator for
		Flourish. It might appear a little wierd, but the idea must be acceaptable... Predispatcher,
		before-Flourish...

		KS10 exluded from regular expression, so it must be hanlded in code.

		Notes:
		- the message structure, that is checked by "MSG_STRUCT" accounts for header and footer newlines
		and for empty lines (\\n only, not lines with spaces);
		- 
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
		analyzer.TEXT_MSG_STRUCT = pmake(r"^\n(?:[ =!\"'\(\)\+,\-\./0-9:;A-Z]+\n)+$")




		def transmutation(upper_layer :Transmutable) -> Transmutable :
			class Preprocessor(chained(upper_layer)):

				def __call__(
								self,
								*plants	:Tuple[
									Tuple[
										str, Generator[Tuple[Path, List[Path], List[Path]], None,None]
									],	...
								]
							):


					# TO DO:	check file name (leaf) to be in uppercase - done in previous vesrion
					# TO DO:	separate (prioritize) "=" check - done by adding "=" to word regex
					# TO DO:	ensure KB00 replacing granted checking (that might means "seeds" maintaining)
					#			- implemented by maintaining "is_new_message" variable as a boolean flag of
					#			inequality of previously shelved and currently parsed CDT's, which guarantee
					#			processing for exectaly situation of KB00 (when there is an old message and
					#			new one replaces it) and so on.
					# TO DO:	mb some messages order check (KE99 must go after KE98).
					# TO DO:	only done (with seeds) if fully processed (like sent to telegram).


					processed	= list()
					Navshelf	= getattr(self, "Navshelf", None)
					Navbow		= getattr(self, "Navbow", dict())
					dispatcher	= str()


					if	not isinstance(Navshelf, LibraryShelf):
						self.loggy.warning(f"No previous NAVTEX watch records found")




					# Unpacking sprout generators
					for sprout, plant in plants:
						if	isinstance(plant, GeneratorType):


							branch, nav_folders, nav_files = next(plant)
							valid_navtex_files = list()


							try:	plant.send(None)
							except	StopIteration:	pass


							self.loggy.debug(f"Current source \"{branch}\"")
							self.loggy.debug(f"Number of files: {len(nav_files)}")




							# Yeah-yeah-yeah, sifting before sifting, then sifting after sifting...
							# Not quit yet! Cause the names of SiftingControllers have changed
							if	callable((Navfiles := getattr(self, "Navfiles", None))):

								sifted_files = Navfiles(nav_files)
								Navfiles.loggy.debug(f"Files after sifting: {len(sifted_files)}")
							else:
								sifted_files = nav_files


							# # As extra (redundant) sifting is no more a subject, the twigs sifting must
							# # happen here. So basically, this might a simple popping out all twigs, cause
							# # in terms of simplification, the sprout must be just a root with NAVTEX files
							# # and any other folders will be popped, cause obviously it's not a NAVTEX files
							# # containers. But, in agile purposes, twigs sifting will do the same interface
							# # as usual for SiftinController. But, there will be the some difference, if no
							# # folder's filter ("Navfolders" in this case) provided, the "sifted_folders"
							# # will be an empty list and repacked to Flourish in that way. This is because
							# # NAVTEX implies not large amount of files to be processed and it might be
							# # simplificated to sprout-filtering.
							# if	callable((Navfolders := getattr(self, "Navfolders", None))):

							# 	sifted_folders = Navfolders(nav_folders)
							# 	Navfolders.loggy.debug(f"Folders after sifting: {len(sifted_folders)}")
							# else:
							# 	sifted_folders = list()




							if	not len(sifted_files):

								self.loggy.debug(f"No NAVTEX files at \"{sprout}\"")
								continue




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

											# HERE IS A TROUBLE!
											# This shelved-check must only prevent "Navanalyzer" job
											# for current file. All files must proceed to dispatcher
											# and be DraftPeek'ed to decide copying, cause the DraftPeek
											# grants files bough persistance!
											#
											# This must solve trouble above
											valid_navtex_files.append(file)
											continue
									else:

										self.loggy.debug(f"No records for \"{file}\", marked as new")
										is_new_message = True
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


										self.loggy.debug(
											"Raw message symbols count: %s"%len(current_check["raw_message"])
										)


								except	Exception as E:

									self.loggy.warning(f"Failed to analyze \"{file}\" due to {CAST(E)}")
									valid_navtex_files.append(file)
									continue




								repr_name = header_id or repr_name




								#
								# Section of decision wether source file must be rewritten or not.
								#
								if	not is_structured:	self.loggy.info(f"{repr_name} failed structure check")
								if	is_sanitized:		self.loggy.info(f"{repr_name} failed layout check")


								if	is_sanitized or not is_structured:
									if	self.rewrite_source(

										file,
										proper_message,
										header=separator,
										footer=separator,

									)	is None:

										# In case source cannot be rewritten, corresponding message will be
										# logged by "rewrite_source" and further processing will be skipped.
										# Hagrid will receive such file anyway.
										valid_navtex_files.append(file)
										continue




								if	header_issue is not None:

									self.loggy.info(f"{header_issue} in {repr_name}")
									current_dispatch += f"{header_issue} in {repr_name}\n"




								# Ignoring all "issues" that might be generated by "analyzer" about CDT,
								# but using fetched date and time strings to process message CDT.
								# Technically it is better to wrap actual "CDT" obtaining in try-except,
								# but if "message_CDT" is not None it must means it was already validated.
								if	message_CDT is not None:
									if(
										len(message_CDT) == 3 and
										isinstance((D := message_CDT[1]), str) and
										isinstance((T := message_CDT[2]), str)
									):
										try:	CDT = TimeTurner(D,T)
										except	Exception as E:
											self.loggy.info(f"Failed to convert CDT for {repr_name}")
										else:
											self.loggy.debug(f"{repr_name} created by {CDT}")
											if	shelved_CDT is not None:
												is_new_message = CDT != shelved_CDT
												# self.loggy.info(f"shelved_CDT = {shelved_CDT}")
												# self.loggy.info(f"CDT = {CDT}")
												# self.loggy.info(f"{is_new_message = }")
											# is_new_message = shelved_CDT <CDT if shelved_CDT is not None else

									else:
										self.loggy.info(f"CDT obtaining problem in {repr_name}")
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




								valid_navtex_files.append(file)
								self.loggy.debug(f"Processed {repr_name}")
							else:
								processed.append([ sprout,( branch, [], valid_navtex_files )])
						else:	self.loggy.warning(f"Invalid sprout \"{plant}\", {type(plant)}")
					else:		self.loggy.debug(f"Prepared plants: {len(processed)}")




					if	callable(pool := getattr(self.loggy, "pool", None)):

						# All NL that wrapps final message over top and bottom must be stripped
						# before message will be pushed to the pool.
						if	dispatcher : pool(("\n%s\n"%dispatcher).strip("\n"))


					# Passing inner shelf so every new word will be stored in both shelfs and "modified"
					# flag will be successfully triggered for LibraryShelf object. The "produce" method for
					# NavBow must be invoked with from_outer flag set to True to maintain only new words.
					analyzer.update_BoW(Navbow)


					# Repacking plants for Flourish. As making generator means make use of variables pointers,
					# so once packed and then changed, at unpacking time will be the same value. That's why
					# repacking takes place in a loop, where each generator being processed separately.
					for _sprout, _plant in processed:
						super().__call__(( _sprout,(( *_plant, ) for _ in range(1) )))




				def rewrite_source(	self,
									file_path			:Path,
									message				:str,
									header				:str	="",
									footer				:str	="",
								)-> Literal[True] | None:

					"""
						Rewrite sanitaized source message file.

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







