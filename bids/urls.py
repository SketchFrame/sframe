from django.urls import path
from .views import(
    postProject,
    BidsDeleteView,
    makeBid,
    ProjectsListView,
    BidsUpdateView,
    viewBidsOnProjects,
    ProjectDeleteView,
    ProjectUpdateView,
    assignTo,
    ViewProject,
)

urlpatterns = [
    path('post/', postProject, name="post-bid"),
    path('view-projects/', ProjectsListView.as_view(), name="view-projects"),
    path('bid/<slug:slug>/', makeBid, name="make-bid"),
    path('update/bid/<int:pk>/', BidsUpdateView.as_view(), name="edit-bid"),
    path('delete/bid/<int:pk>', BidsDeleteView.as_view(), name="delete-bid"),
    path('view/bids/<slug:slug>/', viewBidsOnProjects,
         name="view-project-bids"),
    path('delete/<slug:slug>/', ProjectDeleteView.as_view(), name="delete-project"),
    path('update/<slug:slug>/', ProjectUpdateView.as_view(), name="update-project"),
    path('assign/<slug:slug>/<str:username>/',
         assignTo, name="assign-project"),
    path('view/<slug:slug>', ViewProject.as_view(), name="project-description"),
]
