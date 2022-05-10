from django.core.mail import send_mail

def send_activation_mail(user):
    message = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
    </head>
    <body>
        <h1>Спасибо за регистрацию.</h1>
        <h3>Активируйте ваш аккаунт нажав на эту кнопку:</h3>
        <a target="_self" href="http://127.0.0.1:8000/account/activate/{user.activation_code}"><button style="display: inline-block; font-weight: 400; line-height: 1.5; color: #212529; text-align: center; text-decoration: none; vertical-align: middle; cursor: pointer; -webkit-user-select: none; -moz-user-select: none; user-select: none; background-color: transparent; border: 1px solid transparent; padding: 0.375rem 0.75rem; font-size: 1rem; border-radius: 0.25rem; transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;color:#0d6efd;border-color:#0d6efd;">Activate</button></a>
    </body>
</html>
"""
    send_mail(
        subject='Активация аккаунта',
        message=message,
        html_message=message,
        from_email='youtube@makers.com',
        recipient_list=[user.email, ]
    )