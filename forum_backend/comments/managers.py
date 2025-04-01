from django.db.models import QuerySet

class CommentManager(QuerySet):
    def earlist(self):
        pass

    def latest(self):
        pass

    def between(self, a, b):
        pass

    def non_muted(self, muted_users):
        pass

    def average_thread_content(self, thread_id):
        pass

    def average_user_word_content(self, user_id):
        """
        The average amount of words written by the user
        on the forum. This is useful for awards and determining
        user's standings on the forum
        """

    def user_standing(self, user_id):
        """
        Determines the user's standing on the forum based
        on the amount of content written on the forum
        """
        standings = {
            'beginner': [0, 50],
            'sophomore': [51, 300],
            'elite': [301, 2000],
            'finale': [2000, 400000]
        }
        
        # Average content written / coefficient
        averages = [
            ((0, 100), .1),
            ((101, 300), .4),
            ((301, 40000), 1)
        ]
