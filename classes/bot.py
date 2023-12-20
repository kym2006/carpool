import datetime
import logging
import sys
import traceback
from pathlib import Path
from discord.ext import commands
import json 
import config
from utils import tools
import sqlite3

log = logging.getLogger(__name__)
class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs: object) -> object:
        super().__init__(**kwargs)
        self.help_command = None
        self.start_time = datetime.datetime.utcnow()
        self.version = "1.0.0"

    @property
    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time

    @property
    def config(self):
        return config

    @property
    def tools(self):
        return tools

    @property
    def primary_colour(self):
        return self.config.primary_colour

    @property
    def success_colour(self):
        return self.config.success_colour

    @property
    def error_colour(self):
        return self.config.error_colour

    @property
    def down_commands(self):
        return self.config.down_commands
    
    all_prefix = {}
    cooldown = {}

    async def start_bot(self):
        self.db = sqlite3.connect("data.db")
        query = """
            CREATE TABLE IF NOT EXISTS pools (
                id INTEGER PRIMARY KEY,
                owner_id BIGINT,
                name TEXT,
                description TEXT,
                join_message TEXT,
                limit INTEGER
            )
            """
        self.db.execute(query)
        self.db.commit()

        query = """
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                pool_id INTEGER,
                user_id BIGINT,
                FOREIGN KEY (pool_id) REFERENCES pools (id)
            )
            """
        self.db.execute(query)
        self.db.commit()

        for extension in self.config.initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception:
                log.error(f"Failed to load extension {extension}.")
                log.error(traceback.print_exc())

        await self.start(self.config.token)
        




        
