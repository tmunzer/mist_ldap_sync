from ldap3 import Server, Connection, ALL
        
class Mist_LDAP():
    def __init__(self, config):    
        self.host = config["host"]
        self.port = config["port"]
        self.use_ssl = config["use_ssl"]
        self.tls = config["tls"]
        if self.tls == "None": self.tls = None
        self.bind_user= config["bind_user"]
        self.bind_password= config["bind_password"]
        self.base_dn= config["base_dn"]
        self.search_group= config["search_group"]
        self.user_name= config["user_name"]
        self.user_email= config["user_email"]
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
                if not "computer" in entry.objectClass and entry.__getattribute__(self.user_name):
                    name = str(entry.__getattribute__(self.user_name))
                    email = str(entry.__getattribute__(self.user_email))
                    ad_user_list.append({"name": name, "email": email})
            print("\033[92m\u2714\033[0m")
            return ad_user_list  
        except:
            print('\033[31m\u2716\033[0m')
            exit(1)
        
