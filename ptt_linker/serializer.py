from rest_framework import serializers


class ArticleSerializer(serializers.Serializer):
    Bid = serializers.CharField()
    Aid = serializers.CharField()
    Title = serializers.CharField()
    Comments_Score = serializers.IntegerField()
    Author = serializers.CharField()
    Create_date = serializers.CharField()
    Link = serializers.CharField(source="ArticleLink")


class BoardSerializer(serializers.Serializer):
    BoardName = serializers.CharField(source='Bid')
    Header = serializers.CharField()
    Article_Count = serializers.SerializerMethodField()
    Articles = ArticleSerializer(many=True)

    def get_Article_Count(self, obj):
        return len(obj.Articles)


class CommentSerializer(serializers.Serializer):
    Author = serializers.CharField()
    Comment = serializers.CharField()
    Score = serializers.IntegerField()


class ArticleDetailSerializer(serializers.Serializer):
    Bid = serializers.CharField()
    Aid = serializers.CharField()
    Title = serializers.CharField()
    Comments_Score = serializers.IntegerField()
    Author = serializers.CharField()
    Create_date = serializers.DateTimeField()
    Content = serializers.CharField()
    Comments = CommentSerializer(many=True)
