from time								import sleep
from pygwarts.magical.spells			import patronus
from pygwarts.magical.time_turner		import TimeTurner
from pygwarts.irma.contrib				import LibraryContrib
from pygwarts.hedwig.mail.letter.fields	import SenderField
from pygwarts.hedwig.mail.letter.fields	import RecipientField
from pygwarts.hedwig.mail.letter.fields	import SubjectField
from pygwarts.hedwig.mail.letter.fields	import BodyField
from pygwarts.hedwig.mail.builder.smtp	import SMTPBuilder
from pygwarts.hedwig.mail.utils			import EmailValidator
from gopcredo							import mtfudk
import TelegramWECHoist








# Date point for logging
point	= TimeTurner()
ypoint	= TimeTurner(days=-1)








with open(f"/srv/lcontainer/irma/annex/{ypoint.Ym_aspath}/glibrary{ypoint.dmY_asjoin}.annex") as r:
	daliy_report = r.read()


class Greport(SMTPBuilder):

	@TelegramWECHoist
	class loggy(LibraryContrib):

		handler		= f"/srv/lcontainer/hedwig/report/{point.Ym_aspath}/greport{point.dmY_asjoin}.loggy"
		init_name	= "hedwig"

	class validator(EmailValidator):	pass
	class fm(SenderField):				field_value = "mtf.udk@mail.ru"
	class vtt(RecipientField):			field_value = "v.trekin@mrm.rosmorport.ru"
	class vla(RecipientField):			field_value = "v.lupandin@mrm.rosmorport.ru"
	class sde(RecipientField):			field_value = "d.smirnov@mrm.rosmorport.ru"
	class subj(SubjectField):			field_value = f"A2 gserver {ypoint.dmY_aspath} report"
	class six(BodyField):				field_value = daliy_report








hedwig = Greport()
try_counter = 1


if	daliy_report:

	while True:

		try:

			hedwig.build(
				{
					"endpoint": "smtp.mail.ru",
					"port":		465,
					"password":	mtfudk(),
				}
			)
			break

		except	Exception as E:
			if	try_counter == 3:

				raise
				break

			hedwig.loggy.warning(f"{try_counter} try failed due to: {patronus(E)}")
			try_counter += 1
			sleep(15)


else:	hedwig.loggy.info("Daily report file content not found")







