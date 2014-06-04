from rest_framework import serializers
from rest_framework.reverse import reverse

from xmodule.modulestore.search import path_to_location

from courseware.courses import course_image_url
from student.models import CourseEnrollment, User


class CourseField(serializers.RelatedField):
    """Custom field to wrap a CourseModule object. Read-only.

    To invoke this from a model, you have to add a property to the model (say
    `course`) that returns an instance of the appropriate `CourseModule` object.
    """

    def to_native(self, course):
        course_id = course.id._to_string()
        request = self.context.get('request', None)
        if request:
            video_outline_url = reverse(
                'video-summary-list',
                kwargs={'course_id': course_id},
                request=request
            )
        else:
            video_outline_url = None

        return {
            "id": course_id,
            "name": course.display_name,
            "number": course.number,
            "org": course.display_org_with_default,
            "start": course.start,
            "end": course.end,
            "course_image": course_image_url(course),
            "latest_updates": {
                "video": None
            },
            "video_outline": video_outline_url
        }


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    course = CourseField()

    class Meta:
        model = CourseEnrollment
        fields = ('created', 'mode', 'is_active', 'course')
        lookup_field = 'username'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.Field(source='profile.name')
    course_enrollments = serializers.HyperlinkedIdentityField(
        view_name='courseenrollment-detail',
        lookup_field='username'
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'course_enrollments')
        lookup_field = 'username'
