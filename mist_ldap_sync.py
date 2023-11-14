import os
import sys
import logging
import getopt
from dotenv import load_dotenv
from mist_smtp import Mist_SMTP
from mist_ldap import Mist_LDAP
from mist_psk import Mist


LOGGER = logging.getLogger(__name__)
LOG_FILE = "./mist_ldap_sync.log"
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
        "report_receivers": os.environ.get("SMTP_REPORT_RECEIVERS", default=None).split(","),
    }    

    print("\033[92m\u2714\033[0m")

    if verbose:
        print("".ljust(80, "-"))
        print(" SMTP CONFIG ".center(80))
        print("")
        print(f"enabled            : {smtp_config['enabled']}")
        print(f"host               : {smtp_config['host']}")
        print(f"port               : {smtp_config['port']}")
        print(f"use_ssl            : {smtp_config['use_ssl']}")
        print(f"username           : {smtp_config['username']}")
        print(f"from_name          : {smtp_config['from_name']}")
        print(f"from_email         : {smtp_config['from_email']}")
        print(f"logo_url           : {smtp_config['logo_url']}")
        print(f"email_psk_to_users : {smtp_config['email_psk_to_users']}")
        print(f"enable_qrcode      : {smtp_config['enable_qrcode']}")
        print(f"report_enabled     : {smtp_config['report_enabled']}")
        print(f"report_receivers   : {smtp_config['report_receivers']}")
        print("")
    LOGGER.info(f"enabled            : {smtp_config['enabled']}")
    LOGGER.info(f"host               : {smtp_config['host']}")
    LOGGER.info(f"port               : {smtp_config['port']}")
    LOGGER.info(f"use_ssl            : {smtp_config['use_ssl']}")
    LOGGER.info(f"username           : {smtp_config['username']}")
    LOGGER.info(f"from_name          : {smtp_config['from_name']}")
    LOGGER.info(f"from_email         : {smtp_config['from_email']}")
    LOGGER.info(f"logo_url           : {smtp_config['logo_url']}")
    LOGGER.info(f"email_psk_to_users : {smtp_config['email_psk_to_users']}")
    LOGGER.info(f"enable_qrcode      : {smtp_config['enable_qrcode']}")
    LOGGER.info(f"report_enabled     : {smtp_config['report_enabled']}")
    LOGGER.info(f"report_receivers   : {smtp_config['report_receivers']}")

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
        "psk_vlan": os.environ.get("MIST_PSK_VLAN"),
        "psk_max_usage": os.environ.get("MIST_PSK_MAX_USAGE", 0),
        "allowed_chars": os.environ.get("MIST_PSK_ALLOWED_CHARS", default="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"),
        "excluded_psks": os.environ.get("MIST_PSK_EXCLUDED", default="")
    }
    if not mist_config["host"]:
        print("ERROR: Missing MIST_HOST parameters")
        LOGGER.critical("Missing MIST_HOST parameters")
        sys.exit(1)
    elif not mist_config["api_token"]:
        print("ERROR: Missing MIST_API_TOKEN parameters")
        LOGGER.critical("Missing MIST_API_TOKEN parameters")
        sys.exit(1)
    elif not mist_config["scope"]:
        print("ERROR: Missing MIST_SCOPE parameters")
        LOGGER.critical("Missing MIST_SCOPE parameters")
        sys.exit(1)
    elif not mist_config["scope_id"]:
        print("ERROR: Missing MIST_SCOPE_ID parameters")
        LOGGER.critical("Missing MIST_SCOPE_ID parameters")
        sys.exit(1)
    elif not mist_config["ssid"]:
        print("ERROR: Missing MIST_SSID parameters")
        LOGGER.critical("Missing MIST_SSID parameters")
        sys.exit(1)
    elif mist_config["psk_vlan"]:
        if mist_config["psk_vlan"]:
            try:
                mist_config["psk_vlan"] = int(mist_config["psk_vlan"])
                print("\033[92m\u2714\033[0m")
            except:
                print("ERROR: Wrong MIST_PSK_VLAN value. Must be an integer")
                LOGGER.critical("Wrong MIST_PSK_VLAN value. Must be an integer")
                sys.exit(1)
    elif mist_config["psk_max_usage"]:
        try:
            mist_config["psk_max_usage"] = int(mist_config["psk_max_usage"])
            print("\033[92m\u2714\033[0m")
        except:
            print("ERROR: Wrong MIST_PSK_MAX_USAGE value. Must be an integer, 0 for Unlimited")
            LOGGER.critical("Wrong MIST_PSK_MAX_USAGE value. Must be an integer, 0 for Unlimited")
            sys.exit(1)
    else:
        print("\033[92m\u2714\033[0m")

    if verbose:
        print("".ljust(80, "-"))
        print(" MIST CONFIG ".center(80))
        print("")
        print(f"host          : {mist_config['host']}")
        print(f"scope         : {mist_config['scope']}")
        print(f"scope_id      : {mist_config['scope_id']}")
        print(f"ssid          : {mist_config['ssid']}")
        print(f"psk_length    : {mist_config['psk_length']}")
        print(f"psk_vlan      : {mist_config['psk_vlan']}")
        print(f"psk_max_usage : {mist_config['psk_max_usage']}")
        print(f"allowed_chars : {mist_config['allowed_chars']}")
        print(f"excluded_psks : {mist_config['excluded_psks']}")
        print("")
    LOGGER.info(f"host               : {mist_config['host']}")
    LOGGER.info(f"scope              : {mist_config['scope']}")
    LOGGER.info(f"scope_id           : {mist_config['scope_id']}")
    LOGGER.info(f"ssid               : {mist_config['ssid']}")
    LOGGER.info(f"psk_length         : {mist_config['psk_length']}")
    LOGGER.info(f"psk_vlan           : {mist_config['psk_vlan']}")
    LOGGER.info(f"psk_max_usage      : {mist_config['psk_max_usage']}")
    LOGGER.info(f"allowed_chars      : {mist_config['allowed_chars']}")
    LOGGER.info(f"excluded_psks      : {mist_config['excluded_psks']}")

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
        "recursive_search": eval(os.environ.get("LDAP_RECURSIVE_SEARCH", default=False)),
        "user_name": os.environ.get("LDAP_USER_NAME", default="userPrincipalName"),
        "user_email": os.environ.get("LDAP_USER_EMAIL", default="mail")
    }    
    if not ldap_config["host"]: 
        print('\033[31m\u2716\033[0m')
        print("ERROR: Missing the LDAP HOST")
        LOGGER.critical("Missing the LDAP HOST")
        sys.exit(1)
    elif not ldap_config["bind_user"]: 
        print('\033[31m\u2716\033[0m')
        print("ERROR: Missing the LDAP bind_user")
        LOGGER.critical("Missing the LDAP bind_user")
        sys.exit(1)
    elif not ldap_config["base_dn"]: 
        print('\033[31m\u2716\033[0m')
        print("ERROR: Missing the LDAP base_dn")
        LOGGER.critical("Missing the LDAP base_dn")
        sys.exit(1)
    else:
        print("\033[92m\u2714\033[0m")

    if verbose:
        print("".ljust(80, "-"))
        print(" LDAP CONFIG ".center(80))
        print("")
        print(f"host             : {ldap_config['host']}")
        print(f"port             : {ldap_config['port']}")
        print(f"use_ssl          : {ldap_config['use_ssl']}")
        print(f"tls              : {ldap_config['tls']}")
        print(f"bind_user        : {ldap_config['bind_user']}")
        print(f"base_dn          : {ldap_config['base_dn']}")
        print(f"search_group     : {ldap_config['search_group']}")
        print(f"recursive_search : {ldap_config['recursive_search']}")
        print(f"user_name        : {ldap_config['user_name']}")
        print(f"user_email       : {ldap_config['user_email']}")
        print("")
    LOGGER.info(f"host               : {ldap_config['host']}")
    LOGGER.info(f"port               : {ldap_config['port']}")
    LOGGER.info(f"use_ssl            : {ldap_config['use_ssl']}")
    LOGGER.info(f"tls                : {ldap_config['tls']}")
    LOGGER.info(f"bind_user          : {ldap_config['bind_user']}")
    LOGGER.info(f"base_dn            : {ldap_config['base_dn']}")
    LOGGER.info(f"search_group       : {ldap_config['search_group']}")
    LOGGER.info(f"recursive_search   : {ldap_config['recursive_search']}")
    LOGGER.info(f"user_name          : {ldap_config['user_name']}")
    LOGGER.info(f"user_email         : {ldap_config['user_email']}")

    return ldap_config


###############################################################################
###############################################################################
##################################################################### FUNCTIONS
###############################################################################
class Main():
    def __init__(self, ldap_config, mist_config, smtp_config, dry_run):
        self._print_part("INIT", False)
        self.ldap = Mist_LDAP(ldap_config)
        self.mist = Mist(mist_config)
        self.smtp = Mist_SMTP(smtp_config)
        self.report_delete = []
        self.report_add = []
        self.ldap_user_list = []
        self.mist_user_list = []
        self.dry_run = dry_run

    def sync(self):
        if self.dry_run:
            dry_run_string = " DRY RUN - "
            LOGGER.info("Starting in DRY RUN mode")
        else:
            dry_run_string = ""
        self._print_part("LDAP SEARCH")
        self.ldap_user_list = self.ldap.get_users()
        self._print_part("MIST REQUEST")
        self.mist_user_list = self.mist.get_users()
        self._print_part(f"{dry_run_string}DELETE")
        self._delete_psk()
        self._print_part(f"{dry_run_string}CREATE")
        self._create_psk()
        self._print_part("REPORT")
        self.smtp.send_report(self.report_add, self.report_delete, self.dry_run)

    def _print_part(self, part, space=True):
        if space:
            print()
        print(part.center(80, "_"))

    def _delete_psk(self):
        self.report_delete = []
        for psk in self.mist_user_list:
            try:
                next(item["name"] for item in self.ldap_user_list if item["name"]==psk["name"])
            except:
                if not  psk["name"] in self.mist.excluded_psks:                
                    print(f"User {psk['name']} not found... Removing the psk ".ljust(79, "."), end="", flush=True)
                    report = {"psk": psk["name"], "psk_deleted": False}
                    try:
                        self.mist.delete_ppsk(psk["id"], self.dry_run)
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
                    print(f"    name : {user['name']}")
                if user["email"]:
                    print(f"    email: {user['email']}".format())

                psk = self.mist.create_ppsk(user, self.dry_run)
                if psk:
                    report["psk_added"] = True
                    if user["email"]:
                        res = self.smtp.send_psk(psk["passphrase"], psk["ssid"], user["name"], user["email"], self.dry_run)
                        report["email_sent"] = res
                self.report_add.append(report)
        if not self.report_add:
            print("No PSK to create!")

def _check_only():
        _load_ldap(True)
        _load_mist(True)
        _load_smtp(True)

def _run(check, dry_run):
        ldap_config = _load_ldap(check)
        mist_config= _load_mist(check)
        smtp_config =_load_smtp(check)
        main = Main(ldap_config, mist_config, smtp_config, dry_run)
        main.sync()

def usage():
    print("""
Python Script to rotate Mist PSK.
Written by Thomas Munzer (tmunzer@juniper.net)
---
Usage:
-c, --check         Check the configuration file only and display the values 
                    (passowrds and tokens are not shown)

-d, --dry-run       Dry Run. Execute all the tasks, but does not create/delte
                    PPSKs, and does not send any email

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
MIST_PSK_MAX_USAGE=3
MIST_PSK_VLAN=10
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

#######################################################################################################################################
#######################################################################################################################################
############################################# ENTRYPOINT
#######################################################################################################################################
if __name__=="__main__":
    print("""

Python Script to Syncronize LDAP users and Mist PSK.
Written by Thomas Munzer (tmunzer@juniper.net)
Github: https://github.com/tmunzer/mist_ldap_sync

""")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ce:ahdl:", ["check", "env=", "all", "help", "dry-run", "log-file="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    CHECK = False
    CHECK_ONLY = False
    ENV_FILE = None
    DRY_RUN=False
    for o, a in opts:
        if o in ["-h", "--help"]:
            usage()
            sys.exit()
        elif o in ["-c", "--check"]:
            CHECK_ONLY=True
        elif o in ["-a", "--all"]:
            CHECK=True
        elif o in ["-e", "--env"]:
            ENV_FILE = a
        elif o in ["-d", "--dry-run"]:
            DRY_RUN = True
        elif o in ["-l", "--log-file"]:
            LOG_FILE = a
        else:
            assert False, "unhandled option"

    if ENV_FILE:
        load_dotenv(dotenv_path=ENV_FILE)
    else:
        load_dotenv()


    logging.basicConfig(filename=LOG_FILE, filemode='w')
    LOGGER.setLevel(logging.DEBUG)
    if CHECK_ONLY:
        _check_only()
    else: 
        _run(CHECK, DRY_RUN)
