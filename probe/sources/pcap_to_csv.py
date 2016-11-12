import yaml
import sys
import os
import os.path
import logging
import logging.config
import glob

from inotify.adapters import Inotify

from pcap_to_csv_pool import PcapToCsvPool

class PcapToCsv:
    def __init__(self, process_number, fields, input_directory, output_directory, user=None):
        self._pcap_to_csv_pool = PcapToCsvPool(process_number, fields, output_directory, user)
        self._inotify = i = Inotify()
        self._inotify.add_watch(input_directory.encode("utf8"))
        self._log = logging.getLogger("PcapToCsv")

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
                watch_path = watch_path.decode("utf8")
                filename = filename.decode("utf8")

                if "IN_CREATE" in type_names and filename.endswith(".pcap"):
                    path = os.path.join(watch_path, "*.pcap")
                    files = sorted(glob.glob(path))[0:-1]
                    for pcap_file in files:
                        if not pcap_file.endswith(filename):
                            self._pcap_to_csv_pool.put(pcap_file)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        configuration = yaml.load(f)

    logging.config.dictConfig(configuration["logging_process"])

    c = configuration["process"]
    pcap_to_csv = PcapToCsv(c["process_number"], c["fields"], c["input_directory"], c["output_directory"], c.get("user"))
    pcap_to_csv.run()
