from django.dispatch import receiver
from channels.layers import get_channel_layer
from django.db.models.signals import post_save

from table.models import Vocab
from asgiref.sync import async_to_sync


# Создаем функцию-обработчик для сигнала
@receiver(post_save, sender=Vocab)
def word_created(sender, instance, created, **kwargs):
    print(instance.user_email)
    print(type(instance.user_email))
    print(instance.user_email.id)
    print(type(instance.user_email.id))
    if created:
        print(f"Новое слово создвано нахуй: {instance.word}")
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(instance.user_email.id),
            {
                'type': 'events_alarm',  # Тип сообщения соответствует имени метода
                'message': instance.word
            }
        )


'''
а группу надо создавать обязательно в коннекте?

'''



#        channel_layer = get_channel_layer()
#        async_to_sync(channel_layer.group_send)(
#            str(instance.user_email.id),
#            {
#                "type": "huepizda",
#                "message": f"Новое слово создано нахуй: {instance.word}"
#            }
#        )
