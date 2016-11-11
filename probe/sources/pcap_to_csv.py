import yaml
import sys
import os
import os.path
import logging
import glob

from inotify.adapters import Inotify

from pcap_to_csv_pool import PcapToCsvPool

class PcapToCsv:
    def __init__(self, process_number, fields, input_directory, output_directory):
        self._pcap_to_csv_pool = PcapToCsvPool(process_number, fields, output_directory)
        self._inotify = i = Inotify()
        self._inotify.add_watch(input_directory.encode("utf8"))
        self._log = logging.getLogger("PcapToCsv")
        self.process_existing_file(input_directory)

    def process_existing_file(self, input_directory):
        path = os.path.join(input_directory, "*.pcap")
        files = sorted(glob.glob(path))[0:-1]
        for pcap_file in files:
            try:
                self._pcap_to_csv_pool.put(pcap_file)
            except Exception as e:
                self._log.debug("{} raise {}".format(path, e))

    def run(self):
        self._pcap_to_csv_pool.run()

        for event in self._inotify.event_gen():
            if event is not None :
                (header, type_names, watch_path, filename) = event
                self._log.debug("event :  "+ str((type_names, watch_path, filename)))
                if "IN_CLOSE_WRITE" in type_names:
                    path = os.path.join(watch_path, filename)
                    path = path.decode("utf8")
                    self._log.info("push "+path)
                    self._pcap_to_csv_pool.put(path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with open(sys.argv[1]) as f:
        configuration = yaml.load(f)

    c = configuration["process"]
    pcap_to_csv = PcapToCsv(c["process_number"], c["fields"], c["input_directory"], c["output_directory"])
    pcap_to_csv.run()
