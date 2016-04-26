class SuperUserAccessMixin():
    def get_queryset(self, request):
        if request.user.last_name == 'Олейник':
            return self.model.objects.all()

    def get_model_perms(self, request):
        if request.user.last_name == 'Олейник':
            return {'change': True, 'add': True, 'delete': True}
        else:
            return {'change': False, 'add': False, 'delete': False}
