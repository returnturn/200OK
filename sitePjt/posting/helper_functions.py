from friendship.helper_functions import checkFriendship, getAllFriends
from django.db.models.functions import Cast
import datetime
from django.db.models import DateTimeField
from .models import Post, Comment
from accounts.models import ServerNode
from accounts.models import Author,ServerNode
import requests
from requests.auth import HTTPBasicAuth
from .serializers import AuthorSerializer, PostSerializer, CommentSerializer, PostListSerializer, PostCreateSerializer
from django.utils.dateparse import parse_datetime
from django.core import serializers
import json
from django.utils import timezone


#helper funciton
'''
    get all visible posts, depends on the state of current user

    POST_VISIBILITY = (
    ('PUBLIC', 'Public'),
    ('PRIVATE', 'Prviate to self'),
    ('FRIENDS', 'Private to friends'),
    ('FOAF', 'Private to friends of friends'),
    ('SERVERONLY', 'Private to local friends'),
    )

'''

def getVisiblePosts(requester, author=None):
    result = []
    #the current user hasn't login yet, show some random public posts
    if requester.is_anonymous:
        if author:
            return Post.objects.filter(author=author, visibility='PUBLIC', unlisted=False).order_by('-published')
        else:
            return Post.objects.filter(visibility='PUBLIC', unlisted=False).order_by('-published')

    #only check one author's posts or all posts
    if author:
        posts = Post.objects.filter(author=author, unlisted=False).order_by('-published')
    else:
        posts = Post.objects.filter(unlisted=False).order_by('-published')

    for post in posts:
        if post.author == requester:  # my post
            result.append(post)
        elif post.visibility == 'PUBLIC':  # everyone can see's post
            result.append(post)
        elif post.visibility == 'FRIENDS':  # if friends then append this post
            if checkFriendship(post.author.id, requester.id):
                result.append(post)
        elif post.visibility == 'FOAF':  # friends of friends also can see
            if checkFriendship(post.author.id, requester.id):
                result.append(post)
            else:
                for friend in getAllFriends(post.author.id):
                    if checkFriendship(friend.friend_id, requester.id):
                        result.append(post)
        elif post.visibility == 'SERVERONLY':  # requires to be local friends
            if post.author.host == requester.host:
                result.append(post)
            print("SERVERONLY unimplemented.")
    if author == requester:
        unlisted_posts = Post.objects.filter(author=author, unlisted=True)
        for post in unlisted_posts:
            result.append(post)

    return result

def getRemotePublicPosts():
    remote_posts = []
    nodes = ServerNode.objects.all()

    if not nodes.exists(): 
        return remote_posts

    for node in nodes:
        url = node.host_url
        url += 'posts'
        response = requests.get(url, auth=(node.server_username, node.server_password))
       
        if response.status_code == 200:
            remote_public_posts =response.json()
            for item in remote_public_posts['posts']:
                #Get 
                #everything is a string up to here
                '''   
                serializer = PostCreateSerializer(data=item, context=item)
                if serializer.is_valid():
                    remote_posts.append(Post(**serializer.data))
                '''
                post = PostSerializer(data=item)
                if post.is_valid():
                    #print(post.validated_data)
                    author = Author(**item.get('author'))
                    author.id = findAuthorIdFromUrl(item.get('author')['url'])
                    published = parse_datetime(item['published'])
                    post = Post(**post.validated_data)
                    post.id = item['id']
                    post.published = published
                    post.author = author
                    remote_posts.append(post)
                else:
                    author = getJsonDecodeAuthor(item['author'])
                    post = getJsonDecodePost(item)
                    post.author = author
                    remote_posts.append(post)

        else:
            print(response.json())

    return remote_posts

def getNodePostComment(post_id,node):
    #TODO: Error Handle
    remote_comments = []
    url = node[0].host_url
    url = url +'posts/{}/comments/'.format(str(post_id))
    response = requests.get(url, auth=(node[0].server_username, node[0].server_password))
    if response.status_code == 200:
        remote_comments_data = response.json()
        for item in remote_comments_data['comments']:
            #author.id = findAuthorIdFromUrl(item.get('author')['url'])
            comment = CommentSerializer(data=item)
            if comment.is_valid():
                comment = Comment(**comment.validated_data)
                published = parse_datetime(item['published'])
                author = Author(**item.get('author'))
                comment.id = item['id']
                comment.published = published
                comment.author = author
                remote_comments.append(comment)
            else:
                comment = getJsonDecodeComment(item)
                remote_comments.append(comment)

    return remote_comments  
    
def getNodePost(post_id,node):
    post = None
    url = node[0].host_url
    url = url +'posts/{}/'.format(str(post_id))
    response = requests.get(url, auth=(node[0].server_username, node[0].server_password))
    #TODO: Error Handle
    if response.status_code == 200:  
        remote_post =response.json()
        if 'post' in remote_post.keys():
            remote_post = remote_post['post']
        post = PostSerializer(data=remote_post)
        if post.is_valid():
            post = Post(**post.validated_data)
            author = Author(**remote_post.get('author'))
            author.id = findAuthorIdFromUrl(remote_post.get('author')['url'])
            published = parse_datetime(remote_post['published'])
            post.id = remote_post['id']
            post.published = published
            post.author = author
        else:
            author = getJsonDecodeAuthor(remote_post['author'])
            post = getJsonDecodePost(remote_post)
            post.author = author

    return post

#TODO: Need To handle post
def postNodePostComment(comment_data,node=None):
    author = {
        'id':comment_data.author.url,
        'host':comment_data.author.host,
        'displayName':comment_data.author.displayName,
        'url':comment_data.author.url,
        'github':comment_data.author.github,
    }
    comment ={
        'author':author,
        'comment':comment_data.comment,
        'contentType':comment_data.contentType,
        'published':str(timezone.now()),
        'id':str(comment_data.id)
    }
    body = {
        'query':'addComment',
        'post':comment_data.post.origin,
        'comment':comment
    }
    #response = requests.get(url, auth=(user, pwd))
    print(body)
    node = ServerNode.objects.all()
    url = node[0].host_url
    post_id = body['post'].split('/')[-2]
    url = url + 'posts/{}/comments/'.format(str(post_id))
    response = requests.post(url, json=body, auth=(
        node[0].server_username, node[0].server_password))

#TODO: Not Finish Yet, Waiting for friendship
def getNodeAuthorPosts(author_id,Node=None):
    user = '5000@remote.com'
    pwd = '1'
    #Try request from remote server
    url = 'http://127.0.0.1:5000/service/author/{}/posts/'.format(str(author_id))
    response = requests.get(url, auth=(user, pwd))
    authorPosts = None
    if response.status_code == 200:
        remote_author_posts = response.json()
        print(remote_author_posts)

def findAuthorIdFromUrl(url):
    if url[-1] == '/':
        idx = url[:-1].rindex('/')
        return url[idx+1:-1]
    else:
        idx = url.rindex('/')
        return url[idx+1:]

def getJsonDecodeAuthor(remote_author):
    author = Author()
    author.id = findAuthorIdFromUrl(remote_author['url'])
    author.url = remote_author['url'] if 'url' in remote_author.keys() else 'None'
    author.displayName = remote_author['displayName'] if 'displayName' in remote_author.keys() else 'None'
    author.bio =  remote_author['bio'] if 'bio' in remote_author.keys() else 'None'
    author.host = remote_author['host'] if 'host' in remote_author.keys() else 'None'
    author.github = remote_author['github'] if 'github' in remote_author.keys() else 'None'
    author.date_joined = remote_author['date_joined'] if 'date_joined' in remote_author.keys() else 'None'
    author.last_login = remote_author['last_login'] if 'last_login' in remote_author.keys() else 'None'
    return author

def getJsonDecodeComment(remote_comment):
    comment = Comment()
    comment.comment = remote_comment['comment'] if 'comment' in remote_comment.keys() else 'None'
    comment.author = getJsonDecodeAuthor(remote_comment['author']) if 'author' in remote_comment.keys() else 'None'
    comment.id = remote_comment['id'] if 'id' in remote_comment.keys() else 'None'
    comment.contentType = remote_comment['contentType'] if 'contentType' in remote_comment.keys() else 'None'
    comment.published = parse_datetime(remote_comment['published']) if 'published' in remote_comment.keys() else 'None'
    return comment
   

def getJsonDecodePost(remote_post):
    post = Post()
    post.title=remote_post['title'] if 'title' in remote_post.keys() else 'None'
    post.source=remote_post['source'] if 'source' in remote_post.keys() else 'None'
    post.origin=remote_post['origin'] if 'origin' in remote_post.keys() else 'None'
    post.contentType=remote_post['contentType'] if 'contentType' in remote_post.keys() else 'None'
    post.content=remote_post['content'] if 'content' in remote_post.keys() else 'None'
    post.categories=remote_post['categories'] if 'categories' in remote_post.keys() else 'None'
    post.published = parse_datetime(remote_post['published']) if 'published' in remote_post.keys() else 'None'
    post.id=remote_post['id'] if 'id' in remote_post.keys() else 'None'
    post.visibility=remote_post['visibility'] if 'visibility' in remote_post.keys() else 'None'
    post.unlisted=remote_post['unlisted'] if 'count' in remote_post.keys() else 'None'
    #post.count=remote_post['count'] if 'count' in remote_post.keys() else 'None'
    #post.size=remote_post['size'] if 'size' in remote_post.keys() else 'None'
    #post.next=remote_post['next'] if 'next' in remote_post.keys() else 'None'
    #post.description=remote_post['description'] if 'description' in remote_post.keys() else 'None'
    return post
    #TODO:visibleTo
