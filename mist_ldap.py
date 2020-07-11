from ldap3 import Server, Connection, ALL

def _load_conf(conf_obj, conf_val, conf_type):
    if conf_val in conf_obj: return conf_obj[conf_val]
    else: 
        print("Unable to load {0} \"{1}\" from the configuration file.. Exiting...".format(conf_type, conf_val))
        exit(1)
        
class Mist_LDAP():
    def __init__(self, config):
        self.host = _load_conf(config.ldap, "host", "LDAP")
        self.port = _load_conf(config.ldap, "port", "LDAP")
        self.use_ssl = _load_conf(config.ldap, "use_ssl", "LDAP")
        self.tls = _load_conf(config.ldap, "tls", "LDAP")
        self.bind_user= _load_conf(config.ldap, "bind_user", "LDAP")
        self.bind_password= _load_conf(config.ldap, "bind_password", "LDAP")
        self.base_dn= _load_conf(config.ldap, "base_dn", "LDAP")
        self.search_group= _load_conf(config.ldap, "search_group", "LDAP")
        self.user_name= _load_conf(config.ldap, "user_name", "LDAP")
        self.user_email= _load_conf(config.ldap, "user_email", "LDAP")
        self.server = Server(self.host, port=self.port, use_ssl=self.use_ssl,tls=self.tls)


    def get_users(self, ad_user_list=[]):
        conn = self._connect()
        conn = self._search(conn)
        ad_user_list = self._process(conn, ad_user_list)
        return ad_user_list

    def _connect(self):
        print("Contacting LDAP server on {0}:{1} (SSL: {2}) ".format(self.host, self.port, self.use_ssl).ljust(79, "."), end="", flush=True)
        try:
            conn = Connection(self.server, self.bind_user, self.bind_password, auto_bind=True, read_only=True)
            print("\033[92m\u2714\033[0m")
            return conn
        except:
            print('\033[31m\u2716\033[0m')
            exit(1)


    def _search(self, conn):
        print("Executing LDAP search ".ljust(79, "."), end="", flush=True)
        try:
            conn.search(
                self.base_dn, 
                "(&(objectclass=person)(memberOf={0}))".format(self.search_group), 
                attributes=[self.user_name, self.user_email, "objectClass"]
                )
            print("\033[92m\u2714\033[0m")
            return conn
        except:
            print('\033[31m\u2716\033[0m')
            exit(1)
    

    def _process(self, conn, ad_user_list):
        print("Processing LDAP accounts ".ljust(79, "."), end="", flush=True)
        try:
            for entry in conn.entries:
                if not "computer" in entry.objectClass:
                    name = str(entry.__getattribute__(self.user_name))
                    email = str(entry.__getattribute__(self.user_email))
                    ad_user_list.append({"name": name, "email": email})
            print("\033[92m\u2714\033[0m")
            return ad_user_list  
        except:
            print('\033[31m\u2716\033[0m')
            exit(1)
        
