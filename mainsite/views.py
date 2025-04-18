import openai
import random
import markdown
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def home(request):
    return render(request, 'mainsite/home.html')

@require_http_methods(["GET", "POST"])
def get_report(request):
    summary = None
    formatted_summary = None
    error = None
    question = ''

    # On every GET or failed POST, regenerate math challenge
    a = random.randint(1, 9)
    b = random.randint(1, 9)

    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        word_count = len(question.split())

        # Validate honeypot (bot check)
        if request.POST.get("website"):
            error = "Bot detected."
        # Validate math challenge
        elif request.POST.get("math_answer") != request.POST.get("math_correct"):
            error = "Incorrect math answer. Please try again."
        # Validate content
        elif not question:
            error = "Report content is required."
        elif word_count > 2000:
            error = "Report must not exceed 2000 words."
        else:
            try:
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": settings.OPENAI_SYSTEM_PROMPT},
                        {"role": "user", "content": question}
                    ]
                )
                summary = response.choices[0].message.content.strip()
                formatted_summary = markdown.markdown(summary)
            except Exception as e:
                error = str(e)

    return render(request, 'mainsite/get-report.html', {
        'summary': formatted_summary,
        'error': error,
        'question': question,
        'a': a,
        'b': b,
    })
