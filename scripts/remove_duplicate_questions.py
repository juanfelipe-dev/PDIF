from inspections.models import Question
from core.models import Organization
from collections import defaultdict

org = Organization.objects.first()
seen = set()
duplicates = []
for q in Question.objects.filter(organization=org):
    key = (q.text.strip().lower(), q.sort_order)
    if key in seen:
        duplicates.append(q)
    else:
        seen.add(key)
for dup in duplicates:
    print(f"Deleting duplicate: {dup.text} (sort_order={dup.sort_order})")
    dup.delete()
print(f"Removed {len(duplicates)} duplicate questions.")
