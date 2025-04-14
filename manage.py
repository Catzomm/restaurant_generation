import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lunch_chooser.settings')
    try:
        from django.core.management import execute_from_command_line
    except Exception as e:
        print("Ошибка:", e)
        sys.exit(1)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()