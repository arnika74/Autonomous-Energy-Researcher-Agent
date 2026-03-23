import requests
import json
import time

print('🧪 Testing research endpoint...')
start_time = time.time()

try:
    response = requests.post(
        'http://localhost:8000/research',
        json={'query': 'What is solar energy?'},
        timeout=60
    )

    elapsed = time.time() - start_time
    print(f'⏱️  Request took {elapsed:.1f} seconds')
    print(f'📊 Status: {response.status_code}')

    if response.status_code == 200:
        data = response.json()
        print(f'📋 Response keys: {list(data.keys()) if isinstance(data, dict) else "not dict"}')
        if 'report_id' in data:
            print(f'✅ Report ID: {data["report_id"]}')
        else:
            print('❌ No report_id in response')
            print(f'📄 Full response: {data}')
    else:
        print(f'❌ Error response: {response.text}')

except Exception as e:
    elapsed = time.time() - start_time
    print(f'💥 Exception after {elapsed:.1f} seconds: {e}')