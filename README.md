# NebulaBot

**NebulaBot** is a moderation/helper bot to make moderation *fancier* and *easier* by adding multiple **functionalities** such as **commands** like /announce and more!

---

## **1.** Installation

### Requirements:
- **Python**
    - **Python Lib requirements** :
        - **discord.py**
        `pip install requirements.txt`

### 1. Clone the repository

```bash
git clone https://github.com/ombre77/NebulaBot.git
```
Or **download** the **zip** file and extract it.

### 2. Setup the bot

In the `.env` file, replace the following values:
- `BOT_ID=your_bot_token_here` > replace *`your_bot_token_here`* with your discord bot token.
- `GUILD_IDS=your_guilds_ids_here` > replace *`your_guilds_ids_here`* with you discord guild ids (if you only have to put one, just put it and if you have multiple, separate them by a comma and **NO SPACES**)
---

## **2.** Launch
Open a terminal in the **NebulaBot** folder then type `python .` and let the file running. (You can of course **host** it on host site like **discloud** or **railway**).

---

## **3.** Features
### Commands
- " **/announce [title] [message] ([color])** " send a pretty announcement
- " **/setversion [new_version]** " set the new version
- " **/setname [new_name]** " set the new version name