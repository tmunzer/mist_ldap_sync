import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from mist_qrcode import get_qrcode_as_html

class Mist_SMTP():
    def __init__(self, config):
        if (config["enabled"]):
            self.host = config["host"]
            self.port = config["port"]
            self.use_ssl = config["use_ssl"]
            self.username = config["username"]
            self.password = config["password"]
            self.from_name = config["from_name"]
            self.from_email = config["from_email"]
            self.logo_url = config["logo_url"]
            self.email_psk_to_users = config["email_psk_to_users"]
            self.enable_qrcode = config["enable_qrcode"]
            self.report_enabled = config["report_enabled"]
            self.report_receivers = config["report_receivers"]
            if self.use_ssl:
                self.smtp = smtplib.SMTP_SSL
            else: self.smtp = smtplib.SMTP
        else:
            self.email_psk_to_users = False
            self.report_enabled = False
            

    def _send_email(self, receivers, msg, log_message, dry_run:bool=False):
        print(log_message, end="", flush=True)
        try:             
            if not dry_run:
                with self.smtp(self.host, self.port) as smtp:
                    if self.username and self.password:
                        smtp.login(self.username, self.password)
                    smtp.sendmail(self.from_email, receivers, msg)   
            print("\033[92m\u2714\033[0m")
            return True
        except:              
            print('\033[31m\u2716\033[0m')
            return False


    def send_psk(self, psk, ssid, user_name, user_email, dry_run:bool=False):
        if self.email_psk_to_users:
            msg = MIMEMultipart('alternative')
            msg["Subject"] = "Your Personal Wi-Fi access code"
            msg["From"] = "{0} <{1}>".format(self.from_name, self.from_email)
            msg["To"] = "{0} <{1}>".format(user_name, user_email)

            if self.enable_qrcode:
                qr_info = "You can also scan the QRCode below to configure your device:"
                qr_html = get_qrcode_as_html(ssid, psk)                
            else:
                qr_info = ""
                qr_html = ""

            with open("psk_template.html", "r") as template:
                html = template.read()
            html = html.format(self.logo_url, user_name, ssid, psk, qr_info, qr_html)
            msg_body = MIMEText(html, "html")
            msg.attach(msg_body)

            return self._send_email(user_email, msg.as_string(), "    Sending the email ".ljust(79, "."), dry_run)


    def send_report(self, added_psks, removed_psks, dry_run:bool=False):
        if self.report_enabled and not dry_run:
            print("Generating report ".ljust(79, "."), end="", flush=True)
            msg = MIMEMultipart()
            msg["Subject"] = "Automated PSK Report"
            msg["From"] = "{0} <{1}>".format(self.from_name, self.from_email)
            
            add_table=""
            for psk in added_psks:
                name = psk["name"] if "name" in psk else ""
                email = psk["email"] if "email" in psk else ""
                created = "Yes" if psk["psk_added"] else "No"
                sent = "Yes" if psk["email_sent"] else "No"
                add_table += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(name, email, created, sent )

            delete_table=""
            for psk in removed_psks:
                name = psk["psk"] if "psk" in psk else ""
                deleted = "Yes" if psk["psk_deleted"] else "No"
                delete_table += "<tr><td>{0}</td><td>{1}</td></tr>".format(name, deleted)
            with open("report_template.html", "r") as template:
                html = template.read()
            html = html.format(self.logo_url, datetime.today(), len(added_psks), add_table, len(removed_psks), delete_table)
            msg_body = MIMEText(html, "html")
            msg.attach(msg_body)

            print("\033[92m\u2714\033[0m")
            for receiver in self.report_receivers:
                msg["To"] = receiver
                self._send_email(receiver, msg.as_string(), "Sending report email to {0} ".format(receiver).ljust(79, "."))
            return 
        elif dry_run:
            print("Dry Run... Email Report disabled...")
        else:
            print("Report disabled")