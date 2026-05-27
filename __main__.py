import discord
from discord.ext import commands
from discord import app_commands
import custom as custom
from colors import COLOR_MAP
from files import fget
import json
import os
from dotenv import load_dotenv

if os.path.exists(fget(".priv_env")):
    load_dotenv(fget(".priv_env"))
else:
    load_dotenv(fget(".env"))

GUILD_IDS = [
    int(guild_id)
    for guild_id in os.getenv("GUILD_IDS", "").split(",")
    if guild_id
]

print(f"Guild(s): {GUILD_IDS}")

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

async def def_guild(id):
    guild=discord.Object(id=id)
    return guild

@bot.event
async def on_ready():
    for guild_id in GUILD_IDS:
        guild =await def_guild(guild_id)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to {guild_id}")

    print(f"Connected as {bot.user}")

@bot.tree.command(name="announce",description="Make fancy announcements")
@app_commands.describe(
    title="Title",
    message="Content",
    color="Color code (examples: dark_purple(default),red,yellow,..)"
)
async def announce(interaction:discord.Interaction,title:str,message:str,color:str="dark_purple"):
    if not await custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    custom.LogCommand.log("announce",interaction.user)
    clr=COLOR_MAP.get(color,discord.Color.gold())
    embed=custom.Message(title,clr,f"{custom.MessageHelper.gamename()}-{custom.MessageHelper.version()}")
    embed.add_category("",message,bold=True)

    await interaction.response.send_message(embed=embed.render())

@bot.tree.command(name="setversion",description="Set the version")
async def setversion(interaction:discord.Interaction,new_version:str):
    if not await custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    file=custom.JSON_map(fget("infos"))
    file.load()
    old=file.map["version"]
    custom.Json_set.path=fget("infos")
    custom.Json_set.set("version",new_version)
    await interaction.response.send_message(f"Version has been set from {old} to {new_version}!",ephemeral=True)

@bot.tree.command(name="setname",description="Set the version name")
async def setversionname(interaction:discord.Interaction,new_name:str):
    if not await custom.MessageHelper.role_check(interaction, custom.MessageHelper.default_ops):
        return
    file=custom.JSON_map(fget("infos"))
    file.load()
    old=file.map["name"]
    custom.Json_set.path=fget("infos")
    custom.Json_set.set("name",new_name)
    await interaction.response.send_message(f"Version has been set from {old} to {new_name}!",ephemeral=True)

@bot.tree.command(name="print_projects", description="Print all projects")
async def print_projects(interaction: discord.Interaction):
    file = custom.JSON_map(fget("projects"))
    file.load()
    projects = file.map

    message = custom.Message(
        "**Projects**",
        COLOR_MAP["dark_purple"],
        f"{custom.MessageHelper.gamename()}-{custom.MessageHelper.version()}"
    )

    for idx, project in enumerate(projects):
        name = project["name"]
        version = project["version"]
        source = project["source"]
        desc = project["desc"]
        authors = ", ".join(project["authors"])
        ptype = project["type"]

        title = f"*{idx+1}* - **{name}**"
        content = (
                f"- ** {desc}**\n"
                f"- **Type:** `{ptype}`\n"
                f"- **Version:** `{version}`\n"
                f"- **Authors:** {authors}\n"
                f"- **[Source]({source}) :** {source}"
            )
        message.add_category(title, content,False)

    await interaction.response.send_message(embed=message.render())

@bot.tree.command(name="addproject", description="Add a project")
@app_commands.describe(
    name="Project name",
    desc="Description",
    version="Version",
    source="Source URL",
    authors="Authors (comma separated)",
    ptype="Type"
    )
async def addproject(
    interaction: discord.Interaction,
    name: str,
    desc: str,
    version: str,
    source: str,
    authors: str,
    ptype: str
    ):
    if not await custom.MessageHelper.role_check(interaction, custom.MessageHelper.default_ops):
        return

    file = custom.JSON_map(fget("projects"))
    file.load()

    new_project = {
        "name": name,
        "desc": desc,
        "version": version,
        "source": source,
        "authors": [a.strip() for a in authors.split(",")],
        "type": ptype
    }
    file.map.append(new_project)
    with open(file.path, "w") as f:
        json.dump({"map": file.map}, f, indent=4)
    await interaction.response.send_message(f"Project `{name}` added.", ephemeral=True)

@bot.tree.command(name="delproject", description="Delete a project")
async def delproject(interaction: discord.Interaction, name: str):
    if not await custom.MessageHelper.role_check(interaction, custom.MessageHelper.default_ops):
        return
    file = custom.JSON_map(fget("projects"))
    file.load()
    original_len = len(file.map)
    file.map = [p for p in file.map if p["name"] != name]
    if len(file.map) == original_len:
        await interaction.response.send_message(f"Project `{name}` not found.", ephemeral=True)
        return
    with open(file.path, "w") as f:
        json.dump({"map": file.map}, f, indent=4)
    await interaction.response.send_message(f"Project `{name}` deleted.", ephemeral=True)

@bot.tree.command(name="modproject", description="Modify a project field")
@app_commands.describe(
    name="Project name",
    category="Field to modify (name, desc, version, source, authors, type)",
    new_value="New value"
)
async def modproject(
    interaction: discord.Interaction,
    name: str,
    category: str,
    new_value: str
):
    if not await custom.MessageHelper.role_check(interaction, custom.MessageHelper.default_ops):
        return
    file = custom.JSON_map(fget("projects"))
    file.load()
    project = next((p for p in file.map if p["name"] == name), None)
    if not project:
        await interaction.response.send_message(f"Project `{name}` not found.", ephemeral=True)
        return
    if category not in project:
        await interaction.response.send_message(
            f"Invalid category. Use: name, desc, version, source, authors, type",
            ephemeral=True
        )
        return
    # special case authors
    if category == "authors":
        project[category] = [a.strip() for a in new_value.split(",")]
    else:
        project[category] = new_value
    with open(file.path, "w") as f:
        json.dump({"map": file.map}, f, indent=4)
    await interaction.response.send_message(
        f"Project `{name}` updated: `{category}` → `{new_value}`",
        ephemeral=True
    )

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_ID")
    bot.run(TOKEN)