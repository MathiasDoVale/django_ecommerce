#!/bin/bash
chmod +x wait-for-it.sh

# Wait for the database to be ready
./wait-for-it.sh db:5432 --timeout=30 --strict -- 

python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@gmail.com', 'admin')" | python manage.py shell

exec "$@"