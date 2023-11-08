from rest_framework.response import Response
from ..serializers import *
from ..models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
import pandas as pd

class RankView(APIView):
    """
    랭킹 view
    """
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        members = UserInfoSerializer(CustomUser.objects.all(), many = True).data
        user_pk = self.request.user.pk

        df = pd.DataFrame(members)

        df['rank'] = df['point'].rank(ascending=False, method = 'min').astype(int)

        df = df.sort_values(by = 'rank')

        result = df[['rank', 'id', 'nickname', 'profile_image', 'point']].to_dict(orient = 'records')

        return Response(result)