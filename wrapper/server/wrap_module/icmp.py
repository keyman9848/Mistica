#
# Copyright (c) 2020 Carlos Fernández Sánchez and Raúl Caro Teixidó.
#
# This file is part of Mística 
# (see https://github.com/IncideDigital/Mistica).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from sotp.misticathread import ServerWrapper
from base64 import urlsafe_b64encode,urlsafe_b64decode
from wrapper.server.wrap_server.icmpserver import icmpserver

class icmpwrapper(ServerWrapper):
    
    SERVER_CLASS = icmpserver
    NAME = "icmp"
    CONFIG = {
                "prog": "icmp",
                "wrapserver": "icmpserver",
                "description": "Encodes/Decodes data in ICMP echo requests/responses on data section",
                "args": [
                    {
                        "--max-size": {
                            "help": "Max size of the SOTP packet. Default is 1024 bytes",
                            "nargs": 1,
                            "default": [1024],
                            "type":  int
                        },
                        "--max-retries": {
                            "help": "Maximum number of re-synchronization retries.",
                            "nargs": 1,
                            "default": [5],
                            "type":  int
                        }
                    }
                ]
            }

    def __init__(self, id, qsotp, args, logger):
        ServerWrapper.__init__(self, id, icmpwrapper.NAME, qsotp, icmpwrapper.SERVER_CLASS.NAME, args, logger)
        # Base args
        self.max_size = None
        self.max_retries = None
        # Parsing args
        self.argparser = self.generateArgParser()
        self.parseArguments(args)
        # Logger parameters
        self.logger = logger
        self._LOGGING_ = False if logger is None else True

    def parseArguments(self, args):
        parsed = self.argparser.parse_args(args.split())
        self.max_size = parsed.max_size[0]
        self.max_retries = parsed.max_retries[0]

    def unpackSotp(self, data):
        try:
            # We use base64_urlsafe_encode, change if you encode different.
            return urlsafe_b64decode(data)
        except Exception as e:
            self.logger.exception(f"[{self.name}] Exception at unpackSotp: {e}")
            return

    def unwrap(self, content):
        self._LOGGING_ and self.logger.debug_all(f"[{self.name}] unwrap data: {content}")
        return self.unpackSotp(content)

    def wrap(self, content):
        self._LOGGING_ and self.logger.debug_all(f"[{self.name}] wrap data: {content}")
        urlSafeEncodedBytes = urlsafe_b64encode(content)
        return urlSafeEncodedBytes
