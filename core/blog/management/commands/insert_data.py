from django.core.management.base import BaseCommand
from faker import Faker
from blog.models import Post, Category
from accounts.models import User
import random
from django.utils import timezone

class Command(BaseCommand):
    help = "Generate fake posts with random authors and categories"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.fake.unique.email(),
            password='mxgyuirt22ali',
            is_verified=True,
        )

        categories = []
        if not Category.objects.exists():
            for _ in range(3):
                categories.append(Category.objects.create(name=self.fake.word()))
        else:
            categories = list(Category.objects.all())
        for _ in range(5):
            post = Post.objects.create(
                title=self.fake.sentence(nb_words=5),
                content=self.fake.paragraph(nb_sentences=7),
                price=random.randint(10_000, 250_000),
                author=user,
                status=random.choice([True, False]),
                login_require=random.choice([True, False]),
                counted_view=random.randint(0, 200),
                published_date=self.fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc),
            )

            selected_categories = random.sample(categories, k=random.randint(1, len(categories)))
            post.category.set(selected_categories)
            post.save()

        self.stdout.write(self.style.SUCCESS("Post created."))
