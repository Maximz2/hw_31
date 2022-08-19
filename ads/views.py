import json


from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category, Selection
from ads.permissions import AdEditPermission, SelectionEditPermission
from ads.serializer import AdSerializer, CategorySerializer, AdCreateSerializer, SelectionListSerializer, \
    SelectionDetailSerializer, SelectionSerializer


def index(request):
    return HttpResponse("200 {'status': 'ok'}")


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryView(ListView):
    models = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")

        response = []
        for category in self.object_list:
            response.append({
                "id": category.id,
                "name": category.name,
            })
        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["names"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"]
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["names"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListAPIView):
    """
    Получение списка всех объявлений
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):

        self.queryset = self.queryset.select_related("author", "category").order_by("-price")

        search_categories = request.GET.getlist('cat', [])
        if search_categories:
            self.queryset = self.queryset.filter(category_id_in=search_categories)

        search_text = request.GET.get('text', None)
        if search_text:
            self.queryset = self.queryset.filter(name__icontains=search_text)

        search_location = request.GET.get('location', None)
        if search_location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=search_location)

        min_price = int(request.GET.get('price_from', 0))
        max_price = int(request.GET.get('price_to', 0))
        price_q = None

        if min_price:
            price_q = Q(price__gte=min_price)
            if max_price:
                price_q &= Q(price__lte=max_price)

        elif max_price:
            price_q = Q(price__lte=max_price)

        if price_q is not None:
            self.queryset = self.queryset.filter(price_q)

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    """
    Получение объявления по id
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    """
    Создание объявления
    """
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    """
    Обновление объявления
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]


class AdDeleteView(DestroyAPIView):
    """
    Удаление объявления
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]

# @method_decorator(csrf_exempt, name="dispatch")
# class AdUpdateView(UpdateView):
#     model = Ad
#     fields = ["name", "author", "price", "description", "category"]
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#
#         ad_data = json.loads(request.body)
#
#         self.object.name = ad_data["name"]
#         self.object.price = ad_data["price"]
#         self.object.description = ad_data["description"]
#
#         self.object.author = get_object_or_404(User, id=ad_data["author_id"])
#         self.object.category = get_object_or_404(Category, id=ad_data["category_id"])
#
#         self.object.save()
#
#         return JsonResponse({
#             "id": self.object.id,
#             "name": self.object.name,
#             "author_id": self.object.author_id,
#             "author": self.object.author.first_name,
#             "price": self.object.price,
#             "description": self.object.description,
#             "is_published": self.object.is_published,
#             "category_id": self.object.category_id,
#             "image": self.object.image.url if self.object.image else None,
#         }, safe=False)


# @method_decorator(csrf_exempt, name="dispatch")
# class AdDeleteView(DeleteView):
#     model = Ad
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "ok"}, status=200)


# @method_decorator(csrf_exempt, name="dispatch")
# class AdUploadImageView(UpdateView):
#     model = Ad
#     fields = ["image"]
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#
#         self.object.image = request.FILES.get("image", None)
#         self.object.save()
#
#         return JsonResponse({
#             "id": self.object.id,
#             "name": self.object.name,
#             "author_id": self.object.author_id,
#             "author": self.object.author.first_name,
#             "price": self.object.price,
#             "description": self.object.description,
#             "is_published": self.object.is_published,
#             "category_id": self.object.category_id,
#             "image": self.object.image.url if self.object.image else None,
#         }, safe=False)


class AdUploadImageView(UpdateAPIView):
    """
    Загрузка картинок в объявление
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get('image', None)
        self.object.save()
        return self.update(request, *args, **kwargs)


class SelectionListView(ListAPIView):
    """
    Просмотр списка подборок.
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    """
    Просмотр подборки объявлений по id.
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateView):
    """
    Создание подборки объявлений
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    """
    Изменение подборки объявлений.
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionEditPermission]


class SelectionDeleteView(DestroyAPIView):
    """
    Удаление подборки
    """
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionEditPermission]
