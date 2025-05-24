from pygwarts.magical.time_turner				import TimeTurner
from pygwarts.magical.time_turner.timers		import Callstamp
from pygwarts.irma.contrib						import LibraryContrib
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
from irma_local_intercept						import TelegramTechHoist








point	= TimeTurner()
root	= "/srv/lcontainer/hagrid"








class Hardsync(Tree):

	@TelegramTechHoist
	class loggy(LibraryContrib):

		handler		= f"{root}/hardsync/{point.Ym_aspath}/hardsync{point.dmY_asjoin}.loggy"
		init_name	= "hagrid"

	class leafs(SiftingController): include = r".+",
	class twigs(SiftingController):

		include		= r".+",
		exclude		= "/mnt/R/CKS/ARC", "/mnt/R/SHARE",

	@GrowingPeel
	class thrive(TwigThrive):	pass
	class folders(Germination):	pass

	@GrowingPeel
	@DraftPeek(renew=False)
	class grow(LeafGrowth):		pass
	class files(Rejuvenation):	pass
	class stats(LibraryShelf):	pass
	class trim(SprigTrimmer):	pass
	class trash(Efflorescence):	branches = { "/mnt/R" : ( "/srv/A2/R", )}

	@Callstamp
	@fssprout("/srv/A2/R")
	@PlantRegister("stats")
	class perform(Flourish):
		class twigs(SiftingController): exclude = "/srv/A2/R/CKS/ARC", "/srv/A2/R/SHARE",








if	__name__ == "__main__":

	hardsync = Hardsync(bough="/mnt/R")
	hardsync.perform()
	hardsync.stats.produce(

		f"{root}/replicas/{point.Ym_aspath}/replica{point.dmY_asjoin}.Shelf",
		strict_mode=False,
	)

	prq = PRQ(hardsync.stats)

	hardsync.loggy.info(f"\"/srv/A2/R\" stats:")
	hardsync.loggy.info(f"Size: {byte_size_string(prq.WG(apparent=True))}")
	hardsync.loggy.info(f"Twigs: {prq.TG()}")
	hardsync.loggy.info(f"Leafs: {prq.LG()}")







