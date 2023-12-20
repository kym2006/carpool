# Bot Info
import os

from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")
if "testing" in os.environ:
    token = os.getenv("TEST_TOKEN")

# Additional shards to launch
additional_shards = 0

# The default prefix for commands
default_prefix = "?"

# Permissions to eval
owners = [
    298661966086668290
]

# Bot admins that have access to admin commands
admins = [
    298661966086668290,
    412969691276115968,
    685456111259615252,
]

# Channels to send logs
join_channel = 1186923494882156631
event_channel = 1186923494882156632
admin_channel = 1186923494466932810

# This is where patron roles are at
main_server = 725303414220914758

# Patron roles for premium servers
patron1 = 725303414220914763
patron2 = 725303414220914764
patron3 = 725303414220914765

# The colour used in embeds
primary_colour = 0x8125DA
success_colour = 0x00FF00
error_colour = 0xFF0000

initial_extensions = [
    "cogs.admin",
    "cogs.owner",
    "cogs.configuration",
    "cogs.error_handler",
    "cogs.events",
    "cogs.general",
    "cogs.feature",
]


down_commands=[

]
