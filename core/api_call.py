import requests
from core.settings import Settings
import redis

settings = Settings()


class Query:

    @staticmethod
    def get_position(reference):
        data = f'''
        query{{
            position(reference: "{reference}") {{
                name
                location{{
                    x
                    y
                }}
            }}
        }}
        '''
        r = redis.Redis(decode_responses=True)
        token = r.get('login')
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'JWT {token}'
        }
        response = requests.post(settings.server_url, json={'query': data}, headers=headers).json()

        return response.get('data')

    @staticmethod
    def get_logged_entities():
        data = '''
        query{
            entities(logged:true){
                name
                logged
                location{
                    x
                    y
                }
            }
        }    
        '''
        r = redis.Redis(decode_responses=True)
        token = r.get('login')
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'JWT {token}'
        }
        response = requests.post(settings.server_url, json={'query': data}, headers=headers)

        return response.json().get('data')


class Mutation:

    @staticmethod
    def update_position(x, y, reference):
        data = f'''
        mutation {{
            updatePosition(input: {{
                reference: "{reference}"
                location: {{
                    x: {x}
                    y: {y}
                }}
                }}){{
                    entity {{
                    name
                    location {{
                        x
                        y
                    }}
                }}
            }}
        }}
        '''
        r = redis.Redis(decode_responses=True)
        token = r.get('login')
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'JWT {token}'
        }
        response = requests.post(settings.server_url, json={'query': data}, headers=headers)

        return response.json().get('data')
