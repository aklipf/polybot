import os
import re

TOKEN = os.getenv("DISCORD_TOKEN")
PASSWORD_LENGTH = int(os.getenv("PASSWORD_LENGTH"))

import discord
import emoji

from keysmash.markov import is_keysmash


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

        flitered_message = re.sub(r"http\S+", "", message.content)  # remove url
        flitered_message = emoji.demojize(flitered_message)  # remove unicode emoji
        flitered_message = re.sub(
            r"(<a?)?:\w+:(\d+>)?", "", flitered_message
        )  # remove custom emotes

        if len(flitered_message) >= PASSWORD_LENGTH and is_keysmash(flitered_message):

            password_length = len(flitered_message)

            # Classifying password strength
            if password_length < 8:
                remarks = "⚠️ Very Weak: Easily guessable! Change it immediately."
            elif password_length < 12:
                remarks = "⚠️ Weak: Can be cracked quickly. Use a stronger password."
            elif password_length < 16:
                remarks = "✅ Moderate: Decent password, but can still be improved."
            elif password_length < 20:
                remarks = "✅ Strong: Hard to guess, but consider making it longer."
            else:
                remarks = "✅ Very Strong: Excellent password! Highly secure."

            await message.channel.send(
                f"Bottom password generation detected!\n{remarks}", reference=message
            )

        elif any(
            map(
                lambda file: os.path.splitext(file.filename)[1] in (".png", ".jpg"),
                message.attachments,
            )
        ):
            await message.add_reaction("<:bunny_love:1364348303772483595>")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(TOKEN)
