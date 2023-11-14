"""
-------------------------------------------------------------------------------

    Written by Thomas Munzer (tmunzer@juniper.net)
    Github repository: https://github.com/tmunzer/mist_ldap_sync/

    This script is licensed under the MIT License.

-------------------------------------------------------------------------------
Script managing the communication with the LDAP/LDAPS server
"""

import logging
import sys
from ldap3 import Server, Connection

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class MistLdap:
    """
    Class managing the requests to the LDAP/LDAPS server
    """

    def __init__(self, config):
        self.host = config.get("host")
        self.port = config.get("port")
        self.use_ssl = config.get("use_ssl")
        self.tls = config.get("tls")
        if self.tls == "None":
            self.tls = None
        self.bind_user = config.get("bind_user")
        self.bind_password = config.get("bind_password")
        self.base_dn = config.get("base_dn")
        self.search_group = config.get("search_group")
        self.recursive_search = config.get("recursive_search")
        self.user_name = config.get("user_name")
        self.user_email = config.get("user_email")
        self.server = Server(
            self.host, port=self.port, use_ssl=self.use_ssl, tls=self.tls
        )

    def get_users(self, ad_user_list: list = None):
        """
        Function to retrieve the list of users.
        It will connect to the server, then do the search
        """
        conn = self._connect()
        entries = self._search(conn)
        ad_user_list = self._process(entries, ad_user_list)
        LOGGER.info(f"processing ldap data finished. got {len(ad_user_list)} users")
        return ad_user_list

    def _connect(self):
        print(
            f"Contacting LDAP server on {self.host}:{self.port} "
            "(SSL: {self.use_ssl}) ".ljust(79, "."),
            end="",
            flush=True,
        )
        LOGGER.info(
            f"Contacting LDAP server on {self.host}:{self.port} (SSL: {self.use_ssl})"
        )
        try:
            conn = Connection(
                self.server,
                self.bind_user,
                self.bind_password,
                auto_bind=True,
                read_only=True,
                auto_range=True,
            )
            print("\033[92m\u2714\033[0m")
            LOGGER.info("Connected")
            return conn
        except:
            print("\033[31m\u2716\033[0m")
            LOGGER.critical("Exception occurred", exc_info=True)
            sys.exit(1)

    def _search(self, conn: Connection):
        print("Executing LDAP search ".ljust(79, "."), end="", flush=True)
        LOGGER.info("Executing LDAP search")
        entries = []

        try:
            if self.recursive_search:
                entry_generator = conn.extend.standard.paged_search(
                search_base = self.base_dn,
                search_filter = f"(&(objectclass=person)(memberOf:1.2.840.113556.1.4.1941:={self.search_group}))",
                attributes=[self.user_name, self.user_email, "objectClass"],
                paged_size = 1000
                )
            else:
                entry_generator = conn.extend.standard.paged_search(
                search_base = self.base_dn,
                search_filter = f"(&(objectclass=person)(memberOf={self.search_group}))",
                attributes=[self.user_name, self.user_email, "objectClass"],
                paged_size = 1000
                )


            for entry in entry_generator:
                if "attributes" in entry:
                    entries.append({'dn':entry['dn'], 'attributes': entry['attributes']})
            print("\033[92m\u2714\033[0m")
            LOGGER.info(f"Done: {len(entries)} entries")
            return entries
        except:
            print("\033[31m\u2716\033[0m")
            LOGGER.critical("Exception occurred", exc_info=True)
            sys.exit(1)

    def _process(self, entries: list, ad_user_list:list):
        if not ad_user_list:
            ad_user_list = []
        print("Processing LDAP accounts ".ljust(79, "."), end="", flush=True)
        try:
            for entry in entries:
                LOGGER.debug(f"_process:{entry}")
                if (
                    not "computer" in entry['attributes'].get("objectClass")
                    and self.user_name in entry['attributes']
                ):
                    user = {
                    "name" : str(entry['attributes'][self.user_name])
                    }
                    if self.user_email in entry:
                        user["email"] = str(entry['attributes'][self.user_email])
                    else:
                        user["email"] = ""
                    LOGGER.debug(f"_process:user from LDAP: {user}")
                    ad_user_list.append(user)
            print("\033[92m\u2714\033[0m")
            return ad_user_list
        except:
            print("\033[31m\u2716\033[0m")
            LOGGER.critical("Exception occurred", exc_info=True)
            sys.exit(1)
