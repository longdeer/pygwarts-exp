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








class DebugLevelCounter(Bookmark):

	"""
		Bookmark template to count DEBUG level messages.
	"""

	trigger = " DEBUG :"
	class LevelCounter(HandlingCounter):

		@printf_style("DEBUGS: %s\n")
		@numdiffcase("library_shelf", enhanced=True)
		class Induce(PositiveRegisterCounterInducer):	pass








class InfoLevelCounter(Bookmark):

	"""
		Bookmark template to count INFO level messages.
	"""

	trigger = " INFO :"
	class LevelCounter(HandlingCounter):

		@printf_style("INFOS: %s\n")
		@numdiffcase("library_shelf", enhanced=True)
		class Induce(PositiveRegisterCounterInducer):	pass








class WarningLevelCounter(Bookmark):

	"""
		Bookmark template to count WARNING level messages.
	"""

	trigger = " WARNING :"
	class LevelCounter(HandlingCounter):

		@printf_style("WARNINGS: %s\n")
		@numdiffcase("library_shelf", enhanced=True)
		class Induce(PositiveRegisterCounterInducer):	pass








class ErrorLevelCounter(Bookmark):

	"""
		Bookmark template to count ERROR level messages.
	"""

	trigger = " ERROR :"
	class LevelCounter(HandlingCounter):

		@printf_style("ERRORS: %s\n")
		@numdiffcase("library_shelf", enhanced=True)
		class Induce(PositiveRegisterCounterInducer):	pass








class CriticalLevelCounter(Bookmark):

	"""
		Bookmark template to count CRITICAL level messages.
	"""

	trigger = " CRITICAL :"
	class LevelCounter(HandlingCounter):

		@printf_style("CRITICALS: %s\n")
		@numdiffcase("library_shelf", enhanced=True)
		class Induce(PositiveRegisterCounterInducer):	pass







