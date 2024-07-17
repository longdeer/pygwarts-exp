from pygwarts.magical.chests					import Chest
from pygwarts.magical.chests					import KeyChest
from pygwarts.magical.time_turner				import TimeTurner
from pygwarts.magical.time_turner.timers		import Timestamp
from pygwarts.irma.contrib						import LibraryContrib
from pygwarts.irma.shelve						import LibraryShelf
from pygwarts.irma.shelve.casing				import numdiffcase
from pygwarts.irma.shelve.casing				import seqcase
from pygwarts.irma.access						import LibraryAccess
from pygwarts.irma.access.volume				import VolumeAccess
from pygwarts.irma.access.volume				import AnnexWrapper
from pygwarts.irma.access.bookmark				import Bookmark
from pygwarts.irma.access.bookmarks.counters	import WarningLevelCounter
from pygwarts.irma.access.bookmarks.counters	import ErrorLevelCounter
from pygwarts.irma.access.bookmarks.counters	import CriticalLevelCounter
from pygwarts.irma.access.inducers				import printf_style
from pygwarts.irma.access.inducers.register		import RegisterCounterInducer
from pygwarts.filch.itinerarium					import Mapper
from pygwarts.filch.houses.nettherin			import VALID_IP4
from pygwarts.filch.houses.linkindor			import VALID_MAC
from filch_handlers								import DiscoverywatchAccessHandler
from filch_handlers								import BroadwatchAccessHandler
from filch_handlers								import SNMPWatchAccessHandler
from filch_inducers								import FilchMapInducer
from filch_inducers								import DiscoveredUpsInducer
from filch_inducers								import DiscoveredDownsInducer
from filch_inducers								import DiscoveredMissesInducer
from filch_inducers								import DiscoveredUnmapsInducer
from filch_inducers								import BroadMapsInducer
from filch_inducers								import BroadUnmapsInducer
from filch_inducers								import BroadMissesInducer
from filch_inducers								import ipDiscoveryInducer
from filch_inducers								import BroadPlotInducer
from filch_inducers								import filchcase
from filch_inducers								import SNMPInducer
from hagrid_bookmarks							import Leafs
from hagrid_bookmarks							import Branches
from hagrid_bookmarks							import Twigs
from hagrid_bookmarks							import Masses
from hagrid_bookmarks							import Navtex
from irma_bookmarks								import OptimizedTimestampActivity
from irma_bookmarks								import ShelfCleans
from irma_bookmarks								import ShelfProduces








point = TimeTurner()
ypoint = point.sight(days=-1)








class TestLibrary(LibraryAccess):
	class loggy(LibraryContrib):

		init_name		= f"irma-{point}-test"
		handover_mode	= True


	class filchmap(Mapper):	mapfile	= "/home/vla/ArrestedDevelopment/pygwarts/development/irma/src/filch/broadmap.csv"
	class library_shelf(LibraryShelf):

		grabbing	= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/shelfs/{ypoint.dmY_asjoin}.Shelf"
		producing	= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/shelfs/{point.dmY_asjoin}.Shelf"


	class library_bookmarks(KeyChest):					pass
	class Warnings(WarningLevelCounter):				pass
	class Errors(ErrorLevelCounter):					pass
	class Criticals(CriticalLevelCounter):				pass
	class Activities(OptimizedTimestampActivity):		pass
	class Trackers(ShelfCleans):						pass
	class Produces(ShelfProduces):						pass
	class library_volumes(Chest):						pass
	class NavDrop(VolumeAccess):

		inrange		= point.dmY_aspath
		location	= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/src/hagrid/gnavdrop{point.dmY_asjoin}.loggy"
		@AnnexWrapper("\n\thagrid-navdrop\n","\n\n")
		class Annex(VolumeAccess.Annex):				pass
		class Grows(Navtex.Drops):						pass
		class Trims(Navtex.Trims):						pass
		class Sanitizes(Navtex.Sanits):					pass
		class Unhandled(Navtex.Unknowns):				pass


	class SoftSync(VolumeAccess):

		inrange		= point.dmY_aspath
		location	= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/src/hagrid/gsoftsync{point.dmY_asjoin}.loggy"
		@AnnexWrapper("\n\thagrid-softsync\n","\n\n")
		class Annex(VolumeAccess.Annex):				pass
		class Grows(Branches.GrowCount):				pass
		class Thrives(Twigs.ThriveCount):				pass


	class HardSync(VolumeAccess):

		inrange		= point.dmY_aspath
		location	= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/src/hagrid/ghardsync{point.dmY_asjoin}.loggy"
		@AnnexWrapper("\n\thagrid-harsync\n","\n\n")
		class Annex(VolumeAccess.Annex):				pass
		class Grows(Leafs.GrowCount):					pass
		class LeafTrims(Leafs.TrimCount):				pass
		class Thrives(Twigs.ThriveCount):				pass
		class TwigTrims(Twigs.TrimCount):				pass
		class Mass(Masses.WeightCount):					pass
		class TwigsCount(Masses.TwigsCount):			pass
		class LeafsCount(Masses.LeafsCount):			pass


	class Arch(VolumeAccess):

		inrange		= point.dmY_aspath
		location	= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/src/hagrid/garch{point.dmY_asjoin}.loggy"
		@AnnexWrapper("\n\thagrid-arch\n","\n\n")
		class Annex(VolumeAccess.Annex):				pass
		class Grows(Branches.GrowCount):				pass
		class Moves(Branches.MoveCount):				pass


	class Discovery(VolumeAccess):

		location	= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/src/filch/gdiscovery{point.dmY_asjoin}.loggy"
		@AnnexWrapper("\n\tfilch-discovery\n","\n\n")
		class Annex(VolumeAccess.Annex):				pass
		class filchmap(Mapper):	mapfile	= "/home/vla/ArrestedDevelopment/pygwarts/development/irma/src/filch/discoverymap.csv"
		class Watch(Bookmark):

			trigger		= "Received response for "
			rpattern	= f"(?P<ip>{VALID_IP4}) at (?P<mac>{VALID_MAC})"

			@printf_style("hosts mapped: %s\n")
			@numdiffcase("library_shelf")
			class MappedHosts(FilchMapInducer):											pass
			class DiscoveredHosts(DiscoverywatchAccessHandler):

				@printf_style("hosts discovered: %s\n")
				@numdiffcase("library_shelf")
				class DiscoveredHostsInducer(RegisterCounterInducer):					pass

				@printf_style("missmatched hosts: %s\n\n")
				class MissmatchedHostsInducer(DiscoveredMissesInducer):

					@numdiffcase("library_shelf")
					class MappingsAmount(DiscoveredMissesInducer.MappingsAmount):		pass
					@seqcase("library_shelf")
					class MissmatchMapping(DiscoveredMissesInducer.MissmatchMapping):	pass

				@printf_style("unknown hosts: %s\n\n")
				class UnknownHostsInducer(DiscoveredUnmapsInducer):

					@numdiffcase("library_shelf")
					class MappingsAmount(DiscoveredUnmapsInducer.MappingsAmount):		pass
					@seqcase("library_shelf")
					class UnmappedMapping(DiscoveredUnmapsInducer.UnmappedMapping):		pass

				@printf_style("mapped up: %s\n\n")
				class KnownHostsInducer(DiscoveredUpsInducer):

					@numdiffcase("library_shelf", asnew=False)
					class MappingsAmount(DiscoveredUpsInducer.MappingsAmount):			pass
					@seqcase("library_shelf")
					class MappedHostName(DiscoveredUpsInducer.MappedHostName):			pass

				@printf_style("mapped down: %s\n\n")
				class DownHostsInducer(DiscoveredDownsInducer):

					@numdiffcase("library_shelf", asnew=False)
					class MappingsAmount(DiscoveredDownsInducer.MappingsAmount):		pass
					@seqcase("library_shelf")
					class ipMappedHostName(DiscoveredDownsInducer.ipMappedHostName):	pass



	class Broad(VolumeAccess):

		location	= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/src/filch/gbroadwatch{point.dmY_asjoin}.loggy"
		plotdir		= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/plots/{point.Ymd_aspath}"
		plotdate	= point
		@AnnexWrapper("\n\tfilch-broadwatch\n","\n\n")
		class Annex(VolumeAccess.Annex):				pass
		class Watch(Bookmark):

			trigger		= "who has "
			rpattern	= rf"(?P<dst>{VALID_IP4}) says (?P<src>{VALID_IP4}) \((?P<mac>{VALID_MAC})\)$"

			class TrappedRequests(BroadwatchAccessHandler):

				@printf_style("graphs plotted: %s\n")
				@numdiffcase("library_shelf")
				class Plotter(BroadPlotInducer):										pass

				@printf_style("requests trapped: %s\n")
				@numdiffcase("library_shelf")
				class TotalTrappedInducer(RegisterCounterInducer):						pass

				@printf_style("ip lookups: %s\n\n")
				class LookupRequestsInducer(ipDiscoveryInducer):

					@numdiffcase("library_shelf")
					class MappingsAmount(ipDiscoveryInducer.MappingsAmount):			pass
					@seqcase("library_shelf", postprocessor=ipDiscoveryInducer.slice_check)
					class ipDiscoveryRequests(ipDiscoveryInducer.ipDiscoveryRequests):	pass

				@printf_style("missmatches: %s\n\n")
				class MissmatchedRequestsInducer(BroadMissesInducer):

					@numdiffcase("library_shelf")
					class MappingsAmount(BroadMissesInducer.MappingsAmount):			pass
					@seqcase("library_shelf", postprocessor=ipDiscoveryInducer.slice_check)
					class MissmatchedRequests(BroadMissesInducer.MissmatchedRequests):	pass

				@printf_style("unknown requests: %s\n\n")
				class UnmappedRequestsInducer(BroadUnmapsInducer):

					@filchcase("library_shelf")
					class FilchGather(BroadUnmapsInducer.FilchGather):					pass

				@printf_style("mapped requests: %s\n")
				class MappedRequestsInducer(BroadMapsInducer):

					@filchcase("library_shelf")
					class FilchGather(BroadMapsInducer.FilchGather):					pass


	class SNMP(VolumeAccess):

		location	= f"/home/vla/ArrestedDevelopment/pygwarts/development/irma/src/filch/gsnmpwatch{point.dmY_asjoin}.loggy"
		@AnnexWrapper("\n\tfilch-snmpwatch\n")
		class Annex(VolumeAccess.Annex):												pass
		class Watch(Bookmark):

			trigger	= "trap from "
			rpattern= rf" : \(trap from (?P<src>{VALID_IP4})\) (?P<msg>.+)$"
			class ReceivedMessages(SNMPWatchAccessHandler):

				@printf_style("received traps: %s\n")
				class Inducer(SNMPInducer):

					@filchcase("library_shelf")
					class FilchGather(SNMPInducer.FilchGather):							pass


	@Timestamp
	class timing(LibraryAccess.Access):													pass







