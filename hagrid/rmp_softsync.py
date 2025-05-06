from pygwarts.magical.time_turner			import TimeTurner
from pygwarts.magical.time_turner.timers	import Callstamp
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.irma.shelve					import LibraryShelf
from pygwarts.hagrid.thrivables				import Tree
from pygwarts.hagrid.sprouts				import fssprout
from pygwarts.hagrid.planting				import Flourish
from pygwarts.hagrid.bloom.leafs			import Rejuvenation
from pygwarts.hagrid.planting.leafs			import LeafGrowth
from pygwarts.hagrid.planting.peels			import GrowingPeel
from pygwarts.hagrid.planting.peeks			import BlindPeek
from pygwarts.hagrid.cultivation.sifting	import SiftingController
from irma_local_intercept					import TelegramTechHoist








point	= TimeTurner()
root	= "/srv/lcontainer/hagrid"








class Softsync(Tree):

	@TelegramTechHoist
	class loggy(LibraryContrib):

		handler		= f"{root}/softsync/{point.Ym_aspath}/softsync{point.dmY_asjoin}.loggy"
		init_name	= "hagrid"

	class seeds(LibraryShelf):

		grabbing	= f"{root}/softsync.Shelf"
		reclaiming	= True

	@GrowingPeel
	@BlindPeek("seeds", renew=False)
	class grow(LeafGrowth):		pass
	class files(Rejuvenation):	pass

	@Callstamp
	@fssprout("/srv/A2/R")
	class perform(Flourish):
		class twigs(SiftingController):	exclude = "/srv/A2/R/CKS/ARC", "/srv/A2/R/SHARE"








if	__name__ == "__main__":

	softsync = Softsync(bough="/mnt/H")
	softsync.perform()
	softsync.seeds.produce(rewrite=True, magical=True)







