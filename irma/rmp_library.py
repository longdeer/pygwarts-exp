import	re
from	os										import makedirs
from	typing									import Literal
from	collections								import defaultdict
from	collections								import Counter
from	pygwarts.magical.time_turner			import TimeTurner
from	pygwarts.magical.time_turner.timers 	import Callstamp
from	pygwarts.magical.time_turner.utils 		import hundscale
from	pygwarts.magical.time_turner.utils		import DATETIME_1_P
from	pygwarts.magical.spells					import patronus
from	pygwarts.irma.contrib					import LibraryContrib
from	pygwarts.irma.shelve					import LibraryShelf
from	pygwarts.irma.shelve.casing				import shelf_case
from	pygwarts.irma.shelve.casing				import is_num
from	pygwarts.irma.shelve.casing				import num_diff
from	pygwarts.irma.shelve.casing				import mostsec_diff
from	pygwarts.irma.shelve.casing				import byte_size_diff
from	pygwarts.irma.access					import LibraryAccess
from	pygwarts.irma.access.volume				import LibraryVolume
from	pygwarts.irma.access.bookmarks			import VolumeBookmark
from	pygwarts.irma.access.bookmarks.counters	import WarningCount
from	pygwarts.irma.access.bookmarks.counters	import ErrorCount
from	pygwarts.irma.access.bookmarks.counters	import CriticalCount
from	pygwarts.irma.access.bookmarks.viewers	import ViewWrapper
from	pygwarts.irma.access.bookmarks.viewers	import ViewCase
from	pygwarts.irma.access.handlers			import AccessHandlerRegisterCounter
from	pygwarts.irma.access.handlers.counters	import AccessCounter
from	pygwarts.irma.access.handlers.parsers	import GroupParser
from	pygwarts.irma.access.handlers.parsers	import TargetHandler
from	pygwarts.irma.access.handlers.parsers	import TargetNumberAccumulator
from	pygwarts.irma.access.handlers.parsers	import TargetStringAccumulator
from	pygwarts.irma.access.inducers			import AccessInducer
from	pygwarts.irma.access.inducers.counters	import RegisterCounterInducer
from	pygwarts.irma.access.inducers.recap		import RegisterRecapInducer
from	pygwarts.irma.access.inducers.filters	import plurnum
from	pygwarts.irma.access.inducers.filters	import posnum
from	pygwarts.irma.access.inducers.case		import InducerCase
from	pygwarts.irma.access.annex				import VolumeAnnex
from	pygwarts.irma.access.annex				import LibraryAnnex
from	pygwarts.irma.access.utils				import TextWrapper
from	pygwarts.filch.marauders_map			import MaraudersMap
from	pygwarts.filch.nettherin				import VALID_IP4
from	pygwarts.filch.linkindor				import VALID_MAC
from	pygwarts.filch.linkindor.arp			import ARPResponseInspector
from	pygwarts.filch.linkindor.arp			import ARPRequestInspector
from	irma_local_access						import DiffCaseRegisterRecapAccumulatorInducer
from	irma_local_access						import FilchWatchInducer
from	irma_local_intercept					import TelegramTechHoist








tpoint	= TimeTurner()
ypoint	= TimeTurner(days=-1)
yypoint	= TimeTurner(days=-2)
iroot	= "/srv/lcontainer/irma"
froot	= "/srv/lcontainer/filch"
hroot	= "/srv/lcontainer/hagrid"








class Library(LibraryAccess):

	@TelegramTechHoist
	class loggy(LibraryContrib):

		handler		= f"{iroot}/library/{tpoint.Ym_aspath}/library{tpoint.dmY_asjoin}.loggy"
		init_name	= "irma"

	@Callstamp
	class Annex(LibraryAnnex): 		pass
	class filchmap(MaraudersMap):	pass
	class library_shelf(LibraryShelf):

		grabbing	= f"{iroot}/xshelf/{yypoint.Ym_aspath}/library{yypoint.dmY_asjoin}.xshelf"
		producing	= f"{iroot}/xshelf/{ypoint.Ym_aspath}/library{ypoint.dmY_asjoin}.xshelf"


	case_link	= "library_shelf"
	unique		= True
	joint		= ", "


	@ViewWrapper("\nWARNINGS: ")
	@ViewCase("library_shelf", prep=is_num, post=num_diff)
	class Warnings(WarningCount):	pass
	@ViewWrapper("\nERRORS: ")
	@ViewCase("library_shelf", prep=is_num, post=num_diff)
	class Errors(ErrorCount):		pass
	@ViewWrapper("\nCRITICALS: ")
	@ViewCase("library_shelf", prep=is_num, post=num_diff)
	class Criticals(CriticalCount):	pass


	class CallstampActivity(VolumeBookmark):

		trigger		= " finished in "
		rpattern	= r"finished in (?P<target>[\.\d]+)( seconds)?$"

		class Activities(AccessCounter):

			@TextWrapper("\nactivities: ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class Inducer(RegisterCounterInducer): filter = plurnum

		@AccessHandlerRegisterCounter
		class Duration(TargetNumberAccumulator):

			@TextWrapper("\ntotal time: ")
			@InducerCase("library_shelf", prep=is_num, post=mostsec_diff)
			class Total(RegisterRecapInducer): filter = posnum

			@TextWrapper("\naverage time: ")
			@InducerCase("library_shelf", prep=is_num, post=mostsec_diff)
			class Average(AccessInducer):
				def __call__(self, volume :LibraryVolume) -> str | None :

					if	isinstance(recap := self.get_register_recap(volume), int | float):
						if	isinstance(counter := self.get_register_counter(volume), int):
							if	1 <counter : return str(recap /counter)



	class ShelfTrackers(VolumeBookmark):

		trigger	= "Discarded tracker for"

		class Counter(AccessCounter):

			@TextWrapper("\ntrackers removed: ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class Inducer(RegisterCounterInducer): filter = posnum


	class ShelfProduces(VolumeBookmark):

		trigger	= "successfully produced"

		class Counter(AccessCounter):

			@TextWrapper("\nshelve produced: ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class Inducer(RegisterCounterInducer): filter = posnum


	class GrownCounter(VolumeBookmark):

		trigger		= "Grown leaf"
		rpattern	=  r".+ Grown leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		@AccessHandlerRegisterCounter
		class Accumulator(TargetStringAccumulator):

			@TextWrapper("\nfiles copied ",": ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class CountInducer(RegisterCounterInducer): filter = posnum
			class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):	pass


	class MovedCounter(VolumeBookmark):

		trigger		= "Moved leaf"
		rpattern	=  r".+ Moved leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		@AccessHandlerRegisterCounter
		class Accumulator(TargetStringAccumulator):

			@TextWrapper("\nfiles moved ",": ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class CountInducer(RegisterCounterInducer): filter = posnum
			class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):	pass


	class ClonedCounter(VolumeBookmark):

		trigger		= "Cloned leaf"
		rpattern	=  r".+ Cloned leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		@AccessHandlerRegisterCounter
		class Accumulator(TargetStringAccumulator):

			@TextWrapper("\nfiles cloned ",": ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class CountInducer(RegisterCounterInducer): filter = posnum
			class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):	pass


	class PushedCounter(VolumeBookmark):

		trigger		= "Pushed leaf"
		rpattern	=  r".+ Pushed leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		@AccessHandlerRegisterCounter
		class Accumulator(TargetStringAccumulator):

			@TextWrapper("\nfiles pushed ",": ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class CountInducer(RegisterCounterInducer): filter = posnum
			class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):	pass


	class ThrivedCounter(VolumeBookmark):

		trigger		= "Thrived twig"
		rpattern	=  r".+ Thrived twig \".+[/\\](?P<target>[^/\\]+)\"$"

		@AccessHandlerRegisterCounter
		class Accumulator(TargetStringAccumulator):

			@TextWrapper("\nfolders copied ",": ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class CountInducer(RegisterCounterInducer): filter = posnum
			class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):	pass


	class TrimmedLeafsCounter(VolumeBookmark):

		trigger		= "Trimmed leaf"
		rpattern	=  r".+ Trimmed leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		@AccessHandlerRegisterCounter
		class Accumulator(TargetStringAccumulator):

			@TextWrapper("\nfiles removed ",": ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class CountInducer(RegisterCounterInducer): filter = posnum
			class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):	pass


	class TrimmedTwigsCounter(VolumeBookmark):

		trigger		= "Trimmed twig"
		rpattern	=  r".+ Trimmed twig \".+[/\\](?P<target>[^/\\]+)\"$"

		@AccessHandlerRegisterCounter
		class Accumulator(TargetStringAccumulator):

			@TextWrapper("\nfolders removed ",": ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class CountInducer(RegisterCounterInducer): filter = posnum
			class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):	pass


	class WieghtCounter(VolumeBookmark):

		trigger	= "INFO : Size:"
		rpattern= r".+ Size: (?P<target>\d+)$"

		class Handler(TargetHandler):

			@TextWrapper("\ntotal space: ")
			@InducerCase("library_shelf", prep=is_num, post=byte_size_diff)
			class Inducer(RegisterRecapInducer):						pass


	class TwigsCounter(VolumeBookmark):

		trigger	= "INFO : Twigs:"
		rpattern= r".+ Twigs: (?P<target>\d+)$"

		class Handler(TargetHandler):

			@TextWrapper("\nfolders: ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class Inducer(RegisterRecapInducer):						pass


	class LeafsCounter(VolumeBookmark):

		trigger	= "INFO : Leafs:"
		rpattern= r".+ Leafs: (?P<target>\d+)$"

		class Handler(TargetHandler):

			@TextWrapper("\nfiles: ")
			@InducerCase("library_shelf", prep=is_num, post=num_diff)
			class Inducer(RegisterRecapInducer):						pass




	class NavDrop(LibraryVolume):

		inrange		= ypoint.dmY_aspath
		location	= f"{hroot}/navdrop/{ypoint.Ym_aspath}/navdrop{ypoint.dmY_asjoin}.loggy"

		@TextWrapper("\n\thagrid-navdrop\n","\n")
		class Annex(VolumeAnnex): pass


	class SoftSync(LibraryVolume):

		inrange		= ypoint.dmY_aspath
		location	= f"{hroot}/softsync/{ypoint.Ym_aspath}/softsync{ypoint.dmY_asjoin}.loggy"

		@TextWrapper("\n\thagrid-softsync\n","\n")
		class Annex(VolumeAnnex): pass


	class HardSync(LibraryVolume):

		inrange		= tpoint.dmY_aspath
		location	= f"{hroot}/hardsync/{tpoint.Ym_aspath}/hardsync{tpoint.dmY_asjoin}.loggy"

		@TextWrapper("\n\thagrid-hardsync\n","\n")
		class Annex(VolumeAnnex): pass


	class Arch(LibraryVolume):

		inrange		= ypoint.dmY_aspath
		location	= f"{hroot}/arch/{ypoint.Ym_aspath}/arch{ypoint.dmY_asjoin}.loggy"

		@TextWrapper("\n\thagrid-arch\n","\n")
		class Annex(VolumeAnnex): pass




	class Discovery(LibraryVolume):


		inrange		= ypoint.dmY_aspath
		location	= f"{froot}/discovery/{ypoint.Ym_aspath}/discovery{ypoint.dmY_asjoin}.loggy"


		@TextWrapper("\n\tfilch-discovery\n","\n")
		class Annex(VolumeAnnex):		pass
		class filchmap(MaraudersMap):	pass
		class Watch(VolumeBookmark):


			trigger		= "Received response for"
			rpattern	= rf"(?P<ip>{VALID_IP4}) at (?P<mac>{VALID_MAC})"


			class Inspector(ARPResponseInspector): pass
			class DiscoveredHosts(GroupParser):

				def __call__(self, line :str, volume :LibraryVolume) -> Literal[True] | None :

					if	isinstance(getattr(self, "rpattern", None), re.Pattern):
						if	(match := self.rpattern.search(line)) and (target := match.group("ip", "mac")):
							if	(len(target) == 2) and self.registered(volume):

								ip,mac = target
								self.loggy.debug(f"Considering {mac} discover at {ip}")

								if	(result := self.Inspector(ip, mac)) is not None:
									match result["state"]:

										case 159 | 63: volume[self].setdefault("known_hosts",list()).append(
											{
												**result,
												"description": self.filchmap.ip4map_desc(result["source ip4"])
											}
										)
										case 223: volume[self].setdefault("mismatched_mac",list()).append(dict(result))
										case 199: volume[self].setdefault("unknown_mac",list()).append(dict(result))
										case 216: volume[self].setdefault("mismatched_ip",list()).append(dict(result))
										case 224: volume[self].setdefault("unknown_ip",list()).append(dict(result))
										case rst: self.loggy.warning(f"{self} discovered unknown state {rst}")


									return True


						else:	self.loggy.debug(f"Invalid parse result for line \"{line}\"")
					else:		self.loggy.debug(f"Pattern to match not found")


				@TextWrapper("\nhosts mapped: ")
				@InducerCase("library_shelf", prep=is_num, post=num_diff)
				class MappedHostsInducer(AccessInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :

						if	isinstance(getattr(self, "filchmap"), MaraudersMap):
							if	(hosts := len(self.filchmap.ip4)):

								return str(hosts)


				@TextWrapper("\nhosts discovered: ")
				@InducerCase("library_shelf", prep=is_num, post=num_diff)
				class DiscoveredHostsInducer(RegisterCounterInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :
						if	isinstance(recap := volume[self._UPPER_LAYER], dict):

							return (

								len(recap.get("mismatched_mac",[]))	+
								len(recap.get("mismatched_ip",[]))	+
								len(recap.get("unknown_mac",[]))	+
								len(recap.get("unknown_ip",[]))		+
								len(recap.get("known_hosts",[]))
							)


				@TextWrapper("\n\nmismatched hosts: ")
				class MismatchedHostsInducer(FilchWatchInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :
						if	isinstance(recap := volume[self._UPPER_LAYER], dict):

							misses = list()

							if	(miss_mac := recap.get("mismatched_mac")):	misses.extend(miss_mac)
							if	(miss_ip := recap.get("mismatched_ip")):	misses.extend(miss_ip)
							if	(amount := len(misses)):

								missed = [

									"%s responded from %s"%(

										record.get("source MAC to name"),
										f"{record.get('source ip4 to name')} ip4"

										if record.get("source ip4 to MAC") is not None else

										f"unknown {record.get('source ip4')}"
									)

									for record in misses
								]
								return	"%s\n\t%s"%(

									self.filch_caseamount(amount, volume),
									"\n\t".join(self.filch_caserecords(missed, volume))
								)


				@TextWrapper("\n\nunknown hosts: ")
				class UnknownHostsInducer(FilchWatchInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :
						if	isinstance(recap := volume[self._UPPER_LAYER], dict):

							unknowns = list()

							if	(no_mac := recap.get("unknown_mac")):	unknowns.extend(no_mac)
							if	(no_ip := recap.get("unknown_ip")):		unknowns.extend(no_ip)
							if	(amount := len(unknowns)):

								unknown = [

									"%s responded from %s"%(

										record.get("source MAC"),
										f"{record.get('source ip4 to name')} ip4"

										if record.get("source ip4 to MAC") is not None else

										f"unknown {record.get('source ip4')}"

									)	for record in unknowns
								]
								return	"%s\n\t%s"%(

									self.filch_caseamount(amount, volume),
									"\n\t".join(self.filch_caserecords(unknown, volume))
								)


				@TextWrapper("\n\nmapped up: ")
				class KnownHostsInducer(FilchWatchInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :

						if	isinstance(recap := volume[self._UPPER_LAYER], dict):
							if	(hosts := recap.get("known_hosts")) is not None:

								if	(amount := len(hosts)):

									up = [

										f"{record.get('source ip4 to name')} ({record.get('description')})"
										for record in hosts
									]
									return "%s\n\t%s"%(

										self.filch_caseamount(amount, volume),
										"\n\t".join(self.filch_caserecords(up, volume))
									)


				@TextWrapper("\n\nmapped down: ")
				class DownHostsInducer(FilchWatchInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :

						if	isinstance(recap := volume[self._UPPER_LAYER], dict):
							if	(hosts := recap.get("known_hosts")) is not None:

								up = { record.get("source ip4") for record in hosts }
								down = [ ip4 for ip4 in self.filchmap.ip4 if ip4 not in up ]

								if	(amount := len(down)):

									downs = [

										"%s (%s)"%(

											self.filchmap.ip4[record].get("NAME"),
											self.filchmap.ip4[record].get("DESC")

										)	for record in down
									]
									return	"%s\n\t%s"%(

										self.filch_caseamount(amount, volume),
										"\n\t".join(self.filch_caserecords(downs, volume))
									)


	class Broad(LibraryVolume):


		plotdate	= ypoint
		inrange		= ypoint.dmY_aspath
		plotdir		= f"/srv/dump/bwvisual/{ypoint.Ymd_aspath}"
		location	= f"{froot}/broadwatch/{ypoint.Ym_aspath}/broadwatch{ypoint.dmY_asjoin}.loggy"


		@TextWrapper("\n\tfilch-broadwatch\n","\n")
		class Annex(VolumeAnnex): pass
		class Watch(VolumeBookmark):


			trigger		= "who has"
			rpattern	= rf"(?P<dst>{VALID_IP4}) says (?P<src>{VALID_IP4}) \((?P<mac>{VALID_MAC})\)$"


			class Inspector(ARPRequestInspector): pass
			@AccessHandlerRegisterCounter
			class TrappedRequests(GroupParser):

				def __call__(self, line :str, volume :LibraryVolume) -> Literal[True] | None :

					if	self.registered(volume) and (result := self.Inspector(line)) is not None:

						try:	DT = TimeTurner(*DATETIME_1_P.search(line).group("date", "time"))
						except	Exception as E:

							self.loggy.warning(f"Failed to obtain datetime due to {patronus(E)}")
							return


						match result["state"]:

							case 3581 | 2557 | 1533 | 509:

								volume[self].setdefault("mapped",list()).append(dict(**result, timestamp=DT))

							case 3584 | 1924 | 1536 | 1145:

								volume[self].setdefault("unknown",list()).append(dict(**result, timestamp=DT))

							case 2022 | 1926 | 1634 | 1538 | 998:

								volume[self].setdefault("ip4_lookup",list()).append(dict(**result, timestamp=DT))

							case 4093 | 3997 | 3680 | 2045 | 2020 | 1949 | 1657 | 1632 | 1561 | 1021 | 996:

								volume[self].setdefault("mismatches",list()).append(dict(**result, timestamp=DT))

							case rst: self.loggy.warning(f"{self} discovered unknown state {rst}")


						return True


				@TextWrapper("\nrequests trapped: ")
				@InducerCase("library_shelf", prep=is_num, post=num_diff)
				class TotalTrappedInducer(RegisterCounterInducer):	pass


				@TextWrapper("\ngraphs plotted: ")
				class Plotter(FilchWatchInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :
						if	isinstance(recap := volume[self._UPPER_LAYER], dict):

							totals = defaultdict(int)
							requests = defaultdict(lambda : defaultdict(int))

							for record in recap.get("mapped",list()):
								if	isinstance(stamp := record.get("timestamp"), TimeTurner):

									point = int(hundscale(stamp.HM_asjoin))
									requests[record.get("source ip4 to name")][point] += 1
									totals[point] += 1


							for record in recap.get("ip4_lookup",list()):
								if	isinstance(stamp := record.get("timestamp"), TimeTurner):

									point = int(hundscale(stamp.HM_asjoin))
									requests[record.get("source ip4")][point] += 1
									totals[point] += 1


							for record in recap.get("mismatches",list()):
								if	isinstance(stamp := record.get("timestamp"), TimeTurner):

									point = int(hundscale(stamp.HM_asjoin))
									requests[record.get("source ip4")][point] += 1
									totals[point] += 1


							for record in recap.get("unknown",list()):
								if	isinstance(stamp := record.get("timestamp"), TimeTurner):

									point = int(hundscale(stamp.HM_asjoin))
									totals[point] += 1

									match record.get("state"):

										case 3584 | 1924 | 1536:

											requests[record.get("source ip4")][point] += 1

										case 1145: requests[record.get("source ip4 to name")][point] += 1
										case rest: self.loggy.warning(f"{self} discovered unknown state {rest}")


							if	(amount := len(requests)):

								ndate = self.plotdate.dmY_aspath
								pdate = self.plotdate.dmY_asjoin
								fsdir = self.plotdir
								count = 0

								self.loggy.info(f"Plotting total by {ndate}")
								self.broad_plot(

									axises=totals.items(),
									title=f"total by {ndate}",
									pngpath=fsdir,
									pngname=f"total-{pdate}.png",
								)

								for src, mapping in requests.items():

									self.loggy.info(f"Plotting {src} by {ndate}")
									count += bool(

										self.broad_plot(

											axises=mapping.items(),
											title=f"{src} by {ndate}",
											pngpath=fsdir,
											pngname=f"{src}-{pdate}.png",
										)
									)

								casecount = self.filch_casing(

									count,
									volume,
									getattr(self, getattr(self, "case_link", ""), None),
									"count",
									is_num,
									num_diff
								)
								return f"{casecount}/{amount}" if count != amount else casecount


				@TextWrapper("\n\nmismatches: ")
				class MismatchedRequestsInducer(FilchWatchInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :
						if	isinstance(recap := volume[self._UPPER_LAYER], dict):
							if	isinstance(records := recap.get("mismatches"), list):

								events	= list()
								stamps	= list()
								uniques	= set()

								for record in records:

									stamp = record["timestamp"].format("%H%M %d/%m/%Y")
									match record.get("state"):

										case 4093:	event = "%s gratuitous from %s ip4"%(

											record.get("source MAC to name"), record.get("target ip4 to name")
										)
										case 3997:	event = "%s gratuitous from %s ip4"%(

											record.get("source MAC"), record.get("target ip4 to name")
										)
										case 3680:	event = "%s gratuitous from unknown %s"%(

											record.get("source MAC to name"), record.get("target ip4")
										)
										case 2045:	event = "%s requested from %s ip4"%(

											record.get("source MAC to name"), record.get("source ip4 to name")
										)
										case 2020:	event = "%s requested from unknown %s"%(

											record.get("source MAC to name"), record.get("source ip4")
										)
										case 1949:	event = "%s requested from %s ip4"%(

											record.get("source MAC"), record.get("source ip4 to name")
										)
										case 1657:	event = "%s requested unknown %s from %s ip4"%(

											record.get("source MAC to name"),
											record.get("target ip4"),
											record.get("source ip4 to name")
										)
										case 1632:	event = "%s requested unknown %s from unknown %s"%(

											record.get("source MAC to name"),
											record.get("target ip4"),
											record.get("source ip4")
										)
										case 1561:	event = "%s requested unknown %s from %s ip4"%(

											record.get("source MAC"),
											record.get("target ip4"),
											record.get("source ip4 to name")
										)
										case 1021:	event = "%s requested %s ip4 from %s ip4"%(

											record.get("source MAC to name"),
											record.get("source MAC to name"),
											record.get("source ip4 to name")
										)
										case 996:	event = "%s requested %s ip4 from unknown %s"%(

											record.get("source MAC to name"),
											record.get("source MAC to name"),
											record.get("source ip4")
										)
										case rst:

											self.loggy.warning(f"{self} discovered unknown state {rst}")
											continue


									if	(current := f"{event} at {stamp}") not in uniques:

										uniques.add(current)
										events.append(event)
										stamps.append(stamp)


								if	(amount := len(uniques)):
									return "%s\n\t%s"%(

										self.filch_caseamount(amount, volume),
										"\n\t".join(

											f"{event} at {stamp}"
											for	event,stamp
											in	zip(self.filch_caserecords(events, volume), stamps)
										)
									)


				@TextWrapper("\n\nip4 lookups: ")
				class LookupRequestsInducer(FilchWatchInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :

						if	isinstance(recap := volume[self._UPPER_LAYER], dict):
							if	isinstance(records := recap.get("ip4_lookup"), list):

								events	= list()
								stamps	= list()
								uniques	= set()

								for record in records:

									stamp = record["timestamp"].format("%H%M %d/%m/%Y")
									match record.get("state"):

										case 998:	event = f"{record.get('source MAC to name')} ip4 lookup"
										case 1538:	event = "%s ip4 lookup for unknown %s"%(

												record.get("source MAC"), record.get("target ip4")
											)
										case 1634:	event = "%s ip4 lookup for unknown %s"%(

												record.get("source MAC to name"), record.get("target ip4")
											)
										case 1926:	event = "%s ip4 lookup for %s"%(

												record.get("source MAC"), record.get("target ip4 to name")
											)
										case 2022:	event = "%s ip4 lookup for %s"%(

												record.get("source MAC to name"), record.get("target ip4 to name")
											)
										case rst:

											self.loggy.warning(f"{self} discovered unknown state {rst}")
											continue


									if	(current := f"{event} at {stamp}") not in uniques:

										uniques.add(current)
										events.append(event)
										stamps.append(stamp)


								if	(amount := len(uniques)):
									return "%s\n\t%s"%(

										self.filch_caseamount(amount, volume),
										"\n\t".join(

											f"{event} at {stamp}"
											for	event,stamp
											in	zip(self.filch_caserecords(events, volume), stamps)
										)
									)


				@TextWrapper("\n\nunknown requests: ")
				class UnmappedRequestsInducer(FilchWatchInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :

						if	isinstance(recap := volume[self._UPPER_LAYER], dict):
							if	isinstance(records := recap.get("unknown"), list):

								requests = defaultdict(lambda : defaultdict(int))

								for record in records:
									if	isinstance(record,dict):
										match record.get("state"):

											case 3584 | 1536:

												requests[f"{record.get('source ip4')} ({record.get('source MAC')})"][record.get("target ip4")] += 1

											case 1924:

												requests[f"{record.get('source ip4')} ({record.get('source MAC')})"][record.get("target ip4 to name")] += 1

											case 1145: requests[record.get("source ip4 to name")][record.get("target ip4")] += 1
											case rest: self.loggy.warning(f"{self} discovered unknown state {rest}")


								return self.broad_gather(

									requests,
									volume,
									getattr(self, getattr(self, "case_link", ""), None)
								)


				@TextWrapper("\n\nmapped requests: ")
				class MappedRequestsInducer(FilchWatchInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :

						if	isinstance(recap := volume[self._UPPER_LAYER], dict):
							if	isinstance(records := recap.get("mapped"), list):

								requests = defaultdict(lambda : defaultdict(int))

								for record in records:
									if	isinstance(record,dict):

										requests[record.get("source ip4 to name")][record.get("target ip4 to name")] += 1

								return	self.broad_gather(

									requests,
									volume,
									getattr(self, getattr(self, "case_link", ""), None)
								)


	class SNMP(LibraryVolume):


		inrange		= ypoint.dmY_aspath
		location	= f"{froot}/snmpwatch/{ypoint.Ym_aspath}/snmpwatch{ypoint.dmY_asjoin}.loggy"


		@TextWrapper("\n\tfilch-snmpwatch\n","\n")
		class Annex(VolumeAnnex):		pass
		class Watch(VolumeBookmark):


			trigger		= r"v1 trap"
			rpattern	= rf"\(v1 trap\) (?P<target>.+)"


			@AccessHandlerRegisterCounter
			class Accumulator(TargetStringAccumulator):

				@TextWrapper("\nv1 traps: ")
				class Inducer(FilchWatchInducer):
					def __call__(self, volume :LibraryVolume) -> str | None :

						if	isinstance(recap := self.get_register_recap(volume), list):
							if	isinstance(counter := self.get_register_counter(volume), int):

								count = Counter(recap)
								scount = sorted(

									count,
									key=lambda trap : count[trap],
									reverse=True
								)

								return "%s\n\t%s"%(

									self.filch_caseamount(counter, volume),
									"\n\t".join(

										"%s: %s"%(

											trap,
											self.filch_casing(

												count[trap],
												volume,
												getattr(self, getattr(self, "case_link", ""), None),
												trap,
												is_num,
												num_diff
											)
										)	for trap in scount
									)
								)


	class Overseer(LibraryVolume):


		inrange		= ypoint.dmY_aspath
		location	= f"/srv/lcontainer/sndbx/overseer/loggy/{ypoint.dmY_asjoin}.loggy"


		@TextWrapper("\n\toverseer\n","\n")
		class Annex(VolumeAnnex): pass
		class Watch(VolumeBookmark):


			trigger		= "poll response:"
			rpattern	= re.compile(
				rf"""
					(?P<src>{VALID_IP4})\ poll\ response:\ 
					upsSmartInputLineVoltage:\ (?P<ilv>[\d\.]+)\ V,.+\ 
					upsSmartOutputLoad:\ (?P<sol>\d\d?)\ %,.+\ 
					upsSmartBatteryTemperature:\ (?P<sbt>[\d\.]+)\ °C
				""",
				re.VERBOSE
			)


			class Accumulator(GroupParser):
				def __call__(self, line :str, volume :LibraryVolume) -> Literal[True] | None :

					if	isinstance(getattr(self, "rpattern", None), re.Pattern):
						if	(match := self.rpattern.search(line)):
							src, ilv, sol, sbt = match.group("src", "ilv", "sol", "sbt")

							if	self.registered(volume):
								if	src:

									current = volume[self].setdefault("recap",dict()).setdefault(src,dict())

									if ilv : current.setdefault("input, V",list()).append(float(ilv))
									if sol : current.setdefault("load, %",list()).append(float(sol))
									if sbt : current.setdefault("temperature, °C",list()).append(float(sbt))

									return bool(ilv) or bool(sol) or bool(sbt)


				@TextWrapper("\nupswatch:","\n")
				class Inducer(AccessInducer):

					def __call__(self, volume :LibraryVolume) -> str | None :
						if	isinstance(recap := self.get_register_recap(volume), dict):
							induce = str()

							for src,stat in recap.items():
								if	isinstance(stat,dict):

									self.library_shelf["overseer"] = self.library_shelf["overseer"] or dict()
									host = self.filchmap.ip4map_name(src)
									induce += f"\n\t{host}:\n"

									for item,metrics in stat.items():

										minv = shelf_case(

											min(metrics),
											key=f"{host} minimum {item}",
											shelf=self.library_shelf["overseer"],
											prep=is_num,
											post=num_diff
										)
										maxv = shelf_case(

											max(metrics),
											key=f"{host} maximum {item}",
											shelf=self.library_shelf["overseer"],
											prep=is_num,
											post=num_diff
										)

										induce += f"\t\tminimum {item}: {minv}\n"
										induce += f"\t\tmaximum {item}: {maxv}\n"

							if induce : return induce








if	__name__ == "__main__":

	irma = Library()
	irma.filchmap.CSV(

		f"{froot}/broadmap.csv",
		";",
		IP4=0,
		MAC=1,
		NAME=2,
		DESC=3
	)
	irma.Discovery.filchmap.CSV(

		f"{froot}/discoverymap.csv",
		";",
		IP4=0,
		MAC=1,
		NAME=2,
		DESC=3
	)
	annex = irma.Annex()
	irma.library_shelf.produce(ignore_mod=True, strict_mode=False)

	if	len(annex):

		makedirs(f"{iroot}/annex/{ypoint.Ym_aspath}", exist_ok=True)
		with open(f"{iroot}/annex/{ypoint.Ym_aspath}/library{ypoint.dmY_asjoin}.annex", "w") as dump:

			dump.write(annex)







