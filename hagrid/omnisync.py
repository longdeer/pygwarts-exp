from pygwarts.magical.time_turner			import TimeTurner
from pygwarts.magical.time_turner.timers	import Timestamp
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.irma.contrib.intercept		import ContribInterceptor
from pygwarts.irma.shelve					import LibraryShelf
from pygwarts.hagrid.sprouts				import fssprout
from pygwarts.hagrid.thrivables				import Tree
from pygwarts.hagrid.thrivables				import Copse
from pygwarts.hagrid.planting.peels			import GrowingPeel
from pygwarts.hagrid.planting.peeks			import BlindPeek
from pygwarts.hagrid.planting				import Flourish
from pygwarts.hagrid.planting.leafs			import LeafGrowth
from pygwarts.hagrid.planting.twigs			import TwigProbe
from pygwarts.hagrid.planting.weeds			import SprigTrimmer
from pygwarts.hagrid.bloom.twigs			import Germination
from pygwarts.hagrid.bloom.leafs			import Rejuvenation
from pygwarts.hagrid.bloom.weeds			import Efflorescence
from pygwarts.hagrid.cultivation.sifting	import SiftingController








p = TimeTurner()
class Omni(Copse):

	@ContribInterceptor
	class loggy(LibraryContrib):

		init_name	= "omnisync"
		handler		= f"/home/vla/ArrestedDevelopment/omnisync/{p.Ym_aspath}/{p.dm_asjoin}sync.loggy"
		force_info_stdout		= True
		force_warning_stdout	= True
		force_error_stdout		= True
		force_critical_stdout	= True




	class documents(Copse):
		class container(Tree):	bough	= "/mnt/container/vlaSync/Documents"
		class ghub(Tree):		bough	= "/mnt/ghub/vla/Documents"
		class hhub(Tree):		bough	= "/mnt/hhub/vla/Documents"
		class longdata(Tree):

			@GrowingPeel
			@BlindPeek("ExternalSeeds", renew=False)
			class grow(LeafGrowth):	pass
			bough	= "/media/vla/longdata/pcfrn3/Documents"

		class leafs(SiftingController):

			exclude	= r"/home/vla/Documents/Архив/_work/.+",
			include	= (

				r"/home/vla/Documents/.*",
				r"/mnt/container/vlaSync/Documents/.+",
				r"/mnt/ghub/vla/Documents/.+",
				r"/mnt/hhub/vla/Documents/.+",
				r"/media/vla/longdata/pcfrn3/Documents/.+",
			)
		class twigs(SiftingController):

			exclude	= r"/home/vla/Documents/Архив/_work(/.+)?",
			include	= (

				r"/home/vla/Documents/.+",
				r"/mnt/container/vlaSync/Documents/.+",
				r"/mnt/ghub/vla/Documents/.+",
				r"/mnt/hhub/vla/Documents/.+",
				r"/media/vla/longdata/pcfrn3/Documents/.+",
			)




	class stuff(Copse):
		class container(Tree):		bough	= "/mnt/container/vlaSync/rmp"
		class longdata(Tree):

			@GrowingPeel
			@BlindPeek("ExternalSeeds", renew=False)
			class grow(LeafGrowth):	pass
			bough	= "/media/vla/longdata/pcfrn3/rmp"

		class leafs(SiftingController):
			exclude	= (

				r"/home/vla/rmp/pcs/.+",
				r"/home/vla/rmp/OLHA/.+",
				r"/home/vla/rmp/xerox3315.+",
				r"/home/vla/rmp/TLG2/.+",
				r"/home/vla/rmp/CanonManual/.+",
			)
			include	= (

				r"/home/vla/rmp/.*",
				r"/mnt/container/vlaSync/rmp/.+",
				r"/media/vla/longdata/pcfrn3/rmp/.+",
			)
		class twigs(SiftingController):
			exclude	= (

				r"/home/vla/rmp/pcs(/.+)?",
				r"/home/vla/rmp/OLHA(/.+)?",
				r"/home/vla/rmp/xerox3315(/.+)?",
				r"/home/vla/rmp/TLG2(/.+)?",
				r"/home/vla/rmp/CanonManual(/.+)?",
			)
			include	= (

				r"/home/vla/rmp/.+",
				r"/mnt/container/vlaSync/rmp/.+",
				r"/media/vla/longdata/pcfrn3/rmp/.+",
			)




	class personal(Tree):

		bough	= "/media/vla/longdata/pcfrn3/lngd"
		class leafs(SiftingController):	include	= r"/home/vla/lngd/.*", r"/media/vla/longdata/pcfrn3/lngd/.+",
		class twigs(SiftingController):	include	= r"/home/vla/lngd/.*", r"/media/vla/longdata/pcfrn3/lngd/.+",




	class development(Copse):
		class container(Tree):		bough	= "/mnt/container/ArrestedDevelopment"
		class longdata(Tree):

			@GrowingPeel
			@BlindPeek("ExternalSeeds", renew=False)
			class grow(LeafGrowth):	pass
			bough	= "/media/vla/longdata/ArrestedDevelopment"

		class leafs(SiftingController):
			exclude	= (

				r"/home/vla/ArrestedDevelopment/omnisync/.+",
				r"/mnt/container/ArrestedDevelopment/pygwarts/development/.+",
				r"/media/vla/longdata/ArrestedDevelopment/pygwarts/development/.+",
			)
			include	= (

				r"/home/vla/ArrestedDevelopment/.*",
				r"/mnt/container/ArrestedDevelopment/.+",
				r"/media/vla/longdata/ArrestedDevelopment/.+",
			)
		class twigs(SiftingController):
			exclude	= (

				r"/home/vla/ArrestedDevelopment/omnisync(/.+)?",

				# All stuff about development just collecting, means no cleaning for boughs.
				r"/mnt/container/ArrestedDevelopment/pygwarts/development/.+",
				"/mnt/container/ArrestedDevelopment/pygwarts/global_testing",
				"/mnt/container/ArrestedDevelopment/pygwarts/olds",
				"/mnt/container/ArrestedDevelopment/pygwarts/readyops",
				"/mnt/container/ArrestedDevelopment/pygwarts/exp",

				r"/media/vla/longdata/ArrestedDevelopment/pygwarts/development/.+",
				"/media/vla/longdata/ArrestedDevelopment/pygwarts/olds",
				"/media/vla/longdata/ArrestedDevelopment/pygwarts/readyops",
				"/media/vla/longdata/ArrestedDevelopment/pygwarts/exp",
			)
			include	= (

				r"/home/vla/ArrestedDevelopment/.+",
				r"/mnt/container/ArrestedDevelopment/.+",
				r"/media/vla/longdata/ArrestedDevelopment/.+",
			)




	class LocalSeeds(LibraryShelf):

		grabbing	= "/home/vla/ArrestedDevelopment/omnisync/local.Shelf"
		reclaiming	= True

	class ExternalSeeds(LibraryShelf):

		grabbing	= "/home/vla/ArrestedDevelopment/omnisync/external.Shelf"
		reclaiming	= True


	@GrowingPeel
	class thrive(TwigProbe):		pass
	class germinate(Germination):	pass

	@GrowingPeel
	@BlindPeek("LocalSeeds", renew=False)
	class grow(LeafGrowth):			pass
	class rejuve(Rejuvenation):		pass

	class trim(SprigTrimmer):		pass
	class effloresce(Efflorescence):
		branches	= {

			"/mnt/container/vlaSync/rmp"				: ( "/home/vla/rmp", ),
			"/media/vla/longdata/pcfrn3/rmp"			: ( "/home/vla/rmp", ),
			"/media/vla/longdata/pcfrn3/lngd"			: ( "/home/vla/lngd", ),
			"/mnt/container/vlaSync/Documents"			: ( "/home/vla/Documents", ),
			"/mnt/ghub/vla/Documents"					: ( "/home/vla/Documents", ),
			"/mnt/hhub/vla/Documents"					: ( "/home/vla/Documents", ),
			"/media/vla/longdata/pcfrn3/Documents"		: ( "/home/vla/Documents", ),
			"/mnt/container/ArrestedDevelopment"		: ( "/home/vla/ArrestedDevelopment", ),
			"/media/vla/longdata/ArrestedDevelopment"	: ( "/home/vla/ArrestedDevelopment", ),
		}


	@Timestamp
	@fssprout("/home/vla/ArrestedDevelopment")
	@fssprout("/home/vla/lngd")
	@fssprout("/home/vla/rmp")
	@fssprout("/home/vla/Documents")
	class sync(Flourish):
		class twigs(SiftingController):
			exclude	= (

				"/home/vla/Documents/Соколов",
				"/home/vla/Documents/Проектирование",
				"/home/vla/Documents/Аренда А1",
				r".+/__pycache__",
			)








omni = Omni()
omni.sync()
omni.LocalSeeds.produce(from_outer=True)
omni.ExternalSeeds.produce(from_outer=True)







