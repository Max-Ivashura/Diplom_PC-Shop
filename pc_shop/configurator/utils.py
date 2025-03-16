from catalog.models import AttributeValue

def check_compatibility(components):
    errors = []
    cpu = components.filter(category__name="Процессоры").first()
    motherboard = components.filter(category__name="Материнские платы").first()

    if cpu and motherboard:
        cpu_socket = AttributeValue.objects.filter(product=cpu, attribute__name="Сокет").first()
        mobo_socket = AttributeValue.objects.filter(product=motherboard, attribute__name="Сокет").first()
        if cpu_socket and mobo_socket and cpu_socket.get_value() != mobo_socket.get_value():
            errors.append("Несовместимый сокет процессора и материнской платы")

    # Добавьте дополнительные проверки (например, ОЗУ и БП)
    return errors