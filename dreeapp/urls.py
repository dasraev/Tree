from django.urls import path
from .views import *

urlpatterns = [
    path('blank/', BlankPostView.as_view()),
    path('regions/', RegionListView.as_view()),
    path('district_by_region/<int:pk>', DistrictByRegion.as_view()),
    path('mahalla_by_district/<int:pk>', MahallaByDistrict.as_view()),
    path('treetypes/', TreeTypeListView.as_view()),
    path('tree_by_type/<int:pk>', TreeByTypeView.as_view()),
    path('most_planted/', MostPlantedView.as_view()),
    path('legal/', LegalEntityView.as_view()),
    path('index/', IndexView.as_view()),
    path('menu_footer/', MenuFooterApiView.as_view()),
    path('region_statistics/', RegionStatisticsApi.as_view()),
    path('statistics/', StatisticsApi.as_view()),
    path('static_list/', StaticPageView.as_view()),
    path('connection/', ConnectionView.as_view()),
    path('feedback/', ContactFormView.as_view()),
    path('static_detail/<slug:slug>', StaticPageDetailView.as_view()),
]
