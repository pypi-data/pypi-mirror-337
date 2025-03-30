from typing import List, Optional

from pydantic import BaseModel, Field

from tripletex.core.models import Change, IdUrl, TripletexResponse


class Account(BaseModel):
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    number: Optional[int] = None
    number_pretty: Optional[str] = Field(None, alias="numberPretty")
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    legal_vat_types: Optional[List[IdUrl]] = Field(None, alias="legalVatTypes")
    ledger_type: Optional[str] = Field(None, alias="ledgerType")
    balance_group: Optional[str] = Field(None, alias="balanceGroup")
    vat_type: Optional[IdUrl] = Field(None, alias="vatType")
    vat_locked: Optional[bool] = Field(None, alias="vatLocked")
    currency: Optional[IdUrl] = None
    is_closeable: Optional[bool] = Field(None, alias="isCloseable")
    is_applicable_for_supplier_invoice: Optional[bool] = Field(None, alias="isApplicableForSupplierInvoice")
    require_reconciliation: Optional[bool] = Field(None, alias="requireReconciliation")
    is_inactive: Optional[bool] = Field(None, alias="isInactive")
    is_bank_account: Optional[bool] = Field(None, alias="isBankAccount")
    is_invoice_account: Optional[bool] = Field(None, alias="isInvoiceAccount")
    bank_account_number: Optional[str] = Field(None, alias="bankAccountNumber")
    bank_account_country: Optional[IdUrl] = Field(None, alias="bankAccountCountry")
    bank_name: Optional[str] = Field(None, alias="bankName")
    bank_account_iban: Optional[str] = Field(None, alias="bankAccountIBAN")
    bank_account_swift: Optional[str] = Field(None, alias="bankAccountSWIFT")
    saft_code: Optional[str] = Field(None, alias="saftCode")
    grouping_code: Optional[str] = Field(None, alias="groupingCode")
    display_name: Optional[str] = Field(None, alias="displayName")
    requires_department: Optional[bool] = Field(None, alias="requiresDepartment")
    requires_project: Optional[bool] = Field(None, alias="requiresProject")
    invoicing_department: Optional[IdUrl] = Field(None, alias="invoicingDepartment")
    is_postings_exist: Optional[bool] = Field(None, alias="isPostingsExist")
    quantity_type1: Optional[IdUrl] = Field(None, alias="quantityType1")
    quantity_type2: Optional[IdUrl] = Field(None, alias="quantityType2")
    department: Optional[IdUrl] = None

    class Config:
        populate_by_name = True


class LedgerAccount(BaseModel):
    account: Optional[Account] = None
    sum_amount: Optional[float] = Field(None, alias="sumAmount")
    currency: Optional[IdUrl] = None
    sum_amount_currency: Optional[float] = Field(None, alias="sumAmountCurrency")
    opening_balance: Optional[float] = Field(None, alias="openingBalance")
    opening_balance_currency: Optional[float] = Field(None, alias="openingBalanceCurrency")
    closing_balance: Optional[float] = Field(None, alias="closingBalance")
    closing_balance_currency: Optional[float] = Field(None, alias="closingBalanceCurrency")
    balance_out_in_account_currency: Optional[float] = Field(None, alias="balanceOutInAccountCurrency")
    postings: Optional[List[IdUrl]] = None

    class Config:
        populate_by_name = True


class LedgerAccountResponse(TripletexResponse[LedgerAccount]):
    pass


class VoucherType(BaseModel):
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = Field(None, alias="displayName")

    class Config:
        populate_by_name = True


class VoucherTypeResponse(TripletexResponse[VoucherType]):
    pass


class Voucher(BaseModel):
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    date: Optional[str] = None
    number: Optional[int] = None
    temp_number: Optional[int] = Field(None, alias="tempNumber")
    year: Optional[int] = None
    description: Optional[str] = None
    voucher_type: Optional[IdUrl] = Field(None, alias="voucherType")
    reverse_voucher: Optional[IdUrl] = Field(None, alias="reverseVoucher")
    postings: Optional[List[IdUrl]] = None
    document: Optional[IdUrl] = None
    attachment: Optional[IdUrl] = None
    external_voucher_number: Optional[str] = Field(None, alias="externalVoucherNumber")
    edi_document: Optional[IdUrl] = Field(None, alias="ediDocument")
    supplier_voucher_type: Optional[str] = Field(None, alias="supplierVoucherType")
    was_auto_matched: Optional[bool] = Field(None, alias="wasAutoMatched")
    vendor_invoice_number: Optional[str] = Field(None, alias="vendorInvoiceNumber")
    display_name: Optional[str] = Field(None, alias="displayName")

    class Config:
        populate_by_name = True


class Posting(BaseModel):
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    voucher: Optional[IdUrl] = None
    date: Optional[str] = None
    description: Optional[str] = None
    account: Optional[IdUrl] = None
    amortization_account: Optional[IdUrl] = Field(None, alias="amortizationAccount")
    amortization_start_date: Optional[str] = Field(None, alias="amortizationStartDate")
    amortization_end_date: Optional[str] = Field(None, alias="amortizationEndDate")
    customer: Optional[IdUrl] = None
    supplier: Optional[IdUrl] = None
    employee: Optional[IdUrl] = None
    project: Optional[IdUrl] = None
    product: Optional[IdUrl] = None
    department: Optional[IdUrl] = None
    vat_type: Optional[IdUrl] = Field(None, alias="vatType")
    amount: Optional[float] = None
    amount_currency: Optional[float] = Field(None, alias="amountCurrency")
    amount_gross: Optional[float] = Field(None, alias="amountGross")
    amount_gross_currency: Optional[float] = Field(None, alias="amountGrossCurrency")
    currency: Optional[IdUrl] = None
    close_group: Optional[IdUrl] = Field(None, alias="closeGroup")
    invoice_number: Optional[str] = Field(None, alias="invoiceNumber")
    term_of_payment: Optional[str] = Field(None, alias="termOfPayment")
    row: Optional[int] = None
    type: Optional[str] = None
    external_ref: Optional[str] = Field(None, alias="externalRef")
    system_generated: Optional[bool] = Field(None, alias="systemGenerated")
    tax_transaction_type: Optional[str] = Field(None, alias="taxTransactionType")
    tax_transaction_type_id: Optional[int] = Field(None, alias="taxTransactionTypeId")
    matched: Optional[bool] = None
    quantity_amount1: Optional[float] = Field(None, alias="quantityAmount1")
    quantity_type1: Optional[IdUrl] = Field(None, alias="quantityType1")
    quantity_amount2: Optional[float] = Field(None, alias="quantityAmount2")
    quantity_type2: Optional[IdUrl] = Field(None, alias="quantityType2")
    is_vat_readonly: Optional[bool] = Field(None, alias="isVatReadonly")
    is_amount_vat_closed: Optional[bool] = Field(None, alias="isAmountVatClosed")
    posting_rule_id: Optional[int] = Field(None, alias="postingRuleId")

    class Config:
        populate_by_name = True


class AccountingPeriod(BaseModel):
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    name: Optional[str] = None
    number: Optional[int] = None
    start: Optional[str] = None
    end: Optional[str] = None
    is_closed: Optional[bool] = Field(None, alias="isClosed")
    check_ledger_log_employee_name: Optional[str] = Field(None, alias="checkLedgerLogEmployeeName")
    check_ledger_log_employee_picture_id: Optional[int] = Field(None, alias="checkLedgerLogEmployeePictureId")
    check_ledger_log_time: Optional[str] = Field(None, alias="checkLedgerLogTime")

    class Config:
        populate_by_name = True


class AccountingPeriodResponse(TripletexResponse[AccountingPeriod]):
    pass


class AnnualAccount(BaseModel):
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    year: Optional[int] = None
    start: Optional[str] = None
    end: Optional[str] = None

    class Config:
        populate_by_name = True


class AnnualAccountResponse(TripletexResponse[AnnualAccount]):
    pass


class CloseGroup(BaseModel):
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    date: Optional[str] = None
    postings: Optional[List[IdUrl]] = None

    class Config:
        populate_by_name = True


class CloseGroupResponse(TripletexResponse[CloseGroup]):
    pass


class PostingRules(BaseModel):
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[List[Change]] = None
    url: Optional[str] = None
    account_receivable_customers_id: Optional[IdUrl] = Field(None, alias="accountReceivableCustomersId")
    account_debt_vendors_id: Optional[IdUrl] = Field(None, alias="accountDebtVendorsId")
    account_debt_employees_and_owners_id: Optional[IdUrl] = Field(None, alias="accountDebtEmployeesAndOwnersId")
    account_round_diff_id: Optional[IdUrl] = Field(None, alias="accountRoundDiffId")
    vat_per_department: Optional[bool] = Field(None, alias="vatPerDepartment")
    multiple_industries: Optional[bool] = Field(None, alias="multipleIndustries")
    default_business_activity_type_id: Optional[int] = Field(None, alias="defaultBusinessActivityTypeId")

    class Config:
        populate_by_name = True


class PostingRulesResponse(BaseModel):
    value: Optional[PostingRules] = None

    class Config:
        populate_by_name = True
