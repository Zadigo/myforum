

from comments.models import Comment
from threads.models import SubThread
from django.shortcuts import get_object_or_404
from moderation.models import Report
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, Serializer


# class ReportSerializer(ModelSerializer):
#     class Meta:
#         model = Report
#         fields = ['reference']

#     def save(self, request, **kwargs):
#         thread = get_object_or_404(SubThread, id=self.validated_data.get('thread', None))
#         comment = get_object_or_404(Comment, id=self.validated_data.get('comment', None))
        
#         validated_data = self.validated_data.copy()
#         if thread is not None:
#             validated_data['thread'] = thread

#         if comment is not None:
#             validated_data['comment'] = comment

#         kwargs = {'user': request.user}
#         validated_data = validated_data | kwargs

#         if self.instance is not None:
#             self.instance = self.update(self.instance, validated_data)
#         else:
#             self.instance = self.create(validated_data)

#         if self.instance is None:
#             raise ValueError('update or create returned None')

#         return self.instance


class ReportSerializer(Serializer):
    thread = fields.IntegerField(required=False, allow_null=True)
    comment = fields.IntegerField(required=False, allow_null=True)
    tag = fields.IntegerField(required=False, allow_null=True)

    def _report_thread(self, thread_id, user):
        pass

    def _report_comment(self, comment_id, user):
        comment = get_object_or_404(Comment, id=comment_id)
        report = Report.objects.create(comment=comment, user=user)
        return report

    def save(self, user, **kwargs):
        thread = self.validated_data.get('thread', None)
        comment = self.validated_data.get('comment', None)

        if thread is not None:
            self._report_thread(thread, user)

        if comment is not None:
            self._report_comment(comment, user)
