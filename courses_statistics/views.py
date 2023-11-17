from rest_framework.decorators import api_view
from rest_framework.response import Response

from courses_statistics.models import UserStatistics
from courses_statistics.serializers import UserStatisticsSerializer


@api_view(["GET"])
def get_statistics_data(request):
    stats = UserStatistics.objects.all()
    serializer = UserStatisticsSerializer(stats, many=True)
    return Response(serializer.data)
