from pygwarts.magical.time_turner				import TimeTurner
from pygwarts.magical.time_turner.timers		import Callstamp
from pygwarts.irma.contrib						import LibraryContrib
# from pygwarts.irma.contrib.intercept			import ContribInterceptor
from pygwarts.irma.shelve						import LibraryShelf
from pygwarts.irma.access.utils					import byte_size_string
from pygwarts.hagrid.thrivables					import Tree
from pygwarts.hagrid.sprouts					import fssprout
from pygwarts.hagrid.planting					import Flourish
from pygwarts.hagrid.bloom.leafs				import Rejuvenation
from pygwarts.hagrid.bloom.twigs				import Germination
from pygwarts.hagrid.bloom.weeds				import Efflorescence
from pygwarts.hagrid.planting.leafs				import LeafGrowth
from pygwarts.hagrid.planting.twigs				import TwigThrive
from pygwarts.hagrid.planting.peels				import GrowingPeel
from pygwarts.hagrid.planting.peeks				import DraftPeek
from pygwarts.hagrid.planting.weeds				import SprigTrimmer
from pygwarts.hagrid.cultivation.sifting		import SiftingController
from pygwarts.hagrid.cultivation.registering	import PlantRegister
from pygwarts.hagrid.cultivation.registering	import PlantRegisterQuerier as PRQ
# from pygwarts.hedwig.telegram.announce_decor	import Announcer
from gopcredo									import mrma2tech
from gopcredo									import gmdssA2mrmENGbot








# Date point for logging
point	= TimeTurner()
root	= "/srv/lcontainer/hagrid"








class Ghardsync(Tree):

	# @ContribInterceptor
	# @Announcer(gmdssA2mrmENGbot(), mrma2tech())
	class loggy(LibraryContrib):

		init_name	= "hagrid"
		handler		= f"{root}/hardsync/{point.Ym_aspath}/ghardsync{point.dmY_asjoin}.loggy"

	class leafs(SiftingController): include = r".+",
	class twigs(SiftingController):

		include		= r".+",
		exclude		= "/mnt/H/CKS/ARC", "/mnt/H/SHARE",

	@GrowingPeel
	class thrive(TwigThrive):	pass
	class folders(Germination):	pass

	@GrowingPeel
	@DraftPeek(renew=False)
	class grow(LeafGrowth):		pass
	class files(Rejuvenation):	pass
	class stats(LibraryShelf):	pass
	class trim(SprigTrimmer):	pass
	class trash(Efflorescence):	branches = { "/mnt/H" : ( "/srv/A2/R", )}

	@Callstamp
	@fssprout("/srv/A2/R")
	@PlantRegister("stats")
	class perform(Flourish):
		class twigs(SiftingController): exclude = "/srv/A2/R/CKS/ARC", "/srv/A2/R/SHARE",








hardsync = Ghardsync(bough="/mnt/H")
hardsync.perform()
hardsync.stats.produce(

	f"{root}/replicas/{point.Ym_aspath}/greplica{point.dmY_asjoin}.Shelf",
	strict_mode=False,
)

prq = PRQ(hardsync.stats)

gsize		= byte_size_string(prq.WG(apparent=True))
gfiles		= prq.TG()
gfolders	= prq.LG()

hardsync.loggy.info(f"Sprout \"/srv/A2/R\" stats:")
hardsync.loggy.info(f"Size: {gsize}")
hardsync.loggy.info(f"Twigs: {gfolders}")
hardsync.loggy.info(f"Leafs: {gfiles}")







