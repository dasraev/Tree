from rest_framework import generics, views
from .serializers import *
from .models import *
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum
from .utils import get_feed
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
from django.conf import settings


class TreeTypeListView(generics.ListAPIView):
    queryset = TreeType.objects.all()
    serializer_class = TreeTypeSeriliazer


class TreeByTypeView(generics.ListAPIView):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer

    def get_object(self, pk):
        try:
            return Tree.objects.filter(type=pk)
        except Tree.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # form = TreeForm.objects.get(id=pk)
        # trees = Tree.objects.filter(type__in=[i.type_tree for i in form])
        trees = self.get_object(pk)
        serializer = TreeSerializer(trees, many=True)
        return Response(serializer.data)


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DistrictByRegion(views.APIView):
    def get_object(self, pk):
        try:
            return District.objects.filter(region=pk)
        except District.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        shaharlar = self.get_object(pk)
        serializer = DistrictSerializer(shaharlar, many=True)
        return Response(serializer.data)


class MahallaByDistrict(views.APIView):
    def get_object(self, pk):
        try:
            return Mahalla.objects.filter(district=pk)
        except Mahalla.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        mahalla = self.get_object(pk)
        serializer = MahallaSerializer(mahalla, many=True)
        return Response(serializer.data)


class BlankPostView(generics.CreateAPIView):
    serializer_class = BlankSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        statistics_region = RegionStatistics.objects.get(region_id=serializer.data['region'])
        count = 0
        for i in serializer.data['trees']:
            count += i['amount']

        statistics_region.donated_trees += count
        statistics_region.donated_people += 1
        statistics_region.save(update_fields=['donated_people', 'donated_trees'])

        # user = InstagramUser(str(serializer.data['social_media_url']).split('/')[3], from_cache=True)
        # l=[]
        # for i in MostPlanted.objects.all():
        #    l.append(i.username)
        # if serializer.data['social_media_url'].split('/')[3] not in l:
        #     MostPlanted.objects.create(account_link=serializer.data['social_media_url'],image_url=user.user_data['profile_pic_url_hd'],username=user.user_data['username'],tree_amount=count)
        # else:
        #     most_planted = MostPlanted.objects.get(username=str(serializer.data['social_media_url']).split('/')[3])
        #     most_planted.image_url = user.user_data['profile_pic_url_hd']
        #     most_planted.tree_amount += count
        #     most_planted.save(update_fields=['image_url','tree_amount'])
        # print(serializer.data['social_media_url'].split('/')[4)
        data = serializer.data['social_media_url']
        username = data.split('/')[3]

        if data.split('/')[2] == 'www.instagram.com':
            print(type(username))
            get_feed(username=username, type=1, account_link=data, tree_amount=count)

        if data.split('/')[2] == "t.me":
            # print(data.split('/')[2])
            url = data
            session = HTMLSession()
            response = session.get(url)

            # response.html.render()

            content = response.html.html
            # print('CONTENT',content)
            y = response.html.find('.tgme_page_title', first=True).text
            # print('uuuuuuuuuuuuuuuuurl',y)

            soup = BeautifulSoup(content, "html.parser")
            print('eeeeeeeeeeeeerrrooooooooooorrrrr')
            images = soup.find_all("img")
            profile_picture_path = 'telegram/default.jpg'

            for img in images:
                src = img.get("src")
                print('dsafdsafsda', src)
                if src:
                    x = src
                    print('iiiiiiiiiimmmmm', x)
                    profile_picture_path = f'telegram/{username}.jpg'

                    urlretrieve(x, filename=os.path.join(settings.MEDIA_ROOT, profile_picture_path))
                    # urlretrieve(x, filename=os.path.join(settings.MEDIA_ROOT, profile_picture_path))

            user_model = MostPlanted.objects.get_or_create(username=username,
                                                           defaults={'name': y})
            user_model = user_model[0]
            user_model.image.name = profile_picture_path
            user_model.type = 4
            user_model.account_link = data
            if isinstance(user_model.tree_amount, int):
                user_model.tree_amount += count
            else:
                user_model.tree_amount = count
            user_model.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 45
    page_size_query_param = 'page_size'


# class LegalPagination(PageNumberPagination):
#     page_size = 4
#     page_size_query_param = 'page_size'

class LegalEntityView(generics.ListAPIView):
    queryset = LeganEntity.objects.all()
    serializer_class = LegalSerializer
    # pagination_class = StandardResultsSetPagination


class MostPlantedView(generics.ListAPIView):
    queryset = MostPlanted.objects.order_by('-tree_amount')[:40]
    serializer_class = MostPlantedSerializer
    # pagination_class = StandardResultsSetPagination


class IndexView(generics.RetrieveAPIView):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer

    def get_object(self):
        instance = self.queryset.first()

        return instance


class MenuListView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get(self, request, *args, **kwargs):
        menu = self.get_queryset()
        header = MenuSerializer(menu.filter(header=True), many=True).data
        footer = MenuSerializer(menu.filter(footer=True), many=True).data

        payload = {
            'header': header,
            'footer': footer,
        }
        return Response(payload, status=status.HTTP_200_OK)


class MenuFooterApiView(generics.RetrieveAPIView):
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer

    def get_object(self):
        instance = self.queryset.last()
        instance.menu_header = Menu.objects.filter(header=True)
        instance.menu_footer = Menu.objects.filter(footer=True)
        return instance


# class StatisticsApi(generics.RetrieveAPIView):
#     queryset = RegionStatistics.objects.all()
#     serializer_class = RegionSerializer
#     def get_object(self):
#         instance =


class RegionStatisticsApi(generics.ListAPIView):
    queryset = RegionStatistics.objects.all()
    serializer_class = RegionStatisticsSerializer


class StatisticsApi(generics.ListAPIView):
    queryset = RegionStatistics.objects.all()
    serializer_class = RegionStatisticsSerializer

    def get(self, request):
        x = {'donated_people': RegionStatistics.objects.aggregate(Sum('donated_people'))['donated_people__sum'],
             'donated_trees': RegionStatistics.objects.aggregate(Sum('donated_trees'))['donated_trees__sum'],
             'planted_trees': RegionStatistics.objects.aggregate(Sum('planted_trees'))['planted_trees__sum'],
             'on_plan_planting': RegionStatistics.objects.aggregate(Sum('on_plan_planting'))['on_plan_planting__sum']}
        return Response(x)


# static

class StaticPageView(generics.ListAPIView):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageSerializer


class StaticPageDetailView(generics.RetrieveAPIView):
    queryset = StaticPage
    serializer_class = StaticPageSerializer
    lookup_field = "slug"


class ContactFormView(generics.CreateAPIView):
    serializer_class = ContactFormSerializer


class ConnectionView(generics.RetrieveAPIView):
    queryset = Index.objects.all()
    serializer_class = ConnectionSerializer

    def get_object(self):
        instance = self.queryset.last()
        instance.footer = Footer.objects.last()

        return instance
