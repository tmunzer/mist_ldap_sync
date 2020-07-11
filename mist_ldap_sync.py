import config
from mist_smtp import Mist_SMTP
from mist_ldap import Mist_LDAP
from mist_psk import Mist

class Main():
    def __init__(self):
        self._print_part("INIT", False)
        self.ldap = Mist_LDAP(config)
        self.mist = Mist(config)
        self.smtp = Mist_SMTP(config)
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



if __name__ == "__main__":
    print()
    print("Written by: Thomas Munzer (tmunzer@juniper.net)")
    print("Github: https://github.com/tmunzer/mist_ldap_sync")
    main = Main()
    main.sync()
