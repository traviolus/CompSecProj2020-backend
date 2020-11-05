from django.db import models
from users.models import CustomUser
from topics.models import Topic

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_text = models.TextField(null=False, blank=False)
    comment_createdtime = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(CustomUser, related_name='comments_user', on_delete=models.CASCADE)
    comment_topic = models.ForeignKey(Topic, related_name='comments_topic', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text + ' [in] ' + self.comment_topic.topic_header