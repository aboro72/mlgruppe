from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import openai
from .models import Code


# Create your views here.


def home(request):
    # a = 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
    lang_list = [
        "arduino",
        "bash",
        "basic",
        "batch",
        "c",
        "clike",
        "cpp",
        "csharp",
        "css",
        "dart",
        "django",
        "go",
        "html",
        "http",
        "java",
        "javascript",
        "markup",
        "markup-templating",
        "matlab",
        "mongodb",
        "objectivec",
        "perl",
        "php",
        "powershell",
        "python",
        "r",
        "ruby",
        "rust",
        "sas",
        "sass",
        "scala",
        "sql",
        "swift",
        "yaml",
    ]
    if request.method == "POST":
        code = request.POST["code"]
        lang = request.POST["lang"]
        if lang == "Select Programming Language":
            messages.warning(request, "Please select a programming language")
            return render(
                request,
                "codebot/home.html",
                {"lang_list": lang_list, "code": code, "lang": lang},
            )
        else:
            # OpenAI Key
            openai.api_key = "your-api-key"

            # OpenAI Instance
            openai.Model.list()

            # OpenAI Request
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k-0613",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user",
                         "content": f"Respond only with code. Fix this {lang} code or write a better code: {code}"},
                    ]
                )
                # Parse the response
                response = response["choices"][0]["message"]["content"]
                # response save to db
                record = Code(
                    question=code,
                    code_answer=response,
                    language=lang,
                    user=request.user,
                )
                record.save()
                # response send to user
                messages.success(request, f"Your response is: {response}")
                return render(
                    request,
                    "codebot/home.html",
                    {
                        "lang_list": lang_list,
                        "response": response,
                        "code": code,
                        "lang": lang,
                    },
                )
            except Exception as e:
                return render(
                    request,
                    "codebot/home.html",
                    {"lang_list": lang_list, "code": e, "lang": lang},
                )

    return render(request, "codebot/home.html", {"lang_list": lang_list})


def suggest(request):
    lang_list = [
        "arduino",
        "bash",
        "basic",
        "batch",
        "c",
        "clike",
        "cpp",
        "csharp",
        "css",
        "dart",
        "django",
        "go",
        "html",
        "http",
        "java",
        "javascript",
        "markup",
        "markup-templating",
        "matlab",
        "mongodb",
        "objectivec",
        "perl",
        "php",
        "powershell",
        "python",
        "r",
        "ruby",
        "rust",
        "sas",
        "sass",
        "scala",
        "sql",
        "swift",
        "yaml",
    ]
    if request.method == "POST":
        prompt = request.POST["prompt"]
        lang = request.POST["lang"]
        if lang == "Select Programming Language":
            messages.success(request, "Please select a programming language")
            return render(
                request,
                "codebot/home.html",
                {"lang_list": lang_list, "prompt": prompt, "lang": lang},
            )
        else:
            # OpenAI Key
            openai.api_key = "your-api-key"

            # OpenAI Instance
            openai.Model.list()

            # OpenAI Request
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k-0613",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"Antworte nur mit {lang} Code ohne weitere erklärungen. {prompt}"},
                    ]
                )
                # Parse the response
                response = response["choices"][0]["message"]["content"]
                # response save to db
                record = Code(
                    question=prompt,
                    code_answer=response,
                    language=lang,
                    user=request.user,
                )
                record.save()
                return render(
                    request,
                    "codebot/suggest.html",
                    {
                        "lang_list": lang_list,
                        "response": response,
                        "prompt": prompt,
                        "lang": lang,
                    },
                )
            except Exception as e:
                return render(
                    request,
                    "codebot/suggest.html",
                    {"lang_list": lang_list, "prompt": e, "lang": lang},
                )

    return render(request, "codebot/suggest.html", {"lang_list": lang_list})


def past(request):
    code = Code.objects.filter(user_id=request.user.id)
    return render(request, "codebot/past.html", {"code": code})


def delete_past(request, Past_id):
    past = Code.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, "Code deleted")
    return redirect("codebot:past")
