from _decimal import Decimal

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.vending.models import VendingMachineSlot, Client
from apps.vending.serializers import VendingMachineSlotSerializer, ClientSerializer
from apps.vending.services.prepare_slots_list import prepare_slots_list
from apps.vending.validators import ListSlotsValidator


class VendingMachineSlotView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        validator = ListSlotsValidator(data=request.query_params)
        validator.is_valid(raise_exception=True)
        filters = {}
        if quantity := validator.validated_data["quantity"]:
            filters["quantity__lte"] = quantity

        slots = VendingMachineSlot.objects.filter(**filters)
        result_slots = prepare_slots_list()
        for i in slots:
            for j in result_slots:
                if i.row == j.row and i.column == j.column:
                    result_slots.remove(j)
                    result_slots.append(i)
        result_slots = sorted(set(result_slots), key=lambda x: (x.row, x.column))
        slots_serializer = VendingMachineSlotSerializer(result_slots, many=True)
        return Response(data=slots_serializer.data)

    @staticmethod
    def post(request: Request) -> Response:
        if request.method == "POST":
            slot_id = request.data["id"]
            client_id = request.data["client_id"]
            if not slot_id or not client_id:
                return Response(data="id and client_id is required", status=400)

            slots = VendingMachineSlot.objects.filter(id__exact=slot_id)
            clients = Client.objects.filter(id__exact=client_id)

            if slots and clients:
                slot = slots[0]
                client = clients[0]
                client_credit = client.credit
                price = slot.product.price
                if price > client_credit:
                    return Response(data="Not enough money", status=400)

                if slot.quantity != 0:
                    slot.quantity = slot.quantity - 1
                    client.credit = client.credit - price
                else:
                    return Response(data="Not enough quantity", status=400)

                slot.save()
                client.save()
                return Response(data="Success", status=200)
            else:
                return Response(data="Client or slot not found", status=400)


class ClientView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        clients = Client.objects.filter()
        if request.query_params:
            username = request.query_params["username"]
            clients = Client.objects.filter(username__exact=username)

        clients_serializer = ClientSerializer(clients, many=True)

        return Response(data=clients_serializer.data)

    # Add credits
    @staticmethod
    def post(request: Request) -> Response:
        if request.method == "POST":
            client_id = request.data["id"]
            amount = request.data["amount"]
            if not amount or not client_id:
                return Response(data="client_id and amount is required", status=400)

            clients = Client.objects.filter(id__exact=client_id)
            if clients:
                client = clients[0]
                client.credit = client.credit + Decimal(amount)
                client.save()
                return Response(data=client.first_name+" "+client.last_name+" added "+str(amount)+" credit", status=200)
        else:
            return Response(data=None, status=404)

    # Reset credits
    @staticmethod
    def put(request: Request) -> Response:
        if request.method == "PUT":
            client_id = request.data["id"]
            if not client_id:
                return Response(data="client_id is required", status=400)

            clients = Client.objects.filter(id__exact=client_id)

            if clients:
                client = clients[0]
                client.credit = 0
                client.save()
                return Response(data="Success", status=200)
        else:
            return Response(data=None, status=404)