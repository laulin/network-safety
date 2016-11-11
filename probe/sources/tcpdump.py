import logging
import subprocess


class Tcpdump:
    def __init__(self, interface, buffer_size, pcap_size, pcap_timeout, output_filename, user, post_process=None):
        self._interface = interface
        self._buffer_size = buffer_size
        self._pcap_size = pcap_size
        self._pcap_timeout = pcap_timeout
        self._output_filename = output_filename
        self._user = user
        self._post_process = post_process

        self._log = logging.getLogger(__name__)

    def make_command(self):
        cmd = ["tcpdump",
                "-pni", self._interface,
                "-B", str(self._buffer_size),
                "-C", str(self._pcap_size),
                "-G", str(self._pcap_timeout),
                "-w", self._output_filename,
                "-Z", self._user]

        if self._post_process:
            cmd += ["-z", self._post_process]

        return cmd

    def popen(self, **kwargs):
        cmd = self.make_command()
        self._log.debug(" ".join(cmd))

        return subprocess.Popen(cmd)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    tcpdump = Tcpdump("enp0s3", 10240, 50, 60, "/tmp/%s.pcap")
    process = tcpdump.popen()
    process.wait()
