from django.db import models

class Tag(models.Model) :
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length = 20)

    def __str__(self) :
        return self.tag_name
        