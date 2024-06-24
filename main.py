from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message

from pytgcalls import filters as fl
from pytgcalls import idle
from pytgcalls import PyTgCalls
from pytgcalls.types import ChatUpdate
from pytgcalls.types import GroupCallParticipant
from pytgcalls.types import MediaStream
from pytgcalls.types import Update, GroupCallConfig,AudioQuality
from pytgcalls.types.raw import AudioParameters, AudioStream
# from ffmpeg import FFmpeg
# from pydub import AudioSegment


app = Client(
    'py-tgcalls',
    api_id=21780550,
    api_hash='4681de5092af6855ac444e1c059b4873',
)

call_py = PyTgCalls(app)

video_file = 'https://cdn1.suno.ai/b556f7bc-ca86-4047-b561-f74cdc1f44b1.mp3'
# video_file = 'sample.mkv'
# video_file = 'audio.mp3'
# video_file = 'result.wav'
# video_file = 'result.webm'
# video_file = 'result.opus'
# video_file = 'http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4'

print("hey")
@app.on_message(filters.regex('!play'))
async def play_handler(_: Client, message: Message):
    await call_py.play(
        -1002066055214,
        MediaStream(
            video_file,
            audio_parameters= AudioParameters(bitrate=48000),
            audio_flags=MediaStream.Flags.NO_LATENCY,
            video_flags=MediaStream.Flags.IGNORE,
        ),
        config= GroupCallConfig(auto_start=False)
    )

@app.on_message(filters.regex('!cache'))
async def cache_handler(_: Client, _m: Message):
    print(call_py.cache_peer)


@app.on_message(filters.regex('!ping'))
async def ping_handler(_: Client, _m: Message):
    print(call_py.ping)


@app.on_message(filters.regex('!pause'))
async def pause_handler(_: Client, message: Message):
    await call_py.pause_stream(
        message.chat.id,
    )


@app.on_message(filters.regex('!resume'))
async def resume_handler(_: Client, message: Message):
    await call_py.resume_stream(
        message.chat.id,
    )


@app.on_message(filters.regex('!stop'))
async def stop_handler(_: Client, message: Message):
    await call_py.leave_call(
        message.chat.id,
    )


@app.on_message(filters.regex('!change_volume'))
async def change_volume_handler(_: Client, message: Message):
    await call_py.change_volume_call(
        message.chat.id,
        50,
    )


@app.on_message(filters.regex('!status'))
async def get_play_status(client: Client, message: Message):
    await client.send_message(
        message.chat.id,
        f'Current seconds {call_py.played_time(message.chat.id)}',
    )

@call_py.on_update(
    fl.chat_update(
        ChatUpdate.Status.KICKED | ChatUpdate.Status.LEFT_GROUP,
    ),
)
async def kicked_handler(_: PyTgCalls, update: Update):
    print(f'Kicked from {update.chat_id} or left')


@call_py.on_update(fl.stream_end)
async def stream_end_handler(_: PyTgCalls, update: Update):
    print(f'Stream ended in {update.chat_id}', update)


@call_py.on_update(
    fl.call_participant(GroupCallParticipant.Action.JOINED),
)
async def participant_handler(_: PyTgCalls, update: Update):
    print(f'Participant joined in {update.chat_id}', update)


@call_py.on_update()
async def all_updates(_: PyTgCalls, update: Update):
    print(update)

call_py.start()
idle()