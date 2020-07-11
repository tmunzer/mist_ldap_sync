ldap = {
    "host" : "ldap.domain.local",    
    "port": 389,
    "use_ssl": False,
    "tls": None,
    "bind_user": "administrator@domain.local",
    "bind_password": "secret",
    "base_dn": "DC=domain,DC=local",
    "search_group" : "CN=Wi-Fi Group,OU=Users,DC=domain,DC=local",
    "user_name" : "userPrincipalName",
    "user_email" : "mail"
}

mist = {
    "host": "api.mist.com",
    "apitoken": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "site_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "ssid": "ssid_name",
    "psk_length": 10
}

smtp = {
    "host": "smtp.domain.local",
    "port": 25,
    "use_ssl": False,
    "username": "user@domain.local",
    "password": "secret",
    "from_name": "Wi-Fi Access",
    "from_email": "wi-fi@domain.local",
    "logo_url": "https://cdn.mist.com/wp-content/uploads/logo.png",
    "email_psk_to_users": True,
    "report_enabled": True,
    "report_receivers": ["administrator@domain.local"]
}