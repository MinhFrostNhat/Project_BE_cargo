from django.core.asgi import get_asgi_application

from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from final_project_app.middleware import TokenAuthMiddlewareStack

from final_project_cargo.consumers import Send_cargo_consumers


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': TokenAuthMiddlewareStack(
        URLRouter([
            path('taxi/', Send_cargo_consumers.as_asgi()),
        ])
    ),
})
