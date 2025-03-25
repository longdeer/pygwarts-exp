from pygwarts.irma.access.bookmark			import Bookmark
from pygwarts.irma.access.handlers.counters	import HandlingCounter
from pygwarts.irma.access.handlers.parsers	import ValueHandler
from pygwarts.irma.access.handlers.parsers	import StringAccumulator
from pygwarts.irma.access.inducers			import printf_style
from pygwarts.irma.access.inducers.register	import RegisterRecapInducer
from pygwarts.irma.access.inducers.counters	import PositiveRegisterCounterInducer
from pygwarts.irma.access.inducers.text		import ByteSizeInducer
from pygwarts.irma.access.inducers.text		import StringAccumulatorInducer
from pygwarts.irma.shelve.casing			import numdiffcase








class Leafs:

	"""
		Leafs bookmarks container.
	"""

	class GrowCount(Bookmark):

		"""
			Bookmark template to count copied files.
		"""

		trigger = " Grown leaf "
		class Counter(HandlingCounter):

			@printf_style("leafs grown: %s\n")
			@numdiffcase(link="library_shelf")
			class Inducer(PositiveRegisterCounterInducer):	pass


	class CloneCount(Bookmark):

		"""
			Bookmark template to count cloned files.
		"""

		trigger = " Cloned leaf "
		class Counter(HandlingCounter):

			@printf_style("leafs cloned: %s\n")
			@numdiffcase(link="library_shelf")
			class Inducer(PositiveRegisterCounterInducer):	pass


	class MoveCount(Bookmark):

		"""
			Bookmark template to count moved files.
		"""

		trigger = " Moved leaf "
		class Counter(HandlingCounter):

			@printf_style("leafs moved: %s\n")
			@numdiffcase(link="library_shelf")
			class Inducer(PositiveRegisterCounterInducer):	pass


	class TrimCount(Bookmark):
		"""
			Bookmark template to count removed files.
		"""

		trigger = " Trimmed leaf "
		class Counter(HandlingCounter):

			@printf_style("leafs trimmed: %s\n")
			@numdiffcase(link="library_shelf")
			class Inducer(PositiveRegisterCounterInducer):	pass








class Branches:

	"""
		Branches bookmarks container.
	"""

	class GrowCount(Bookmark):

		"""
			Bookmark template to count copied files with parents folders creations.
		"""

		trigger = "Grown branch "
		class Counter(HandlingCounter):

			@printf_style("branches created: %s\n")
			@numdiffcase(link="library_shelf")
			class Inducer(PositiveRegisterCounterInducer):	pass


	class CloneCount(Bookmark):

		"""
			Bookmark template to count cloned files with parents folders creations.
		"""

		trigger = "Cloned branch "
		class Counter(HandlingCounter):

			@printf_style("branches cloned: %s\n")
			@numdiffcase(link="library_shelf")
			class Inducer(PositiveRegisterCounterInducer):	pass


	class MoveCount(Bookmark):

		"""
			Bookmark template to count moved files with parents folders creations.
		"""

		trigger = "Moved branch "
		class Counter(HandlingCounter):

			@printf_style("branches moved: %s\n")
			@numdiffcase(link="library_shelf")
			class Inducer(PositiveRegisterCounterInducer):	pass







class Twigs:

	"""
		Twigs bookmarks container.
	"""

	class ThriveCount(Bookmark):

		"""
			Bookmark template to count created directories.
		"""

		trigger = "Thrived twig "
		class Counter(HandlingCounter):

			@printf_style("directories created: %s\n")
			@numdiffcase(link="library_shelf")
			class Inducer(PositiveRegisterCounterInducer):	pass


	class TrimCount(Bookmark):

		"""
			Bookmark template to count removed folders.
		"""

		trigger = "Trimmed twig "
		class Counter(HandlingCounter):

			@printf_style("folders removed: %s\n")
			@numdiffcase(link="library_shelf")
			class Inducer(PositiveRegisterCounterInducer):	pass








class Masses:

	"""
		Container for collecting size, folders and files counts.
	"""

	class WeightCount(Bookmark):

		"""
			Bookmark template to count size of source folder.
		"""

		trigger		= "Size: "
		rpattern	= r"(?P<target>\d+)$"
		class Trigger(ValueHandler):

			@printf_style("sprout size: %s\n")
			@numdiffcase("library_shelf", preprocessor=ByteSizeInducer.byte_size)
			class Inducer(RegisterRecapInducer):					pass


	class TwigsCount(Bookmark):

		"""
			Bookmark template to count number of folders in source.
		"""

		trigger		= "Twigs: "
		rpattern	= r"(?P<target>\d+)$"
		class Trigger(ValueHandler):

			@printf_style("twigs: %s\n")
			@numdiffcase("library_shelf")
			class Inducer(RegisterRecapInducer):			pass


	class LeafsCount(Bookmark):

		"""
			Bookmark template to count number of files in source.
		"""

		trigger		= "Leafs: "
		rpattern	= r"(?P<target>\d+)$"
		class Trigger(ValueHandler):

			@printf_style("leafs: %s\n")
			@numdiffcase("library_shelf")
			class Inducer(RegisterRecapInducer):			pass








class Navtex:

	"""
		Navtex bookmarks container.
	"""

	class Drops(Bookmark):

		trigger		= "Grown leaf "
		rpattern	= r"\".*(?P<target>[Kk][A-Za-z]\d{2})\.[Tt][Ll][Xx]\"$"
		class Trigger(StringAccumulator):

			@printf_style("new messages: %s\n")
			class Inducer(StringAccumulatorInducer):

				joint	= ", "
				unique	= True


	class Trims(Bookmark):

		trigger		= "Trimmed leaf "
		rpattern	= r"\".*(?P<target>[Kk][A-Za-z]\d{2})\.[Tt][Ll][Xx]\"$"
		class Trigger(StringAccumulator):

			@printf_style("removed messages: %s\n")
			class Inducer(StringAccumulatorInducer):

				joint	= ", "
				unique	= True


	class Sanits(Bookmark):

		trigger		= " was rewritten"
		rpattern	= r"\".*(?P<target>[Kk][A-Za-z]\d{2})\.[Tt][Ll][Xx]\" was rewritten$"
		class Trigger(StringAccumulator):

			@printf_style("sanitized messages: %s\n")
			class Inducer(StringAccumulatorInducer):

				joint	= ", "
				unique	= True


	class Unknowns(Bookmark):

		trigger		= " Not handled "
		rpattern	= r"\"(?P<target>\S+\" in [Kk][A-Za-z]\d{2} line \d+)"
		class Trigger(StringAccumulator):

			@printf_style("unknown words: %s\n")
			class Inducer(StringAccumulatorInducer):

				joint	= ", "
				unique	= True







