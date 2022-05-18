from rest_framework import serializers


class ArticleSerializer(serializers.Serializer):
    Bid = serializers.CharField()
    Aid = serializers.CharField()
    Title = serializers.CharField()
    Comments_Score = serializers.IntegerField()
    Author = serializers.CharField()
    Create_date = serializers.DateField()


class BoardSerializer(serializers.Serializer):
    BoardName = serializers.CharField(source='Bid')
    Header = serializers.CharField()
    Articles = ArticleSerializer(many=True)


class CommentSerializer(serializers.Serializer):
    Author = serializers.CharField()
    Comment = serializers.CharField()
    Score = serializers.IntegerField()


class ArticleDetailSerializer(ArticleSerializer):
    Bid = serializers.CharField()
    Aid = serializers.CharField()
    Title = serializers.CharField()
    Comments_Score = serializers.IntegerField()
    Author = serializers.CharField()
    Create_date = serializers.DateTimeField()
    Content = serializers.CharField()
    Comments = CommentSerializer(many=True)
