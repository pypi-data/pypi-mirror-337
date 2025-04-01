class Course:
    
    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f'{self.name} [{self.duration} horas] ({self.link})'

courses = [
        Course("Introduccion a Linux", 15, ''),
        Course('Personalizacion de Linux', 3, ''),
        Course('Introduccion al Hacking', 53, ''),
        ]

def list_courses():
    for course in courses:
        print(course)

def serch_course(name):
    for course in courses:
        if course.name == name:
            return course
    return None
