import mistapi
import random
import logging
import sys

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Mist:
    def __init__(self, config):
        self.scope = config.get("scope")
        self.scope_id = config.get("scope_id")
        self.ssid = config.get("ssid")
        self.psk_length = config.get("psk_length")
        self.psk_vlan = config.get("psk_vlan")
        self.psk_max_usage = config.get("psk_max_usage")
        self.allowed_chars = config.get("allowed_chars")
        self.excluded_psks = config.get("excluded_psks")
        self.apisession = mistapi.APISession(
            host=config.get("host"), apitoken=config.get("api_token")
        )
        self.apisession.login()

    def _get_random_alphanumeric_string(self):
        result_str = "".join(
            (random.choice(self.allowed_chars) for i in range(self.psk_length))
        )
        return result_str

    def get_users(self, mist_user_list=[]):
        print(f"Requesting the list of PSKs ".ljust(79, "."), end="", flush=True)
        LOGGER.info(f"Requesting the list of PSKs")
        try:
            psks = self.get_ppks()
            for psk in psks:
                mist_user_list.append({"name": psk["name"], "id": psk["id"]})
            print("\033[92m\u2714\033[0m")
            LOGGER.info(f"Got {len(mist_user_list)} users")
            return mist_user_list
        except:
            print("\033[31m\u2716\033[0m")
            LOGGER.critical("Exception occurred", exc_info=True)
            sys.exit(2)

    def get_ppks(self):
        if self.scope == "org":
            response = mistapi.api.v1.orgs.psks.listOrgPsks(
                self.apisession, self.scope_id, limit=1000
            )
        else:
            response = mistapi.api.v1.sites.psks.listSitePsks(
                self.apisession, self.scope_id, limit=1000
            )
        data = mistapi.get_all(self.apisession, response)
        return data

    def delete_ppsk(self, psk_id, dry_run: bool = False):
        LOGGER.debug(f"deleting psk with id {psk_id}")
        if dry_run:
            LOGGER.info("dry run mode... I'm not deleting the psk")
            return True
        else:
            if self.scope == "org":
                response = mistapi.api.v1.orgs.psks.deleteOrgPsk(
                    self.apisession, self.scope_id, psk_id
                )
            else:
                response = mistapi.api.v1.sites.psks.listSitePsks(
                    self.apisession, self.scope_id, psk_id
                )
            return response.data

    def create_ppsk(self, user, dry_run: bool = False):
        print(" Creating the PPSK for user ".ljust(79, "."), end="", flush=True)
        psk = self._get_random_alphanumeric_string()
        psk_data = {
            "usage": "multi",
            "name": user["name"],
            "ssid": self.ssid,
            "vlan_id": self.psk_vlan,
            "passphrase": psk,
            "max_usage": self.psk_max_usage,
        }
        try:
            LOGGER.debug(f"creating psk for user {user['name']}")
            if dry_run:
                res = psk_data
                res["id"] = 1
                LOGGER.info("dry run mode... I'm not creating the psk")
            else:
                if self.scope == "org":
                    response = mistapi.api.v1.orgs.psks.createOrgPsk(
                        self.apisession, self.scope_id, psk_data
                    )
                else:
                    response = mistapi.api.v1.sites.psks.createSitePsk(
                        self.apisession, self.scope_id, psk_data
                    )
            if (
                response.data.get("id")
                and response.data.get("ssid")
                and response.data.get("passphrase")
            ):
                print("\033[92m\u2714\033[0m")
                LOGGER.info(f"psk created")
                return res
            else:
                print("\033[31m\u2716\033[0m")
                LOGGER.error(f"psk not created")
                return None
        except:
            print("\033[31m\u2716\033[0m")
            LOGGER.critical("Exception occurred", exc_info=True)
            return None
