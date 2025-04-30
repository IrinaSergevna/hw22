from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product  # Убедись, что импорт правильный


class Command(BaseCommand):
    help = "Удаляет все продукты и загружает тестовые данные из фикстур"

    def handle(self, *args, **kwargs):
        self.stdout.write("Удаление всех продуктов...")
        Product.objects.all().delete()

        self.stdout.write("Загрузка тестовых данных...")
        call_command("loaddata", "categories.json")
        call_command("loaddata", "products.json")

        self.stdout.write(
            self.style.SUCCESS("База успешно заполнена тестовыми данными!")
        )
