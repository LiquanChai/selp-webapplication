from django.conf.urls import patterns, include, url
import usermgt
from .views import QuizListView, CategoriesListView,\
    ViewQuizListByCategory,\
    QuizDetailView, QuizCreateView, QuizUpdateView,\
    add_category,quiz_answer,quiz_marks


urlpatterns = patterns('',
                    url(r'^add_category/$', add_category),
                    url(regex=r'^quiz_create/$', view=QuizCreateView.as_view(), name='quiz_create'),
                    url(r'^quiz_answer/(?P<pk>[\d-]+)/$', quiz_answer, name='quiz_answer'),
                    url(r'^rank/$', quiz_marks, name='quiz_marks'),
                    url(regex=r'^quiz_update/(?P<pk>[\d-]+)/$', view=QuizUpdateView.as_view(), name='quiz_update'),
                    url(regex=r'^quiz/$', view=QuizListView.as_view(), name='quiz_index'),
                    url(regex=r'^$', view=CategoriesListView.as_view(), name='quiz_category_list_all'),
                    url(regex=r'^category/(?P<category_name>[\w.-]+)/$', view=ViewQuizListByCategory.as_view(), name='quiz_category_list_matching'),
                    #  passes variable 'quiz_name' to quiz_take view
                    url(regex=r'^quiz/(?P<pk>[\d-]+)/$', view=QuizDetailView.as_view(), name='quiz_start_page'),
                    url(r'^accounts/', include('usermgt.urls')),
)
