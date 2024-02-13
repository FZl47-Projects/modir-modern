

# get course file path
def course_video_path(instance, path):
    course = instance.course.title
    return f'files/video/courses/{course}/{path}'


# get course file path
def introduction_video_path(instance, path):
    course = instance.title
    return f'files/video/courses/{course}/{path}'


# get course images path
def course_images_path(instance, path):
    course = instance.title
    return f'images/courses/{course}/{path}'
