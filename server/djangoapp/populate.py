from .models import CarMake, CarModel


def initiate():
    data = {
        "Nissan": [
            ("Pathfinder", "SUV"),
            ("Qashqai", "SUV"),
            ("XTrail", "SUV"),
        ],
        "Mercedes": [
            ("A-Class", "SEDAN"),
            ("C-Class", "SEDAN"),
            ("E-Class", "SEDAN"),
        ],
        "Audi": [
            ("A4", "SEDAN"),
            ("A5", "SEDAN"),
            ("Q7", "SUV"),
        ],
        "Kia": [
            ("Sorento", "SUV"),
            ("Carnival", "SUV"),
            ("Cerato", "SEDAN"),
        ],
        "Toyota": [
            ("Corolla", "SEDAN"),
            ("Camry", "SEDAN"),
            ("Kluger", "SUV"),
        ],
    }

    for make_name, models in data.items():
        car_make, _ = CarMake.objects.get_or_create(
            name=make_name,
            defaults={
                "description": f"{make_name} automobile manufacturer."
            },
        )

        for model_name, model_type in models:
            CarModel.objects.get_or_create(
                car_make=car_make,
                name=model_name,
                defaults={
                    "type": model_type,
                    "year": 2023,
                },
            )