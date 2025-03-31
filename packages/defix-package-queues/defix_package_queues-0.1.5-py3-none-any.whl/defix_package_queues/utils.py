def get_queue_name(service_name: str):
    name_parts = service_name.split('-')
    for i, part in enumerate(name_parts):
        name_parts[i] = part[0].upper() + part[1:]

    return ''.join(name_parts)
