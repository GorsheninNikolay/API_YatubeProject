from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, related_name='posts',
        blank=True, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings'
    )


"""
E:django.db.utils.IntegrityError: CHECK constraint failed: block_for_yourself
"""
#       class Meta:
#           constraints = [
#               models.CheckConstraint(
#                   check=~models.Q(user=models.F('following')),
#                   name='block_for_yourself'
#               ),
# Из-за UniqueConstraint pytest тоже не пропускает, однако
# UniqueConstraint работает и не позволяет создавать одинаковые
# Подписки
"""
django.db.utils.IntegrityError:
UNIQUE constraint failed: api_follow.user_id, api_follow.following_id
"""
#           models.UniqueConstraint(
#               fields=['user', 'following'], name='unique_follow'
#           ),
#        ]
