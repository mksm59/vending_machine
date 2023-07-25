from apps.vending.models import VendingMachineSlot
from apps.vending.tests.factories import VendingMachineSlotFactory


def prepare_slots_list() -> list[VendingMachineSlot]:
    result = []
    for i in range(1, 4):
        for j in range(1, 4):
            result.append(VendingMachineSlotFactory.build(product=None, quantity=0, row=i, column=j))
    return result