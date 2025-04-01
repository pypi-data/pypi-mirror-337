import time
import threading
from PySide6.QtCore import QRunnable, QObject, Signal
from dvatioff_audio.waapi.waapi_utils import get_wwise_profiler_capture_log, unsubscribe_wwise_profiler_capture_log
import queue



class CaptureWwiseProfilerLogWorkerSignals(QObject):
    finished = Signal(bool)


class CaptureWwiseProfilerLogWorker(QRunnable):
    def __init__(self, waapi_client, events_unplayed, events_played, events_error):
        super().__init__()
        self.signals = CaptureWwiseProfilerLogWorkerSignals()
        self.waapi_client = waapi_client
        self.events_unplayed = events_unplayed
        self.events_played = events_played
        self.events_error = events_error
        self.stop_requested = False
        self.handler = None

    def run(self):
        events_queue = queue.Queue()
        def worker():
            self.handler = get_wwise_profiler_capture_log(self.waapi_client, events_queue)
        worker_thread = threading.Thread(target=worker)
        worker_thread.start()

        while True:
            if self.stop_requested:
                break
            try:
                new_event, severity, _time = events_queue.get_nowait()
                if new_event in self.events_unplayed:
                    if severity == "Error":
                        self.events_error.append((new_event, _time))
                        self.events_unplayed.remove(new_event)
                        self.signals.finished.emit(False)
                    elif severity == "Normal":
                        self.events_played.append((new_event, _time))
                        self.events_unplayed.remove(new_event)
                        self.signals.finished.emit(False)
                if not self.events_unplayed:
                    self.signals.finished.emit(True)
                    break
            except queue.Empty:
                pass
            time.sleep(0.05)

    def stop(self):
        self.stop_requested = True
        if self.handler:
            unsubscribe_wwise_profiler_capture_log(self.waapi_client, self.handler)