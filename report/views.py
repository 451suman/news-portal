import csv
import tempfile
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import get_user_model

from newspaper.models import Post
# Create your views here.
User = get_user_model()

COLUMNS = [
    "first_name",
    "last_name",
    "username",
    "email",
    "is_staff",
    "is_active",
    "is_superuser",
    "last_login",
    "date_joined",
]

class UserReportView(View):
    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposion"] = "attachment; filename=users.csv"

        users = User.objects.all().only(*COLUMNS).values(*COLUMNS)

        writer = csv.DictWriter(response, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)

        return response

# 127.0.0.1:8000/api/v1/post/
# 127.0.0.1:8000/post/

#   both url is is dame so django got confused 

# to remove confule we use app_name
# # {%urls "report:post"%}






# import tempfile
# from django.http import HttpResponse
# from django.views import View
# from django.template.loader import render_to_string
# from weasyprint import HTML
# from .models import Post  # Ensure you import your Post model

# class PostPDFFile(View):
#     def get(self, request, *args, **kwargs):
#         # Query set
#         posts = Post.objects.all()

#         # Render the HTML template with the context
#         html_string = render_to_string("reports/posts.htm", {"posts": posts})
#         html = HTML(string=html_string, base_url=request.build_absolute_uri())

#         # Create HTTP response with PDF content type
#         response = HttpResponse(content_type='application/pdf')
#         response["Content-Disposition"] = "attachment; filename=posts.pdf"  # Fixing the spelling
#         response["Content-Transfer-Encoding"] = "binary"  # Fixing the spelling

#         # Write the PDF to a temporary file and then to the response
#         with tempfile.NamedTemporaryFile(delete=True) as output:
#             # Write the PDF result directly to the output
#             result = html.write_pdf()
#             output.write(result)
#             output.flush()

#             # Open the temporary file and read its contents
#             output.seek(0)  # Go back to the beginning of the file
#             response.write(output.read())

#         return response
