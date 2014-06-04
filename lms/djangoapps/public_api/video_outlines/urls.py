"""
A block basically corresponds to a usage ID in our system.

"""
from django.conf.urls import patterns, url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import VideoSummaryList

urlpatterns = patterns('public_api.video_outlines.views',
    url(r'^(?P<course_id>[^/]*)$', VideoSummaryList.as_view(), name='video-summary-list'),
#    url(
#        r'^(?P<username>\w+)/course_enrollments/$',
#        UserCourseEnrollmentsList.as_view(),
#        name='courseenrollment-detail'
#    ),
)

