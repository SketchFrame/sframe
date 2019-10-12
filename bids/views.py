from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from .forms import PostProjectForm, BidProjectForm, BidUpdateForm
from users.models import UserExtended
from .models import project, Bids
from notifications.models import Notifications
from seller.decorators import seller_required
from seller.models import Seller
from django.utils import timezone

@login_required
def postProject(request):
    if request.method == 'POST':
        form = PostProjectForm(request.POST)
        if form.is_valid():
            postProject = form.save(commit=False)
            postProject.user = get_object_or_404(
                UserExtended, user__username=request.user.username)
            postProject.save()
            messages.success(request, 'Posted The Project')
            return redirect('/')
    else:
        form = PostProjectForm()

    return render(request, 'bids/post-project.html', {
        'form': form
    })


# @method_decorator([login_required, seller_required], name="dispatch")
class ProjectsListView(ListView):
    model = project
    template_name = "bids/project-list.html"
    ordering = ['-posted_date']

@method_decorator([login_required], name="dispatch")
class ProjectDeleteView(DeleteView):
    model = project
    template_name = "bids/delete-project.html"
    success_url = '/'


@method_decorator([login_required], name="dispatch")
class ProjectUpdateView(UpdateView):
    model = project
    fields = [
        'title',
        'category',
        'description',
        'budget',
    ]
    template_name = "bids/update-project.html"


@login_required
@seller_required
def makeBid(request, slug):
    try:
        bid = Bids.objects.get(Q(project__slug=slug) &
                            Q(user__user__user=request.user))
        return redirect('edit-bid', pk=bid.id)
    except ObjectDoesNotExist:
        if request.method == 'POST':
            print("Step")
            form = BidProjectForm(request.POST)
            if form.is_valid():
                postBid = form.save(commit=False)
                postBid.user = get_object_or_404(
                    Seller, user__user=request.user)
                postBid.project = get_object_or_404(project, slug=slug)
                postBid.save()
                messages.success(request, 'Bidded on the Project')
                return redirect('/')
        else:
            form = BidProjectForm()
    return render(request, 'bids/make-bid.html', {
        'form': form
    })

class ViewProject(DetailView):
    model = project
    context_object_name = "project"
    template_name = "bids/view-project-details.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bids'] = Bids.objects.filter(project__slug=self.kwargs['slug'])
        return context

@method_decorator([login_required, seller_required], name="dispatch")
class BidsUpdateView(UpdateView):
    model = Bids
    form_class = BidUpdateForm
    template_name = "bids/update-bid.html"


@method_decorator([login_required, seller_required], name="dispatch")
class BidsDeleteView(DeleteView):
    model = Bids
    form_class = BidUpdateForm
    template_name = "bids/delete-bid.html"


@login_required
def viewBidsOnProjects(request, slug):
    bids = Bids.objects.filter(project__slug=slug)
    # notification = Notifications.objects.filter(Q(bid__project__slug=slug) & Q(user__user=request.user))
    # notification.viewed = True
    # notification.save()
    return render(request, "bids/view-bids.html", {
        'bids': bids
    })


@login_required
def assignTo(request, username, slug):
    seller = Seller.objects.get(user__user__username=username)
    projectName = project.objects.get(slug=slug)
    projectName.is_assigned = True
    projectName.assignedTo = seller.user
    projectName.assignedOn = timezone.now()
    projectName.save()
    Notifications.objects.create(
        user=seller.user,
        title=f"Your bid on {projectName.title} has been selected.",
        description=f"{request.user.username} has assigned you for their project",
        bid=Bids.objects.get(Q(project__slug=slug) & Q(user=seller)),
        category="ProjectAssigned",
    )
    messages.success(request, f"Assigned to {seller.user.user.username}")
    return redirect('/')
