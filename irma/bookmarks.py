from pygwarts.magical.time_turner.timers	import Sectimer
from pygwarts.irma.access.volume			import VolumeAccess
from pygwarts.irma.access.bookmark			import Bookmark
from pygwarts.irma.access.handlers.counters	import HandlingCounter
from pygwarts.irma.access.handlers.parsers	import NumberAccumulator
from pygwarts.irma.access.inducers			import printf_style
from pygwarts.irma.access.inducers.register	import RegisterRecapInducer
from pygwarts.irma.access.inducers.register	import RegisterRecapAndCounterInducer
from pygwarts.irma.access.inducers.counters	import PositiveRegisterCounterInducer
from pygwarts.irma.access.inducers.counters	import MultipleRegisterCounterInducer
from pygwarts.irma.shelve.casing			import numdiffcase








class ShelfCleans(Bookmark):

	"""
		Bookmark template to count LibraryShelf keys cleanings.
	"""

	trigger = " cleaned out from original shelf"
	class Counter(HandlingCounter):

		@printf_style("trackers removed: %s\n")
		@numdiffcase(link="library_shelf", enhanced=True)
		class Inducer(PositiveRegisterCounterInducer):	pass


class ShelfProduces(Bookmark):

	"""
		Bookmark template to count LibraryShelf producings.
	"""

	trigger = " successfully produced"
	class Counter(HandlingCounter):

		@printf_style("produced Shelfs: %s\n")
		@numdiffcase(link="library_shelf", enhanced=True)
		class Inducer(PositiveRegisterCounterInducer):	pass








class OptimizedTimestampActivity(Bookmark):

	"""
		Bookmark template to count all Timestamp finish lines and induces it's count, average and total time.
	"""

	trigger = " finished in "
	rpattern = r"finished in (?P<target>\d+\.\d+)( seconds)?$"
	class Activity(HandlingCounter):

		@printf_style("activities: %s\n")
		@numdiffcase("library_shelf", enhanced=True)
		class Inducer(MultipleRegisterCounterInducer):			pass


	class Duration(NumberAccumulator):

		@printf_style("average time: %s\n")
		@numdiffcase("library_shelf", Sectimer.sectimer, enhanced=True)
		class AverageInducer(RegisterRecapAndCounterInducer):

			def __call__(self, volume :VolumeAccess) -> str or None :

				if	(recap_and_counter := super().__call__(volume)) is not None:

					try:

						recap	= float(recap_and_counter[0])
						counter	= float(recap_and_counter[1])


						if	counter > 1:

							average = float(recap) /float(counter)
							self.loggy.debug(f"Inducing average {average}")


							return str(average)


						self.loggy.debug(f"Zero register counter linked with {volume} register")


					except	Exception as E:
						self.loggy.warning(f"Inducer {self} failed with {CAST(E)}")


		@printf_style("total time: %s\n")
		@numdiffcase("library_shelf", Sectimer.sectimer, enhanced=True, asnew=True)
		class TotalInducer(RegisterRecapInducer):	pass







