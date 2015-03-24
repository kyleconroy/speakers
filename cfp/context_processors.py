from cfp.models import Profile


def empty_profile(request):
    if request.user.is_authenticated():
        profile = Profile.generate(request.user)
        return {'empty_profile': profile.is_empty()}
    return {}
