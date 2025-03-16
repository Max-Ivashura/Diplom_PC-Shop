from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CommunityBuild, Comment, PCBuild
from .forms import CommunityBuildForm, CommentForm

@login_required
def publish_build(request, build_id):
    build = get_object_or_404(PCBuild, id=build_id, user=request.user)
    community_build = CommunityBuild.objects.create(
        user=request.user,
        pc_build=build,
        title=build.title,
        description=build.description,
        category='gaming'  # Пример, можно сделать выбор в форме
    )
    return redirect('community_build_detail', pk=community_build.pk)

def community_builds(request):
    builds = CommunityBuild.objects.filter(is_approved=True)
    return render(request, 'community/builds.html', {'builds': builds})

def community_build_detail(request, pk):
    build = get_object_or_404(CommunityBuild, pk=pk)
    comments = build.comment_set.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.build = build
            comment.user = request.user
            comment.save()
            return redirect('community_build_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'community/build_detail.html', {'build': build, 'comments': comments, 'form': form})