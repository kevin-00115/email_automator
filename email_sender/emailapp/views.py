from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.

@csrf_exempt
def send_email(request):
    if request.method =="POST":
        try:
            note = ''
            data = request.POST
            from_email = data['from']
            to_email = data['to_email']
            subject = data['subject']
            body_html = data['body']
            note = data.get('note','')

            password = data['password']

            settings.EMAIL_HOST_USER = from_email
            settings.EMAIL_HOST_PASSWORD = password


            attachment = request.FILES.get("attachment", None)

            email = EmailMessage(subject, body_html, from_email,[to_email])
            if attachment:
                email.attach(attachment.name, attachment.read(), attachment.content_type)
            email.content_subtype = 'html'
            email.send()

            return JsonResponse({"status":1, "message":"Success", "note":note })
        except Exception as e:
            return JsonResponse({"status":2, "message": str(e), "note": note})

    return JsonResponse({"message":"Invalid reuqest method"})

