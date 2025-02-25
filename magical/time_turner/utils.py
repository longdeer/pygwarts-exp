







@dataclass
class MonthsCases:
	"""
		Take a month name and represent it's cases
	"""

	NOMINATIVE		:str
	GENITIVE		:str
	DATIVE			:str
	ACCUSATIVE		:str
	ABLATIVE		:str
	PREPOSITIONAL	:str








class MonthsLocals:
	"""
		Container for Russian month cases.

		Might be accessed by month short name (JAN, FEB, ...)
		or by month number as string (01, 02, ...)
	"""

	def __init__(self, local_cases :dict):

		self.LOCALS = local_cases


	def __getitem__(self, month :str) -> MonthsCases or KeyError:

		try:	return self.LOCALS[int(month)]
		except	(ValueError, KeyError) as E:	raise ValueError(f"Invalid month value \"{month}\"")




	@property
	def	JAN(self): return self.LOCALS[1]
	@property
	def	FEB(self): return self.LOCALS[2]
	@property
	def	MAR(self): return self.LOCALS[3]
	@property
	def	APR(self): return self.LOCALS[4]
	@property
	def	MAY(self): return self.LOCALS[5]
	@property
	def	JUN(self): return self.LOCALS[6]
	@property
	def	JUL(self): return self.LOCALS[7]
	@property
	def	AUG(self): return self.LOCALS[8]
	@property
	def	SEP(self): return self.LOCALS[9]
	@property
	def	OCT(self): return self.LOCALS[10]
	@property
	def	NOV(self): return self.LOCALS[11]
	@property
	def	DEC(self): return self.LOCALS[12]








RU_LOCAL_CASES_DICT = {

	1:	MonthsCases("январь",	"января", "январю",	"январь", "январём", "январе",),
	2:	MonthsCases("февраль", "февраля", "февралю", "февраль", "февралём", "феврале",),
	3:	MonthsCases("март", "марта", "марту", "март", "мартом", "марте",),
	4:	MonthsCases("апрель", "апреля", "апрелю", "апрель", "апрелем", "апреле",),
	5:	MonthsCases("май", "мая", "маю", "май", "маем", "мае",),
	6:	MonthsCases("июнь", "июня", "июню", "июнь", "июнем", "июне",),
	7:	MonthsCases("июль", "июля", "июлю", "июль", "июлем", "июле",),
	8:	MonthsCases("август", "августа", "августу", "август", "августом", "августе",),
	9:	MonthsCases("сентябрь", "сентября", "сентябрю", "сентябрь", "сентябрём", "сентябре",),
	10:	MonthsCases("октябрь", "октября", "октябрю", "октябрь", "октябрём", "октябре",),
	11:	MonthsCases("ноябрь", "ноября", "ноябрю", "ноябрь", "ноябрём", "ноябре",),
	12:	MonthsCases("декабрь", "декабря", "декабрю", "декабрь", "декабрём", "декабре",),
}








RUMonths = MonthsLocals(RU_LOCAL_CASES_DICT)







