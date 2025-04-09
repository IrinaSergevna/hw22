from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Создаём группы модераторов и контент-менеджеров и назначаем права'

    def handle(self, *args, **options):
        # Создаём группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(
            name='Модератор продуктов',
        )
        moderator_group.permissions.set([
            Permission.objects.get(codename='can_unpublish_product', content_type__app_label='catalog'),
            Permission.objects.get(codename='delete_product', content_type__app_label='catalog'),
            Permission.objects.get(codename='can_edit_product', content_type__app_label='catalog'),
        ])
        moderator_group.save()

        # Создаём группу "Контент-менеджер"
        content_manager_group, created = Group.objects.get_or_create(
            name='Контент-менеджер',
        )
        content_manager_group.permissions.set([
            Permission.objects.get(codename='add_product', content_type__app_label='catalog'),
            Permission.objects.get(codename='can_edit_product', content_type__app_label='catalog'),
            Permission.objects.get(codename='add_blogpost', content_type__app_label='blog'),
            Permission.objects.get(codename='can_edit_blogpost', content_type__app_label='blog'),
            Permission.objects.get(codename='can_manage_blog', content_type__app_label='blog'),
            Permission.objects.get(codename='can_publish_blog', content_type__app_label='blog'),
        ])
        content_manager_group.save()