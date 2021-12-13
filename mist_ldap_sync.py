from dotenv import load_dotenv
import getopt
import os
import sys
from mist_smtp import Mist_SMTP
from mist_ldap import Mist_LDAP
from mist_psk import Mist

#######################################################################################################################################
#### SMTP CONFIG
def _load_smtp(verbose):
    print("Loading SMTP settings ".ljust(79, "."), end="", flush=True)    
    smtp_config = {
        "enabled": eval(os.environ.get("SMTP_ENABLED", default="False")),
        "host": os.environ.get("SMTP_HOST", default=None),
        "port": int(os.environ.get("SMTP_PORT", default=587)),
        "use_ssl": eval(os.environ.get("SMTP_USE_SSL", default="True")),
        "username": os.environ.get("SMTP_USERNAME", default=None),
        "password": os.environ.get("SMTP_PASSWORD", default=None),
        "from_name": os.environ.get("SMTP_FROM_NAME", default="Wi-Fi Access"),
        "from_email": os.environ.get("SMTP_FROM_EMAIL", default=None),
        "logo_url": os.environ.get("SMTP_LOGO_URL", default="https://cdn.mist.com/wp-content/uploads/logo.png"),
        "email_psk_to_users": eval(os.environ.get("SMTP_EMAIL_PSK_TO_USERS", default="True")),
        "enable_qrcode": eval(os.environ.get("SMTP_ENABLE_QRCODE", default="True")),
        "report_enabled": eval(os.environ.get("SMTP_REPORT_ENABLED", default="False")),
        "report_receivers": os.environ.get("SMTP_REPORT_RECEIVERS", default=None).split(",")
    }    

    print("\033[92m\u2714\033[0m")

    if verbose:
        print("".ljust(80, "-"))
        print(" SMTP CONFIG ".center(80))
        print("")    
        print("enabled            : {0}".format(smtp_config["enabled"]))
        print("host               : {0}".format(smtp_config["host"]))
        print("port               : {0}".format(smtp_config["port"]))
        print("use_ssl            : {0}".format(smtp_config["use_ssl"]))
        print("username           : {0}".format(smtp_config["username"]))
        print("from_name          : {0}".format(smtp_config["from_name"]))
        print("from_email         : {0}".format(smtp_config["from_email"]))
        print("logo_url           : {0}".format(smtp_config["logo_url"]))
        print("email_psk_to_users : {0}".format(smtp_config["email_psk_to_users"]))
        print("enable_qrcode      : {0}".format(smtp_config["enable_qrcode"]))
        print("report_enabled     : {0}".format(smtp_config["report_enabled"]))
        print("report_receivers   : {0}".format(smtp_config["report_receivers"]))
        print("")

    return smtp_config

#############################################
#### Mist CONFIG

def _load_mist(verbose):
    print("Loading MIST settings ".ljust(79, "."), end="", flush=True)     
    mist_config = {
        "host": os.environ.get("MIST_HOST", default=None),
        "api_token": os.environ.get("MIST_API_TOKEN", default=None),
        "scope": os.environ.get("MIST_SCOPE", default=None),
        "scope_id": os.environ.get("MIST_SCOPE_ID", default=None),
        "ssid": os.environ.get("MIST_SSID", default=None),
        "psk_length": int(os.environ.get("MIST_PSK_LENGTH", default=12)),
        "allowed_chars": os.environ.get("MIST_PSK_ALLOWED_CHARS", default="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"),
    }
    if not mist_config["host"]: 
        print("ERROR: Missing the LDAP HOST")
        print("ERROR: Missing the MIST HOST")
        exit(1)
    elif not mist_config["api_token"]: 
        print("ERROR: Missing the LDAP HOST")
        print("ERROR: Missing the API TOKEN")
        exit(1)
    elif not mist_config["scope"]: 
        print("ERROR: Missing the LDAP HOST")
        print("ERROR: Missing the SCOPE")
        exit(1)
    elif not mist_config["scope_id"]: 
        print("ERROR: Missing the LDAP HOST")
        print("ERROR: Missing the scope_id")
        exit(1)
    elif not mist_config["ssid"]: 
        print("ERROR: Missing the LDAP HOST")
        print("ERROR: Missing the ssid")
        exit(1)
    else:
        print("\033[92m\u2714\033[0m")

    if verbose:
        print("".ljust(80, "-"))
        print(" MIST CONFIG ".center(80))
        print("")
        print("host          : {0}".format(mist_config["host"]))
        print("scope         : {0}".format(mist_config["scope"]))
        print("scope_id      : {0}".format(mist_config["scope_id"]))
        print("ssid          : {0}".format(mist_config["ssid"]))
        print("psk_length    : {0}".format(mist_config["psk_length"]))
        print("allowed_chars : {0}".format(mist_config["allowed_chars"]))
        print("")

    return mist_config

#############################################
#### PSK CONFIG

def _load_ldap(verbose):
    print("Loading LDAP settings ".ljust(79, "."), end="", flush=True)      
    ldap_config = {
        "host": os.environ.get("LDAP_HOST", default=None),
        "port": int(os.environ.get("LDAP_PORT", default=389)),
        "use_ssl": eval(os.environ.get("LDAP_USE_SSL", default="False")),
        "tls": os.environ.get("LDAP_TLS", default=None),
        "bind_user": os.environ.get("LDAP_BIND_USER", default=""),
        "bind_password": os.environ.get("LDAP_BIND_PASSWORD", default=""),
        "base_dn": os.environ.get("LDAP_BASE_DN", default=None),
        "search_group": os.environ.get("LDAP_SEARCH_GROUP", default=None),
        "user_name": os.environ.get("LDAP_USER_NAME", default="userPrincipalName"),
        "user_email": os.environ.get("LDAP_USER_EMAIL", default="mail")
    }    
    if not ldap_config["host"]: 
        print('\033[31m\u2716\033[0m')
        print("ERROR: Missing the LDAP HOST")
        exit(1)
    elif not ldap_config["bind_user"]: 
        print('\033[31m\u2716\033[0m')
        print("ERROR: Missing the LDAP bind_user")
        exit(1)
    elif not ldap_config["base_dn"]: 
        print('\033[31m\u2716\033[0m')
        print("ERROR: Missing the LDAP base_dn")
        exit(1)
    else:
        print("\033[92m\u2714\033[0m")

    if verbose:
        print("".ljust(80, "-"))
        print(" LDAP CONFIG ".center(80))
        print("")
        print("host         : {0}".format(ldap_config["host"]))
        print("port         : {0}".format(ldap_config["port"]))
        print("use_ssl      : {0}".format(ldap_config["use_ssl"]))
        print("tls          : {0}".format(ldap_config["tls"]))
        print("bind_user    : {0}".format(ldap_config["bind_user"]))
        print("base_dn      : {0}".format(ldap_config["base_dn"]))
        print("search_group : {0}".format(ldap_config["search_group"]))
        print("user_name    : {0}".format(ldap_config["user_name"]))
        print("user_email   : {0}".format(ldap_config["user_email"]))
        print("")

    return ldap_config


#######################################################################################################################################
#######################################################################################################################################
############################################# FUNCTIONS
#######################################################################################################################################
class Main():
    def __init__(self, ldap_config, mist_config, smtp_config):
        self._print_part("INIT", False)
        self.ldap = Mist_LDAP(ldap_config)
        self.mist = Mist(mist_config)
        self.smtp = Mist_SMTP(smtp_config)
        self.report_delete = []
        self.report_add = []
        self.ldap_user_list = []
        self.mist_user_list = []

    def sync(self):
        self._print_part("LDAP SEARCH")
        self.ldap_user_list = self.ldap.get_users()
        self._print_part("MIST REQUEST")
        self.mist_user_list = self.mist.get_users()
        self._print_part("DELETE")
        self._delete_psk()
        self._print_part("CREATE")
        self._create_psk()
        self._print_part("REPORT")
        self.smtp.send_report(self.report_add, self.report_delete)

    def _print_part(self, part, space=True):
        if space: print()
        print(part.center(80, "_"))

    def _delete_psk(self):
        self.report_delete = []
        for psk in self.mist_user_list:
            try:
                next(item["name"] for item in self.ldap_user_list if item["name"]==psk["name"])
            except:
                print("User {0} not found... Removing the psk ".format(psk["name"]).ljust(79, "."), end="", flush=True)
                report = {"psk": psk["name"], "psk_deleted": False}
                try:
                    self.mist.delete_ppsk(psk["id"])
                    print("\033[92m\u2714\033[0m")
                    report["psk_deleted"] = True
                except:              
                    print('\033[31m\u2716\033[0m')
                finally:
                    self.report_delete.append(report)
        if not self.report_delete: print("No PSK to delete!")


    def _create_psk(self):
        self.report_add = []
        for user in self.ldap_user_list:
            try:
                next(item["name"] for item in self.mist_user_list if item["name"]==user["name"])
            except:
                print("New User detected ".ljust(80, "-"))
                report = {"name": user["name"], "email": user["email"], "psk_added": False, "email_sent": False}
                if user["name"]:
                    print("    name : {0}".format(user["name"]))
                if user["email"]:
                    print("    email: {0}".format(user["email"]))

                psk = self.mist.create_ppsk(user)
                if psk:
                    report["psk_added"] = True
                    if user["email"]:
                        res = self.smtp.send_psk(psk["passphrase"], psk["ssid"], user["name"], user["email"])
                        report["email_sent"] = res
                self.report_add.append(report)
        if not self.report_add: print("No PSK to create!")

def _chck_only():
        _load_ldap(True)
        _load_mist(True)
        _load_smtp(True)

def _run(check):
        ldap_config = _load_ldap(check)
        mist_config= _load_mist(check)
        smtp_config =_load_smtp(check)
        main = Main(ldap_config, mist_config, smtp_config)
        main.sync()        

def usage():
    print("""
Python Script to rotate Mist PSK.
Written by Thomas Munzer (tmunzer@juniper.net)
---
Usage:
-c, --check         Check the configuration file only and display the values 
                    (passowrds and tokens are not shown)

-e, --env=file      Configuration file location. By default the script
                    is looking for a ".env" file in the script root folder

-a, --all           Check the configuration file (-c) and run the script

---
Configuration file example:
LDAP_HOST="dc.myserver.com"
LDAP_PORT=389
LDAP_USE_SSL=False
LDAP_TLS=None
LDAP_BIND_USER="administrator@myserver.com"
LDAP_BIND_PASSWORD="secret"
LDAP_BASE_DN="DC=myserver,DC=com"
LDAP_SEARCH_GROUP="CN=dot11,OU=LAB Groups,DC=myserver,DC=com"
LDAP_USER_NAME="userPrincipalName"
LDAP_USER_EMAIL="mail"

MIST_HOST="api.mist.com"
MIST_API_TOKEN=""
MIST_SCOPE="orgs"
MIST_SCOPE_ID=""
MIST_SSID=""
MIST_PSK_LENGTH=10
MIST_PSK_ALLOWED_CHARS="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"

SMTP_ENABLED=True
SMTP_HOST="smtp.myserver.com"
SMTP_PORT=465
SMTP_USE_SSL=True
SMTP_USERNAME="user@myserver.com"
SMTP_PASSWORD="secret"
SMTP_FROM_NAME="Wi-Fi Access"
SMTP_FROM_EMAIL=""
SMTP_LOGO_URL="https://cdn.mist.com/wp-content/uploads/logo.png"
SMTP_EMAIL_PSK_TO_USERS=True
SMTP_ENABLE_QRCODE=True
SMTP_REPORT_ENABLED=True
SMTP_REPORT_RECEIVERS="user.1@myserver.com,user.2@myserver.com"

    """)

def main():    
    print("""

Python Script to Syncronize LDAP users and Mist PSK.
Written by Thomas Munzer (tmunzer@juniper.net)
Github: https://github.com/tmunzer/mist_ldap_sync

""")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ce:ah", ["check", "env=", "all", "help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    check = False
    check_only = False
    env_file = None
    for o, a in opts:
        if o in ["-h", "--help"]:
            usage()
            sys.exit()
        elif o in ["-c", "--check"]:
            check_only=True
        elif o in ["-a", "--all"]:
            check=True
        elif o in ["-e", "--env"]:
            env_file = a
        else:
            assert False, "unhandled option"
  
    if env_file:
        load_dotenv(dotend_path=env_file)
    else:
        load_dotenv()

    if check_only:
        _chck_only()
    else: 
        _run(check)


#######################################################################################################################################
#######################################################################################################################################
############################################# ENTRYPOINT
#######################################################################################################################################
if __name__=="__main__":
        main()
