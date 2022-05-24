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


class QueryParamsSerializer(serializers.Serializer):
    Title = serializers.CharField(required=False)
    Author = serializers.CharField(required=False)
    Score = serializers.IntegerField(required=False)

    Take = serializers.IntegerField()
    Skip = serializers.IntegerField()

    def validate(self, data):
        """
        At least has one param
        """

        title: str = data.get('Title')
        author: str = data.get('Author')
        score: int = data.get('Score')
        if not (title or author or score):
            raise serializers.ValidationError("Must has at least one param")

        if (not title.strip() and not author.strip()):
            raise serializers.ValidationError("Must has at least one param")

        return data
