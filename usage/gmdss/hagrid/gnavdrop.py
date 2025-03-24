from pygwarts.magical.time_turner				import TimeTurner
from pygwarts.magical.time_turner.timers		import Callstamp
from pygwarts.irma.contrib						import LibraryContrib
# from pygwarts.irma.contrib.intercept			import ContribInterceptor
from pygwarts.irma.shelve						import LibraryShelf
from pygwarts.hagrid.thrivables					import Tree
from pygwarts.hagrid.thrivables					import Copse
from pygwarts.hagrid.sprouts					import fssprout
from pygwarts.hagrid.planting					import Flourish
from pygwarts.hagrid.bloom.leafs				import Rejuvenation
from pygwarts.hagrid.bloom.weeds				import Efflorescence
from pygwarts.hagrid.planting.leafs				import LeafGrowth
from pygwarts.hagrid.planting.peeks				import DraftPeek
from pygwarts.hagrid.planting.weeds				import SprigTrimmer
from pygwarts.hagrid.cultivation.sifting		import SiftingController
# from pygwarts.hedwig.telegram.announce_decor	import Announcer
from navtex_preprocessor						import Navpreprocessor
from gopcredo									import GMDSSA2MRM
from gopcredo									import gmdssa2mrm_announcer_bot








point	= TimeTurner()
root	= "/srv/lcontainer/hagrid"








class Gnavdrop(Copse):

	# @ContribInterceptor
	# @Announcer(gmdssa2mrm_announcer_bot(), GMDSSA2MRM())
	class loggy(LibraryContrib):

		init_name	= "hagrid"
		handler		= f"{root}/navdrop/{point.Ym_aspath}/gnavdrop{point.dmY_asjoin}.loggy"
		pool_timer	= .5

	class Targets(Copse):

		class jrcm(Tree): bough = "/mnt/jrcnavm"
		class jrcr(Tree): bough = "/mnt/jrcnavr"
		class leafs(SiftingController):
			include = r".+/[Kk][A-Za-z]\d\d\.[tT][lL][xX]", r"/mnt/jrcnavm/.+", r"/mnt/jrcnavr/.+",

	@DraftPeek(renew=False)
	class grow(LeafGrowth):		pass
	class files(Rejuvenation):	pass
	class trim(SprigTrimmer):	pass
	class trash(Efflorescence):

		branches = {

			"/mnt/jrcnavm": ( "/srv/A2/R/CKS/ARQ/NAVTEX", ),
			"/mnt/jrcnavr": ( "/srv/A2/R/CKS/ARQ/NAVTEX", ),
		}

	@Callstamp
	@fssprout("/srv/A2/R/CKS/ARQ/NAVTEX")
	@Navpreprocessor("K")
	class perform(Flourish):

		class Navfiles(SiftingController):	include = r".+/[Kk][A-Za-z]\d\d\.[tT][lL][xX]",
		class Navbow(LibraryShelf):

			grabbing	= f"{root}/gnavbag.Shelf"
			reclaiming	= True

		class Navshelf(LibraryShelf):

			grabbing	= f"{root}/gnavdrop.Shelf"
			reclaiming	= True








navdrop = Gnavdrop()
navdrop.perform()
navdrop.perform.Navbow.produce(magical=True)
navdrop.perform.Navshelf.produce(

	rewrite=True,
	magical=True,
	ignore_mod=navdrop.perform.Navshelf.diff,
)







