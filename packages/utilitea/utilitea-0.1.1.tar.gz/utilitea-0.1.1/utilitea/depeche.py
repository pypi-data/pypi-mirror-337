import uuid
import threading
import queue
import time
from typing import Callable, Optional

class StatusMessage:
    """Represents a status message."""
    def __init__(self, message: str):
        self.id = uuid.uuid4()  # Unique ID
        self.message = message
        self.stale = False  # Initially set to False
        self.finished = False  # Must be explicitly set

    def mark_stale(self):
        """Mark message as stale."""
        self.stale = True

    def mark_finished_safely(self, status_updater):
        """Mark message as finished only if it's the topmost in the queue, otherwise mark stale."""
        with status_updater.lock:
            if status_updater.active_message == self:
                self.finished = True  # Set finished if this is the active message
            else:
                self.stale = True  # Otherwise, mark as stale

class StatusUpdater:
	"""Handles concurrent message updates using a queue and a user-defined callable."""
	def __init__(self, on_message: Callable[[str], None]):
		"""
		:param on_message: A callable that processes messages.
		"""
		self.message_queue = queue.Queue()
		self.on_message = on_message  # User-defined callable for processing messages
		self.running = threading.Event()
		self.running.set()
		self.active_message: Optional[StatusMessage] = None  # Track the current active message
		self.active_start_time: Optional[float] = None  # Track when a message was activated
		self.lock = threading.Lock()  # Ensure thread safety

		self.consumer_thread = threading.Thread(target=self._consume_messages, daemon=True)
		self.consumer_thread.start()

	def add_message(self, message: str) -> StatusMessage:
		"""Creates and queues a new message."""
		msg = StatusMessage(message)
		self.message_queue.put(msg)
		return msg  # Return reference for potential stale marking

	def _consume_messages(self):
		"""Continuously processes messages from the queue."""
		while self.running.is_set():
			with self.lock:
				if not self.active_message or self.active_message.finished or self.active_message.stale:
					elapsed_time = (time.time() - self.active_start_time) if self.active_start_time else float("inf")

                    # Ensure at least 0.5 seconds has passed before replacing the message
					if elapsed_time >= 0.5:				
						try:
							# Fetch the next message
							self.active_message = self.message_queue.get_nowait()

							if not self.active_message.stale and not self.active_message.finished:
								self.on_message(self.active_message.message)  # Call user-defined function
						except queue.Empty:
							self.on_message("Ready")  # Indicate that the queue is waiting for messages
							time.sleep(1)  # Avoid excessive CPU usage
			time.sleep(0.1)  # Avoid busy-waiting

	def stop(self):
		"""Stops the consumer thread."""
		self.running.clear()
		self.consumer_thread.join()