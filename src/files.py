FILES={
    "infos":"./json/.infos.json",
    ".env":"./env/.env",
    ".priv_env":"./env/.priv_env"
}

def fget(name):
    return FILES.get(name,None)