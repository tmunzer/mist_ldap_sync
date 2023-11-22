# Mist LDAP Sync
 This is Python script to automatically create/delete Mist PPSK for user in AD/LDAP/LDAPS Group.

## MIT LICENSE
 
Copyright (c) 2021 Thomas Munzer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the  Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## How it works?
1. The script will retrieve all the LDAP/AD users that belong to a specific user group. It will only query for username and email attributes
2. The script will retrieve all the Mist Site or Org PPSK created for the configured SSID
3. The script will look for
  * PPSKs not tied to any users from the AD/LDAP. If any, it will delete the PPSK
  * Users without PPSK. If any it will create the PPSK.

<div>
<img src="https://github.com/tmunzer/mist_ldap_sync/raw/main/._readme/img/generate.png" width="45%">
</div>
 
4. If configured, the script will send the new PPSK to each user

<div>
<img src="https://github.com/tmunzer/mist_ldap_sync/raw/main/._readme/img/user.png" width="45%">
</div>

5. If configured, the script will send a report with created/deleted PPSK to the administrator(s)

<div>
<img src="https://github.com/tmunzer/mist_ldap_sync/raw/main/._readme/img/report.png" width="45%">
</div>


## How to use it?
1. Just install the dependencies manually or with the `requirements.txt` file. For example with `pîp -r requirements.txt`.
2. Then configure the `config.py` file.
3. And to finish start the script with `python mist_ldap_sync.py` or `python3 mist_ldap_sync.py` depending on your system

##  Curent Limitation
- If you have multiple sites, the script must be run for each site

## Configuration
### Script settings
Check the `example.env` file to know how to configure the script. You will have to create a `.env` file with the required settings.

By default, the script is looking for the `.env` file in its own directory. You can also pass the `.env` file location when running the script with the `-e` option (i.e. `python3 mist_psk_rotate.py -e <path to the env file>`).

You can use the `-c` option to check your configuration.

<div>
<img src="https://github.com/tmunzer/mist_ldap_sync/raw/main/._readme/img/check.png" width="50%">
</div>

### CONFIGURATION VARIABLES
| Variable Name | Type | Default Value | Comment |
| ------------- | ---- | ------------- | ------- |
|LDAP_HOST | string | | Required. LDAP/AD FQDN or IP Address |
|LDAP_PORT | integer | False | 389 | LDAP/AD Port |
|LDAP_USE_SSL | boolean | False | False | |
|LDAP_TLS | string | False | None | |
|LDAP_BIND_USER | string | | Required. User used to query LDAP/AD |
|LDAP_BIND_PASSWORD | string | | User Password used to query LDAP/AD |
|LDAP_BASE_DN | string | | Required. Query Base DN |
|LDAP_SEARCH_GROUP | string | | Used to limit query to users belonging to specific LDAP/AD group |
|LDAP_RECURSIVE_SEARCH | boolean | False | Set to True to enable recursive group search in LDAP/AD |
|LDAP_USER_NAME | string | "userPrincipalName" | LDAP field used to name the PSK |
|LDAP_USER_EMAIL | string | "mail" | LDAP field used to send the PSK by email |
|MIST_HOST | string | | Required. Mist host (e.g: "api.mist.com", "api.eu.mist.com") | 
|MIST_API_TOKEN | string | | Required. Mist API Token (need write access to create the PSKs) |
|MIST_SCOPE | string | | Required. Scope where to create the PSKs: "orgs" or "sites" |
|MIST_SCOPE_ID | string | | Required. org_id or site_id where to create the PSKs |
|MIST_SSID | string | | Required. SSID name used to create the PSKs |
|MIST_PSK_LENGTH | integer | 12 | PSK length |
|MIST_PSK_VLAN | integer |  | PSK VLAN (The VLAN must be allowed in the WLAN configuration) |
|MIST_PSK_EMAIL | boolean | False | If the PSK must be sent by Mist. This will automatically set `SMTP_EMAIL_PSK_TO_USERS` to `False` |
|MIST_PSK_MAX_USAGE | integer | 0 | Required. Sets Max devices active per PSK, set to 0 for Unlimited |
|MIST_PSK_ALLOWED_CHARS | string | "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789" | Allowed characters in the PSK |
|MIST_PSK_EXCLUDED | array | | Name of the PSKs to exclude from the automated process |
|SMTP_ENABLED | boolean | False | |
|SMTP_HOST | string | | Required if SMTP_ENABLED. SMTP Server FQDN or IP Address |
|SMTP_PORT | integer | 465 | SMTP Server Port |
|SMTP_USE_SSL | boolean | True | To use SMTPS / START-TLS |
|SMTP_USERNAME | string | | SMTP Username |
|SMTP_PASSWORD | string | | SMTP Password |
|SMTP_FROM_NAME | string | "Wi-Fi Access" | |
|SMTP_FROM_EMAIL | string | | |
|SMTP_EMAIL_PSK_TO_USERS | boolean | True | To automatically send email to newly created users |
|SMTP_LOGO_URL | string | "https://cdn.mist.com/wp-content/uploads/logo.png" | Email Logo |
|SMTP_ENABLE_QRCODE | boolean | True | To include configuration QRCode in the email |
|SMTP_REPORT_ENABLED | boolean | False | To send a report by email about the newly created / deleted PSKs |
|SMTP_REPORT_RECEIVERS | array | | Required if SMTP_REPORT_ENABLED. Email addresses that will receive the report |



### Email template
**Any change in the `psk_template.html` is at your own risks!**

If you want to customize the email sent to the users, you can modify the `psk_template.html` file. It's basicaly a HTML file, but:
- Be sure to use double curly brackets "{{" and "}}" instead of single curly brackets for HTML
- The script will inject 3 information in the template:
  - `{0}` will be replaced by the logo image location. It must be published on a web server and reachable by the users' devices
  - `{1}` will be replaced by the user name
  - `{2}` will be replaced by the SSID name
  - `{3}` wll be replaced by the PPSK value
  - If QRcode is enabled, `{4}` wll be replaced by the QRCode information (i.e. "You can also scan the QRCode below to configure your device:")
  - If QRcode is enabled, `{5}` wll be replaced by the QRCode
