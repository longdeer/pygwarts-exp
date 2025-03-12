# from pygwarts.magical.chests					import Chest
# from pygwarts.magical.chests					import KeyChest
# from pygwarts.magical.time_turner.timers		import Timestamp
# from pygwarts.irma.shelve.casing				import numdiffcase
# from pygwarts.irma.shelve.casing				import seqcase
# from pygwarts.irma.access						import LibraryAccess
# from pygwarts.irma.access.volume				import AnnexWrapper
# from pygwarts.irma.access.bookmark				import Bookmark
# from pygwarts.irma.access.bookmarks.counters	import WarningLevelCounter
# from pygwarts.irma.access.bookmarks.counters	import ErrorLevelCounter
# from pygwarts.irma.access.bookmarks.counters	import CriticalLevelCounter
# from pygwarts.irma.access.inducers				import printf_style
# from pygwarts.irma.access.inducers.register		import RegisterCounterInducer
# from filch_handlers								import DiscoverywatchAccessHandler
# from filch_handlers								import SNMPWatchAccessHandler
# from filch_inducers								import FilchMapInducer
# from filch_inducers								import DiscoveredUpsInducer
# from filch_inducers								import DiscoveredDownsInducer
# from filch_inducers								import DiscoveredMissesInducer
# from filch_inducers								import DiscoveredUnmapsInducer
# from filch_inducers								import BroadMapsInducer
# from filch_inducers								import BroadUnmapsInducer
# from filch_inducers								import BroadMissesInducer
# from filch_inducers								import ipDiscoveryInducer
# from filch_inducers								import BroadPlotInducer
# from filch_inducers								import filchcase
# from filch_inducers								import SNMPInducer
# from hagrid_bookmarks							import Leafs
# from hagrid_bookmarks							import Branches
# from hagrid_bookmarks							import Twigs
# from hagrid_bookmarks							import Masses
# from hagrid_bookmarks							import Navtex
# from irma_bookmarks								import OptimizedTimestampActivity
# from irma_bookmarks								import ShelfCleans
# from irma_bookmarks								import ShelfProduces

from collections								import defaultdict
from pygwarts.magical.time_turner				import TimeTurner
from pygwarts.irma.contrib						import LibraryContrib

from pygwarts.filch.nettherin			import VALID_IP4
from pygwarts.filch.linkindor			import VALID_MAC

from pygwarts.magical.spells			 		import flagrate
from pygwarts.irma.shelve						import LibraryShelf
from pygwarts.irma.access						import LibraryAccess
from pygwarts.filch.marauders_map				import MaraudersMap
from pygwarts.irma.access.bookmarks.counters	import WarningCount
from pygwarts.irma.access.bookmarks.counters	import ErrorCount
from pygwarts.irma.access.bookmarks.counters	import CriticalCount
from pygwarts.irma.access.bookmarks.viewers		import ViewWrapper
from pygwarts.irma.access.bookmarks.viewers		import ViewCase
from pygwarts.irma.shelve.casing				import is_num
from pygwarts.irma.shelve.casing				import num_diff

from pygwarts.irma.access.volume				import LibraryVolume
from pygwarts.irma.access.bookmarks				import VolumeBookmark
from pygwarts.irma.access.handlers				import AccessHandlerRegisterCounter
from pygwarts.irma.access.handlers.counters		import AccessCounter
from pygwarts.irma.access.handlers.parsers		import TargetHandler
from pygwarts.irma.access.handlers.parsers		import TargetNumberAccumulator
from pygwarts.irma.access.handlers.parsers		import TargetStringAccumulator
from pygwarts.irma.access.inducers				import AccessInducer
from pygwarts.irma.access.inducers.counters		import RegisterCounterInducer
from pygwarts.irma.access.inducers.recap		import RegisterRecapInducer
from pygwarts.irma.access.inducers.filters		import plurnum
from pygwarts.irma.access.inducers.filters		import posnum
from pygwarts.irma.access.utils					import TextWrapper
from pygwarts.irma.access.utils					import byte_size_string
from pygwarts.irma.shelve.casing				import ShelfCase
from pygwarts.irma.shelve.casing				import NumDiffCase
from casing										import mostsec_diff
from casing										import byte_size_diff
from pygwarts.magical.time_turner.timers 		import mostsec
from pygwarts.irma.access.annex					import VolumeAnnex
from pygwarts.irma.access.annex					import LibraryAnnex
from pygwarts.irma.shelve.casing				import shelf_case
from pygwarts.irma.shelve.casing				import is_iterable
from pygwarts.irma.shelve.casing				import seq_diff
from pygwarts.irma.access.inducers.case			import InducerCase

from handlers									import DiscoverywatchAccessHandler
from handlers									import BroadwatchAccessHandler
from inducers									import DiffCaseRegisterRecapAccumulatorInducer
from inducers									import FilchWatchInducer







# # Date points for logging and access
# tpoint	= TimeTurner()
# ypoint	= TimeTurner(days=-1)
# yypoint	= TimeTurner(days=-2)








# def mostsec_diff(num1 :int|float|str, num2 :int|float|str) -> str :

# 	diff = eval(f"{num1}-{num2 if num2 is not None else 0}")
# 	left = f"{' (-' if str(diff).startswith('-') else ' (+'}"

# 	return f"{mostsec(num1)}{left}{mostsec(diff)})"


# def byte_size_diff(num1 :int|float|str, num2 :int|float|str) -> str :

# 	diff = eval(f"{num1}-{num2 if num2 is not None else 0}")
# 	left = f"{' (-' if str(diff).startswith('-') else ' (+'}"

# 	return f"{byte_size_string(num1)}{left}{byte_size_string(abs(diff))})"








# class AccumulatorInducer(AccessInducer):

# 	case_link	= "library_shelf"
# 	unique		= True
# 	joint		= ", "

# 	def __call__(self, volume :LibraryVolume) -> str :

# 		if	isinstance(recap := self.get_register_recap(volume), list):
# 			if	getattr(self, "unique", False):


# 				uniqs	= set()
# 				accum	= [ acc for acc in map(str,recap) if not (acc in uniqs or uniqs.add(acc)) ]
# 			else:
# 				accum	= list(map(str,recap))


# 			if	isinstance(m := getattr(self, getattr(self, "case_link", ""),None), LibraryShelf|dict):


# 				if	str(volume) not in m : m[str(volume)] = dict()
# 				if	(casing := shelf_case(

# 					accum,
# 					key=str(self),
# 					shelf=m[str(volume)],
# 					prep=is_iterable,
# 					post=seq_diff,
# 				)):
# 					return str(getattr(self, "joint", " ")).join(casing)
# 			return	str(getattr(self, "joint", " ")).join(accum)














# class NavDropsCounter(VolumeBookmark):

# 	trigger	 = "Grown leaf "
# 	rpattern	= r"\".*(?P<target>[Kk][A-Za-z]\d{2})\.[Tt][Ll][Xx]\"$"

# 	class Accumulator()








# for i in 1,2,3,4,5,6:
# for i in 2,3,4:
# for i in 2,3:
for i in 2,:

	tpoint	= TimeTurner([ i,3,2025 ])
	ypoint	= TimeTurner([ i,3,2025 ], days=-1)
	yypoint	= TimeTurner([ i,3,2025 ], days=-2)

	class Irma(LibraryAccess):
		# class loggy(LibraryContrib):

		# 	handler		= f"/mnt/container/ArrestedDevelopment/pygwarts/development/irma-library/{tpoint.dmy_asjoin}.loggy"
		# 	init_name	= f"irma-{tpoint.dmy_asjoin}"
		# 	init_level	= 10
		# 	force_error	= "*.filchmap*",

		class filchmap(MaraudersMap):	pass
		class library_shelf(LibraryShelf):

			grabbing	= f"/mnt/container/ArrestedDevelopment/pygwarts/development/Shelfs/{yypoint.dmY_asjoin}.Shelf"
			producing	= f"/mnt/container/ArrestedDevelopment/pygwarts/development/Shelfs/{ypoint.dmY_asjoin}.Shelf"

		case_link = "library_shelf"
		class Annex(LibraryAnnex):		pass

		# @ViewWrapper("\nWARNINGS: ")
		# @ViewCase("library_shelf", prep=is_num, post=num_diff)
		# class Warnings(WarningCount):												pass
		# @ViewWrapper("\nERRORS: ")
		# @ViewCase("library_shelf", prep=is_num, post=num_diff)
		# class Errors(ErrorCount):													pass
		# @ViewWrapper("\nCRITICALS: ")
		# @ViewCase("library_shelf", prep=is_num, post=num_diff)
		# class Criticals(CriticalCount):												pass

		# class CallstampActivity(VolumeBookmark):

		# 	trigger		= " finished in "
		# 	rpattern	= r"finished in (?P<target>[\.\d]+)( seconds)?$"

		# 	class Activities(AccessCounter):

		# 		@TextWrapper("\nactivities: ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class Inducer(RegisterCounterInducer): filter = plurnum

		# 	@AccessHandlerRegisterCounter
		# 	class Duration(TargetNumberAccumulator):

		# 		@TextWrapper("\ntotal time: ")
		# 		@InducerCase("library_shelf", prep=is_num, post=mostsec_diff)
		# 		class Total(RegisterRecapInducer): filter = posnum

		# 		@TextWrapper("\naverage time: ")
		# 		@InducerCase("library_shelf", prep=is_num, post=mostsec_diff)
		# 		class Average(AccessInducer):
		# 			def __call__(self, volume :LibraryVolume) -> str | None :

		# 				if	isinstance(recap := self.get_register_recap(volume), int | float):
		# 					if	isinstance(counter := self.get_register_counter(volume), int):
		# 						if	1 <counter : return str(recap /counter)

		# class ShelfTrackers(VolumeBookmark):

		# 	trigger	= "cleaned out from original shelf"

		# 	class Counter(AccessCounter):

		# 		@TextWrapper("\ntrackers removed: ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class Inducer(RegisterCounterInducer): filter = posnum


		# class ShelfProduces(VolumeBookmark):

		# 	trigger	= "successfully produced"

		# 	class Counter(AccessCounter):

		# 		@TextWrapper("\nshelve produced: ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class Inducer(RegisterCounterInducer): filter = posnum

		# class GrownCounter(VolumeBookmark):

		# 	trigger		= "Grown leaf"
		# 	rpattern	=  r".+ Grown leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		# 	@AccessHandlerRegisterCounter
		# 	class Accumulator(TargetStringAccumulator):

		# 		@TextWrapper("\nfiles copied ",": ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class CountInducer(RegisterCounterInducer): filter = posnum
		# 		class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):

		# 			case_link	= "library_shelf"
		# 			unique		= True
		# 			joint		= ", "


		# class MovedCounter(VolumeBookmark):

		# 	trigger		= "Moved leaf"
		# 	rpattern	=  r".+ Moved leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		# 	@AccessHandlerRegisterCounter
		# 	class Accumulator(TargetStringAccumulator):

		# 		@TextWrapper("\nfiles moved ",": ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class CountInducer(RegisterCounterInducer): filter = posnum
		# 		class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):

		# 			case_link	= "library_shelf"
		# 			unique		= True
		# 			joint		= ", "


		# class ClonedCounter(VolumeBookmark):

		# 	trigger		= "Cloned leaf"
		# 	rpattern	=  r".+ Cloned leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		# 	@AccessHandlerRegisterCounter
		# 	class Accumulator(TargetStringAccumulator):

		# 		@TextWrapper("\nfiles cloned ",": ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class CountInducer(RegisterCounterInducer): filter = posnum
		# 		class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):

		# 			case_link	= "library_shelf"
		# 			unique		= True
		# 			joint		= ", "


		# class PushedCounter(VolumeBookmark):

		# 	trigger		= "Pushed leaf"
		# 	rpattern	=  r".+ Pushed leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		# 	@AccessHandlerRegisterCounter
		# 	class Accumulator(TargetStringAccumulator):

		# 		@TextWrapper("\nfiles pushed ",": ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class CountInducer(RegisterCounterInducer): filter = posnum
		# 		class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):

		# 			case_link	= "library_shelf"
		# 			unique		= True
		# 			joint		= ", "


		# class ThrivedCounter(VolumeBookmark):

		# 	trigger		= "Thrived twig"
		# 	rpattern	=  r".+ Thrived twig \".+[/\\](?P<target>[^/\\]+)\"$"

		# 	@AccessHandlerRegisterCounter
		# 	class Accumulator(TargetStringAccumulator):

		# 		@TextWrapper("\nfolders copied ",": ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class CountInducer(RegisterCounterInducer): filter = posnum
		# 		class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):

		# 			case_link	= "library_shelf"
		# 			unique		= True
		# 			joint		= ", "


		# class TrimmedLeafsCounter(VolumeBookmark):

		# 	trigger		= "Trimmed leaf"
		# 	rpattern	=  r".+ Trimmed leaf \".+[/\\](?P<target>[^/\\]+)\"$"

		# 	@AccessHandlerRegisterCounter
		# 	class Accumulator(TargetStringAccumulator):

		# 		@TextWrapper("\nfiles removed ",": ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class CountInducer(RegisterCounterInducer): filter = posnum
		# 		class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):

		# 			case_link	= "library_shelf"
		# 			unique		= True
		# 			joint		= ", "


		# class TrimmedTwigsCounter(VolumeBookmark):

		# 	trigger		= "Trimmed twig"
		# 	rpattern	=  r".+ Trimmed twig \".+[/\\](?P<target>[^/\\]+)\"$"

		# 	@AccessHandlerRegisterCounter
		# 	class Accumulator(TargetStringAccumulator):

		# 		@TextWrapper("\nfolders removed ",": ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class CountInducer(RegisterCounterInducer): filter = posnum
		# 		class ReprInducer(DiffCaseRegisterRecapAccumulatorInducer):

		# 			case_link	= "library_shelf"
		# 			unique		= True
		# 			joint		= ", "


		# class WieghtCounter(VolumeBookmark):

		# 	trigger	= "INFO : Size:"
		# 	rpattern= r".+ Size: (?P<target>\d+)$"

		# 	class Handler(TargetHandler):
		# 		@TextWrapper("\ntotal space: ")
		# 		@InducerCase("library_shelf", prep=is_num, post=byte_size_diff)
		# 		class Inducer(RegisterRecapInducer):	pass

		# class TwigsCounter(VolumeBookmark):

		# 	trigger	= "INFO : Twigs:"
		# 	rpattern= r".+ Twigs: (?P<target>\d+)$"

		# 	class Handler(TargetHandler):
		# 		@TextWrapper("\nfolders: ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class Inducer(RegisterRecapInducer):	pass

		# class LeafsCounter(VolumeBookmark):

		# 	trigger	= "INFO : Leafs:"
		# 	rpattern= r".+ Leafs: (?P<target>\d+)$"

		# 	class Handler(TargetHandler):
		# 		@TextWrapper("\nfiles: ")
		# 		@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 		class Inducer(RegisterRecapInducer):	pass

		# class NavDrop(LibraryVolume):

		# 	inrange		= ypoint.dmY_aspath
		# 	location	= f"/mnt/container/ArrestedDevelopment/pygwarts/development/loggy/gnavdrop{ypoint.dmY_asjoin}.loggy"
		# 	@TextWrapper("\n\thagrid-navdrop\n","\n\n")
		# 	class Annex(VolumeAnnex):												pass
		# 	# class Sanitizes(Navtex.Sanits):													pass
		# 	# class Unhandled(Navtex.Unknowns):												pass

		# class SoftSync(LibraryVolume):

		# 	inrange		= ypoint.dmY_aspath
		# 	location	= f"/mnt/container/ArrestedDevelopment/pygwarts/development/loggy/gsoftsync{ypoint.dmY_asjoin}.loggy"
		# 	@TextWrapper("\n\thagrid-softsync\n","\n\n")
		# 	class Annex(VolumeAnnex):												pass

		# class HardSync(LibraryVolume):

		# 	inrange		= tpoint.dmY_aspath
		# 	location	= f"/mnt/container/ArrestedDevelopment/pygwarts/development/loggy/ghardsync{tpoint.dmY_asjoin}.loggy"
		# 	@TextWrapper("\n\thagrid-hardsync\n","\n\n")
		# 	class Annex(VolumeAnnex):												pass

		# class Arch(LibraryVolume):

		# 	inrange		= ypoint.dmY_aspath
		# 	location	= f"/mnt/container/ArrestedDevelopment/pygwarts/development/loggy/garch{ypoint.dmY_asjoin}.loggy"
		# 	@TextWrapper("\n\thagrid-arch\n","\n\n")
		# 	class Annex(VolumeAnnex):												pass

		# class Discovery(LibraryVolume):

		# 	inrange		= ypoint.dmY_aspath
		# 	location	= f"/mnt/container/ArrestedDevelopment/pygwarts/development/loggy/gdiscovery{ypoint.dmY_asjoin}.loggy"
		# 	@TextWrapper("\n\tfilch-discovery\n","\n\n")
		# 	class Annex(VolumeAnnex):												pass
		# 	class filchmap(MaraudersMap):	pass
		# 	class Watch(VolumeBookmark):

		# 		trigger		= "Received response for"
		# 		rpattern	= rf"(?P<ip>{VALID_IP4}) at (?P<mac>{VALID_MAC})"

		# 		class DiscoveredHosts(DiscoverywatchAccessHandler):

		# 			@TextWrapper("\nhosts mapped: ")
		# 			@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 			class MappedHosts(AccessInducer):
		# 				def __call__(self, volume :LibraryVolume) -> str | None :
		# 					if	(hosts := len(self.filchmap.ip4)) : return str(hosts)


		# 			@TextWrapper("\nhosts discovered: ")
		# 			@InducerCase("library_shelf", prep=is_num, post=num_diff)
		# 			class DiscoveredHostsInducer(RegisterCounterInducer):
		# 				def __call__(self, volume :LibraryVolume) -> str | None :

		# 					if	isinstance(recap := volume[self._UPPER_LAYER], dict):
		# 						return (

		# 							len(recap.get("missmatched_mac",[]))
		# 							+
		# 							len(recap.get("missmatched_ip",[]))
		# 							+
		# 							len(recap.get("unknown_mac",[]))
		# 							+
		# 							len(recap.get("unknown_ip",[]))
		# 							+
		# 							len(recap.get("known_hosts",[]))
		# 						)


		# 			@TextWrapper("\n\nmissmatched hosts: ")
		# 			class MissmatchedHostsInducer(AccessInducer):
		# 				def __call__(self, volume :LibraryVolume) -> str | None :

		# 					if	isinstance(recap := volume[self._UPPER_LAYER], dict):
		# 						misses = list()

		# 						if	(miss_mac := recap.get("missmatched_mac")):	misses.extend(miss_mac)
		# 						if	(miss_ip := recap.get("missmatched_ip")):	misses.extend(miss_ip)

		# 						if	(amount := len(misses)):
		# 							missed = [

		# 								"%s response from %s mac"%(

		# 									record.get("filch_mapped_host_name"),
		# 									record.get("filch_maced_host_name")

		# 								)	if record.get("filch_mapped_mac") is not None else

		# 								"%s mac response from unknown %s"%(

		# 									record.get("filch_maced_host_name"),
		# 									record.get("discovered_ip")

		# 								)	for record in misses
		# 							]
		# 							return	"%s\n\t%s"%(amount if 1 <amount else "", "\n\t".join(missed))


		# 			@TextWrapper("\n\nunknown hosts: ")
		# 			class UnknownHostsInducer(AccessInducer):
		# 				def __call__(self, volume :LibraryVolume) -> str | None :

		# 					if	isinstance(recap := volume[self._UPPER_LAYER], dict):
		# 						unknowns = list()

		# 						if	(no_mac := recap.get("unknown_mac")):	unknowns.extend(no_mac)
		# 						if	(no_ip := recap.get("unknown_ip")):		unknowns.extend(no_ip)

		# 						if	(amount := len(unknowns)):
		# 							unknowned = [

		# 								"%s response from unknown %s"%(

		# 									record.get("filch_mapped_host_name")
		# 									if record.get("filch_mapped_mac") is not None else
		# 									record.get("discovered_ip"),
		# 									record.get("discovered_mac")

		# 								)	for record in unknowns
		# 							]
		# 							return	"%s\n\t%s"%(amount if 1 <amount else "", "\n\t".join(unknowned))


		# 			@TextWrapper("\n\nmapped up: ")
		# 			class KnownHostsInducer(FilchWatchInducer):
		# 				def __call__(self, volume :LibraryVolume) -> str | None :

		# 					if	isinstance(recap := volume[self._UPPER_LAYER], dict):
		# 						if	(hosts := recap.get("known_hosts")) is not None:

		# 							if	(amount := len(hosts)):
		# 								up = [

		# 									"%s (%s)"%(

		# 										record.get("filch_mapped_host_name"),
		# 										record.get("filch_mapped_description")

		# 									)	for record in hosts
		# 								]
		# 								caseamount = self.filch_casing(

		# 									amount,
		# 									volume,
		# 									getattr(self, getattr(self, "case_link", ""), None),
		# 									"amount",
		# 									is_num,
		# 									num_diff
		# 								)
		# 								caseup = self.filch_casing(

		# 									up,
		# 									volume,
		# 									getattr(self, getattr(self, "case_link", ""), None),
		# 									"hosts",
		# 									is_iterable,
		# 									self.filch_seq_diff
		# 								)
		# 								return	"%s\n\t%s"%(

		# 									caseamount if 1 <amount else "",
		# 									"\n\t".join(caseup)
		# 								)


		# 			@TextWrapper("\n\nmapped down: ")
		# 			class DownHostsInducer(FilchWatchInducer):
		# 				def __call__(self, volume :LibraryVolume) -> str | None :

		# 					if	isinstance(recap := volume[self._UPPER_LAYER], dict):
		# 						if	(hosts := recap.get("known_hosts")) is not None:

		# 							up = { record.get("discovered_ip") for record in hosts }
		# 							down = [ ip4 for ip4 in self.filchmap["IP4"] if ip4 not in up ]

		# 							if	(amount := len(down)):
		# 								downs = [

		# 									"%s (%s)"%(

		# 										self.filchmap["IP4"][record].get("NAME"),
		# 										self.filchmap["IP4"][record].get("DESC")

		# 									)	for record in down
		# 								]
		# 								caseamount = self.filch_casing(

		# 									amount,
		# 									volume,
		# 									getattr(self, getattr(self, "case_link", ""), None),
		# 									"amount",
		# 									is_num,
		# 									num_diff
		# 								)
		# 								casedown = self.filch_casing(

		# 									downs,
		# 									volume,
		# 									getattr(self, getattr(self, "case_link", ""), None),
		# 									"hosts",
		# 									is_iterable,
		# 									self.filch_seq_diff
		# 								)
		# 								return	"%s\n\t%s"%(

		# 									caseamount if 1 <amount else "",
		# 									"\n\t".join(casedown)
		# 								)


		class Broad(LibraryVolume):

			inrange		= ypoint.dmY_aspath
			location	= f"/mnt/container/ArrestedDevelopment/pygwarts/development/loggy/gbroadwatch{ypoint.dmY_asjoin}.loggy"
			plotdir		= f"/mnt/container/ArrestedDevelopment/pygwarts/development/bwvisual/{ypoint.Ymd_aspath}"
			plotdate	= ypoint
			@TextWrapper("\n\tfilch-broadwatch\n","\n\n")
			class Annex(VolumeAnnex):												pass
			class Watch(VolumeBookmark):

				trigger		= "who has"
				rpattern	= rf"(?P<dst>{VALID_IP4}) says (?P<src>{VALID_IP4}) \((?P<mac>{VALID_MAC})\)$"

				# class TrappedRequests(BroadwatchAccessHandler):	pass
				@AccessHandlerRegisterCounter
				class TrappedRequests(BroadwatchAccessHandler):

		# # 			@printf_style("graphs plotted: %s\n")
		# # 			@numdiffcase("library_shelf")
		# # 			class Plotter(BroadPlotInducer):										pass

					@TextWrapper("\nrequests trapped: ")
					@InducerCase("library_shelf", prep=is_num, post=num_diff)
					class TotalTrappedInducer(RegisterCounterInducer):						pass

					# @TextWrapper("\nip4 lookups: ")
					# class LookupRequestsInducer(FilchWatchInducer):
					# 	def __call__(self, volume :LibraryVolume) -> str | None :

					# 		if	isinstance(recap := volume[self._UPPER_LAYER], dict):
					# 			if	isinstance(records := recap.get("ip_lookup"), list):

					# 				ip_lookups = list()
					# 				uniques = set()

					# 				for record in records:

					# 					current = (

					# 						"%s ip4 lookup at %s"%(

					# 							record.get("source_maced_name"),
					# 							record.get("timestamp").format("%H%M %d/%m/%Y")
					# 						)


					# 						if	(record.get("source_maced_ip") is not None)
					# 						and
					# 							(record.get("source_maced_name") is not None)
					# 						else


					# 						"%s lookup from %s at %s"%(

					# 							record.get("target_mapped_name"),
					# 							record.get("source_maced_name"),
					# 							record.get("timestamp").format("%H%M %d/%m/%Y")
					# 						)


					# 						if	(record.get("source_maced_name") is not None)
					# 						and
					# 							(record.get("target_mapped_name") is not None)
					# 						else


					# 						"unknown %s lookup from %s at %s"%(

					# 							record.get("request_target_ip"),
					# 							record.get("source_maced_name"),
					# 							record.get("timestamp").format("%H%M %d/%m/%Y")
					# 						)


					# 						if	(record.get("source_maced_name") is not None)
					# 						and
					# 							(record.get("request_target_ip") is not None)
					# 						else


					# 						"%s ip4 lookup from unknown %s at %s"%(

					# 							record.get("target_mapped_name"),
					# 							record.get("request_source_mac"),
					# 							record.get("timestamp").format("%H%M %d/%m/%Y")
					# 						)


					# 						if	(record.get("target_mapped_ip") is not None)
					# 						and
					# 							(record.get("target_mapped_name") is not None)
					# 						else


					# 						"unknown %s lookup from unknown %s at %s"%(

					# 							record.get("request_target_ip"),
					# 							record.get("request_source_mac"),
					# 							record.get("timestamp").format("%H%M %d/%m/%Y")
					# 						)
					# 					)

					# 					if	current not in uniques:

					# 						uniques.add(current)
					# 						ip_lookups.append(current)

					# 				if	(amount := len(ip_lookups)):
					# 					caseamount = self.filch_casing(

					# 						amount,
					# 						volume,
					# 						getattr(self, getattr(self, "case_link", ""), None),
					# 						"amount",
					# 						is_num,
					# 						num_diff
					# 					)
					# 					caselook = self.filch_casing(

					# 						ip_lookups,
					# 						volume,
					# 						getattr(self, getattr(self, "case_link", ""), None),
					# 						"records",
					# 						is_iterable,
					# 						self.filch_seq_diff
					# 					)
					# 					return	"%s\n\t%s"%(

					# 						caseamount if 1 <amount else "",
					# 						"\n\t".join(caselook)
					# 					)


					@TextWrapper("\nmissmatches: ")
					class MissmatchedRequestsInducer(FilchWatchInducer):
						def __call__(self, volume :LibraryVolume) -> str | None :

							if	isinstance(recap := volume[self._UPPER_LAYER], dict):
								misses = list()

								if	(miss_mac := recap.get("missmatched_mac")) is not None:
									misses.extend(miss_mac)
								if	(miss_ip := recap.get("missmatched_ip")) is not None:
									misses.extend(miss_ip)

								for record in misses:

									current = (

										"request with %s mac missmatching at %s"%(

											record.get("source_mapped_name"),
											record.get("timestamp").format("%H%M %d/%m/%Y")
										)

										if record.get("source_mapped_name") is not None else

										"request with %s ip4 missmatching at %s"%(

											record.get("source_maced_name"),
											record.get("timestamp").format("%H%M %d/%m/%Y")
										)

										if record.get("target_mapped_name") is not None else

										"unknown %s request with %s ip4 missmatching at %s"%(

											record.get("request_target_ip"),
											record.get("source_maced_name"),
											record.get("timestamp").format("%H%M %d/%m/%Y")
										)
									)



					# @TextWrapper("\nunknown requests: ")
					# class UnmappedRequestsInducer(FilchWatchInducer):
					# 	def __call__(self, volume :LibraryVolume) -> str | None :

					# 		if	isinstance(recap := volume[self._UPPER_LAYER], dict):
					# 			if	isinstance(records := recap.get("unmapped_requests"), list):
					# 				requests = defaultdict(lambda : defaultdict(int))

					# 				for record in records:
					# 					if	isinstance(record, dict):
					# 						requests[
					# 							record.get("source_mapped_name")
					# 							or
					# 							record.get("request_source_ip")
					# 						][	record.get("target_mapped_name")
					# 							or
					# 							record.get("request_target_ip")
					# 						]	+= 1

					# 				return	self.broad_gather(

					# 					requests,
					# 					volume,
					# 					getattr(self, getattr(self, "case_link", ""), None)
					# 				)


					# @TextWrapper("\nmapped requests: ")
					# class MappedRequestsInducer(FilchWatchInducer):
					# 	def __call__(self, volume :LibraryVolume) -> str | None :

					# 		if	isinstance(recap := volume[self._UPPER_LAYER], dict):
					# 			if	isinstance(records := recap.get("mapped_requests"), list):
					# 				requests = defaultdict(lambda : defaultdict(int))

					# 				for record in records:
					# 					if	isinstance(record, dict):
					# 						requests[
					# 							record.get("source_mapped_name")
					# 						][	record.get("target_mapped_name")
					# 						]	+= 1

					# 				return	self.broad_gather(

					# 					requests,
					# 					volume,
					# 					getattr(self, getattr(self, "case_link", ""), None)
					# 				)


		# class SNMP(LibraryVolume):

		# 	inrange		= ypoint.dmY_aspath
		# 	location	= f"/srv/lcontainer/filch/snmpwatch/{ypoint.Ym_aspath}/gsnmpwatch{ypoint.dmY_asjoin}.loggy"
		# 	@TextWrapper("\n\tfilch-snmpwatch\n")
		# 	class Annex(VolumeAnnex):												pass
		# 	class Watch(Bookmark):

		# 		trigger	= "trap from "
		# 		rpattern= rf" : \(trap from (?P<src>{VALID_IP4})\) (?P<msg>.+)$"
		# 		class ReceivedMessages(SNMPWatchAccessHandler):

		# 			@printf_style("received traps: %s\n")
		# 			class Inducer(SNMPInducer):

		# 				@filchcase("library_shelf")
		# 				class FilchGather(SNMPInducer.FilchGather):							pass

		# @Timestamp
		# class timing(LibraryAccess.Access):													pass


	irma = Irma()
	irma.filchmap.CSV(

		"/mnt/container/ArrestedDevelopment/pygwarts/development/loggy/broadmap.csv",
		";",
		IP4=0,
		MAC=1,
		NAME=2,
		DESC=3
	)
	# irma.Discovery.filchmap.CSV(

	# 	"/mnt/container/ArrestedDevelopment/pygwarts/development/loggy/discoverymap.csv",
	# 	";",
	# 	IP4=0,
	# 	MAC=1,
	# 	NAME=2,
	# 	DESC=3
	# )
	print(irma.Annex())
	print(f"\n\n-------------------------------------------------------------------")
	# print(irma.Broad.Inspection())
	# print(irma.Discovery.Inspection())
	# irma.library_shelf.produce(ignore_mod=True, strict_mode=False)







# glibrary = Glibrary()
# glibrary.timing()
# glibrary.save_Annex(f"/srv/lcontainer/irma/annex/{ypoint.Ym_aspath}/glibrary{ypoint.dmY_asjoin}.annex")
# glibrary.library_shelf.produce(from_outer=True, strict_mode=False)







