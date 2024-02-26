import requests

def generate_response_sk(input_text, prompt):
    sidekick_url = "https://servicesessentials.ibm.com/apis/v1/curator-ai/executeModel"
    payload = {
        "prompt": prompt + input_text,
        "modelId": "7"
    }

    headers = {
        "Content-Type": "application/json",
        'x-access-token':'e9060152-68cc-449a-a813-72328ea7f8b7',
        'x-security-key':'d81c7ee6-b208-49d4-a4b4-477cbc8b923e'
    }

    try:
        response = requests.post(sidekick_url, headers=headers, json=payload)
        response.raise_for_status()
        answer = response.json()
        print(answer)
        return {"success": True, "source": "SideKick", "data": answer}
    except requests.exceptions.RequestException as e:
        if response:
            print(response.status_code)
            print(response.json())
        else:
            print(e)
        return {"success": False, "error": "Something went wrong!"}

input_text = " fascinating facts about the solar system"
prompt = "Tell me"
result = generate_response_sk(input_text, prompt)