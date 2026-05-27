import discord
from discord.ext import commands
from discord import app_commands
import json
import time

class Message:
    def __init__(self,title:str,color:discord.Color,desc:str=None):
        self.title=title
        self.color=color
        self.desc=desc

        self.embed=discord.Embed(
            title=self.title,
            color=self.color,
            description=self.desc
        )
        self.footer("developed by Odysseus :3")
    
    def add_category(self,name:str,content:str,inline=True,bold=False):
        if bold:
            content=f"**{content}**"
        self.embed.add_field(name=name,value=content,inline=inline)

    def footer(self,content:str):
        self.embed.set_footer(text=content)

    def render(self):
        return self.embed

class JSON_map:
    def __init__(self,path:str):
        self.path=path
        self.map={}
    
    def load(self):
        with open(self.path,"r") as f:
            file=json.load(f)
        self.map=file.get("map")

class Json_set:
    path=""
    @classmethod
    def set(cls,key,value):
        file=JSON_map(cls.path)
        file.load()
        file.map[key]=value
        new_content={"map":file.map}
        with open(cls.path,"w") as f:
            json.dump(new_content,f)

class LogCommand:
    @classmethod
    def log(cls, name: str, user: str):
        now = time.localtime()

        day = now.tm_mday
        month = now.tm_mon         
        year = now.tm_year % 100  
        hour = now.tm_hour         
        minute = now.tm_min 
        second = now.tm_sec 

        print(f"[{day:02}/{month:02}/{year:02} {hour:02}:{minute:02}:{second:02}] User {user} issued command '{name}'")

class MessageHelper:
    default_ops=["|[-Owner-]|","[-Mod-]"]

    @staticmethod
    async def role_check(interaction: discord.Interaction, role: str | list[str] = "[-Mod-]"):
        user_roles = [r.name for r in interaction.user.roles]

        if isinstance(role, str):
            role = [role,]

        has_permission = any(r in user_roles for r in role)

        if not has_permission:
            await interaction.response.send_message(
                "You do not have the permission required to execute this",
                ephemeral=True
            )
            return False

        return True
    
    @staticmethod
    def version():
        file=JSON_map("./.infos.json")
        file.load()
        map=file.map
        return map["version"]
    
    @staticmethod
    def gamename():
        file=JSON_map("./.infos.json")
        file.load()
        map=file.map
        return map["name"]