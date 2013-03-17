# Canary Settings

# To customize, either edit this file (will mess with updating, though) or
# put new settings in another file and set the environment variable
# CANARY_SETTINGS to its path.

# Whether or not to be in debug mode
DEBUG = False

# The environment (e.g. QA or Development)
# Don't set this in production
# ENV = "dev"

# The directory in which to store server status
STORE_DIR = "servers"

# The length of time to wait before giving up when connecting to a server
TIMEOUT = 10 # seconds

# Minimum amount of time between checks
TIME_BETWEEN = 60 # seconds

# Allow requests from any origin, essentially bypassing CORS
ALLOW_ALL_ORIGINS = False

# Allowed CORS Origins
CORS_ALLOWED = []
