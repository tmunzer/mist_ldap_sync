import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from mist_qrcode import generate_qrcode

def _load_conf(conf_obj, conf_val, conf_type):
    if conf_val in conf_obj: return conf_obj[conf_val]
    else: 
        print('\033[31m\u2716\033[0m')
        print("Unable to load {0} \"{1}\" from the configuration file.. Exiting...".format(conf_type, conf_val))
        exit(1)

class Mist_SMTP():
    def __init__(self, config):
        print("Loading SMTP settings ".ljust(79, "."), end="", flush=True)
        if hasattr(config, "smtp"):
            self.host = _load_conf(config.smtp, "host", "SMTP")
            self.port = _load_conf(config.smtp, "port", "SMTP")
            self.use_ssl = _load_conf(config.smtp, "use_ssl", "SMTP")
            self.username = _load_conf(config.smtp, "username", "SMTP")
            self.password = _load_conf(config.smtp, "password", "SMTP")
            self.from_name = _load_conf(config.smtp, "from_name", "SMTP")
            self.from_email = _load_conf(config.smtp, "from_email", "SMTP")
            self.logo_url = _load_conf(config.smtp, "logo_url", "SMTP")
            self.email_psk_to_users = _load_conf(config.smtp, "email_psk_to_users", "SMTP")
            self.enable_qrcode = _load_conf(config.smtp, "enable_qrcode", "SMTP")
            self.report_enabled = _load_conf(config.smtp, "report_enabled", "SMTP")
            self.report_receivers = _load_conf(config.smtp, "report_receivers", "SMTP")
            if self.use_ssl:
                self.smtp = smtplib.SMTP_SSL
            else: self.smtp = smtplib.SMTP
            print("\033[92m\u2714\033[0m")
        else:
            print('\033[31m\u2716\033[0m')
            print("SMTP DISABLED")
            self.email_psk_to_users = False
            self.report_enabled = False
            

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

            if self.enable_qrcode:
                qr_info = "You can also scan the QRCode below to configure your device:"
                qr = generate_qrcode(ssid, psk)

                qr_html = ""
                fg_color = "#eee"
                bg_color = "black"
                for i in qr:
                    qr_html+="<tr>"
                    for j in i:
                        if j: color = bg_color
                        else: color = fg_color
                        qr_html +="<td style=\"background-color:{0}; height:5px; width: 5px; padding: 0px; margin: 0px\"></td>\r\n".format(color)
                    qr_html+="</tr>\r\n"
            else:
                qr_info = ""
                qr_html = ""

            with open("psk_template.html", "r") as template:
                html = template.read()
            html = html.format(self.logo_url, user_name, ssid, psk, qr_info, qr_html)
            msg_body = MIMEText(html, "html")
            msg.attach(msg_body)

        #    with open("logo.png", "rb") as logo:
        #        logo_cid = MIMEImage(logo.read())
        #        logo_cid.add_header("Content-Disposition", "attachment", filename="logo-cid.png", id="logo-cid")
        #        msg.attach(logo_cid)
            return self._send_email(user_email, msg.as_string(), "    Sending the email ".ljust(79, "."))


    def send_report(self, added_psks, removed_psks):
        if self.report_enabled:
            print("Generating report ".ljust(79, "."), end="", flush=True)
            msg = MIMEMultipart()
            msg["Subject"] = "Automated PSK Report"
            msg["From"] = "{0} <{1}>".format(self.from_name, self.from_email)
            msg["To"] = ""
            
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
            return self._send_email(self.report_receivers, msg.as_string(), "Sending the email ".ljust(79, "."))
        else:
            print("Report disabled")