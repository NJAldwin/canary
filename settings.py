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

# API Key SQLite storage information
DB_DIR = "databases"
APIKEY_DB = "keys.db"

# IP Addresses to allow requests from even if no API key is provided
# Note requests  from these IPs will be treated as if they have a valid API key
# thus they will be allowed in CORS if ALLOW_CORS_WITH_VALID_API_KEY is set
ADDRESSES_IGNORE_API_KEY = []

# Send a CORS allow header if a request is made with a valid API key
ALLOW_CORS_WITH_VALID_API_KEY = True

# CORS Origins which always send the allowed header
CORS_ALLOWED = []
