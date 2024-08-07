from django.core.management.base import BaseCommand
from django.utils import timezone
from result_module.models import Students

class Command(BaseCommand):
    help = 'Update student numbers for existing records'

    def handle(self, *args, **kwargs):
        current_year = timezone.now().year
        prefix = f'S5502-{current_year}'

        students = Students.objects.all()
        for student in students:
            if not student.student_number:
                last_student = Students.objects.filter(student_number__startswith=prefix).order_by('student_id').last()
                if last_student:
                    last_serial = int(last_student.student_number.split('-')[-1])
                else:
                    last_serial = 0
                new_serial = last_serial + 1
                student.student_number = f'{prefix}-{new_serial:04d}'
                student.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated student numbers'))
