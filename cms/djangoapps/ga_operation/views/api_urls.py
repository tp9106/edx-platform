from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^delete_course$', 'cms.djangoapps.ga_operation.views.api.delete_course', name="delete_course"),
)