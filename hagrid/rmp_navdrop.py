from pygwarts.magical.time_turner			import TimeTurner
from pygwarts.magical.time_turner.timers	import Callstamp
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.irma.shelve					import LibraryShelf
from pygwarts.hagrid.thrivables				import Tree
from pygwarts.hagrid.thrivables				import Copse
from pygwarts.hagrid.sprouts				import fssprout
from pygwarts.hagrid.planting				import Flourish
from pygwarts.hagrid.bloom.leafs			import Rejuvenation
from pygwarts.hagrid.bloom.weeds			import Efflorescence
from pygwarts.hagrid.planting.leafs			import LeafGrowth
from pygwarts.hagrid.planting.peeks			import DraftPeek
from pygwarts.hagrid.planting.weeds			import SprigTrimmer
from pygwarts.hagrid.cultivation.sifting	import SiftingController
from navtex_preprocessor					import NavtexPreprocessor
from irma_local								import TelegramOperatorHoist








point	= TimeTurner()
root	= "/srv/lcontainer/hagrid"








class Navdrop(Copse):

	@TelegramOperatorHoist
	class loggy(LibraryContrib):

		handler		= f"{root}/navdrop/{point.Ym_aspath}/navdrop{point.dmY_asjoin}.loggy"
		init_name	= "hagrid"
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
	@NavtexPreprocessor
	class perform(Flourish):

		class Navfiles(SiftingController):	include = r".+/[Kk][A-Za-z]\d\d\.[tT][lL][xX]",
		class Navbow(LibraryShelf):

			grabbing	= f"{root}/Navbag.Shelf"
			reclaiming	= True

		class Navshelf(LibraryShelf):

			grabbing	= f"{root}/Navdrop.Shelf"
			reclaiming	= True








if	__name__ == "__main__":

	navdrop = Navdrop()
	navdrop.perform()
	navdrop.perform.Navbow.produce(magical=True)
	diff = navdrop.perform.Navshelf.real_diff
	for tracker in diff : navdrop.perform.Navshelf.loggy.info(f"Discarded tracker for \"{tracker}\"")
	navdrop.perform.Navshelf.produce(

		rewrite=True,
		magical=True,
		ignore_mod=len(diff),
	)







