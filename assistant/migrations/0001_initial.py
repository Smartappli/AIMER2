from typing import ClassVar

from django.db import migrations
from pgvector.django import VectorExtension


class Migration(migrations.Migration):
    operations: ClassVar[list] = [
        VectorExtension()
    ]
