from pygwarts.magical.time_turner			import TimeTurner
from pygwarts.magical.time_turner.timers	import Callstamp
from pygwarts.irma.contrib					import LibraryContrib
from pygwarts.hagrid.thrivables				import Tree
from pygwarts.hagrid.thrivables				import Copse
from pygwarts.hagrid.sprouts				import fssprout
from pygwarts.hagrid.planting				import Flourish
from pygwarts.hagrid.bloom.leafs			import Rejuvenation
from pygwarts.hagrid.bloom.leafs			import Transfer
from pygwarts.hagrid.planting.leafs			import LeafGrowth
from pygwarts.hagrid.planting.leafs			import LeafMove
from pygwarts.hagrid.planting.peels			import ThrivingPeel
from pygwarts.hagrid.cultivation.sifting	import SiftingController








point	= TimeTurner()
root	= "/srv/lcontainer/hagrid"








class Garch(Copse):

	class loggy(LibraryContrib):

		handler		= f"{root}/arch/{point.Ym_aspath}/harch{point.dmY_asjoin}.loggy"
		init_name	= "hagrid"

	class cparchive(Copse):
		class navtex(Tree):

			bough	= "/srv/A2/R/CKS/ARC"
			class leafs(SiftingController): include	= r"/srv/A2/R/CKS/ARQ/NAVTEX/[^/]*\.[Tt][Ll][Xx]",

		class ships(Tree):

			bough	= "/srv/A2/R/CKS/ARC"
			class leafs(SiftingController): include	= "/srv/A2/R/CKS/MAIL/SHIPS/MAIL.FLN",

		@ThrivingPeel(point.Ymd_aspath)
		class grow(LeafGrowth):		pass
		class files(Rejuvenation):	pass

	class mvarchive(Tree):

		bough = "/srv/A2/R/CKS/ARC"
		class leafs(SiftingController):

			include	= (

				r"/srv/A2/R/CKS/ARQ/OUT/[^/]*/[^/]*\.[Tt][^/]*",
				r"/srv/A2/R/CKS/ARQ/IN/[^/]*/[^/]*\.[Tt][^/]*",
				r"/srv/A2/R/CKS/ARQ/NAVTEX/[^/]*\.[Tt][^Ll][^/]*",
				r"/srv/A2/R/CKS/OUTSEA/[^/]*/[^/]*\.[Tt][^/]+",
				r"/srv/A2/R/CKS/MAIL/MSG/POVESTKI/[^/]*\.[Tt][^/]*",
				r"/srv/A2/R/CKS/MAIL/MSG/PRIP/[^/]*\.[Tt][^/]*",
				r"/srv/A2/R/CKS/MAIL/SHIPS/[^/]*/[^/]*\.[Tt][^/]*",
				r"/srv/A2/R/CKS/TOSEA/[^/]*/[^/]*\.[Tt][^/]*",
				r"/srv/A2/R/CKS/INMSAT_C/IN/[^/]*\.[Tt][^/]*",
				r"/srv/A2/R/CKS/INMSAT_C/OUT/[^/]*\.[Tt][^/]*",
			)

		@ThrivingPeel(point.Ymd_aspath)
		class graft(LeafMove):		pass
		class files(Transfer):		pass

	@Callstamp
	@fssprout("/srv/A2/R/CKS")
	class perform(Flourish):
		class twigs(SiftingController):

			exclude	= (

				"/srv/A2/R/CKS/ARC",
				"/srv/A2/R/CKS/ARQ/COMMON_1",
				"/srv/A2/R/CKS/ARQ/COMMON_2",
				"/srv/A2/R/CKS/ARQ/COMMON_3",
				"/srv/A2/R/CKS/ARQ/COMMON_4",
				"/srv/A2/R/CKS/ARQ/COMMON_5",
				"/srv/A2/R/CKS/ARQ/REPORT_1",
				"/srv/A2/R/CKS/ARQ/REPORT_2",
				"/srv/A2/R/CKS/ARQ/REPORT_3",
				"/srv/A2/R/CKS/ARQ/REPORT_4",
				"/srv/A2/R/CKS/ARQ/REPORT_5",
				"/srv/A2/R/CKS/CALL",
				"/srv/A2/R/CKS/UKAZ",
				"/srv/A2/R/CKS/OUTSEA/MUSOR.RCH",
				"/srv/A2/R/CKS/MAIL/MSG/BLIND",
			)








if	__name__ == "__main__" : Garch().perform()







