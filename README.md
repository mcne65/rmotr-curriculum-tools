# rmotr curriculum tools

rmotr_curriculum create_course "Advanced Python Programming" (optional uuid)

rmotr_curriculum create_unit PATH_TO_COURSE UNIT_NAME UNIT_ORDER

rmotr_curriculum create_lesson PATH_TO_UNIT LESSON_NAME LESSON_ORDER -t lesson-type

rmotr_curriculum remove_unit PATH_TO_UNIT
rmotr_curriculum remove_lesson PATH_TO_LESSON

rmotr_curriculum swap_units?

^Alias? create_reading_lesson, create_assignment_lesson, create_quizz

Casos:
 Add Unit con empty course
 Add Unit con not empty coures, appended at the end
 Add Unit in between
 Add lesson con empty unit
 Add lesson con not empty unit, at the end
 Add lesson in between
