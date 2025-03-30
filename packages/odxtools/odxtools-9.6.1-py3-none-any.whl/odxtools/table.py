# SPDX-License-Identifier: MIT
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from xml.etree import ElementTree

from .admindata import AdminData
from .dataobjectproperty import DataObjectProperty
from .diagcomm import DiagComm
from .element import IdentifiableElement
from .exceptions import odxassert, odxrequire
from .nameditemlist import NamedItemList
from .odxlink import OdxDocFragment, OdxLinkDatabase, OdxLinkId, OdxLinkRef, resolve_snref
from .snrefcontext import SnRefContext
from .specialdatagroup import SpecialDataGroup
from .tablerow import TableRow
from .utils import dataclass_fields_asdict


@dataclass
class TableDiagCommConnector:
    semantic: str

    diag_comm_ref: Optional[OdxLinkRef]
    diag_comm_snref: Optional[str]

    @property
    def diag_comm(self) -> DiagComm:
        return self._diag_comm

    @staticmethod
    def from_et(et_element: ElementTree.Element,
                doc_frags: List[OdxDocFragment]) -> "TableDiagCommConnector":

        semantic = odxrequire(et_element.findtext("SEMANTIC"))

        diag_comm_ref = OdxLinkRef.from_et(et_element.find("DIAG-COMM-REF"), doc_frags)
        diag_comm_snref = None
        if (dc_snref_elem := et_element.find("DIAG-COMM-SNREF")) is not None:
            diag_comm_snref = odxrequire(dc_snref_elem.get("SHORT-NAME"))

        return TableDiagCommConnector(
            semantic=semantic, diag_comm_ref=diag_comm_ref, diag_comm_snref=diag_comm_snref)

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        return {}

    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:
        if self.diag_comm_ref is not None:
            self._diag_comm = odxlinks.resolve(self.diag_comm_ref, DiagComm)

    def _resolve_snrefs(self, context: SnRefContext) -> None:
        if self.diag_comm_snref is not None:
            dl = odxrequire(context.diag_layer)
            self._diag_comm = resolve_snref(self.diag_comm_snref, dl.diag_comms, DiagComm)


@dataclass
class Table(IdentifiableElement):
    """This class represents a TABLE."""
    key_label: Optional[str]
    struct_label: Optional[str]
    admin_data: Optional[AdminData]
    key_dop_ref: Optional[OdxLinkRef]
    table_rows_raw: List[Union[TableRow, OdxLinkRef]]
    table_diag_comm_connectors: List[TableDiagCommConnector]
    sdgs: List[SpecialDataGroup]
    semantic: Optional[str]

    @property
    def key_dop(self) -> Optional[DataObjectProperty]:
        """The key data object property associated with this table."""
        return self._key_dop

    @property
    def table_rows(self) -> NamedItemList[TableRow]:
        """The table rows (both local and referenced) in this table."""
        return self._table_rows

    @staticmethod
    def from_et(et_element: ElementTree.Element, doc_frags: List[OdxDocFragment]) -> "Table":
        """Reads a TABLE."""
        kwargs = dataclass_fields_asdict(IdentifiableElement.from_et(et_element, doc_frags))
        odx_id = kwargs["odx_id"]
        key_label = et_element.findtext("KEY-LABEL")
        struct_label = et_element.findtext("STRUCT-LABEL")
        admin_data = AdminData.from_et(et_element.find("ADMIN-DATA"), doc_frags)
        key_dop_ref = OdxLinkRef.from_et(et_element.find("KEY-DOP-REF"), doc_frags)

        table_rows_raw: List[Union[OdxLinkRef, TableRow]] = []
        for sub_elem in et_element:
            if sub_elem.tag == "TABLE-ROW":
                table_rows_raw.append(
                    TableRow.tablerow_from_et(
                        sub_elem, doc_frags, table_ref=OdxLinkRef.from_id(odx_id)))
            elif sub_elem.tag == "TABLE-ROW-REF":
                table_rows_raw.append(OdxLinkRef.from_et(sub_elem, doc_frags))

        table_diag_comm_connectors = [
            TableDiagCommConnector.from_et(dcc_elem, doc_frags) for dcc_elem in et_element.iterfind(
                "TABLE-DIAG-COMM-CONNECTORS/TABLE-DIAG-COMM-CONNECTOR")
        ]
        sdgs = [
            SpecialDataGroup.from_et(sdge, doc_frags) for sdge in et_element.iterfind("SDGS/SDG")
        ]
        semantic = et_element.get("SEMANTIC")

        return Table(
            key_label=key_label,
            struct_label=struct_label,
            admin_data=admin_data,
            key_dop_ref=key_dop_ref,
            table_rows_raw=table_rows_raw,
            table_diag_comm_connectors=table_diag_comm_connectors,
            sdgs=sdgs,
            semantic=semantic,
            **kwargs)

    def _build_odxlinks(self) -> Dict[OdxLinkId, Any]:
        result = {self.odx_id: self}

        for table_row_wrapper in self.table_rows_raw:
            if isinstance(table_row_wrapper, TableRow):
                result.update(table_row_wrapper._build_odxlinks())

        for dcc in self.table_diag_comm_connectors:
            result.update(dcc._build_odxlinks())

        for sdg in self.sdgs:
            result.update(sdg._build_odxlinks())

        return result

    def _resolve_odxlinks(self, odxlinks: OdxLinkDatabase) -> None:
        self._key_dop: Optional[DataObjectProperty] = None
        if self.key_dop_ref is not None:
            self._key_dop = odxlinks.resolve(self.key_dop_ref, DataObjectProperty)

        table_rows = []
        for table_row_wrapper in self.table_rows_raw:
            if isinstance(table_row_wrapper, TableRow):
                table_row = table_row_wrapper
                table_row._resolve_odxlinks(odxlinks)
            else:
                odxassert(isinstance(table_row_wrapper, OdxLinkRef))
                table_row = odxlinks.resolve(table_row_wrapper, TableRow)

            table_rows.append(table_row)

        self._table_rows = NamedItemList(table_rows)

        for dcc in self.table_diag_comm_connectors:
            dcc._resolve_odxlinks(odxlinks)

        for sdg in self.sdgs:
            sdg._resolve_odxlinks(odxlinks)

    def _resolve_snrefs(self, context: SnRefContext) -> None:
        for table_row_wrapper in self.table_rows_raw:
            if isinstance(table_row_wrapper, TableRow):
                table_row_wrapper._resolve_snrefs(context)

        for dcc in self.table_diag_comm_connectors:
            dcc._resolve_snrefs(context)

        for sdg in self.sdgs:
            sdg._resolve_snrefs(context)
