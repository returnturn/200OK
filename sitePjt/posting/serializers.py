from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment
from accounts.models import Author
from accounts.serializers import AuthorSerializer
from django.utils.dateparse import parse_datetime


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')
    published = serializers.SerializerMethodField('get_published')
    id = serializers.SerializerMethodField('get_id')
    unlisted = serializers.SerializerMethodField('get_unlisted')

    class Meta:
        model = Post
        #get source field done plz..
        fields = ('title', 'source', 'origin', 'contentType', 'content',
                  'author', 'categories', 'published', 'id', 'visibility',
                  'unlisted',
                  )

    def get_author(self, obj):
    	return Author(**self.context['author'])
    
    def get_unlisted(self, obj):
    	return self.context['unlisted'] == 'True'
    
    def get_id(self, obj):
    	return self.context['id']
    
    def get_published(self, obj):
    	return parse_datetime(self.context['published'])

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = Post
        #get source field done plz..
        fields = ('title', 'source', 'origin', 'contentType', 'content',
                  'author', 'categories', 'published', 'id', 'visibility',
                  'unlisted'
                  )

    def get_author(self, obj):
    	return AuthorSerializer(obj.author).data

    def create(self, validated_data):
        validated_data['author'] = self.context.get('author')
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.source = validated_data.get('source', instance.source)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.content = validated_data.get('content', instance.content)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.published = validated_data.get('published', instance.published)
        instance.id = validated_data.get('id', instance.id)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.author = self.context.get('author')
        instance.save()
        return instance


class PostListSerializer(serializers.Serializer):
    query = serializers.SerializerMethodField('get_query')
    count = serializers.SerializerMethodField('get_count')
    posts = serializers.SerializerMethodField('get_posts')

    class Meta:
        fields = ('query', 'count', 'posts')

    def get_query(self, obj):
        return self.context.get('query')

    def get_count(self, obj):
        return self.context.get('count')

    def get_posts(self, obj):
        return PostSerializer(obj, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')
    post = serializers.SerializerMethodField('get_post')

    def get_author(self, obj):
	    return AuthorSerializer(obj.author).data
    
    def get_post(self, obj):
	    #return PostSerializer(obj.post).data
        return obj.post.id

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType', 'published', 'id', 'post')
    
    def create(self, validated_data):
        validated_data['author'] = self.context.get('author')
        validated_data['post'] = self.context.get('post')
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.published = validated_data.get('published', instance.published)
        instance.id = validated_data.get('id', instance.id)
        instance.author = self.context.get('author', instance.author)
        instance.post = self.context.get('post', instance.post)
        instance.save()
        return instance