import hashlib

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible

def get_hash_path(content):
    h = hashlib.md5()
    for chunk in content.chunks():
        h.update(chunk)
    return h.hexdigest()

@deconstructible
class MediaFileSystemStorage(FileSystemStorage):
    #def get_valid_name(self, name, max_length=1250):
    #    print(name)
    #    return name

    def _save(self, name, content):
        h = get_hash_path(content)
        path = '{}/{}/{}/{}'.format(h[:2], h[2:4], h, name[2:])

        if self.exists(path):
            return path
        return super(MediaFileSystemStorage, self)._save(path, content)


class FileStorage(models.Model):
    # http://stackoverflow.com/questions/15885201/django-uploads-discard-uploaded-duplicates-use-existing-file-md5-based-check
    # curl -X POST -u 'oleynik@mosgmp.ru:123' -F 'fileupload=@Gruntfile.js;filename="Gruntfile.js"' -F 'uploader=66' http://127.0.0.1:8000/api/file/
    fileupload = models.FileField(max_length=400, storage=MediaFileSystemStorage())
    #name = models.CharField(max_length=100, blank=True)
    #md5_sum = models.CharField(max_length=32, blank=True)
    uploader = models.ForeignKey('authentication.Employee', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    #def save(self, *args, **kwargs):
    #    if not self.pk:
    #        self.name = self.fileupload.name
    #        h = hashlib.md5()
    #        for chunk in self.fileupload.chunks():
    #            h.update(chunk)
    #        self.md5_sum = h.hexdigest()
    #    return super(FileStorage, self).save(*args, **kwargs)
