from django.db.models import Q
from django.views.generic import ListView

from .models import Product


class ProductListView(ListView):
    model = Product
    paginate_by = 24

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        brand = self.request.GET.get("brand")

        if brand:
            queryset = queryset.filter(brand__iexact=brand.strip())

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(brand__icontains=query)
                | Q(supplier__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get a list of unique brand names
        # Get a list of truly unique brand names, ignoring case and leading/trailing whitespace
        context["unique_brands"] = Product.objects.values_list(
            "brand", flat=True
        ).distinct().order_by("brand")
        context["current_brand"] = self.request.GET.get("brand", "")
        return context
