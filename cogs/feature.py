import logging
import platform
import time
from typing import Optional
from discord import app_commands

import discord
import psutil
from discord.ext import commands
#from paginator import Paginator, Page, NavigationType
from utils.paginator import Paginator
import sqlite3

log = logging.getLogger(__name__)


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.paginator = Paginator(bot)
    
    @app_commands.command(description="Create a new pool. Specify name, description, message shown to new members, and size of this group", name="createpool")

    async def createpool(self, ctx, *, name: str, description: str, message: str, limit: int):
        cursor = self.bot.db.cursor()
        
        # Execute the INSERT statement
        cursor.execute("INSERT INTO pools (owner_id, name, description, join_message, limit) VALUES (?, ?, ?, ?, ?)",
                       (ctx.user.id, name, description, join_message, limit))
        # Commit the changes and close the connection
        self.bot.db.commit()
        self.bot.db.close()
        await ctx.response.send_message("Pool created successfully!")
    
    @app_commands.command(description="Join a pool", name="joinpool")
    async def joinpool(self, ctx, *, id: int):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT * FROM pools WHERE id = ?", (id,))
        pool = cursor.fetchone()
        if pool is None:
            await ctx.response.send_message("Pool not found!")
        else:
            cursor.execute("SELECT * FROM members WHERE pool_id = ? AND user_id = ?", (id, ctx.user.id))
            member = cursor.fetchone()
            if member is not None:
                await ctx.response.send_message("You are already in this pool!")
            else:
                cursor.execute("SELECT COUNT(*) FROM members WHERE pool_id = ?", (id,))
                count = cursor.fetchone()[0]
                if count >= pool[5]:
                    await ctx.response.send_message("This pool is full!")
                else:
                    cursor.execute("INSERT INTO members (pool_id, user_id) VALUES (?, ?)", (id, ctx.user.id))
            
            # Commit the changes and close the connection
            
            self.bot.db.commit()
            self.bot.db.close()
            await ctx.response.send_message("Joined pool successfully!")
            # send the pool's join message to the member
            await ctx.user.send(pool[4])
    
    @app_commands.command(description="Leave a pool", name="leavepool")
    async def leavepool(self, ctx, *, id: int):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT * FROM pools WHERE id = ?", (id,))
        pool = cursor.fetchone()
        if pool is None:
            await ctx.response.send_message("Pool not found!")
        else:
            cursor.execute("SELECT * FROM members WHERE pool_id = ? AND user_id = ?", (id, ctx.user.id))
            member = cursor.fetchone()
            if member is None:
                await ctx.response.send_message("You are not in this pool!")
            else:
                cursor.execute("DELETE FROM members WHERE pool_id = ? AND user_id = ?", (id, ctx.user.id))
            
            # Commit the changes and close the connection
            
            self.bot.db.commit()
            self.bot.db.close()
            await ctx.response.send_message("Left pool successfully!")

    @app_commands.command(description="List all pools", name="listpools")
    async def listpools(self, ctx):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT * FROM pools")
        pools = cursor.fetchall()
        if pools is None:
            await ctx.response.send_message("No pools found!")
        else:
            for pool in pools:
                await ctx.response.send_message(f"{pool[0]}: {pool[1]}")
        
        # Commit the changes and close the connection
    
        self.bot.db.commit()
    
    @app_commands.command(description="List all members in a pool", name="listmembers")
    async def listmembers(self, ctx, *, id: int):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT * FROM pools WHERE id = ?", (id,))
        pool = cursor.fetchone()
        if pool is None:
            await ctx.response.send_message("Pool not found!")
        else:
            cursor.execute("SELECT * FROM members WHERE pool_id = ?", (id,))
            members = cursor.fetchall()
            if members is None:
                await ctx.response.send_message("No members found!")
            else:
                res=""
                for member in members:
                    res+=member+"\n"
                
                await ctx.response.send_message(res)
        
        # Commit the changes and close the connection
    
        self.bot.db.commit()
        self.bot.db.close()

    @app_commands.command(description="Delete a pool", name="deletepool")
    async def deletepool(self, ctx, *, id: int):
        # check if the user is the owner of the pool
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT * FROM pools WHERE id = ?", (id,))
        pool = cursor.fetchone()
        if pool is None:
            await ctx.response.send_message("Pool not found!")
        else:
            if pool[1] != ctx.user.id:
                await ctx.response.send_message("You are not the owner of this pool!")
            else:
                cursor.execute("DELETE FROM pools WHERE id = ?", (id,))
                cursor.execute("DELETE FROM members WHERE pool_id = ?", (id,))

            
            # Commit the changes and close the connection
            
            self.bot.db.commit()
            self.bot.db.close()
            await ctx.response.send_message("Pool deleted successfully!")

    @app_commands.command(description="Search for a pool", name="searchpool")
    async def searchpool(self, ctx, *, name: str):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT * FROM pools WHERE name LIKE %?%", (name,))
        pools = cursor.fetchall()
        if pools is None:
            await ctx.response.send_message("No pools found!")
        else:
            for pool in pools:
                await ctx.response.send_message(f"{pool[0]}: {pool[1]}")
        
        # Commit the changes and close the connection
    
        self.bot.db.commit()

    @app_commands.command(description="Edit a pool", name="editpool")
    async def editpool(self, ctx, *, id: int, name: str, description: str, message: str, limit: int):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT * FROM pools WHERE id = ?", (id,))
        pool = cursor.fetchone()
        if pool is None:
            await ctx.response.send_message("Pool not found!")
        else:
            if pool[1] != ctx.user.id:
                await ctx.response.send_message("You are not the owner of this pool!")
            else:
                cursor.execute("UPDATE pools SET name = ?, description = ?, join_message = ?, limit = ? WHERE id = ?", (name, description, message, limit, id))
            
            # Commit the changes and close the connection
            
            self.bot.db.commit()
            self.bot.db.close()
            await ctx.response.send_message("Pool updated successfully!")


    @app_commands.command(description="Get info about a pool", name="poolinfo")
    async def poolinfo(self, ctx, *, id: int):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT * FROM pools WHERE id = ?", (id,))
        pool = cursor.fetchone()
        if pool is None:
            await ctx.response.send_message("Pool not found!")
        else:
            await ctx.response.send_message(f"Name: {pool[1]}\nDescription: {pool[2]}\nJoin message: {pool[3]}\nLimit: {pool[4]}")
    
    @app_commands.command(description="Get info about a user", name="userinfo")
    async def userinfo(self, ctx, *, id: int):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT * FROM members WHERE user_id = ?", (id,))
        member = cursor.fetchone()
        if member is None:
            await ctx.response.send_message("Member not found!")
        else:
            await ctx.response.send_message(f"Pool ID: {member[1]}")

    

    

    
    
    
    
    




    async def setup(bot):
        await bot.add_cog(Core(bot))

