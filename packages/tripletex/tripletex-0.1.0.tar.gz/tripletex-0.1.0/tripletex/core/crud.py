from typing import TypeVar

from crudclient import Crud, JSONDict, RawResponse

T = TypeVar("T")


class TripletexCrud(Crud[T]):

    def _convert_to_model(self, data: RawResponse) -> T | JSONDict:
        """
        TripleTex-specific method to convert API response to data model.
        """
        validated_data = self._validate_response(data)

        if not isinstance(validated_data, dict):
            raise ValueError(f"Unexpected response type: {type(validated_data)}")

        cleaned_data = validated_data.get("value", validated_data)

        return self._datamodel(**cleaned_data) if self._datamodel else validated_data
