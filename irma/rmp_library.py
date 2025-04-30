from pygwarts.magical.time_turner				import TimeTurner
from pygwarts.magical.time_turner.timers 		import Callstamp
from pygwarts.irma.contrib						import LibraryContrib
from pygwarts.irma.shelve						import LibraryShelf
from pygwarts.irma.shelve.casing				import is_num
from pygwarts.irma.shelve.casing				import num_diff
from pygwarts.irma.shelve.casing				import mostsec_diff
from pygwarts.irma.shelve.casing				import byte_size_diff
from pygwarts.irma.access						import LibraryAccess
from pygwarts.irma.access.volume				import LibraryVolume
from pygwarts.irma.access.bookmarks				import VolumeBookmark
from pygwarts.irma.access.bookmarks.counters	import WarningCount
from pygwarts.irma.access.bookmarks.counters	import ErrorCount
from pygwarts.irma.access.bookmarks.counters	import CriticalCount
from pygwarts.irma.access.bookmarks.viewers		import ViewWrapper
from pygwarts.irma.access.bookmarks.viewers		import ViewCase
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
from pygwarts.irma.access.inducers.case			import InducerCase
from pygwarts.irma.access.annex					import VolumeAnnex
from pygwarts.irma.access.annex					import LibraryAnnex
from pygwarts.irma.access.utils					import TextWrapper
from pygwarts.filch.marauders_map				import MaraudersMap
from irma_local									import TelegramTechHoist
from bookmarks									import DiscoveryWatch
from bookmarks									import BroadWatch
from inducers									import DiffCaseRegisterRecapAccumulatorInducer








tpoint	= TimeTurner()
ypoint	= TimeTurner(days=-1)
yypoint	= TimeTurner(days=-2)
iroot	= "/srv/lcontainer/irma"
froot	= "/srv/lcontainer/filch"








class Library(LibraryAccess):

	@TelegramTechHoist
	class loggy(LibraryContrib):

		handler		= f"{iroot}/library/{tpoint.Ym_aspath}/library{tpoint.dmY_asjoin}.loggy"
		init_name	= "irma"

	class filchmap(MaraudersMap):	pass
	class library_shelf(LibraryShelf):

		grabbing	= f"{iroot}/xshelf/{yypoint.Ym_aspath}/library{yypoint.dmY_asjoin}.xshelf"
		producing	= f"{iroot}/xshelf/{ypoint.Ym_aspath}/library{ypoint.dmY_asjoin}.xshelf"

	case_link	= "library_shelf"
	unique		= True
	joint		= ", "

	@Callstamp
	class Annex(LibraryAnnex): 		pass


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

		trigger	= "cleaned out from original shelf"

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


	class SoftSync(LibraryVolume):

		inrange		= ypoint.dmY_aspath
		location	= f"{iroot}/softsync/{ypoint.Ym_aspath}/softsync{ypoint.dmY_asjoin}.loggy"
		@TextWrapper("\n\thagrid-softsync\n","\n")
		class Annex(VolumeAnnex):		pass

	class HardSync(LibraryVolume):

		inrange		= tpoint.dmY_aspath
		location	= f"{iroot}/hardsync/{tpoint.Ym_aspath}/hardsync{tpoint.dmY_asjoin}.loggy"
		@TextWrapper("\n\thagrid-hardsync\n","\n")
		class Annex(VolumeAnnex):		pass

	class Arch(LibraryVolume):

		inrange		= ypoint.dmY_aspath
		location	= f"/srv/lcontainer/hagrid/arch/{ypoint.Ym_aspath}/arch{ypoint.dmY_asjoin}.loggy"
		@TextWrapper("\n\thagrid-arch\n","\n")
		class Annex(VolumeAnnex):		pass

	class Discovery(LibraryVolume):

		inrange		= ypoint.dmY_aspath
		location	= f"{froot}/discovery/{ypoint.Ym_aspath}/discovery{ypoint.dmY_asjoin}.loggy"
		@TextWrapper("\n\tfilch-discovery\n","\n")
		class Annex(VolumeAnnex):		pass
		class filchmap(MaraudersMap):	pass
		class Watch(DiscoveryWatch):	pass

	class Broad(LibraryVolume):

		plotdate	= ypoint
		inrange		= ypoint.dmY_aspath
		plotdir		= f"/srv/dump/bwvisual/{ypoint.Ymd_aspath}"
		location	= f"{froot}/broadwatch/{ypoint.Ym_aspath}/broadwatch{ypoint.dmY_asjoin}.loggy"
		@TextWrapper("\n\tfilch-broadwatch\n","\n")
		class Annex(VolumeAnnex):		pass
		class Watch(BroadWatch):		pass








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
		with open(f"{iroot}/annex/{ypoint.Ym_aspath}/library{ypoint.dmY_asjoin}.annex", "w") as dump:
			dump.write(annex)







