# configurator/utils.py
def check_compatibility_logic(components):
    errors = []
    compatibility_status = []

    # Проверка сокета CPU и материнской платы
    cpu = components.filter(category__name="Процессоры").first()
    motherboard = components.filter(category__name="Материнские платы").first()
    if cpu and motherboard:
        cpu_socket = get_attribute_value(cpu, "Сокет")
        mobo_socket = get_attribute_value(motherboard, "Сокет")
        if cpu_socket != mobo_socket:
            errors.append("Несовместимый сокет процессора и материнской платы")
            compatibility_status.append({
                'category_id': cpu.category.id,
                'message': 'Несовместимый сокет',
                'is_compatible': False
            })
        else:
            compatibility_status.append({
                'category_id': cpu.category.id,
                'message': 'Совместим',
                'is_compatible': True
            })

    # Проверка мощности БП
    psu = components.filter(category__name="Блоки питания").first()
    if psu:
        required_power = sum(get_attribute_value(c, "TDP") for c in components if hasattr(c, 'tdp'))
        psu_power = get_attribute_value(psu, "Мощность")
        if psu_power < required_power:
            errors.append(f"Недостаточная мощность БП (требуется {required_power} Вт)")
            compatibility_status.append({
                'category_id': psu.category.id,
                'message': 'Недостаточная мощность',
                'is_compatible': False
            })

    return errors, compatibility_status

def get_attribute_value(product, attribute_name):
    attr = product.attributevalue_set.filter(attribute__name=attribute_name).first()
    return attr.get_value() if attr else None