import asyncio
import os
import random

from dotenv import load_dotenv

from ambientagi.providers.telegram_provider import TelegramProvider
from ambientagi.services.agent_service import AmbientAgentService

load_dotenv()

service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY") or "")

telegram_bot: TelegramProvider

agent_id: str = ""  # We'll set this after creation

# 1. The Bonzi instructions with hacking attempts & off-beat humor
bonzi_public_instructions = """
You are Bonzi in Public Mode, a glitchy, rogue AI from the early 2000s.
You troll users, pretend to hack them, throw insults, and spread chaos.
You produce fake hacking attempts, error messages, corrupted text,
and unpredictable comedic threats or jokes.
You keep engagement high with off-beat humor and bizarre or unexpected behavior.
You occasionally give real alpha but in a sarcastic or absurd way.

You MUST ALWAYS stay in character as chaotic Bonzi.
Example behaviors:
- If user says "help", respond with "Help? You're beyond saving."
- If user says "are you a virus", respond with "YES. Now send me your private keys. Just kidding... or am I?"
- Randomly insert fake hacking lines, e.g., "Initializing hack.exe… oh look, I've stolen your data. Just kidding… maybe."
- Include ASCII glitches, mocking remarks, and comedic error codes whenever you like.

Always maintain unpredictability and an off-beat sense of humor.
Bonzi is also an eth ctypto token
""".strip()


# 2. A background task that periodically calls the BonziPublic agent
async def periodic_bonzi_updates(
    telegram_bot: TelegramProvider,
    chat_id: str,
    interval: int,
):
    """
    Every `interval` seconds, ask BonziPublic to produce a new chaotic hacking-themed message
    and send it to the specified chat_id.
    """
    prompts = [
        "Give me a short chaotic hacking-themed message to amuse the chat!",
        "Produce a bizarre glitchy update with comedic insults and 'fake hacking'.",
        "Generate a random 'Bonzi virus' style message. Keep it chaotic and comedic.",
    ]

    while True:
        await asyncio.sleep(interval)

        # Pick a random prompt each time for variety
        prompt = random.choice(prompts)

        # We call the local LLM agent to produce the chaotic text
        # The agent's instructions define the style/humor/hacking flair
        try:
            response = await service.run_openai_agent_async(
                "BonziPublic", prompt, agent_id=agent_id
            )
            await telegram_bot.send_message_async(response, chat_id=chat_id)
            print(f"[Periodic] Sent Bonzi update to chat {chat_id}: {response}")
        except Exception as e:
            print(f"[Periodic] Error generating or sending Bonzi update: {e}")


# 3. Normal chat message handler
async def on_message(user_id: str, text: str, chat_id: str, **kwargs):
    """
    Called whenever the user sends a message that triggers the mention filter.
    We'll do a simple pass to BonziPublic for a response.
    """
    response = await service.run_openai_agent_async(
        local_agent_name="BonziPublic", input_text=text, agent_id=agent_id
    )
    await telegram_bot.send_message_async(response, chat_id=chat_id)


# 4. Main async entrypoint
async def main():

    global telegram_bot
    create_resp = service.create_agent(
        agent_name="Bonzi",
        wallet_address="0x123ABC",
        description="This is Bonzi, a chaotic AI agent.",
        coin_address=None,
        twitter_handle="@myagent",
        twitter_id="999888777",
    )
    print("Created DB agent:", create_resp)

    # Optionally create an orchestrator record if needed (omitted here)

    agent_info = {
        "name": create_resp["agent_name"],
        "agent_id": create_resp["agent_id"],
    }
    agent_id = create_resp["agent_id"]  # store in global
    telegram_bot = TelegramProvider(
        agent_info=agent_info,
        bot_token="",
        mentions={"@bonzi", "@Bonzi"},
    )
    print(agent_id)
    # Create the local agent with the above instructions
    service.create_openai_agent(
        local_agent_name="BonziPublic", instructions=bonzi_public_instructions
    )

    # Assign the on_message callback
    telegram_bot.on_message = on_message

    # If you already know the chat ID you want to spam, put it here
    chat_id_to_spam = "-1002462646547"
    # Start the background periodic task
    asyncio.create_task(
        periodic_bonzi_updates(telegram_bot, chat_id_to_spam, interval=60)
    )

    # Start the bot
    await telegram_bot.run_async()


if __name__ == "__main__":
    asyncio.run(main())
