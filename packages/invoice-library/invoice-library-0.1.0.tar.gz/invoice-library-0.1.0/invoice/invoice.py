from django.db.models import Sum

STORAGE_COST_PER_DAY = 5.0
LABOUR_COST_BY_ROLE = {
    "WM": 30.0, "FO": 25.0, "P": 20.0,
    "PA": 18.0, "S": 35.0, "D": 28.0, "IC": 22.0
}
EQUIPMENT_COST_PER_HOUR = 15.0

def calculate_storage_cost(inventory, storage_days):
    return storage_days * STORAGE_COST_PER_DAY * inventory.quantity if inventory else 0

def calculate_labour_cost(labour_queryset):
    return sum(l.hours_worked * LABOUR_COST_BY_ROLE.get(l.worker_role, 20.0) for l in labour_queryset)

def calculate_equipment_cost(equipment_queryset):
    total_hours = equipment_queryset.aggregate(total_hours=Sum("hours_used"))["total_hours"] or 0
    return total_hours * EQUIPMENT_COST_PER_HOUR

def generate_invoice(billing_instance):
    storage_cost = calculate_storage_cost(billing_instance.shipment.inventory, billing_instance.storage_days)
    labour_cost = calculate_labour_cost(billing_instance.shipment.labour_set.all())
    equipment_cost = calculate_equipment_cost(billing_instance.shipment.equipment_set.all())

    billing_instance.storage_cost, billing_instance.labour_cost, billing_instance.equipment_cost = storage_cost, labour_cost, equipment_cost
    billing_instance.calculate_total()
    billing_instance.save()

    return f"Invoice: {billing_instance.invoice_number}, Total: {billing_instance.total_amount}".encode('utf-8')