mport sqlite3
from pprint import pprint
import asyncio
import aiohttp
import smtplib as smtp


def get_email_list(filename):
    con = sqlite3.connect(filename)
    cur = con.cursor()
    email_list = []
    for item in cur.execute("SELECT * FROM contacts"):
        email_list.append([item[3], item[1]])
    con.close()
    return email_list


class EmailSender:
    def __init__(self):
        self.server = smtp.SMTP_SSL('smtp.yandex.com', 465)
        self.server.set_debuglevel(1)
        self.server.ehlo('opavelokruglov@yandex.ru')
        self.server.login('opavelokruglov@yandex.ru', '********')
        self.server.auth_plain()

    async def email_sending(self, email_list):
        async with aiohttp.ClientSession() as session:
            for email, name in email_list:
                self.server.sendmail('opavelokruglov@yandex.ru', email,
                                     f"Dear {name}!Thanks, that you are using our wonderful service.")
        self.server.quit()


email_list = get_email_list('contacts.db')
i = EmailSender()
asyncio.run(i.email_sending(email_list))
