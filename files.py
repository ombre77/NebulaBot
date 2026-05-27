FILES={
    "infos":".infos.json",
    ".env":".env",
    ".priv_env":".priv_env",
    "projects":"./projects.json"
}

def fget(name):
    return FILES.get(name,None)