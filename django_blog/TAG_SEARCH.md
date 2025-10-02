Tagging & Search - django_blog

Tagging:
- Add comma-separated tags in the "Tags" input when creating or editing a post.
- Tags are normalized to lowercase and deduplicated.
- Click a tag to view all posts with that tag: /tags/<tag_name>/

Search:
- Use the search box in the header to query title, content, or tags.
- Search URL example: /search/?q=django

Notes:
- New tags are auto-created.
- If you need tag slugs or advanced tag features, consider using django-taggit in future.
