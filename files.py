FILES={
    "infos":".infos.json",
    ".env":".env",
    ".priv_env":".priv_env"
}

def fget(name):
    return FILES.get(name,None)