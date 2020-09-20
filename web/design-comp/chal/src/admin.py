import requests
import config

def visit(url, requester_id, host):
    try:
        requests.post(
            config.ADMIN_API,
            json={
                'url': [
                    f'{host}/admin/login?token={config.ADMIN_TOKEN}',
                    url,
                    f'{host}/admin/rate?token={config.ADMIN_TOKEN}&user={requester_id}&score=8&submit'
                ],
                'timeout': config.ADMIN_TIMEOUT
            },
            timeout=1
        )
        return True
    except requests.exceptions.ReadTimeout:
        return True
    except:
        return False
