import random
from typing import List, Dict
from datetime import datetime, timedelta

class MockDataGenerator:
  def __init__(self):
      self.universities = [
          "MIT", "Stanford", "Harvard", "Berkeley", "Oxford",
          "Cambridge", "Tokyo University", "ETH Zurich",
          "CalTech", "Princeton", "Yale", "Columbia",
          "University of Toronto", "Imperial College London",
          "National University of Singapore", "TU Munich"
      ]
      
      self.departments = [
          "Computer Science", "Data Science", "Software Engineering",
          "Information Technology", "Artificial Intelligence",
          "Cybersecurity", "Web Development", "Robotics",
          "Computer Engineering", "Information Systems",
          "Digital Innovation", "Game Development",
          "Business Analytics", "Cloud Computing"
      ]
      
      self.interests = [
          "Programming", "AI/ML", "Web Development", "Data Science",
          "Cloud Computing", "Cybersecurity", "Mobile Development",
          "DevOps", "Blockchain", "IoT", "Quantum Computing",
          "AR/VR", "Natural Language Processing", "Computer Vision",
          "Robotics", "Big Data", "Full Stack Development",
          "UI/UX Design", "System Architecture", "Microservices"
      ]
      
      self.course_topics = [
          "Python Programming", "Java Development", "Web Development",
          "Machine Learning", "Data Structures", "Algorithms",
          "Cloud Architecture", "Network Security", "Database Management",
          "Software Engineering", "JavaScript Fundamentals",
          "React Development", "Node.js Backend", "DevOps Practices",
          "Docker & Kubernetes", "AWS Cloud Services", "Azure Cloud",
          "Blockchain Development", "iOS Development", "Android Development"
      ]
      
      self.skill_levels = ["Beginner", "Intermediate", "Advanced"]
      
      self.course_durations = ["2 weeks", "4 weeks", "6 weeks", "8 weeks", "10 weeks"]

  def generate_user_data(self, num_users: int = 1) -> List[Dict]:
      users = []
      for i in range(num_users):
          user = {
              "userID": f"U{random.randint(1000, 9999)}",
              "name": f"User_{random.randint(100, 999)}",
              "age": random.randint(18, 45),
              "university": random.choice(self.universities),
              "department": random.choice(self.departments),
              "interest": random.sample(self.interests, k=random.randint(2, 4)),
              "preTestScore": random.randint(40, 100),
              "preTestDescription": self._generate_pretest_description()
          }
          users.append(user)
      return users[0] if num_users == 1 else users

  def generate_course_data(self, num_courses: int = 10) -> List[Dict]:
      courses = []
      for i in range(num_courses):
          course = {
              "courseID": f"CS{random.randint(100, 999)}",
              "courseName": random.choice(self.course_topics),
              "courseDescription": self._generate_course_description(),
              "courseLevel": random.choice(self.skill_levels),
              "duration": random.choice(self.course_durations),
              "lastUpdated": self._generate_random_date()
          }
          courses.append(course)
      return courses

  def _generate_pretest_description(self) -> str:
      strengths = random.sample([
          "programming fundamentals",
          "problem-solving skills",
          "analytical thinking",
          "mathematical concepts",
          "logical reasoning",
          "data structures",
          "algorithm design",
          "software design patterns",
          "database concepts",
          "web technologies"
      ], k=random.randint(1, 2))
      
      weaknesses = random.sample([
          "advanced algorithms",
          "system design",
          "database optimization",
          "security concepts",
          "architectural patterns",
          "distributed systems",
          "cloud architecture",
          "performance optimization",
          "scalability concepts",
          "microservices"
      ], k=random.randint(1, 2))
      
      return f"Strong in {', '.join(strengths)}. Needs improvement in {', '.join(weaknesses)}."

  def _generate_course_description(self) -> str:
      descriptions = [
          "A comprehensive course covering fundamental concepts and practical applications.",
          "An in-depth exploration of advanced topics with hands-on projects.",
          "Learn essential skills through interactive lectures and real-world examples.",
          "Master core concepts through practical exercises and case studies.",
          "Develop professional-grade skills with industry-standard tools and practices.",
          "A project-based learning experience with real-world applications.",
          "Gain practical experience through hands-on workshops and assignments.",
          "Learn from industry experts with real-world case studies.",
          "Build your portfolio with practical projects and assignments.",
          "Master the latest technologies and best practices in the industry."
      ]
      return random.choice(descriptions)

  def _generate_random_date(self) -> str:
      end_date = datetime.now()
      start_date = end_date - timedelta(days=365)
      random_date = start_date + timedelta(days=random.randint(0, 365))
      return random_date.strftime("%Y-%m-%d")
 

# # Initialize the mock data generator
# mock_gen = MockDataGenerator()

# # Generate sample user data
# sample_user = mock_gen.generate_user_data()
# print("\nSample User Data:")
# print(json.dumps(sample_user, indent=2))

# # Generate sample course data
# sample_courses = mock_gen.generate_course_data(20)
# print("\nSample Course Data: ", len(sample_courses))
# print("\nSample Course Data:")
# print(json.dumps(sample_courses, indent=2))