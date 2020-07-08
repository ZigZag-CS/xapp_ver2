from django.shortcuts import render

def home_page(request):
    # print(f'Session owner: { request.session.get("first_name", "Unknown") }')
    context = {
        "title": "Hello world",
        "content": "Welcome to pages page"

    }
    if request.user.is_authenticated:
        context.update({
            "premium_content": "YAHOOOOO"
        }
        )
    return render(request, 'pages/home_page.html', context)