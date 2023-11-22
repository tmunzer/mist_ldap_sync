"""
-------------------------------------------------------------------------------

    Written by Thomas Munzer (tmunzer@juniper.net)
    Github repository: https://github.com/tmunzer/mist_ldap_sync/

    This script is licensed under the MIT License.

-------------------------------------------------------------------------------
Script managing the communication with the Mist Cloud
"""
import random
import logging
import sys
import mistapi

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Mist:
    """
    Class managing the requests to the Mist Cloud
    """
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

    def get_users(self, mist_user_list:list=[]):
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
        if self.scope == "orgs":
            response = mistapi.api.v1.orgs.psks.listOrgPsks(
                self.apisession, self.scope_id, ssid=self.ssid, limit=1000
            )
        else:
            response = mistapi.api.v1.sites.psks.listSitePsks(
                self.apisession, self.scope_id, ssid=self.ssid,limit=1000
            )
        data = mistapi.get_all(self.apisession, response)
        return data

    def delete_ppsk(self, psk_id, dry_run: bool = False):
        LOGGER.debug(f"deleting psk with id {psk_id}")
        if dry_run:
            LOGGER.info("dry run mode... I'm not deleting the psk")
            return True
        else:
            if self.scope == "orgs":
                response = mistapi.api.v1.orgs.psks.deleteOrgPsk(
                    self.apisession, self.scope_id, psk_id
                ).data
            else:
                response = mistapi.api.v1.sites.psks.listSitePsks(
                    self.apisession, self.scope_id, psk_id
                ).data
            return response

    def create_ppsk(self, user, dry_run: bool = False):
        print(" Creating the PPSK for user ".ljust(79, "."), end="", flush=True)
        psk = self._get_random_alphanumeric_string()
        psk_data = {
            "usage": "multi",
            "name": user["name"],
            "email": user.get("email"),
            "ssid": self.ssid,
            "vlan_id": self.psk_vlan,
            "passphrase": psk,
            "max_usage": self.psk_max_usage,
        }
        try:
            LOGGER.debug(f"creating psk for user {user['name']}")
            if dry_run:
                response = psk_data                
                response["id"] = 1
                LOGGER.info("dry run mode... I'm not creating the psk")
            else:
                if self.scope == "orgs":
                    response = mistapi.api.v1.orgs.psks.createOrgPsk(
                        self.apisession, self.scope_id, psk_data
                    ).data
                else:
                    response = mistapi.api.v1.sites.psks.createSitePsk(
                        self.apisession, self.scope_id, psk_data
                    ).data

            LOGGER.debug(response)
            if (
                response.get("id")
                and response.get("ssid")
                and response.get("passphrase")
            ):
                print("\033[92m\u2714\033[0m")
                LOGGER.info(f"psk created")
                return response
            else:
                print("\033[31m\u2716\033[0m")
                LOGGER.error(f"psk not created")
                return None
        except:
            print("\033[31m\u2716\033[0m")
            LOGGER.critical("Exception occurred", exc_info=True)
            return None

    def create_ppsk_bulk(self, users, dry_run: bool = False):
        if dry_run:
            dry_run_string = "DRY RUN - "
        else:
            dry_run_string = ""
        stop_index = len(users)
        run = 0
        batch_size = 100
        while run * batch_size < stop_index:
            user_names = []
            run += 1
            start = (run - 1) * batch_size
            stop = run * batch_size
            psks_to_create = users[ start : stop ]
            psks_data = []
            print()
            print(
                    f" {dry_run_string}BATCH {start} "
                    f"to {stop} ".center(79, "-")
                )
            for user in psks_to_create:
                LOGGER.debug(
                        f"create_ppsk_bulk:create_ppsk_bulk:"
                        f"creating psk for user {user['name']}"
                    )
                passphrase = self._get_random_alphanumeric_string()
                psk = {
                    "usage": "multi",
                    "name": user["name"],
                    "ssid": self.ssid,
                    "vlan_id": self.psk_vlan,
                    "passphrase": passphrase,
                    "max_usage": self.psk_max_usage,
                }
                psks_data.append(psk)
                user_names.append(user["name"])
            try:
                print(
                        f"sending request for psk batch "
                        f"{start} to {stop} "
                        .ljust(79, "."), end="", flush=True
                    )
                LOGGER.debug(
                        f"create_ppsk_bulk:sending request for psk batch "
                        f"{start} to {stop}"
                )
                if dry_run:
                    response = {"updated":[],"errors":[]}
                    LOGGER.info("create_ppsk_bulk:dry run mode... I'm not creating the psks")
                else:
                    if self.scope == "orgs":
                        response = mistapi.api.v1.orgs.psks.importOrgPsks(
                            self.apisession, self.scope_id, psks_data
                        ).data
                    else:
                        response = mistapi.api.v1.sites.psks.importSitePsks(
                            self.apisession, self.scope_id, psks_data
                        ).data
                print("\033[92m\u2714\033[0m")
                LOGGER.debug(response)
                for error in response.get("errors", []):
                    LOGGER.error(f"create_ppsk_bulk:{error}")
                for user in users:
                    if user["name"] in user_names:
                        print(
                                f"Checking PPSK creation for user {user['name']} "
                                .ljust(79, "."), end="", flush=True
                            )
                        if user["name"] in response["updated"]:
                            user["psk_added"] = True
                            print("\033[92m\u2714\033[0m")
                            LOGGER.info(f"create_ppsk_bulk:psk {user['name']} created")
                        else:
                            print("\033[31m\u2716\033[0m")
                            LOGGER.error(f"create_ppsk_bulk:psk {user['name']} not created")
                            LOGGER.error("Exception occurred", exc_info=True)

            except:
                print("\033[31m\u2716\033[0m")
                LOGGER.critical("Exception occurred", exc_info=True)

        return users
