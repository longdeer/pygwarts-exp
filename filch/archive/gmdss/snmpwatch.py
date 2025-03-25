from pygwarts.magical.time_turner				import TimeTurner
from pygwarts.irma.contrib						import LibraryContrib
from pygwarts.filch.routes						import WatchRoutes
from pygwarts.filch.houses.apppuf.snmp			import SNMPtrap
from pygwarts.filch.itinerarium					import Mapper
from pygwarts.irma.contrib.intercept			import ContribInterceptor
from pygwarts.hedwig.telegram.announce_decor	import Announcer
from watchdogs									import UptimeWatchdog
from watchdogs									import TrapWatchdog
from snmp_mibs									import GMDSSA2MIB
from gopcredo									import mrma2tech
from gopcredo									import gmdssA2mrmENGbot








# Date point for logging and job start
point = TimeTurner()
kill_timer = point.diff(subtrahend=TimeTurner(timepoint="2359"))

if	kill_timer >= 0: print(f"{__file__} invokation out of schedule")

else:

	class Gwatch(WatchRoutes):

	@ContribInterceptor
	@Announcer(gmdssA2mrmENGbot(), mrma2tech())
	@UptimeWatchdog
	@TrapWatchdog
	class loggy(LibraryContrib):

		init_name	= "filch"
		handler		= f"/srv/lcontainer/filch/snmpwatch/{point.Ym_aspath}/gsnmpwatch{point.dmY_asjoin}.loggy"


	class filch(Mapper):	mapfile = "/srv/lcontainer/filch/gbroadmap.csv"
	class Trap(SNMPtrap):

		listen_ip			= "192.168.162.111"
		listen_community	= "trap"
		listen_timeout		= kill_timer

		class withMIB(GMDSSA2MIB):

			load_modules = "POLYGON-MIB", "POLYCOM740-MIB", "XPPC-MIB",
			load_sources = "/srv/lcontainer/filch/mibs",








	watch = Gwatch()
	watch.Trap()







