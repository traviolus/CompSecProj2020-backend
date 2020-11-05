from django.db import models
from users.models import CustomUser
from tags.models import Tag

class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_header = models.CharField(max_length = 50)
    topic_body = models.TextField(blank=True, null=True)
    topic_tag = models.ManyToManyField(Tag, related_name='topics_tag')
    topic_createdtime = models.DateTimeField(auto_now_add=True)
    topic_lastmodified = models.DateTimeField(blank=True, null=True)
    topic_user = models.ForeignKey(CustomUser, related_name='topics_user', on_delete=models.CASCADE)

    def __str__(self):
        return self.topic_header + ' : ' + self.topic_user.user_name
    
    def get_tag_name(self):
        return Tag.objects.filter(topics_tag=self).values_list('tag_name', flat=True)

    def get_user_name(self):
        return CustomUser.objects.get(topics_user=self).user_name