from django.http import HttpResponse


def index(request):
    return HttpResponse(
        """
    <body>
        <style>li { list-style: none;} li::before { content: "➡ "}</style>
        <h1> Dynamic web application using python and react</h1>
        <ul>
            <li><a href="/api">/api</a></li>
            <li><a href="/admin">/admin</a></li>
             <li><a href="/blog">/blog</a></li>
        </ul>
    </body>
    """)