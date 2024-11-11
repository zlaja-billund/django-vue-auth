from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string


class EmailHandler:

    @classmethod
    def send_request_reset_password(self, user_email, reset_password_url):

        raw_text_content = render_to_string(
            template_name="emails/reset_password_raw.txt",
            context={"reset_password_url": reset_password_url}
        )

        html_content = render_to_string(
            template_name="emails/reset_password.html",
            context={"reset_password_url" : reset_password_url }
        )

        try:
            email_message = EmailMultiAlternatives(
                subject="Reset your password",
                body=raw_text_content,
                from_email=settings.EMAIL_FROM,
                to=[user_email],
            )

            email_message.attach_alternative(html_content, "text/html")
            email_message.send(fail_silently=False)
        except BadHeaderError:
            return False

        # if everything is ok just return to view true
        return True
