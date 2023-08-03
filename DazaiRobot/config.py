class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    API_ID = 19099900
    API_HASH = "2b445de78e5baf012a0793e60bd4fbf5"

    CASH_API_KEY = "PRPSG4AY3Q3H0QG0"  # Get this value for currency converter from https://www.alphavantage.co/support/#api-key

    DATABASE_URL = "postgres://hsmuekcu:mL-fqMUTRXpd2-i7BTNXlLPM9mS9HtKg@snuffleupagus.db.elephantsql.com/hsmuekcu"  # A sql database url from elephantsql.com

    EVENT_LOGS = MadaraUchihaBotLog)  # Event logs channel to note down important bot level events

    REDIS_URL = "redis://default:Wmy7H43tmBvnieH5QbPdlPSHEFFgLyMS@redis-17894.c257.us-east-1-3.ec2.cloud.redislabs.com:17894" # Get it from redis.com

    MONGO_DB_URI = "mongodb+srv://sonu55:sonu55@cluster0.vqztrvk.mongodb.net/?retryWrites=true&w=majority"  # Get ths value from cloud.mongodb.com

    # Telegraph link of the image which will be shown at start command.
    START_IMG = "https://graph.org/file/60e01e9303094d231be1f.jpg"

    PM_START_IMG = "https://graph.org/file/60e01e9303094d231be1f.jpg"

    SUPPORT_CHAT = "JHBots"  # Your Telegram support group chat username where your users will go and bother you

    TOKEN = "6330964987:AAGGGM2iz-2hTmZLkiigTQgTCHMPePRC6AY"  # Get bot token from @BotFather on Telegram

    TIME_API_KEY = "S3J6EISOC17L"  # Get this value from https://timezonedb.com/api

    OWNER_ID = "6198858059"  # User id of your telegram account (Must be integer)

    # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
