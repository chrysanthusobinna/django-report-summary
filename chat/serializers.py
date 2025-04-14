from rest_framework import serializers

class ChatRequestSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=10000)

    def validate_question(self, value):
        word_count = len(value.strip().split())
        if word_count > 2000:
            raise serializers.ValidationError("Question must not exceed 2000 words.")
        return value
