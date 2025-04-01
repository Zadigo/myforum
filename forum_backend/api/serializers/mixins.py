class SerializerMixin:
    user = None

    def save(self, user=None, **kwargs):
        self.user = user
        return super().save(**kwargs)
