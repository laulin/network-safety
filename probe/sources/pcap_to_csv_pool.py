import multiprocessing
import logging

from pcap_to_csv_task import PcapToCsvTask

class PcapToCsvPool:
    def __init__(self, process_number, fields, output_directory):
        self._pool = None
        self._queue = multiprocessing.Queue()
        self._process_number = process_number
        self._pcap_to_csv_task = PcapToCsvTask(fields, output_directory)
        self._log = logging.getLogger("PcapToCsvPool")

    def task(self, queue):
        while True:
            file_name = queue.get()
            try:
                self._pcap_to_csv_task.do(file_name)
                self._log.info("finished conversion on " + file_name)
            except Exception as e:
                self._log.debug(e)

    def run(self):
        self._pool = multiprocessing.Pool(self._process_number, self.task,(self._queue,))


    def put(self, input_filename):
        self._log.info("request conversion on " + file_name)
        self._queue.put(input_filename)

if __name__ == "__main__":
    import sys
    import glob
    import time

    pcap_to_csv_pool = PcapToCsvPool(4, ["frame.len", "frame.time_epoch", "eth.src", "eth.dst", "ip.src", "ip.dst"], "/tmp")
    pcap_to_csv_pool.run()

    for x in glob.glob(sys.argv[1]):
        print("ask for " + x)
        pcap_to_csv_pool.put(x)

    while True:
        time.sleep(1)
