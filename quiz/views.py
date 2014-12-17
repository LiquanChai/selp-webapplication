import random
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect,render_to_response
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView, FormView
from django.core.urlresolvers import reverse
 
from .models import Quiz, Category, Progress 
from django.template import RequestContext
 
@login_required
def quiz_marks(request):
    # ranking ordered by total score/mark
    allp = Progress.objects.all()
    for p in allp:
        p.total_score = sum([x.pass_mark for x in p.score.all()])
        p.save()
    allp = Progress.objects.all().order_by('-total_score')
    return render_to_response('marks.html', RequestContext(request, {'allp': allp}))


@login_required
def add_category(request):
    try:
        if request.method == 'POST':
            category = request.POST.get('category', '').strip('"\' ')
        if category is None or category == '':
            raise Exception('Null category is not allowed')
        Category.objects.new_category(category)
        return HttpResponseRedirect(reverse('quiz_category_list_all'))

    except Exception, e:
        print e 
        return HttpResponseRedirect(reverse('quiz_category_list_all'))


@login_required
def quiz_answer(request,pk):
    # the controller to decide and show the correct answer
    try:
        c = Category.objects.get(id=pk)
        if request.session.get('cid', default=0) != pk:
            request.session['cid'] = pk
            request.session['qid'] = 0
        qid = request.session.get('qid', default=0)
        print qid, pk
        if request.method == 'GET':
            if qid == 0 :
                request.session['qid'] = 0
            if qid == 10 :
                request.session['qid'] = 0
                return render_to_response('single_complete.html', RequestContext(request, {'category': c, "status":False}))
            p, status = Progress.objects.get_or_create(user=request.user)
            p.save()
            nqs = Quiz.objects.filter(category=c).exclude(id__in=p.score.all().values_list('id', flat=True)).order_by('?')
            if len(nqs) == 0:
                return render_to_response('single_complete.html', RequestContext(request, {'category': c, "status":True}))
            else:
                nq = nqs[0]
            request.session['qid'] += 1
            return render_to_response('answer.html', RequestContext(request, {'quiz': nq}))
        else :
            # answer 
            qid = request.POST.get("qid")
            nq = Quiz.objects.get(id=qid)
            A = B = C = D = True
            if request.POST.get('A', '') == '':
                A = False
            if request.POST.get('B', '') == '':
                B = False
            if request.POST.get('C', '') == '':
                C = False
            if request.POST.get('D', '') == '':
                D = False
            print A,B,C,D, nq.A, nq.B, nq.C, nq.D # show choice again
            print (A == nq.A), (B == nq.B), (C == nq.C) ,  (D == nq.D)

            status = ((A == nq.A) and (B == nq.B) and (C == nq.C) and (D == nq.D))
            print status
            if status == True: # add score
                p, so = Progress.objects.get_or_create(user=request.user)
                p.save()
                p.score.add(nq)
                p.save()
            return render_to_response('answer_status.html', RequestContext(request, {'quiz': nq, 'status': status}))
    except Exception, e:
        print e 
        return HttpResponseRedirect(reverse('quiz_category_list_all'))

class QuizMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required('quiz.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)
        return queryset


class QuizListView(ListView):
    # list all quizess before start the category.
    model = Quiz

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.all()

class QuizCreateView(CreateView):
    # admin can create a new quiz.
    model = Quiz
    success_msg = "Quiz created!"


class QuizUpdateView(UpdateView):
    # the view let admin can change the quiz.
    model = Quiz
    def get_success_url(self):
        return reverse("quiz_start_page",
            kwargs={"pk": self.object.pk})

class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'pk'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CategoriesListView(ListView):
    # showing at the main page.
    model = Category


class ViewQuizListByCategory(ListView):
    #  showing the quizzes contained iin the category.
    model = Quiz
    template_name = 'view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            category=self.kwargs['category_name']
        )

        return super(ViewQuizListByCategory, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self).get_context_data(**kwargs)

        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCategory, self).get_queryset()
        return queryset.filter(category=self.category)


