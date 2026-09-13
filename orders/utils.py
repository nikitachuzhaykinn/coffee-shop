from django.core.mail import send_mail
from django.conf import settings


def send_order_emails(order):
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@coffeeshop.local')

    items_lines = []
    for item in order.items.select_related('product').all():
        line = f"  • {item.quantity}x {item.product.name} — {item.price} ₽"
        if item.modifiers:
            mod_names = [m.get('name', str(m.get('id', ''))) for m in item.modifiers]
            line += f" ({', '.join(mod_names)})"
        items_lines.append(line)
    items_text = '\n'.join(items_lines)

    delivery_text = 'Самовывоз' if order.delivery_type == 'pickup' else f'Доставка по адресу: {order.address}'

    subject = f"Подтверждение заказа #{order.order_id} | Coffee Shop"
    message = (
        f"Здравствуйте, {order.first_name}!\n\n"
        f"Ваш заказ #{order.order_id} успешно оформлен.\n\n"
        f"Состав заказа:\n{items_text}\n\n"
        f"Тип получения: {delivery_text}\n"
        f"Итого: {order.total_amount} ₽\n\n"
        f"Спасибо за заказ!\n"
        f"Coffee Shop"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[order.email],
        fail_silently=True,
    )

    admin_emails = [email for _, email in getattr(settings, 'ADMINS', [])]
    if admin_emails:
        admin_message = (
            f"Новый заказ #{order.order_id}\n\n"
            f"Клиент: {order.first_name} {order.last_name}\n"
            f"Email: {order.email}\n"
            f"Телефон: {order.phone}\n"
            f"Тип: {delivery_text}\n\n"
            f"Состав:\n{items_text}\n\n"
            f"Итого: {order.total_amount} ₽"
        )
        send_mail(
            subject=f"Новый заказ #{order.order_id}",
            message=admin_message,
            from_email=from_email,
            recipient_list=admin_emails,
            fail_silently=True,
        )