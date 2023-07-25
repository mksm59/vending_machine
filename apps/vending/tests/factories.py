from _decimal import Decimal
from datetime import datetime
import pytest
from factory import Faker
from factory.django import DjangoModelFactory
from apps.vending.models import Product, VendingMachineSlot, Client


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    id = Faker("uuid4")
    name = "Snickers Bar"
    price = Decimal("10.40")
    created_at = datetime(2023, 5, 30, 12)
    updated_at = datetime(2023, 5, 30, 23)


class VendingMachineSlotFactory(DjangoModelFactory):
    class Meta:
        model = VendingMachineSlot

    id = Faker("uuid4")
    product = Faker("uuid4")
    quantity = 1
    row = 1
    column = 1


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    id = Faker("uuid4")
    first_name = 'John'
    last_name = 'Smith'
    credit = Decimal("100.00")


@pytest.mark.django_db
def test_product_creation():
    test_product = ProductFactory(name="Heidi chocolate", price=Decimal("5.32"))

    stored_product = Product.objects.get(id=test_product.id)

    assert isinstance(stored_product, type(test_product))
    assert stored_product.price == Decimal("5.32")
    assert stored_product.name == "Heidi chocolate"


@pytest.mark.django_db
def test_vending_machine_slot_creation():
    product = ProductFactory()
    test_vending_machine_slot = VendingMachineSlotFactory(product=product, quantity=1, row=1, column=1)

    stored_vending_machine_slot = VendingMachineSlot.objects.get(id=test_vending_machine_slot.id)

    assert isinstance(stored_vending_machine_slot, type(test_vending_machine_slot))
    assert stored_vending_machine_slot.quantity == 1
    assert stored_vending_machine_slot.row == 1
    assert stored_vending_machine_slot.column == 1


@pytest.mark.django_db
def test_client_creation():
    test_client = ClientFactory(first_name='Mark', last_name='Woods', credit=Decimal("50.00"))

    stored_client = Client.objects.get(id=test_client.id)

    assert isinstance(stored_client, type(test_client))
    assert stored_client.credit == Decimal("50.00")
    assert stored_client.first_name == "Mark"
    assert stored_client.last_name == "Woods"