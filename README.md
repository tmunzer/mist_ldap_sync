# Mist LDAP Sync
 This is Python script to automatically create/delete Mist PPSK for user in AD/LDAP/LDAPS Group.

## How it works?
1. The script will retrieve all the users belong to a specific group. It will only ask for username and email attributes
2. The script will retrieve all the Mist PPSK for os specific SSID on a specific site
3. The script will look for PPSKs not tied to any users from the AD/LDAP. If any, it will delete the PPSK
4. The script will look for users without PPSK. If any it will create the PPSK. At this point, if the `config.py` file contains the SMTP settings, it will send an email to the user with the PPSK information.
5. If configured, the script will send a report with created/deleted PPSK to the administrator(s)

## How to use it?
1. Just install the dependencies manually or with the `requirements.txt` file. For example with `pîp -r requirements.txt`.
2. Then configure the `config.py` file.
3. And to finish start the script with `python mist_ldap_sync.py` or `python3 mist_ldap_sync.py` depending on your system

##  Curent Limitation
- If you have multiple sites, the script must be run for each site

## Configuration
### Script settings
Check the `config_example.py` file to know how to configure the script. You will have to create a `config.py` file with the required settings 

### Email template
**Any change in the `psk_template.html` is at your own risks!**

If you want to customize the email sent to the users, you can modify the `psk_template.html` file. It's basicaly a HTML file, but:
- Be sure to use double brackets "{{" and "}}" instead of single brackets for HTML
- The script will inject 3 information in the template:
  - `{0}` will be replaced by the logo image location. It must be published on a web server and reachable by the users' devices
  - `{1}` will be replaced by the user name
  - `{2}` will be replaced by the SSID name
  - `{3}` wll be replaced by the PPSK value
 
### ToDo
- store the script logs in a log file
- generate a connection QRcode to add in the emai (this will allow the  automate the users' devices configuration to access the network, just by scanning the QRcode)