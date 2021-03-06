# Copyright 2015 Intel Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Automation of QEMU hypervisor for launching vhost-cuse enabled guests.
"""

import logging

from conf import settings as S
from vnfs.qemu.qemu import IVnfQemu

class QemuDpdkVhostCuse(IVnfQemu):
    """
    Control an instance of QEMU with vHost cuse guest communication.
    """
    def __init__(self):
        """
        Initialisation function.
        """
        super(QemuDpdkVhostCuse, self).__init__()
        self._logger = logging.getLogger(__name__)

        # calculate indexes of guest devices (e.g. charx, dpdkvhostuserx)
        i = self._number * 2
        if1 = str(i)
        if2 = str(i + 1)
        net1 = 'net' + str(i + 1)
        net2 = 'net' + str(i + 2)

        self._cmd += ['-netdev',
                      'type=tap,id=' + net1 + ',script=no,downscript=no,' +
                      'ifname=dpdkvhostcuse' + if1 + ',vhost=on',
                      '-device',
                      'virtio-net-pci,mac=' +
                      S.getValue('GUEST_NET1_MAC')[self._number] +
                      ',netdev=' + net1 + ',csum=off,gso=off,' +
                      'guest_tso4=off,guest_tso6=off,guest_ecn=off',
                      '-netdev',
                      'type=tap,id=' + net2 +
                      ',script=no,downscript=no,' +
                      'ifname=dpdkvhostcuse' + if2 + ',vhost=on',
                      '-device',
                      'virtio-net-pci,mac=' +
                      S.getValue('GUEST_NET2_MAC')[self._number] +
                      ',netdev=' + net2 + ',csum=off,gso=off,' +
                      'guest_tso4=off,guest_tso6=off,guest_ecn=off',
                     ]

    # helper functions

    def _modify_dpdk_makefile(self):
        """
        Modifies DPDK makefile in Guest before compilation
        """
        self.execute_and_wait("sed -i -e 's/CONFIG_RTE_LIBRTE_VHOST_USER=n/" +
                              "CONFIG_RTE_LIBRTE_VHOST_USER=y/g'" +
                              "config/common_linuxapp")
