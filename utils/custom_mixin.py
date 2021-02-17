from rest_framework import serializers

class QuerySetFilterMixin(object):
    def get_queryset(self):
        # This query is okay for Organization user
        # this query return data based on created by and mapped to related organization
        # queryset = super().get_queryset().filter(created_by__profile__organization_id=self.request.user.profile.organization)
        return queryset

    def perform_create(self, serializer):
        serializer.created_by = self.request.user
        serializer.updated_by = self.request.user
        serializer.save()

    def perform_update(self, serializer):
        serializer.updated_by = self.request.user
        serializer.save()


class CustomBaseSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        validated_data['updated_by'] = self.updated_by

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            validated_data['created_by'] = self.created_by
            self.instance = self.create(validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance