from django.db import transaction

from inventory.models.inventory import Inventory
from plants.models.plants import Plant

class PlantsService:
    
    @staticmethod
    @transaction.atomic
    def create(**validated_data):
        plant = Plant.objects.create(**validated_data)
        
        Inventory.objects.create(
            plant=plant,
            quantity=0,
        )
        
        return plant