import eel
import threading
import sys
from app import app

eel.init('templates')

def run_flask():
    app.run(host='localhost', port=8001, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    try:
        eel.start('index.html', size=(1000, 800), mode='chrome')
    except (SystemExit, MemoryError, KeyboardInterrupt):
        print("Fechando o aplicativo.")

    sys.exit()
