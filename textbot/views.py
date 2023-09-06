from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import openai
from openai.api_resources import ChatCompletion
from .models import Text


def handle_502_error(request, exception=None):
    return render(request, "error/502.html", status=502)



def home(request):
    lang_list = [
        "German",
        "English",
        "Spanish",
        "French",
        "Italian",
        "Portug",
        "Nederland",
    ]
    if request.method == "POST":
        text = request.POST.get("text")
        lang = request.POST.get("lang")
        if lang == "Select Language":
            messages.warning(request, "Please select a language")
            return render(
                request,
                "textbot/home.html",
                {"lang_list": lang_list, "text": text, "lang": lang},
            )
        else:
            openai.api_key = "your-api-key"

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k-0613",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f'Fix this {lang} text or write a better text in {lang}: {text}'},
                    ]
                )

                response = response["choices"][0]["message"]["content"]

                record = Text(
                    question=text,
                    text_answer=response,
                    language=lang,
                    user=request.user,
                )
                record.save()

                messages.success(request, f"Your response is: {response}")
                return render(
                    request,
                    "textbot/home.html",
                    {
                        "lang_list": lang_list,
                        "response": response,
                        "text": text,
                        "lang": lang,
                    },
                )
            except Exception as e:
                return render(
                    request,
                    "textbot/home.html",
                    {"lang_list": lang_list, "text": e, "lang": lang},
                )

    return render(request, "textbot/home.html", {"lang_list": lang_list})


def suggest(request):
    lang_list = [
        "German",
        "English",
        "Spanish",
        "French",
        "Italian",
        "Portug",
        "Nederland",
    ]
    if request.method == "POST":
        text = request.POST.get("text")
        lang = request.POST.get("lang")
        if lang == "Select Programming Language":
            messages.success(request, "Please select a programming language")
            return render(
                request,
                "textbot/home.html",
                {"lang_list": lang_list, "text": text, "lang": lang},
            )
        else:
            openai.api_key = "your-api-key"

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k-0613",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"Suggest a {lang} code for: {text}"},
                    ]
                )

                response = response["choices"][0]["message"]["content"]

                record = Text(
                    question=text,
                    text_answer=response,
                    language=lang,
                    user=request.user,
                )
                record.save()

                return render(
                    request,
                    "textbot/suggest.html",
                    {
                        "lang_list": lang_list,
                        "response": response,
                        "text": text,
                        "lang": lang,
                    },
                )
            except Exception as e:
                return render(
                    request,
                    "textbot/suggest.html",
                    {"lang_list": lang_list, "prompt": e, "lang": lang},
                )

    return render(request, "textbot/suggest.html", {"lang_list": lang_list})



def translate(request):
    lang_list = [
        "German",
        "English",
        "Spanish",
        "French",
        "Italian",
        "Portug",
        "Nederland",
    ]
    if request.method == "POST":
        text = request.POST.get("text")
        lang1 = request.POST.get("lang1")
        lang2 = request.POST.get("lang2")
        if lang1 == "Select source Language":
            messages.success(request, "Please select a source language")
            return render(
                request,
                "textbot/translate.html",
                {"lang_list": lang_list, "text": text, "lang1": lang1, "lang2": lang2},
            )
        elif lang2 == "Select target Language":
            messages.success(request, "Please select a target language")
            return render(
                request,
                "textbot/translate.html",
                {"lang_list": lang_list, "text": text, "lang1": lang1, "lang2": lang2},
            )
        else:
            openai.api_key = "your-api-key"

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k-0613",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"Translate the following text from {lang1} to {lang2}: {text}"},
                    ]
                )

                response = response["choices"][0]["message"]["content"]

                record = Text(
                    question=text,
                    text_answer=response,
                    language=lang1,
                    language2=lang2,
                    user=request.user,
                )
                record.save()

                return render(
                    request,
                    "textbot/translate.html",
                    {
                        "lang_list": lang_list,
                        "response": response,
                        "text": text,
                        "lang1": lang1,
                        "lang2": lang2,
                    },
                )
            except Exception as e:
                return render(
                    request,
                    "textbot/translate.html",
                    {"lang_list": lang_list, "text": e, "lang1": lang1, "lang2": lang2},
                )

    return render(request, "textbot/translate.html", {"lang_list": lang_list})



def past(request):
    text = Text.objects.filter(user_id=request.user.id)
    return render(request, "textbot/past.html", {"text": text})



def delete_past(request, past_id):
    past = Text.objects.get(pk=past_id)
    past.delete()
    messages.success(request, "Text deleted")
    return redirect("textbot:past")

