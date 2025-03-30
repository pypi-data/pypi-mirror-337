import os

from crudclient import API

from tripletex.core.client import TripletexClient
from tripletex.core.config import TripletexConfig, TripletexTestConfig
from tripletex.endpoints.country.api import TripletexCountries
from tripletex.endpoints.ledger.api import (
    TripletexAccountingPeriod,
    TripletexAnnualAccount,
    TripletexCloseGroup,
    TripletexLedger,
    TripletexPostingRules,
    TripletexVoucherType,
)
from tripletex.endpoints.supplier.api import TripletexSuppliers


class TripletexAPI(API):
    client_class = TripletexClient

    def __init__(
        self,
        client: TripletexClient | None = None,
        client_config: TripletexConfig | TripletexTestConfig | None = None,
        debug: bool | None = None,
        **kwargs
    ) -> None:

        if debug is None:
            debug = os.environ.get("DEBUG", "0") == "1"

        if client:
            super().__init__(client=client)
        elif client_config:
            super().__init__(client_config=client_config)
        elif debug:
            super().__init__(client_config=TripletexTestConfig())
        else:
            super().__init__(client_config=TripletexConfig())

    def _register_endpoints(self):
        self.countries = TripletexCountries(self.client)
        self.suppliers = TripletexSuppliers(self.client)

        # Ledger endpoints
        self.ledger = TripletexLedger(self.client)
        self.ledger.accounting_period = TripletexAccountingPeriod(self.client, parent=self.ledger)
        self.ledger.annual_account = TripletexAnnualAccount(self.client, parent=self.ledger)
        self.ledger.close_group = TripletexCloseGroup(self.client, parent=self.ledger)
        self.ledger.voucher_type = TripletexVoucherType(self.client, parent=self.ledger)
        self.ledger.posting_rules = TripletexPostingRules(self.client, parent=self.ledger)
