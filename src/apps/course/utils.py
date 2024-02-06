

# get course file path
def course_video_path(instance, path):
    course = instance.course.title
    return f'files/video/courses/{course}/{path}'
