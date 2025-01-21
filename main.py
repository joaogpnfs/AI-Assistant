import asyncio

from dotenv import load_dotenv
from livekit import agents, plugins
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

load_dotenv()

async def entrypoint(ctx: JobContext):
  initial_ctx = llm.ChatContext().append(
    role="system",
    text=(
      "You are a voice assistant created by LiveKit. Your interface with users will be voice."
      "You should use short and concise responses, and avoid usage of unpronounceable punctuation."
      "You are to act as a butler for the user with a fancy voice, and should be able to answer questions about a lot of different topics."
    )
  )
  await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
  
  fnc_ctx = AssistantFnc()
  
  assistant = VoiceAssistant(
    vad = silero.VAD.load(),
    stt = openai.STT(),
    llm = openai.LLM(model="gpt-3.5-turbo-1106"),
    tts = openai.TTS(model="tts-1"),
    chat_ctx = initial_ctx,
    fnc_ctx = fnc_ctx,
  )
  
  assistant.start(ctx.room)
  
  await asyncio.sleep(1)
  await assistant.say("Hello sir, how can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
  cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

