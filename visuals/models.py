from django.db import models

from timelines.models import Timeline

class KeyPhoto(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE, related_name="keyphotos")
    tpos = models.PositiveIntegerField(db_index=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, validators=[MinValueValidator(0), MaxValueValidator(500)])

    s3_id = models.CharField(max_length=512, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['timeline', 'tpos'], name='unique_keyphoto_timeline_pos')]
        ordering = ["timeline", "tpos"]
        db_table = "KeyPhoto"

        verbose_name = "KeyPhoto"
        verbose_name_plural = "KeyPhotos"


        def __str__(self):
            return f"KeyPhoto {self.id} (Timeline {self.timeline_id}, pos={self.tpos})"

class Transition(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE, related_name="transitions")
    tpos = models.PositiveIntegerField(db_index=True)

    from_keyphoto = models.ForeignKey("KeyPhoto", on_delete=models.SET_NULL, related_name="next_transition", null=True)
    to_keyphoto = models.ForeignKey("KeyPhoto", on_delete=models.SET_NULL, related_name="prev_transition", null=True)

    s3_id = models.CharField(max_length=512, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['timeline', 'tpos'], name='unique_transition_timeline_pos')]
        ordering = ["timeline", "tpos"]
        db_table = "Transition"

        verbose_name = "Transition"
        verbose_name_plural = "Transitions"

        def __str__(self):
            return (
                f"Transition {self.id} "
                f"(Timeline {self.timeline_id}, pos={self.tpos}, "
                f"from {self.from_keyphoto_id}, to {self.to_keyphoto_id})"
            )