# makefile to manage dpdk package
#

# Copyright 2015 OPNFV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Contributors:
#   Aihua Li, Huawei Technologies.

include ../mk/master.mk
include ../package-list.mk

.PHONY: install force_make

ifndef VHOST_USER
    VHOST_USER = n
endif
WORK_DIR = dpdk
TAG_DONE_FLAG = $(WORK_DIR)/.$(DPDK_TAG).tag.done
DPDK_VANILLA = ../../src_vanilla/dpdk
DPDK_CUSE = ../../src_cuse/dpdk

# the name has been changed from version to version
ifeq ($(DPDK_TAG),v1.6.0r0)
    DPDK_TARGET = x86_64-default-linuxapp-gcc
    CONFIG_FILE = $(WORK_DIR)/config/defconfig_x86_64-default-linuxapp-gcc
else
    DPDK_TARGET = x86_64-native-linuxapp-gcc
    CONFIG_FILE = $(WORK_DIR)/config/common_linuxapp
endif

all: force_make
	@echo "Finished making $(WORK_DIR) "

INSTALL_TARGET = force_make

# modify CONFIG_FILE to enable VHOST_USER build and restore original CONFIG_FILE after the build
force_make: $(TAG_DONE_FLAG)
	$(AT)cd $(WORK_DIR) && git pull $(DPDK_URL) $(DPDK_TAG)
	$(AT)sed -i -e 's/CONFIG_RTE_LIBRTE_VHOST_USER=.\+/CONFIG_RTE_LIBRTE_VHOST_USER=$(VHOST_USER)/g' $(CONFIG_FILE)
	$(AT)sed -i -e 's/CONFIG_RTE_BUILD_COMBINE_LIBS=./CONFIG_RTE_BUILD_COMBINE_LIBS=y/g' $(CONFIG_FILE)
	$(AT)sed -i -e 's/CONFIG_RTE_LIBRTE_VHOST=./CONFIG_RTE_LIBRTE_VHOST=y/g' $(CONFIG_FILE)
	$(AT)sed -i -e 's/CONFIG_RTE_LIBRTE_KNI=./CONFIG_RTE_LIBRTE_KNI=n/g' $(CONFIG_FILE)
	$(AT)cd $(WORK_DIR); make install T=$(DPDK_TARGET) -j
	$(AT)cd `dirname $(CONFIG_FILE)` && git checkout `basename $(CONFIG_FILE)` && cd -
	$(AT)echo "VHOST_USER = $(VHOST_USER)"
ifeq ($(VHOST_USER),n)
	$(AT)cd $(WORK_DIR)/lib/librte_vhost/eventfd_link; make
endif
	@echo "Make done"

install: $(INSTALL_TARGET)
	$(AT)sudo cp -a $(WORK_DIR)/$(DPDK_TARGET)/kmod $(INSTALL_DIR)/lib/modules/$(KERNEL_VERSION)
	@echo "install done"

# hard way to clean and clobber
clean:
	$(AT)cd $(WORK_DIR) && git clean -xfd *.o
clobber:
	$(AT)rm -rf $(WORK_DIR)
	$(AT)rm -rf $(DPDK_VANILLA)
	$(AT)rm -rf $(DPDK_CUSE)

# distclean is for developer who would like to keep the
# clone git repo, saving time to fetch again from url
distclean:
	$(AT)cd $(WORK_DIR) && git clean -xfd && git checkout -f

test:
	@echo "Make test in $(WORK_DIR) (stub) "

sanity:
	@echo "Make sanity in $(WORK_DIR) (stub) "

$(WORK_DIR):
	$(AT)git clone $(DPDK_URL)
	$(AT)mkdir -p $(DPDK_VANILLA)
	$(AT)cp -rf ./* $(DPDK_VANILLA)
	$(AT)mkdir -p $(DPDK_CUSE)
	$(AT)cp -rf ./* $(DPDK_CUSE)

$(TAG_DONE_FLAG): $(WORK_DIR)
	$(AT)cd $(WORK_DIR); git checkout $(DPDK_TAG)
	$(AT)touch $@
