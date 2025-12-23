from config import settings

def main():
    print("Bot_Token: ", settings.BOT_TOKEN)
    print("Database_URL: ", settings.DATABASE_URL)


if __name__ == "__main__":
    main()