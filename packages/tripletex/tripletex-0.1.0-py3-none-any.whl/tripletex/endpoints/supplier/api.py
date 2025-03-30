from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.supplier.models import Supplier, SupplierResponse


class TripletexSuppliers(TripletexCrud[Supplier]):
    _resource_path = "supplier"
    _datamodel = Supplier
    _api_response_model = SupplierResponse
    allowed_actions = ["list", "read", "create", "update", "destroy"]  # listupdate and listcreate must be implemented on the crud.py file
