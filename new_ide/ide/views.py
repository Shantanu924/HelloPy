import json
from django.shortcuts import render
from django.http import JsonResponse
from django.view.decorators.csrf import csrf_exempt
import subprocess

def index(request):
    return render(request, 'ide/index.html')

@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code','')
        try:
            result = subprocess.run(
                ['python3', '-c', code],
                capture_output=True,
                text = True,
                timeout = 5
            )
            output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            output = f"Error:{str(e)}"
        return JsonResponse({'output':output})