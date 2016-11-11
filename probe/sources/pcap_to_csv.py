import yaml
import sys
import os.path
import logging

from inotify.adapters import Inotify

from pcap_to_csv_pool import PcapToCsvPool

class PcapToCsv:
    def __init__(self, process_number, fields, input_directory, output_directory):
        self._pcap_to_csv_pool = PcapToCsvPool(process_number, fields, output_directory)
        self._inotify = i = Inotify(input_directory)
        self._inotify.add_watch(input_directory.encode("utf8"))
        self._log = logging.getLogger("PcapToCsv")

    def run(self):
        self._pcap_to_csv_pool.run()

        for event in self._inotify.event_gen():
            if event is not None :
                (header, type_names, watch_path, filename) = event
                if "CLOSE" in type_names:
                    path = os.path.join(watch_path, filename)
                    self._log.info("push "+path)
                    self._pcap_to_csv_pool.put(path)

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        configuration = yaml.load(f)

    c = configuration["process"]
    pcap_to_csv = PcapToCsv(c["process_number"], c["fields"], c["input_directory"], c["output_directory"])
