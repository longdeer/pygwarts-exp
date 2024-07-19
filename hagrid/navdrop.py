from pygwarts.magical.time_turner.timers				import Timestamp
from pygwarts.irma.contrib								import LibraryContrib
from pygwarts.irma.contrib.intercept					import ContribInterceptor
from pygwarts.irma.shelve								import LibraryShelf
from pygwarts.hagrid.thrivables							import Tree
from pygwarts.hagrid.thrivables							import Copse
from pygwarts.hagrid.sprouts							import fssprout
from pygwarts.hagrid.planting							import Flourish
from pygwarts.hagrid.bloom.leafs						import Rejuvenation
from pygwarts.hagrid.bloom.weeds						import Efflorescence
from pygwarts.hagrid.planting.leafs						import LeafProbe
from pygwarts.hagrid.planting.leafs						import LeafGrowth
from pygwarts.hagrid.planting.peeks						import DraftPeek
from pygwarts.hagrid.planting.weeds						import TrimProbe
from pygwarts.hagrid.planting.weeds						import SprigTrimmer
from pygwarts.hagrid.cultivation.sifting				import SiftingController
from pygwarts.hagrid.cultivation.navtex_preprocessor	import Navpreprocessor
from pygwarts.hedwig.telegram.announce_decor			import Announcer
# telegram creditor to be obtained furhter and used as Announcer arguments
from credistr											import longrabitbot
from credistr											import rabitChannel








class Navdrop(Copse):

	@ContribInterceptor
	@Announcer(longrabitbot(), rabitChannel()).strneg
	class loggy(LibraryContrib):

		pool_timer		= .5
		init_name		= "navdrop"
		init_level		= 10
		handover_mode	= True
		handler			= "/home/vla/ArrestedDevelopment/pygwarts/development/hagrid/navdrop.loggy"
		force_info		= (

			"Navdrop.perfom.Navbow.inner_shelf",
			"Navdrop.perfom.Navfiles*",
			"Navdrop.perfom.Navshelf*",
			"Navdrop.Boughs.leafs*",
		)


	strict_thrive = False
	class Boughs(Copse):
		class jrcm(Tree):	bough = "/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/jrcnavm"
		class jrcr(Tree):	bough = "/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/jrcnavr"
		class leafs(SiftingController):
			include	= (

				r".+/[Kk][A-Za-z]\d\d\.[tT][lL][xX]",
				r"/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/jrcnavm/.+",
				r"/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/jrcnavr/.+",
			)
		class twigs(SiftingController):
			include	= (

				r"/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/jrcnavm/.+",
				r"/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/jrcnavr/.+",
			)


	@DraftPeek(renew=False)
	class grow(LeafGrowth):		pass
	class rejuve(Rejuvenation):	pass


	class trim(SprigTrimmer):	pass
	class clean(Efflorescence):
		branches	= {

			"/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/jrcnavm": (
				"/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/R/CKS/ARQ/NAVTEX",
			),
			"/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/jrcnavr": (
				"/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/R/CKS/ARQ/NAVTEX",
			),
		}


	@Timestamp
	@fssprout("/mnt/container/ArrestedDevelopment/pygwarts/global_testing/hagrid/R/CKS/ARQ/NAVTEX")
	@Navpreprocessor("K")
	class perfom(Flourish):

		class Navfiles(SiftingController):	include	= r".+/[Kk][A-Za-z]\d\d\.[tT][lL][xX]",
		class Navbow(LibraryShelf):

			grabbing	= "/home/vla/ArrestedDevelopment/pygwarts/development/hagrid/navbag.Shelf"
			reclaiming	= True

		class Navshelf(LibraryShelf):

			grabbing	= "/home/vla/ArrestedDevelopment/pygwarts/development/hagrid/navdrop.Shelf"
			reclaiming	= True








navdrop = Navdrop()
navdrop.perfom()
navdrop.perfom.Navbow.produce(from_outer=True)
navdrop.perfom.Navshelf.produce(

	from_outer=True,
	rewrite=True,
	ignore_mod=(len(navdrop.perfom.Navshelf) != len(navdrop.perfom.Navshelf()))
)







