from os													import makedirs
from os													import path		as ospath
from typing												import Callable
from collections										import defaultdict
from collections										import Counter
from collections.abc									import Sequence
from pygwarts.magical.philosophers_stone				import Transmutable
from pygwarts.magical.philosophers_stone.transmutations	import ControlledTransmutation
from pygwarts.magical.time_turner						import TimeTurner
from pygwarts.magical.patronus							import CAST
from pygwarts.irma.access.volume						import VolumeAccess
from pygwarts.irma.access.inducers						import AccessInducer
from pygwarts.irma.access.inducers.register				import RegisterRecapInducer
from pygwarts.irma.shelve								import LibraryShelf
from pygwarts.irma.shelve.casing						import numdiffcase
from matplotlib											import pyplot	as pp








class filchcase(ControlledTransmutation):

	"""
		irma.access.inducers decorator class, that involves irma.shelve.casing functionality with filch
		statistics gathering adaptation. It implies the wrapping over a Transmutable, that takes a dict
		as a two-level mapping. The first level (root keys) are considered as sources of some records,
		when the second level keys are considered those records targets, and finally their values
		are integers that represents counts of those records frequencies.
	"""

	def __init__(self, link :str, asnew :bool =True):

		self.link	= link
		self.asnew	= asnew


	def __call__(self, chained_layer :Transmutable) -> Callable :

		chained	= super().__call__(chained_layer)
		link	= self.link
		asnew	= self.asnew




		def transmutation(upper_layer :Transmutable) -> Transmutable :
			class Transmute(chained(upper_layer)):

				def __call__(self, records :dict) -> str or None :

					if	isinstance(records, dict) and len(records) :
						self.loggy.debug(f"Obtained case map {len(records)} root keys")


						if	isinstance(shelf := getattr(self, link, None), LibraryShelf):
							prevcase, shelf[str(self)] = shelf[str(self)], dict(records)



							records_view	= str()
							records_total	= int()
							sorted_sources	= sorted(

								records,
								key=lambda x : sum(records[x][y] for y in records[x]),
								reverse=True
							)




							for src in sorted_sources:
								if	(
										prevcase is not None and src not in prevcase
									)	or	(
										prevcase is None and asnew
									):

									srcname = f"(+) {src}"
									newsrc	= True
								else:
									srcname = src
									newsrc	= False


								src_total	= int()
								src_string	= str()




								# Obtain descending amount of single target
								# records order for current host.
								targets = records[src]
								soreted_targets = sorted(targets, key=lambda x : targets[x], reverse=True)




								for target in soreted_targets:

									target_name		=	f"(+) {target}" if(

										not newsrc and
										prevcase is not None and
										target not in prevcase[src]

									)	else target


									current			=	targets[target]
									current_view	=	numdiffcase.defaultcase(

										current,
										*numdiffcase.eval_diff(current, prevcase[src][target])

									)	if	(

										not newsrc and
										prevcase is not None and
										target in prevcase[src] and
										current != prevcase[src][target]

									)	else current


									src_total		+=	current
									records_total	+=	current
									src_string		+=	str(f"\t\t{target_name}: {current_view}\n")




								shelf[str(self)][src]["TOTAL"] = src_total




								if	len(targets) >2:

									src_total_view	=	numdiffcase.defaultcase(

										src_total,
										*numdiffcase.eval_diff(src_total, prevcase[src]["TOTAL"])

									)	if	(

										not newsrc and
										prevcase is not None and
										"TOTAL" in prevcase[src] and
										src_total != prevcase[src]["TOTAL"]

									)	else src_total

									records_view	+=	f"\t{srcname}: {src_total_view}\n{src_string}"
								else:
									records_view	+=	f"\t{srcname}:\n{src_string}"




							shelf[str(self)]["TOTAL"] = records_total




							requests_total_view = (

								numdiffcase.defaultcase(
							
									records_total,
									*numdiffcase.eval_diff(records_total, prevcase["TOTAL"])
							
							)	if	(

								prevcase is not None and
								"TOTAL" in prevcase and
								records_total != prevcase["TOTAL"]

							)	else	records_total
							)	if		records_total >1 else ""


							return	"%s\n%s"%(requests_total_view, records_view)


						else:

							self.loggy.warning(f"\"{link}\" doesn't point to a LibraryShelf object")
							return	super().__call__(records)


			return	Transmute




		# Completing controlled transmutation
		transmutation.CHAIN_OVER_HOOK = True
		self.CHAIN_LAYER_HOOK = transmutation


		return	transmutation
















class FilchRegisterRecapInducer(RegisterRecapInducer):
	class MappingsAmount(Transmutable):

		def __call__(self, amount :int | float | str) -> str :
			self.loggy.debug(f"Considering amount {amount}")

			if	int(float(amount)) : return	str(amount)




	class FilchGather(Transmutable):
		def __call__(self, requests :dict) -> str or None :

			if	isinstance(requests, dict) and len(requests):

				requests_view	= str()
				requests_total	= int()
				sorted_sources	= sorted(

					requests,
					key=lambda x : sum(requests[x][y] for y in requests[x]),
					reverse=True
				)


				for src in sorted_sources:

					src_total	= int()
					src_string	= str()


					# Obtain descending amount of single target requests order for current host.
					targets = requests[src]
					soreted_targets = sorted(targets, key=lambda x : targets[x], reverse=True)


					for target in soreted_targets:

						current			=	targets[target]
						src_total		+=	current
						requests_total	+=	current
						src_string		+=	f"\t\t{target}: {current}\n"


					if	len(targets) >1 :	requests_view += f"\t{src}: {src_total}\n{src_string}"
					else				:	requests_view += f"\t{src}:\n{src_string}"


				return	"%s\n%s"%(requests_total if requests_total >1 else "", requests_view)


			self.loggy.debug("No requests found")
















class FilchMapInducer(AccessInducer):

	"""
		Induces amount of mapped by filch entities
	"""

	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(register := super().__call__(volume)) is not None :
			if	hasattr(self, "filchmap"):
				if	(mapped_hosts := len(self.filchmap)) >0 :


					self.loggy.debug(f"Filch mapped {mapped_hosts} hosts")
					return	str(mapped_hosts)


				self.loggy.debug("No hosts mapped by Filch")
			else:
				self.loggy.debug(f"Inducer {self} couldn't find Filch map")
















class DiscoveryResponsesInducer(FilchRegisterRecapInducer):

	"""
		Super for filch discovery Inducers
	"""

	class MappedHostName(Transmutable):
		def __call__(self, mappings :Sequence) -> list :

			self.loggy.debug(f"Obtaining host names of {len(mappings)} mappings")
			return	[ mapper.get("filch_mapped_host_name") for mapper in mappings ]


	class MappedHostDescription(Transmutable):
		def __call__(self, mappings :Sequence) -> list :

			self.loggy.debug(f"Obtaining host descriptions of {len(mappings)} mappings")
			return	[ mapper.get("filch_mapped_description") for mapper in mappings ]


	class ipMappedHostName(Transmutable):
		def __call__(self, mappings :Sequence) -> list :

			self.loggy.debug(f"Obtaining host names of {len(mappings)} ip addresses")
			return	[ self.filchmap.ipmap_host(ip) for ip in mappings ]


	class ipMappedHostDescription(Transmutable):
		def __call__(self, mappings :Sequence) -> list :

			self.loggy.debug(f"Obtaining host descriptions of {len(mappings)} ip addresses")
			return	[ self.filchmap.ipmap_desc(ip) for ip in mappings ]


	class MissmatchMapping(Transmutable):
		def __call__(self, mappings :Sequence) -> list :

			self.loggy.debug(f"Obtaining host names of {len(mappings)} missmatches")
			return	[

				"%s response with %s mac"%(
					mapper.get("filch_mapped_host_name"), mapper.get("filch_maced_host_name")
				)

				if mapper.get("filch_mapped_mac") is not None else

				"%s response from unknown %s"%(
					mapper.get("filch_maced_host_name"), mapper.get("discovered_ip")
				)

				for mapper in mappings
			]


	class UnmappedMapping(Transmutable):
		def __call__(self, mappings :Sequence) -> list :

			self.loggy.debug(f"Obtaining names of {len(mappings)} unmapped hosts")
			return	[

				"%s response with unknown %s"%(
					mapper.get("filch_mapped_host_name"), mapper.get("discovered_mac")
				)

				if mapper.get("filch_mapped_mac") is not None else

				"%s unknown response from unknown %s"%(
					mapper.get("discovered_mac"), mapper.get("discovered_ip")
				)

				for mapper in mappings
			]








class DiscoveredUpsInducer(DiscoveryResponsesInducer):

	"""
		Induces recap dictionary
	"""

	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict) and (hosts := recap.get("known_hosts")) is not None :

				try:

					if	(amount := len(hosts)) >0 and (amount_view := self.MappingsAmount(amount)):
						return	"%s\n\t%s"%(

							amount_view if amount >1 else str(),
							"\n\t".join(

								f"{host_name} ({description})" for host_name, description
								in zip(self.MappedHostName(hosts), self.MappedHostDescription(hosts))
							)
						)


					self.loggy.debug(f"Inducer {self} found no mapped hosts discovered")


				except	Exception as E:

					self.loggy.warning(f"Inducer {self} failed due to {CAST(E)}")
			else:	self.loggy.warning(f"Inducer {self} obtained invalid recap")








class DiscoveredMissesInducer(DiscoveryResponsesInducer):

	"""
		Induces hosts, that mapped in any way, but missmatched by other's mac or unknown ip
	"""

	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict) and not (misses := list()):

				if	(miss_mac := recap.get("missmatched_mac")) is not None	: misses.extend(miss_mac)
				if	(miss_ip := recap.get("missmatched_ip")) is not None	: misses.extend(miss_ip)


				try:

					if	(amount := len(misses)) >0 and (amount_view := self.MappingsAmount(amount)):
						return	"%s\n\t%s"%(

							amount_view if amount >1 else str(),
							"\n\t".join(self.MissmatchMapping(misses))
						)


					self.loggy.debug(f"Inducer {self} found no missmatched hosts discovered")


				except	Exception as E:

					self.loggy.warning(f"{self} failed due to {CAST(E)}")
			else:	self.loggy.warning(f"Inducer {self} obtained invalid recap")








class DiscoveredUnmapsInducer(DiscoveryResponsesInducer):

	"""
		Induces hosts, that either mapped by ip but has unknown mac, or mapped by mac, but has unknown ip
	"""

	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict) and not (unknowns := list()):

				if	(no_mac := recap.get("unknown_mac")) is not None	: unknowns.extend(no_mac)
				if	(no_ip := recap.get("unknown_ip")) is not None		: unknowns.extend(no_ip)


				try:

					if	(amount := len(unknowns)) >0 and (amount_view := self.MappingsAmount(amount)):
						return	"%s\n\t%s"%(

							amount_view if amount >1 else str(),
							"\n\t".join(self.UnmappedMapping(unknowns))
						)


					self.loggy.debug(f"Inducer {self} found no unmapped hosts discovered")


				except	Exception as E:

					self.loggy.warning(f"{self} failed due to {CAST(E)}")
			else:	self.loggy.warning(f"Inducer {self} obtained invalid recap")








class DiscoveredDownsInducer(DiscoveryResponsesInducer):

	"""
		Induces mapped hosts that left after discoverd up and all missmatches
	"""

	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict) and not (discoveres := list()):

				if	(up_hosts := recap.get("known_hosts")) is not None :
					discoveres.extend( host.get("discovered_ip") for host in up_hosts )

				if	(miss_ip := recap.get("missmatched_ip")) is not None :
					discoveres.extend( host.get("discovered_ip") for host in  miss_ip )

				if	(miss_mac := recap.get("missmatched_mac")) is not None :
					discoveres.extend( host.get("discovered_ip") for host in miss_mac )


				try:

					amount = len(remained := set(self.filchmap.lmap).difference(discoveres))

					if	amount >0 and (amount_view := self.MappingsAmount(amount)):
						return	"%s\n\t%s"%(

							amount_view if amount >1 else str(),
							"\n\t".join(

								f"{host_name} ({description})" for host_name, description in zip(
									self.ipMappedHostName(remained),self.ipMappedHostDescription(remained)
								)
							)
						)


					self.loggy.debug(f"Inducer {self} found no mapped hosts down")


				except	Exception as E:

					self.loggy.warning(f"{self} failed due to {CAST(E)}")
			else:	self.loggy.warning(f"Inducer {self} obtained invalid recap")
















class BroadwatchRequestsInducer(FilchRegisterRecapInducer):

	"""
		Induces ARP requests that a recaped as counted dictionaries
	"""

	class MissmatchedRequests(Transmutable):
		def __call__(self, mappings :Sequence) -> list :

			self.loggy.debug(f"Obtaining host names of {len(mappings)} missmatches")
			return	[

				"%s source mac missmatching at %s"%(

					mapper.get("source_mapped_name"),
					mapper.get("timestamp").format("%H%M %d/%m/%Y")
				)


				if mapper.get("source_mapped_name") is not None else


				"%s source ip missmatching at %s"%(

					mapper.get("source_maced_name"),
					mapper.get("timestamp").format("%H%M %d/%m/%Y")
				)


				if mapper.get("target_mapped_name") is not None else


				"%s unknown request missmatched %s ip at %s"%(

					mapper.get("request_target_ip"),
					mapper.get("source_maced_name"),
					mapper.get("timestamp").format("%H%M %d/%m/%Y")
				)


				for mapper in mappings
			]




	class ipDiscoveryRequests(Transmutable):
		def __call__(self, mappings :Sequence) -> list :

			self.loggy.debug(f"Obtaining host names of {len(mappings)} ip discoveres")
			return	[

				"%s ip lookup at %s"%(

					mapper.get("source_maced_name"),
					mapper.get("timestamp").format("%H%M %d/%m/%Y")
				)


				if	(mapper.get("source_maced_ip") is not None)		and
					(mapper.get("source_maced_name") is not None)	else


				"%s missmatched %s lookup at %s"%(

					mapper.get("source_maced_name"),
					mapper.get("target_mapped_name"),
					mapper.get("timestamp").format("%H%M %d/%m/%Y")
				)


				if	(mapper.get("source_maced_name") is not None)	and
					(mapper.get("target_mapped_name") is not None)	else


				"%s missmatched unknown %s lookup at %s"%(

					mapper.get("source_maced_name"),
					mapper.get("request_target_ip"),
					mapper.get("timestamp").format("%H%M %d/%m/%Y")
				)


				if	(mapper.get("source_maced_name") is not None)	and
					(mapper.get("request_target_ip") is not None)	else


				"%s ip lookup from unknown %s at %s"%(

					mapper.get("target_mapped_name"),
					mapper.get("request_source_mac"),
					mapper.get("timestamp").format("%H%M %d/%m/%Y")
				)


				if	(mapper.get("target_mapped_ip") is not None)	and
					(mapper.get("target_mapped_name") is not None)	else


				"%s unknown lookup from unknown %s at %s"%(

					mapper.get("request_target_ip"),
					mapper.get("request_source_mac"),
					mapper.get("timestamp").format("%H%M %d/%m/%Y")
				)


				for mapper in mappings
			]




	@staticmethod
	def slice_check(
						request		:str,
						previous	:Sequence,
						current		:Sequence,
						processor	:Callable
					)-> str or None	:

		"""
			For filch seqcase postprocessor
		"""

		sliced		= " ".join(request.split()[:-2])
		counter		= Counter(current)[request]
		processed	= False


		for sliced_record in ( " ".join(record.split()[:-2]) for record in previous ):
			if	sliced == sliced_record:

				processed = request
				break


		for i in range(counter) : current.remove(request)
		return	(processed or f"(+) {request}") + (f" (x{counter})" if counter >1 else "")









class BroadMapsInducer(BroadwatchRequestsInducer):

	"""
		Induces ARP requests with mapped sources and targets
	"""

	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict) and isinstance(records := recap.get("mapped_requests"), list) :
				requests = defaultdict(lambda : defaultdict(int))

				for record in records:
					if	not isinstance(record, dict):

						self.loggy.warning(f"{self} found invalid \"{record}\"")
					else:
						requests[record.get("source_mapped_name")][record.get("target_mapped_name")] += 1


				if	(induce := self.FilchGather(requests)) is not None : return induce
			else:	self.loggy.debug("Couldn't obtain records")








class BroadUnmapsInducer(BroadwatchRequestsInducer):

	"""
		Induces ARP requests with unmapped sources or targets
	"""

	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict) and isinstance(records := recap.get("unmapped_requests"), list) :
				requests = defaultdict(lambda : defaultdict(int))

				for record in records:
					if	not isinstance(record, dict):

						self.loggy.warning(f"{self} found invalid \"{record}\"")
					else:
						source = record.get("source_mapped_name") or record.get("request_source_ip")
						target = record.get("target_mapped_name") or record.get("request_target_ip")
						requests[source][target] += 1


				if	(induce := self.FilchGather(requests)) is not None : return induce
			else:	self.loggy.debug("Couldn't obtain records")








class BroadMissesInducer(BroadwatchRequestsInducer):

	"""
		Induces requests with missmatched ip or mac
	"""

	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict) and not (misses := list()):

				if	(miss_mac := recap.get("missmatched_mac")) is not None	: misses.extend(miss_mac)
				if	(miss_ip := recap.get("missmatched_ip")) is not None	: misses.extend(miss_ip)


				try:

					if	(amount := len(misses)) >0 and (amount_view := self.MappingsAmount(amount)):
						return	"%s\n\t%s"%(

							amount_view if amount >1 else str(),
							"\n\t".join(self.MissmatchedRequests(misses))
						)


					self.loggy.debug(f"Inducer {self} found no missmatched requests")


				except	Exception as E:

					self.loggy.warning(f"{self} failed due to {CAST(E)}")
			else:	self.loggy.warning(f"Inducer {self} obtained invalid recap")








class ipDiscoveryInducer(BroadwatchRequestsInducer):

	"""
		Induces broadcast ip lookups
	"""

	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict) and (lookups := recap.get("ip_lookup")) is not None :

				try:

					if	(amount := len(lookups)) >0 and (amount_view := self.MappingsAmount(amount)):
						return	"%s\n\t%s"%(

							amount_view if amount >1 else str(),
							"\n\t".join(self.ipDiscoveryRequests(lookups))
						)


					self.loggy.debug(f"Inducer {self} found no ip lookups")


				except	Exception as E:

					self.loggy.warning(f"{self} failed due to {CAST(E)}")
			else:	self.loggy.warning(f"Inducer {self} obtained invalid recap")
















class BroadPlotInducer(RegisterRecapInducer):

	"""
		Gather all requests and plot graphs
	"""

	plotdir		:str
	plotdate	:TimeTurner


	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		if	not hasattr(self, "plotdir") : self.loggy.warning(f"Inducer {self} found no plotting directory")
		if	not hasattr(self, "plotdate"):
			self.loggy.warning(f"Inducer {self} found no plotting date")

		elif	isinstance(self.plotdate, TimeTurner) : pass
		else:
			try:	self.plotdate = TimeTurner(self.plotdate)
			except	ValueError : self.loggy.warning(f"Plotting date is not TimeTurnerable object")




	def __call__(self, volume :VolumeAccess) -> str or None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict):

				totals		= defaultdict(int)
				requests	= defaultdict(lambda : defaultdict(int))


				if	isinstance(mapped := recap.get("mapped_requests"), list):

					for record in mapped:

						source = record.get("source_mapped_name") or record.get("request_source_ip")
						if	(target := record.get("timestamp")) and isinstance(target, TimeTurner) :

							point = int(TimeTurner.hundscale(target.HM_asjoin))
							totals[point] += 1
							requests[source][point] += 1


					self.loggy.debug(f"Gathered {len(mapped)} mapped sources")
					del mapped
				else:
					self.loggy.debug("No mapped sources found")




				if	isinstance(unmapped := recap.get("unmapped_requests"), list):

					for record in unmapped:

						source = record.get("source_mapped_name") or record.get("source_maced_name")
						source = source or record.get("request_source_ip")
						if	(target := record.get("timestamp")) and isinstance(target, TimeTurner) :
							
							point = int(TimeTurner.hundscale(target.HM_asjoin))
							totals[point] += 1
							requests[source][point] += 1


					self.loggy.debug(f"Gathered {len(unmapped)} unmapped sources")
					del unmapped
				else:
					self.loggy.debug("No unmapped sources found")




				if	isinstance(miss_mac := recap.get("missmatched_mac"), list):

					for record in miss_mac:

						source = record.get("source_mapped_name") or record.get("request_source_ip")
						if	(target := record.get("timestamp")) and isinstance(target, TimeTurner) :
							
							point = int(TimeTurner.hundscale(target.HM_asjoin))
							totals[point] += 1
							requests[source][point] += 1


					self.loggy.debug(f"Gathered {len(miss_mac)} missmatched mac sources")
					del miss_mac
				else:
					self.loggy.debug("No missmatched mac sources found")




				if	isinstance(miss_ip := recap.get("missmatched_ip"), list):

					for record in miss_ip:

						source = record.get("source_mapped_name") or record.get("request_source_ip")
						if	(target := record.get("timestamp")) and isinstance(target, TimeTurner) :
							
							point = int(TimeTurner.hundscale(target.HM_asjoin))
							totals[point] += 1
							requests[source][point] += 1


					self.loggy.debug(f"Gathered {len(miss_ip)} missmatched ip sources")
					del miss_ip
				else:
					self.loggy.debug("No missmatched ip sources found")




				if	isinstance(lookups := recap.get("ip_lookup"), list):

					for record in lookups:

						source = record.get("request_source_ip")
						if	(target := record.get("timestamp")) and isinstance(target, TimeTurner) :
							
							point = int(TimeTurner.hundscale(target.HM_asjoin))
							totals[point] += 1
							requests[source][point] += 1


					self.loggy.debug(f"Gathered {len(lookups)} lookup sources")
					del lookups
				else:
					self.loggy.debug("No lookup sources found")




				if	(counter := len(requests)):

					requests_gathered = sum( requests[X][Y] for X in requests for Y in requests[X] )
					self.loggy.debug(f"Gathered {requests_gathered} requests total")


					if	hasattr(self, "plotdir") and hasattr(self, "plotdate"):

						try:

							# Total requests poltting.
							# TODO: infer plot names by some escalatable variables.
							self.bwplotter(

								axises=totals.items(),
								title=f"total by {self.plotdate.dmY_aspath}",
								pngpath=self.plotdir,
								pngname=f"total-{self.plotdate.dmY_asjoin}.png",
							)


							# Requests by hosts for parsed date
							for source, requests_time_mapping in requests.items():

								self.bwplotter(

									axises=requests_time_mapping.items(),
									title=f"{source} by {self.plotdate.dmY_aspath}",
									pngpath=self.plotdir,
									pngname=f"{source}-{self.plotdate.dmY_asjoin}.png",
								)


							if	counter - self.bwplotter.plotting_counter >0 :

								self.loggy.info(f"{self.bwplotter.plotting_counter} plots out of {counter}")
								return	f"{self.bwplotter.plotting_counter} out of {counter}"


							self.loggy.info(f"{self.bwplotter.plotting_counter} plots")
							del totals,requests


							return	str(self.bwplotter.plotting_counter)


						except	OSError as E:
						# except	Exception as E:

							self.loggy.warning(f"Plotting failed due ot {CAST(E)}")
					else:	self.loggy.debug("Plotting aborted")
				else:		self.loggy.debug("No requests gathered")
			else:			self.loggy.warning(f"Inducer {self} obtained invalid recap")








	class bwplotter(Transmutable):

		"""
			Makes the most valuable visual with vertical lines for ARP requests count
			at every minute of monitoring.
		"""

		def __init__(self, *args, **kwargs):

			super().__init__(*args, **kwargs)
			self.plotting_counter = int()


		def __call__(	self,
						axises		:iter,
						title		:str,
						pngpath		:str,
						pngname		:str,
						linecolor	:str	="red",
						linewidth	:int	=1,
						fontsize	:int	=20,
						Xlength		:int	=40,
						Ylength		:int	=20,
					)-> str or None	:

			"""
				Takes axises as prepared iterable, that consist of X,Y pairs.
				Plot veritcal lines with provided or defaulted attributes
				and saves png file to destination path, which also returned as string.
			"""

			pp.figure(figsize=(Xlength,Ylength))
			pp.title(title, fontsize=fontsize)


			self.loggy.info(f"Plotting {title}")
			self.loggy.debug(f"Axises length {len(axises)}")
			self.loggy.debug(f"Lines width {linewidth}")
			self.loggy.debug(f"Lines color {linecolor}")
			self.loggy.debug(f"Font size {fontsize}")
			self.loggy.debug(f"X length {Xlength}")
			self.loggy.debug(f"Y length {Ylength}")


			try:

				makedirs(pngpath, exist_ok=True)
				self.loggy.debug(f"Output directory validated")

			except	Exception as E:

				self.loggy.critical(f"Failed to validate path {pngpath} due to {E.__class__.__name__}: {E}")
				return




			savepath = ospath.join(pngpath, pngname)
			self.loggy.debug(f"Output final destination {savepath}")


			try:

				Ys = set()
				for X,Y in axises:

					Ys.add(Y)
					pp.vlines(

						x=X,
						ymin=0,
						ymax=Y,
						linewidth=linewidth,
						color=linecolor,
					)


			except	Exception as E:

				self.loggy.critical(f"Failed tp plot {title} due to {E.__class__.__name__}: {E}")
				return




			# X-axis tuning to be 24 hours scale
			pp.xlabel("Hours (MSK)", fontsize=fontsize)
			pp.xlim(-10, 2310)
			pp.xticks(

				[ i for i in range(0, 2400, 100) ],
				labels=[ i for i in range(24) ],
				fontsize=fontsize,
			)


			# Y-axis tuning
			pp.ylabel("ARP requests", fontsize=fontsize)
			pp.ylim(0)
			pp.yticks(self.cooler_make_Y_ticks(Ys, Ylength), fontsize=fontsize)


			pp.savefig(savepath)
			pp.close()
			self.plotting_counter += 1


			return	savepath




		def make_Y_ticks(self, Ymaximum :int, Ylength :int) -> range :

			"""
				Calculating of double Y-axis length scaled. It is calculated in the way
				the range step is a lowest quotient of Y maximum and doubled Y length,
				the range start is a modulo of Y maximum and range step,
				the range maximum is Y maimum plus one to include Y maximum.
			"""

			if	(step := Ymaximum //(2 *Ylength)):

				return	range(Ymaximum %step, Ymaximum +1, step)
			return		range(Ymaximum +1)




		def cooler_make_Y_ticks(self, Ys :set, Ylength :int) -> list :

			"""
				Calculates the list of ticks from double Y-axis length scaled ticks,
				that present on the plot.
			"""

			return	[ tick for tick in self.make_Y_ticks(max(Ys), Ylength) if tick in Ys ]
















class SNMPInducer(FilchRegisterRecapInducer):

	"""
		Inducer for SNMP trap messages collection. Relies on a "recap" as a filch-mapped dictionary.
	"""

	def __call__(self, volume :VolumeAccess) -> str | None :

		if	(recap := super().__call__(volume)) is not None :
			if	isinstance(recap, dict):
				if	(induce := self.FilchGather(recap)) is not None : return induce







