from time import time


class Clock:
    def __init__(self) -> None:
        self.start_time = time()
    
    def stop(self) -> None:
        print(f"[TIME] {time() - self.start_time}")