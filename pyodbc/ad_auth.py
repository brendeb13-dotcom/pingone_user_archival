import os
from ldap3 import Server, Connection, ALL, NTLM, Tls
import ssl
import traceback

# --- Active Directory Configuration ---
# These values will need to be set as environment variables in your production environment
# and in your crontab file for the automated jobs.
# For now, they are placeholders.
AD_SERVER_ADDRESS = os.environ.get("AD_SERVER", "your_ad_server.example.com")
AD_SERVER_PORT = int(os.environ.get("AD_PORT", 636)) # 636 is for LDAPS (secure)
AD_USE_TLS = AD_SERVER_PORT == 636

# --- Service Account for Binding and Searching ---
# This is a read-only account that the application uses to connect to AD.
AD_BIND_USER = os.environ.get("AD_BIND_USER", "CN=ServiceAccount,OU=Services,DC=example,DC=com")
AD_BIND_PASSWORD = os.environ.get("AD_BIND_PASSWORD", "ServiceAccountPassword")

# --- Search Configuration ---
# The base path to start searching for users.
AD_USER_SEARCH_BASE = os.environ.get("AD_USER_SEARCH_BASE", "OU=Users,DC=example,DC=com")
# The attribute that holds the username for login (e.g., sAMAccountName, userPrincipalName)
AD_USER_LOGIN_ATTRIBUTE = "sAMAccountName"


def authenticate_ad_user(username: str, password: str) -> dict | None:
    """
    Authenticates a user against Active Directory and fetches their group memberships.

    Args:
        username: The user's login name (e.g., sAMAccountName).
        password: The user's password.

    Returns:
        A dictionary containing user details and groups if authentication is successful,
        otherwise None.
    """
    if not password:
        # AD does not allow empty passwords.
        return None

    try:
        # --- Define the AD Server ---
        # Use TLS for a secure connection if the port is 636
        tls_config = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2) if AD_USE_TLS else None
        server = Server(AD_SERVER_ADDRESS, port=AD_SERVER_PORT, use_ssl=AD_USE_TLS, tls=tls_config, get_info=ALL)

        # --- Find the User's Full Distinguished Name (DN) ---
        # First, connect using the service account to find the user.
        with Connection(server, user=AD_BIND_USER, password=AD_BIND_PASSWORD, auto_bind=True) as conn:
            search_filter = f"({AD_USER_LOGIN_ATTRIBUTE}={username})"
            conn.search(
                search_base=AD_USER_SEARCH_BASE,
                search_filter=search_filter,
                attributes=['distinguishedName'] # We only need the user's DN
            )

            if not conn.entries:
                print(f"AD Auth: User '{username}' not found.")
                return None
            
            user_dn = conn.entries[0].distinguishedName.value

        # --- Authenticate the User ---
        # Now, try to connect (bind) as the actual user with their password.
        # This is the actual authentication step.
        with Connection(server, user=user_dn, password=password, auto_bind=True) as user_conn:
            print(f"AD Auth: Successfully authenticated user '{username}'.")
            
            # --- Fetch User's Groups ---
            # If authentication is successful, search again for the user's details,
            # this time requesting the 'memberOf' attribute.
            user_conn.search(
                search_base=AD_USER_SEARCH_BASE,
                search_filter=search_filter,
                attributes=['displayName', 'mail', 'memberOf']
            )
            
            user_entry = user_conn.entries[0]
            
            # --- Clean up Group Names ---
            # The 'memberOf' attribute returns a list of full DNs for each group.
            # We'll extract just the common name (CN) for simplicity.
            groups = []
            for group_dn in user_entry.memberOf.values:
                # Example group_dn: "CN=App_CSV_Uploaders,OU=Groups,DC=example,DC=com"
                # We just want "App_CSV_Uploaders"
                cn_part = group_dn.split(',')[0]
                group_name = cn_part.split('=')[1]
                groups.append(group_name)

            return {
                "username": username,
                "display_name": user_entry.displayName.value if 'displayName' in user_entry else username,
                "email": user_entry.mail.value if 'mail' in user_entry else None,
                "groups": groups
            }

    except Exception as e:
        print("--- AD Authentication Error ---")
        print(f"An error occurred during AD authentication for user '{username}'.")
        traceback.print_exc()
        print("--- End AD Authentication Error ---")
        return None

