from pygwarts.magical.time_turner				import TimeTurner
from pygwarts.magical.time_turner.timers		import Callstamp
from pygwarts.irma.contrib						import LibraryContrib
# from pygwarts.irma.contrib.intercept			import ContribInterceptor
from pygwarts.irma.shelve						import LibraryShelf
from pygwarts.hagrid.thrivables					import Tree
from pygwarts.hagrid.sprouts					import fssprout
from pygwarts.hagrid.planting					import Flourish
from pygwarts.hagrid.bloom.leafs				import Rejuvenation
from pygwarts.hagrid.planting.leafs				import LeafGrowth
from pygwarts.hagrid.planting.peels				import GrowingPeel
from pygwarts.hagrid.planting.peeks				import BlindPeek
from pygwarts.hagrid.cultivation.sifting		import SiftingController
# from pygwarts.hedwig.telegram.announce_decor	import Announcer
from gopcredo									import mrma2tech
from gopcredo									import gmdssA2mrmENGbot








# Date point for logging
point	= TimeTurner()
root	= "/srv/lcontainer/hagrid"








class Softsync(Tree):

	# @ContribInterceptor
	# @Announcer(gmdssA2mrmENGbot(), mrma2tech())
	class loggy(LibraryContrib):

		init_name	= "hagrid"
		handler		= f"{root}/softsync/{point.Ym_aspath}/gsoftsync{point.dmY_asjoin}.loggy"

	class seeds(LibraryShelf):

		grabbing	= f"{root}/gsoftsync.Shelf"
		reclaiming	= True

	@GrowingPeel
	@BlindPeek("seeds", renew=False)
	class grow(LeafGrowth):		pass
	class files(Rejuvenation):	pass

	@Callstamp
	@fssprout("/srv/A2/R")
	class perform(Flourish):
		class twigs(SiftingController):	exclude = "/srv/A2/R/CKS/ARC", "/srv/A2/R/SHARE"








softsync = Softsync(bough="/mnt/H")
softsync.perform()
softsync.seeds.produce(rewrite=True, magical=True)







