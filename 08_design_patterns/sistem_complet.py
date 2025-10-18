# SISTEM COMPLET cu toate pattern-urile!

# 1. SINGLETON - Logger Global
class SystemLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message):
        import datetime
        entry = {
            'timestamp': datetime.datetime.now().strftime('%H:%M:%S'),
            'message': message
        }
        self.logs.append(entry)
        print(f"[LOG {entry['timestamp']} {message}")


# 2. FACTORY - User Factory
class UserFactory:
    @staticmethod
    def create_user(role, nume, email):
        if role == "student":
            return Student(nume, email)
        elif role == "instructor":
            return Instructor(nume, email)
        elif role == "admin":
            return Admin(nume, email)
        else:
            raise ValueError(f"Rol necunoscut: {role}")


class User:
    def __init__(self, nume, email):
        self.nume = nume
        self.email = email


class Student(User):
    def __init__(self, nume, email):
        super().__init__(nume, email)
        self.cursuri_inscrise = []


class Instructor(User):
    def __init__(self, nume, email):
        super().__init__(nume, email)
        self.cursuri_create = []


class Admin(User):
    def __init__(self, nume, email):
        super().__init__(nume, email)
        self.permisiuni = ['create', 'read', 'update', 'delete']


# 3. BUILDER - Course Builder
class CourseBuilder:
    def __init__(self):
        self.course = {
            'title': '',
            'instructor': '',
            'duration': 0,
            'difficulty': 'Începător',
            'topics': [],
            'has_quiz': False,
            'has_certificate': False,
            'price': 0
        }
        self.logger = SystemLogger()  # Singleton!

    def set_title(self, title):
        self.course['title'] = title
        self.logger.log(f"Titlu setat: {title}")
        return self

    def set_instructor(self, instructor):
        self.course['instructor'] = instructor
        self.logger.log(f"Instructor setat: {instructor}")
        return self

    def set_duration(self, hours):
        self.course['duration'] = hours
        self._calculate_price()
        self.logger.log(f"Durată setată: {hours} ore")
        return self

    def add_topic(self, topic):
        if topic not in self.course['topics']:
            self.course['topics'].append(topic)
            self.logger.log(f"Subiect adăugat: {topic}")
        return self

    def _calculate_price(self):
        """Calculează prețul automat"""
        base_price = self.course['duration'] * 50

        if self.course['difficulty'] == 'Intermediar':
            base_price *= 1.5
        elif self.course['difficulty'] == 'Avansat':
            base_price *= 2

        if self.course['has_quiz']:
            base_price += 100
        if self.course['has_certificate']:
            base_price += 200

        self.course['price'] = int(base_price)

    def build(self):
        self._calculate_price()
        self.logger.log(f"Curs finalizat: {self.course['title']}")
        return self.course.copy()


# UTILIZARE - toate pattern-urile împreună:
def main():
    # Singleton logger
    logger = SystemLogger()

    # Factory pentru utilizatori
    factory = UserFactory()
    instructor = factory.create_user("instructor", "Prof. Ana", "ana@academy.com")
    student = factory.create_user("student", "Ion Student", "ion@student.com")

    # Builder pentru curs
    course = (CourseBuilder()
              .set_title("Python Fundamentals")
              .set_instructor("Prof. Ana")
              .set_duration(10)
              .add_topic("Variables")
              .add_topic("Functions")
              .add_topic("OOP")
              .build())

    print(f"Curs creat: {course}")

    # Toate log-urile sunt în aceeași instanță!
    for log in logger.logs:
        print(f"📝 {log['timestamp']}: {log['message']}")


if __name__ == "__main__":
    main()