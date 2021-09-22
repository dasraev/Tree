from rest_framework import serializers
from . import models
from .models import TreeBlank


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = '__all__'


class MahallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mahalla
        fields = '__all__'


class TreeTypeSeriliazer(serializers.ModelSerializer):
    class Meta:
        model = models.TreeType
        fields = '__all__'


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tree
        fields = '__all__'


class TreeBlankSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TreeBlank
        fields = ['id', 'amount', 'tree', ]


class BlankSerializer(serializers.ModelSerializer):
    trees = TreeBlankSerializer(many=True)

    class Meta:
        model = models.Blank
        fields = ['region', 'district', 'mahalla', 'social_media_url', 'payment_type', 'trees', ]

    def create(self, validated_data):
        trees = validated_data.pop('trees')
        blank = models.Blank.objects.create(**validated_data)
        sum = 0
        for tree in trees:
            print(tree['amount'])
            treeblank = models.TreeBlank.objects.create(**tree, blank=blank)
            treeblank.save()

        return blank


class LegalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeganEntity
        fields = '__all__'


class MostPlantedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MostPlanted
        fields = '__all__'


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Index
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        exclude = ['footer', 'header']


class FooterSerializer(serializers.ModelSerializer):
    menu_header = MenuSerializer(many=True)
    menu_footer = MenuSerializer(many=True)

    class Meta:
        model = models.Footer
        exclude = ['address_link']
        # fields = '__all__'


class RegionStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegionStatistics
        fields = ['id', 'region', 'image', 'donated_people', 'planted_trees', 'on_plan_planting']


class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaticPage
        fields = ('id', 'title', 'slug', 'content')


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactForm
        exclude = ['created_at']


class FooterSerializer2(serializers.ModelSerializer):
    # phone = serializers.CharField(max_length=30)
    # mail = serializers.EmailField(max_length=30)
    # full_address = serializers.CharField(max_length=100)
    class Meta:
        model = models.Footer
        # fields = '__all__'
        fields = ['phone', 'mail', 'full_address', 'address_link']


class ConnectionSerializer(serializers.ModelSerializer):
    footer = FooterSerializer2()

    class Meta:
        model = models.Index
        # fields = '__all__'
        fields = ['s2_description', 's3_title', 's3_btn_text', 's3_slug', 'footer']
