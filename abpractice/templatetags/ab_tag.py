from django import template
from ..models import Cart

register = template.Library()

@register.simple_tag
def any_function(request):
    a = Cart.objects.filter(user_id=request.user.id)
    return a.count()