import subprocess
import sys
import time


def start_api():

    print("🚀 Starting API...")

    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000"
        ]
    )


def start_bot():

    print("🤖 Starting Bot...")

    return subprocess.Popen(
        [
            sys.executable,
            "bot.py"
        ]
    )


if __name__ == "__main__":

    api = start_api()

    time.sleep(3)

    bot = start_bot()


    print("\n✅ API + BOT Started")


    try:

        api.wait()
        bot.wait()


    except KeyboardInterrupt:

        print("\n⛔ Stopping services...")

        api.terminate()
        bot.terminate()