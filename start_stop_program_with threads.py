import threading
import logging
import signal

thread_list = []

def foo() -> None:
	print('im foo()')

def stop() -> None:
	for thread in thread_list:
		thread['event'].set()
		thread['thread'].join()
		
def wrap(f, stop) -> None:
	while not stop.is_set():
		f()

def start() -> None:
	event = threading.Event()
	thread = threading.Thread(target=wrap, args=(foo, event))
	thread_list.append({'thread': thread, 'event': event})
	thread.start()

def signal_handler(sig, frame) -> None:
		print('Caught signal: %s', sig)
		stop()
		logging.info("Program successfully terminated")
		print("Good bye!")

def run() -> None:
	signal.signal(signal.SIGCHLD, signal_handler)
	signal.signal(signal.SIGUSR1, signal_handler)
	signal.signal(signal.SIGUSR2, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGQUIT, signal_handler)
	signal.signal(signal.SIGPIPE, signal_handler)
	start()

if __name__ == "__main__":
	run()
