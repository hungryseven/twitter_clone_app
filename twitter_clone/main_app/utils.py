from tweets.forms import TweetForm

class DataMixin:
    '''Общий миксин с данными, которые используются на каждой странице (например, форма для твитов).'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TweetForm()
        return context