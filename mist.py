from req import mist_get, mist_delete, mist_post
import random
import string

def _load_conf(conf_obj, conf_val, conf_type):
    if conf_val in conf_obj: return conf_obj[conf_val]
    else: 
        print("Unable to load {0} \"{1}\" from the configuration file.. Exiting...".format(conf_type, conf_val))
        exit(1)

class Mist():
    def __init__(self, config):
        self.host = _load_conf(config.mist, "host", "MIST")
        self.apitoken = _load_conf(config.mist, "apitoken", "Mist")
        self.site_id = _load_conf(config.mist, "site_id", "Mist")
        self.ssid = _load_conf(config.mist, "ssid", "Mist")
        self.psk_length = _load_conf(config.mist, "psk_length", "Mist")
        
    def _get_random_alphanumeric_string(self):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(self.psk_length)))
        return result_str

    def get_users(self, mist_user_list=[]):
        res = self.get_ppks()
        if "result" in res:
            for psk in res["result"]:
                mist_user_list.append({"name": psk["name"], "id": psk["id"]})
        return mist_user_list

    def get_ppks(self):
        url = "https://{0}/api/v1/sites/{1}/psks?ssid={2}".format(self.host, self.site_id, self.ssid)
        response = mist_get(self.apitoken, url)
        return response

    def delete_ppsk(self, psk_id):
        url = "https://{0}/api/v1/sites/{1}/psks/{2}".format(self.host, self.site_id, psk_id)
        response = mist_delete(self.apitoken, url)
        return response

    def create_ppsk(self, user):
        print("    Creating the PPSK for user ".ljust(79, "."), end="", flush=True)
        psk = self._get_random_alphanumeric_string()
        psk_data = {
            "usage": "multi",
            "name": user["name"],
            "ssid": self.ssid,
            "passphrase": psk,
            "id": 1
        }
        try:
            url = "https://{0}/api/v1/sites/{1}/psks".format(self.host, self.site_id)
            res = mist_post(self.apitoken, url, psk_data)["result"] 
            if "id" in res and "ssid" in res and "passphrase" in res:       
                print("\033[92m\u2714\033[0m")
                return res
            else:
                print('\033[31m\u2716\033[0m')
                return None
        except:
            print('\033[31m\u2716\033[0m')
            return None


        
 