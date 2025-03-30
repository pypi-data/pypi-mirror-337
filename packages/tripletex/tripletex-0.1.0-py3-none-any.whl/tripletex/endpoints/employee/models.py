from typing import Optional

from pydantic import BaseModel

from tripletex.core.models import IdUrl, TripletexResponse


class Employee(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[list[str]] = None
    url: Optional[str] = None
    display_name: Optional[str] = None
    employee_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    email: Optional[str] = None
    phone_number_mobile_country: IdUrl
    phone_number_mobile: Optional[str] = None
    phone_number_home: Optional[str] = None
    phone_number_work: Optional[str] = None
    national_identity_number: Optional[str] = None
    dnumber: Optional[str] = None
    international_id: IdUrl
    bank_account_number: Optional[str] = None
    iban: Optional[str] = None
    bic: Optional[str] = None
    creditor_bank_country_id: Optional[int] = None
    uses_abroad_payment: Optional[bool] = None
    user_type: IdUrl
    allow_information_registration: Optional[bool] = None
    is_contact: Optional[bool] = None
    is_proxy: Optional[bool] = None
    comments: Optional[str] = None
    address: IdUrl
    department: IdUrl
    employments: IdUrl
    holiday_allowance_earned: IdUrl
    employee_category: IdUrl
    is_auth_project_overview_url: Optional[bool] = None
    picture_id: Optional[int] = None
    company_id: Optional[int] = None


class EmployeeResponse(TripletexResponse[Employee]):
    pass
