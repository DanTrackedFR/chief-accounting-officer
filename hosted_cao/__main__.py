"""Host-provisioned configuration; never accept filesystem paths over HTTP."""
import json
import logging
import os
import signal
import threading
from pathlib import Path
from .service import Service, Server

def main():
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    config=json.loads(Path(os.environ['CAO_SERVICE_CONFIG']).read_text())
    service=Service(config['job_root'],config['companies'],config['credentials'])
    service.start_worker()
    server=Server((os.environ.get('CAO_HOST','127.0.0.1'),int(os.environ.get('CAO_PORT','8080'))),service)
    def stop(*_):threading.Thread(target=server.shutdown,daemon=True).start()
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    try:server.serve_forever(poll_interval=.1)
    finally:server.server_close();service.close()

if __name__=='__main__':main()
