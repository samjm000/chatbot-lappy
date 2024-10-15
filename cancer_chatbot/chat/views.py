from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from openai import OpenAI
import json

def home_view(request):
    print("Home view accessed")
    return render(request, 'chat/home.html')

def chat_view(request):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    prompt = request.GET.get("prompt")
    
    def event_stream():
        yield "data: {\"response\": \"Processing...\"}\n\n"
        completion = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
            messages=[
                {"role": "system", "content": "You are a concise, empathetic assistant for cancer patients. Provide responses that are brief and to the point, always respectful and supportive. Encourage contacting healthcare providers for more information."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            top_p=0.9,
            max_tokens=50,
            stream=True
        )
        for token in completion:
            if hasattr(token.choices[0].delta, "content"):
                content = token.choices[0].delta.content
                yield f"data: {json.dumps({'response': content})}\n\n"
        
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


    # completion = client.chat.completions.create(
    #     model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
    #     messages=[
    #         {"role": "system", "content": "You are a kind, empathetic assistant for cancer patients..."},
    #         {"role": "user", "content": prompt},
    #     ],
    #     temperature=0.7
    # )

    # Access the message content correctly
    response = completion.choices[0].message.content
    print(f"Response: {response}")
    return JsonResponse({"response": response})



