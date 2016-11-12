import os
import os.path
from datetime import datetime
import time
import logging
from pwd import getpwnam

from tshark import Tshark


class PcapToCsvTask:
    def __init__(self, fields, output_directory, user=None):
        self._tshark = Tshark(fields)
        self._output_directory = output_directory
        self._log = logging.getLogger("PcapToCsvTask")
        self._user = user

    def do(self, input_filename):
        # try to make a subdirectory about the current day, like /xxx/2016-08-10
        now = datetime.now()
        day_directory = "{}-{}-{}".format(now.year, now.month, now.day)
        destination_directory = os.path.join(self._output_directory, day_directory)

        try:
            os.mkdir(destination_directory)
            self._log.info("directory {} created".format(destination_directory))
        except:
            self._log.debug("directory {} not created".format(destination_directory))

        # making the convertion
        output = self._tshark.check_output(input_filename)
        self._log.debug("conversion of {} done".format(input_filename))
        timestamp = int(round(time.time() * 1000))
        csv_filename = os.path.join(destination_directory, "{}.csv".format(timestamp))

        # writing the csv file
        with open(csv_filename, "w") as f:
            f.write(output)
        # changing the right
        if self._user:
            info = getpwnam(self._user)
            os.chown(csv_filename, info.pw_uid, info.pw_gid)

        self._log.info("csv file {} created".format(csv_filename))
        # removing the source file
        os.remove(input_filename)
        self._log.debug("pcap file {} removed".format(input_filename))

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG)
    pcap_to_csv_task = PcapToCsvTask(["frame.len", "frame.time_epoch", "eth.src", "eth.dst", "ip.src", "ip.dst"], "/tmp")
    pcap_to_csv_task.do(sys.argv[1])
