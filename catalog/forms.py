from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите название"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "rows": 5, "placeholder": "Введите описание"})
        self.fields["price"].widget.attrs.update({"class": "form-control", "placeholder": "Введите цену"})
        self.fields["category"].widget.attrs.update({"class": "form-select"})
        self.fields["image"].widget.attrs.update({"class": "form-control"})

    def clean_name(self):
        name = self.cleaned_data.get("name")
        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(f"Название не может содержать слово '{word}'.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        description_lower = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise ValidationError(f"Описание не может содержать слово '{word}'.")
        return description

    def clean_price(self):
        # Проверка корректного ввода цены продукта
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            # Проверка размера файла (5 МБ = 5 * 1024 * 1024 байт)
            max_size = 5 * 1024 * 1024  # 5 МБ
            if image.size > max_size:
                raise ValidationError("Размер изображения не должен превышать 5 МБ.")

            # Проверка формата файла
            valid_formats = ["image/jpeg", "image/png"]
            if image.content_type not in valid_formats:
                raise ValidationError("Изображение должно быть в формате JPEG или PNG.")
        return image