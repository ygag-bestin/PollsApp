from rest_framework import serializers
from polls.models import Question, Choice, Comment


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text', 'votes']


class QuestionSerializer(serializers.ModelSerializer):
    # choice = serializers.StringRelatedField(many=True, read_only=True)
    choice = ChoiceSerializer(many=True, read_only=False)
    pub_date = serializers.DateTimeField(format="%d-%b-%Y",
                                         input_formats=['%d-%b-%Y',
                                                        'iso-8601'])
    expiry_date = serializers.DateTimeField(format="%d-%b-%Y",
                                            input_formats=['%d-%b-%Y',
                                                           'iso-8601'])

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'expiry_date', 'pub_date', 'added_by',
                  'choice']

    def create(self, validated_data):
        choice_validated_data = validated_data.pop('choice')
        question = Question.objects.create(**validated_data)
        choices_serializer = self.fields['choice']
        for each in choice_validated_data:
            each['question'] = question
        choice = choices_serializer.create(choice_validated_data)
        return question


class CommentSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(read_only=True,
                                          source='question.question_text')

    class Meta:
        model = Comment
        fields = ['id', 'email', 'body', "question_text", ]
