from django.db import models


class WithoutExcludedManager(models.Manager):

    def get_queryset(self):
        return super(WithoutExcludedManager, self).get_queryset().filter(excluded=False)

    def with_excluded(self):
        u"""
        Hack pra poder pegar os itens excluídos junto com os normais pelo manager padrão e por related manager.

        Funciona em código e nos templates.
        e.g.: instance.relatedmodel_set.with_excluded
        """
        return super(WithoutExcludedManager, self).get_queryset().filter(**self.core_filters)

    def only_excluded(self):
        u"""
        Hack pra poder pegar só os itens excluídos pelo manager padrão e por related manager.

        Funciona em código e nos templates.
        e.g.: instance.relatedmodel_set.only_excluded
        """
        return super(WithoutExcludedManager, self).get_queryset().filter(id=self.instance.id).filter(excluded=True)


class WithExcludedManager(models.Manager):

    def get_queryset(self):
        return super(WithExcludedManager, self).get_queryset().all()
