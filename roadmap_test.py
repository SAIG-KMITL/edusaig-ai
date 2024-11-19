from internal.roadmap_agent import generate_roadmap
from utils.mock_data import MockDataGenerator
import json
import traceback

# Initialize the mock data generator
mock_gen = MockDataGenerator()

# Generate sample user data
sample_user = mock_gen.generate_user_data()
print("\nSample User Data:")
print(json.dumps(sample_user, indent=2))

# Generate sample course data
sample_courses = mock_gen.generate_course_data(10)
print("\nSample Course Data: ", len(sample_courses))

try:
  roadmap = generate_roadmap(sample_user, sample_courses)
  print("\nGenerated and Validated Roadmap:")
  print(json.dumps(roadmap, indent=2))
except Exception as e:
  print(f"\nError generating roadmap: {str(e)}")
  print(f"Error type: {type(e)}")
  print(traceback.format_exc())