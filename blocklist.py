"""
This file just contains the blocklist of the JWT tokens. It will be imported by app and the logout resource
 so that tokens can be added to the blocklist when the user logs out. 
"""

BLOCKLIST=set()  # Use Redis for good performance because this set will be erased and the app restarts. 