from storages.backends.s3boto3 import S3Boto3Storage

# 장고 MEDIA 파일을 다루는 각종 설정을 커스텀할 수 있습니다.
#  - "media" 폴더에 저장되도록 location 설정을 해줍니다.
#  - "public-read" 권한으로 업로드되도록 default_acl 설정을 해줍니다.
class AwsMediaStorage(S3Boto3Storage):
    location='media'
    default_acl='public-read'

class CustomS3Storage(S3Boto3Storage):
    location = 'media'  # 업로드된 파일이 저장될 S3 경로 설정

    def get_available_name(self, name, max_length=None):
        # 파일명을 안전한 형태로 인코딩하여 반환
        return super().get_available_name(name.encode('utf-8').decode('utf-8'), max_length)
