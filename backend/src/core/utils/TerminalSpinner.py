import sys
import time
import threading
import itertools

class TerminalSpinner:
    """
    A context manager to display a waiting animation in the terminal.
    """
    def __init__(self, message="Downloading..."):
        # Chars of the animation
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.message = message
        self.running = False
        self.thread = None

    def spin(self):
        while self.running:
            sys.stdout.write(f"\r{next(self.spinner)} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
            
        sys.stdout.write(f"\r{' ' * (len(self.message) + 2)}\r")
        sys.stdout.flush()

    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        self.thread.join()
        
        if exc_type is None:
            print(f"✅ {self.message} : Success !")
        else:
            print(f"❌ {self.message} : Failed !")