# Schemas

```python
poetry add validate-docbr
```
```
src/schemas/partner.py
```
```python
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import Field, validator
from validate_docbr import CNPJ, CPF

from src.services.exceptions import InvalidDocumentException


class PartnerCreate(CamelModel):
    name: str = Field(..., description='Nome do parçeiro')
    document: str = Field(..., description='Cnpj do parçeiro')
    active: bool = Field(True, description='Parceiro ativo ou inativo')
    business_address: str = Field(..., description='Endereço do parçeiro')

    @validator('document')
    def validate_document(cls, value):
        """Validate the document
        :param: value: the document to validate

        :return: the document
        :raises: InvalidDocumentException
        """
        if not CPF().validate(value) and not CNPJ().validate(value):
            raise InvalidDocumentException()

        value = ''.join(v for v in value if v.isalnum())

        return value


class PartnerUpdate(PartnerCreate):
    id: int  # noqa VNE003


class Partner(PartnerUpdate):
    class Config:
        orm_mode = True



```

```
tests/unit/schemas/test_partner.py
```

```python
import pytest
from pydantic import ValidationError

from src.schemas.partner import PartnerCreate
from src.services.exceptions import InvalidDocumentException


@pytest.mark.asyncio()
async def test_parter_create_when_payload_is_valid_then_parses_without_error():
    # arrange
    payload = {
        'name': 'test',
        'document': '12272084000100',
        'active': 'false',
        'businessAddress': 'rua test',
    }

    # act
    partner_create = PartnerCreate.parse_obj(payload)

    # assert
    assert partner_create.name == 'test'
    assert partner_create.document == '12272084000100'
    assert not partner_create.active
    assert partner_create.business_address == 'rua test'


@pytest.mark.asyncio()
async def test_parter_create_when_document_is_invalid_then_raises_a_validation_error():
    # arrange
    payload = {
        'name': 'test',
        'document': '12272084000101',
        'active': 'true',
        'businessAddress': 'rua test',
    }

    # act
    with pytest.raises(InvalidDocumentException) as error:
        PartnerCreate.parse_obj(payload)

    # assert
    assert error.value.detail == 'Invalid CPF/CNPJ'
    assert error.value.status_code == 422


@pytest.mark.asyncio()
async def test_parter_create_when_payload_not_have_name_then_raises_a_validation_error():
    # arrange
    payload = {
        'document': '12272084000100',
        'active': 'true',
        'businessAddress': 'rua test',
    }

    # act
    with pytest.raises(ValidationError) as error:
        PartnerCreate.parse_obj(payload)

    # assert
    assert (
        str(error.value)
        == '1 validation error for PartnerCreate\nname\n  field required (type=value_error.missing)'
    )


@pytest.mark.asyncio()
async def test_parter_create_when_payload_not_have_active_attribute_then_parses_and_return_default_value():
    # arrange
    payload = {
        'name': 'test',
        'document': '12272084000100',
        'businessAddress': 'rua test',
    }

    # act
    partner_create = PartnerCreate.parse_obj(payload)

    # assert
    assert partner_create.name == 'test'
    assert partner_create.document == '12272084000100'
    assert partner_create.active
    assert partner_create.business_address == 'rua test'

```
