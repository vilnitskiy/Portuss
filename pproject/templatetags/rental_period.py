from django import template
register = template.Library()


@register.simple_tag
def rental_period(self):
    rental_perion = self.rental_perion_end - self.rental_perion_begin
    return rental_perion
