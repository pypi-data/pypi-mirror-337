from typing import List, Optional

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import (
    AnnualAccount,
    AnnualAccountResponse,
    CloseGroup,
    CloseGroupResponse,
    PostingRulesResponse,
    VoucherType,
    VoucherTypeResponse,
)

from .accounting_period import TripletexAccountingPeriod  # noqa F401
from .ledger import TripletexLedger


class TripletexAnnualAccount(TripletexCrud[AnnualAccount]):
    _resource_path = "annualAccount"
    _datamodel = AnnualAccount
    _api_response_model = AnnualAccountResponse
    _parent_resource = TripletexLedger
    _methods = ["list", "read"]

    def search(
        self,
        id: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[AnnualAccount]:
        """
        Find annual accounts corresponding with sent data.

        Args:
            id: List of IDs
            year_from: From and including
            year_to: To and excluding
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of AnnualAccount objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if id:
            params["id"] = id
        if year_from:
            params["yearFrom"] = year_from
        if year_to:
            params["yearTo"] = year_to
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)


class TripletexCloseGroup(TripletexCrud[CloseGroup]):
    _resource_path = "closeGroup"
    _datamodel = CloseGroup
    _api_response_model = CloseGroupResponse
    _parent_resource = TripletexLedger
    _methods = ["list", "read"]

    def search(
        self,
        date_from: str,
        date_to: str,
        id: Optional[str] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[CloseGroup]:
        """
        Find close groups corresponding with sent data.

        Args:
            date_from: From and including
            date_to: To and excluding
            id: List of IDs
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of CloseGroup objects
        """
        params: JSONDict = {"dateFrom": date_from, "dateTo": date_to, "from": from_index, "count": count}

        if id:
            params["id"] = id
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)


class TripletexVoucherType(TripletexCrud[VoucherType]):
    _resource_path = "voucherType"
    _datamodel = VoucherType
    _api_response_model = VoucherTypeResponse
    _parent_resource = TripletexLedger
    _methods = ["list", "read"]

    def search(
        self, name: Optional[str] = None, from_index: int = 0, count: int = 1000, sorting: Optional[str] = None, fields: Optional[str] = None
    ) -> List[VoucherType]:
        """
        Find voucher types corresponding with sent data.

        Args:
            name: Containing
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of VoucherType objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if name:
            params["name"] = name
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)


class TripletexPostingRules(TripletexCrud):
    _resource_path = "postingRules"
    _parent_resource = TripletexLedger
    _methods = ["list"]

    def get(self, fields: Optional[str] = None) -> PostingRulesResponse:
        """
        Get posting rules for current company.

        Args:
            fields: Fields filter pattern

        Returns:
            PostingRules object
        """
        params: JSONDict = {}
        if fields:
            params["fields"] = fields

        return self.custom_action("", method="get", params=params)
