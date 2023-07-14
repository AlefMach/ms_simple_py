def success_response(description=None) -> dict:
    return {'success': True, 'description': description}


def failed_response(description=None) -> dict:
    return {'success': False, 'description': description}
