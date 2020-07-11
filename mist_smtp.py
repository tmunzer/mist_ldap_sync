import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime

def _load_conf(conf_obj, conf_val, conf_type):
    if conf_val in conf_obj: return conf_obj[conf_val]
    else: 
        print("Unable to load {0} \"{1}\" from the configuration file.. Exiting...".format(conf_type, conf_val))
        exit(1)

class Mist_SMTP():
    def __init__(self, config):
        self.host = _load_conf(config.smtp, "host", "SMTP")
        self.port = _load_conf(config.smtp, "port", "SMTP")
        self.use_ssl = _load_conf(config.smtp, "use_ssl", "SMTP")
        self.username = _load_conf(config.smtp, "username", "SMTP")
        self.password = _load_conf(config.smtp, "password", "SMTP")
        self.from_name = _load_conf(config.smtp, "from_name", "SMTP")
        self.from_email = _load_conf(config.smtp, "from_email", "SMTP")
        self.reports_receiver_emails = _load_conf(config.smtp, "reports_receiver_emails", "SMTP")
        self.logo_url = _load_conf(config.smtp, "logo_url", "SMTP")
        self.email_psk_to_users = _load_conf(config.smtp, "email_psk_to_users", "SMTP")
        self.report_enabled = _load_conf(config.smtp, "report_enabled", "SMTP")
        self.report_receivers = _load_conf(config.smtp, "report_receivers", "SMTP")
        if self.use_ssl:
            self.smtp = smtplib.SMTP_SSL
        else: self.smtp = smtplib.SMTP

    def _send_email(self, receivers, msg, log_message):
        print(log_message, end="", flush=True)
        try:          
            with self.smtp(self.host, self.port) as smtp:
                if self.username and self.password:
                    smtp.login(self.username, self.password)
                smtp.sendmail(self.from_email, receivers, msg)      
            print("\033[92m\u2714\033[0m")
            return True
        except:              
            print('\033[31m\u2716\033[0m')
            return False


    def send_psk(self, psk, ssid, user_name, user_email):
        if self.email_psk_to_users:
            msg = MIMEMultipart('alternative')
            msg["Subject"] = "Your Personal Wi-Fi access code"
            msg["From"] = "{0} <{1}>".format(self.from_name, self.from_email)
            msg["To"] = "{0} <{1}>".format(user_name, user_email)

            with open("email_template.html", "r") as template:
                html = template.read()
            html = html.format(user_name, ssid, psk, self.logo_url)
            msg_body = MIMEText(html, "html")
            msg.attach(msg_body)

        #    with open("logo.png", "rb") as logo:
        #        logo_cid = MIMEImage(logo.read())
        #        logo_cid.add_header("Content-Disposition", "attachment", filename="logo-cid.png", id="logo-cid")
        #        msg.attach(logo_cid)
            return self._send_email(user_email, msg.as_string(), "    Sending the email ".ljust(79, "."))


    def send_report(self, added_psks, removed_psks):
        if self.report_enabled:
            print("".ljust(80, "-"))
            print("Generating report ".ljust(79, "."), end="", flush=True)
            # msg = MIMEMultipart()
            # msg["Subject"] = "Automated PSK Report"
            # msg["From"] = "{0} <{1}>".format(self.from_name, self.from_email)
            # msg["To"] = self.report_receivers
            
            message="""From: {0} <{1}>
To: 
Subject: Automated PSK Report

New Report - {2}
            
            
Added PSK ({3}): 
""".format(self.from_name, self.from_email, datetime.today(), len(added_psks))
            for psk in added_psks:
                if psk["psk_added"]: psk_created = "Created"
                else: psk_created: "NOT Created"
                if psk["email_sent"]: psk_sent = "Email sent to {0}".format(psk["email"])
                elif psk["email"]: psk_sent = "Email NOT sent to {0}".format(psk["email"])
                else: psk_sent = "Email not sent"
                message+="{0} -- {1} and {2}\r\n".format(psk["name"], psk_created, psk_sent)
            message += """
PSK Removed ({0}):
""".format(len(removed_psks))
            for psk in removed_psks:
                if psk["psk_deleted"]: psk_deleted = "Deleted"
                else: psk_deleted = "False"
                message+="{0} -- {1}\r\n".format(psk["psk"], psk_deleted)
            message+="\r\n"

            print("\033[92m\u2714\033[0m")
            self._send_email(self.report_receivers, message, "Sending the email ".ljust(79, "."))