from __future__ import annotations

import logging
import os
from functools import cached_property
from typing import TYPE_CHECKING

from cloudshell.snmp.autoload.generic_snmp_autoload import GenericSNMPAutoload

from cloudshell.paloalto.autoload.panos_if_table import PANOSIfTable
from cloudshell.paloalto.autoload.panos_snmp_system_info import PanOSSNMPSystemInfo

if TYPE_CHECKING:
    from cloudshell.snmp.autoload.services.system_info_table import SnmpSystemInfo

logger = logging.getLogger(__name__)


class PanOSGenericSNMPAutoload(GenericSNMPAutoload):
    def __init__(self, snmp_handler, resource_model):
        super().__init__(snmp_handler, logger, resource_model)
        self.load_mibs(os.path.abspath(os.path.join(os.path.dirname(__file__), "mibs")))

    @cached_property
    def system_info_service(self) -> SnmpSystemInfo:
        return PanOSSNMPSystemInfo(self.snmp_handler, logger)

    @property
    def port_table_service(self) -> PANOSIfTable:
        if not self._port_table_service:
            self._port_table_service = PANOSIfTable(
                resource_model=self._resource_model,
                ports_snmp_table=self.port_snmp_table,
                logger=self.logger,
            )
        return self._port_table_service
