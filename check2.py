from time import sleep, perf_counter
from threading import Thread
class Stock(Thread):
    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol
    def run(self):
        sleep(1)


start_time = perf_counter()

symbols = ['MSFT', 'GOOGL', 'AAPL', 'META']
threads = []

for symbol in symbols:
    t = Stock(symbol)
    threads.append(t)    
    t.start()

symbols = ['MSFT', 'GOOGL', 'AAPL', 'META']
threads = []

for symbol in symbols:
    t = Stock(symbol)
    threads.append(t)    
    t.start()
    print(t)

for t in threads:
    print(t)
    t.join()
    print(t)


end_time = perf_counter()

