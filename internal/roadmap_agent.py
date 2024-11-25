from typing import List, Dict, Any, TypedDict
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    user_data: Dict[str, Any]
    courses: List[Dict[str, Any]]
    messages: List[Any]
    roadmap: Dict[str, Any]
    validated_roadmap: Dict[str, Any]

# Initialize LLM
llm = ChatOpenAI(
  model=os.getenv('SAIG_LLM_MODEL'),
  base_url=os.getenv('SAIG_LLM_URL'),
  api_key="NA",
  temperature=0.6,
  max_tokens=2048,
  top_p=0.95
)

# Cache the regex pattern at module level
JSON_PATTERN = re.compile(r'START_JSON(.*?)END_JSON', re.DOTALL)

def create_profile_analyzer_agent():
    def profile_analyzer(state: AgentState) -> AgentState:
        # Original prompt preserved exactly
        prompt = f"""
        **User Profile:**
        {json.dumps(state['user_data'], indent=2)}

        **Task:**
        Analyze the user profile to determine learning requirements, skill level, priorities, and a recommended learning path.

        **Output Format:**
        START_JSON
        {{
            "learning_requirements": {{
                "key_areas": ["string"],
                "skill_level": "string",
                "priorities": ["string"],
                "recommended_path": ["string"]
            }}
        }}
        END_JSON

        **Important:**
        - Ensure the response is enclosed in START_JSON and END_JSON.
        - Return only the JSON object.
        - Identify key areas based on the user's interests and goals.
        - Determine the skill level (Beginner, Intermediate, Advanced).
        - List priorities based on the user's needs.
        - Provide a recommended learning path as a list of course names.
        - Do not include any additional text or code outside the START_JSON and END_JSON delimiters.
        """

        # Single message creation and invocation
        response = llm.invoke([HumanMessage(content=prompt)])
        
        try:
            # Optimized JSON extraction
            if match := JSON_PATTERN.search(response.content):
                analysis = json.loads(match.group(1).strip())
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as error:
            print(f"Error occurred in create_profile_analyzer_agent: {error}")
            print(f"Response content: {response.content}")
            analysis = {
                "learning_requirements": {
                    "key_areas": ["--"],
                    "skill_level": "--",
                    "priorities": ["--"],
                    "recommended_path": ["--"]
                }
            }
        
        state['messages'].append({"role": "profile_analyzer", "content": analysis})
        print("create_profile_analyzer_agent done!!")
        return state
    
    return profile_analyzer

def create_course_matcher_agent():
    def course_matcher(state: AgentState) -> AgentState:
        # Pre-process courses once
        filtered_courses = [{
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "level": course.level,
            "duration": course.duration,
            "status": course.status
        } for course in state['courses']]
        
        # Original prompt preserved exactly
        prompt = f"""
        **Profile Analysis:**
        {json.dumps(state['messages'][-1]["content"], indent=2)}

        **Available Courses:**
        {json.dumps(filtered_courses, indent=2)}

        **Task:**
        Create a structured learning roadmap based on the profile analysis and available courses.

        **Output Format:**
        START_JSON
        {{
            "roadmap": {{
                "recommended_courses": [
                    {{
                        "id": "string",
                        "title": "string",
                        "description": "string",
                        "level": "string",
                        "duration": integer,
                        "status": "string",
                        "priority": integer
                    }}
                ],
                "total_duration": integer,
                "learning_path": "string"
            }}
        }}
        END_JSON

        **Important:**
        - Ensure the response is enclosed in START_JSON and END_JSON.
        - Return only the JSON object.
        - Limit the roadmap to a maximum of 8 courses.
        - Only include courses with status "published".
        - Assign priorities based on learning progression:
            * Beginner courses: priority 1
            * Intermediate courses: priority 2
            * Advanced courses: priority 3
            * Optional courses: priority 4
        - Calculate total_duration as the sum of all recommended course durations in minutes.
        - Create learning_path by joining the course titles with " → ".
        - Ensure selected courses match the user's skill level and interests.
        - Do not include any additional text outside the START_JSON and END_JSON delimiters.
        """

        response = llm.invoke([HumanMessage(content=prompt)])
        
        try:
            if match := JSON_PATTERN.search(response.content):
                roadmap = json.loads(match.group(1).strip())
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as error:
            print(f"Error occurred in create_course_matcher_agent: {error}")
            print(f"Response content: {response.content}")
            roadmap = {
                "roadmap": {
                    "recommended_courses": [{
                        "id": "--", "title": "--", "description": "--",
                        "level": "--", "duration": 0, "status": "published",
                        "priority": 1
                    }],
                    "total_duration": 0,
                    "learning_path": "--"
                }
            }

        state['roadmap'] = roadmap
        print("create_course_matcher_agent done!!")
        return state

    return course_matcher

def create_roadmap_validator_agent():
    def roadmap_validator(state: AgentState) -> AgentState:
        # Original prompt preserved exactly
        prompt = f"""
        You are an expert educational curriculum designer. Review and optimize the following learning roadmap:

        **Current Roadmap:**
        {json.dumps(state['roadmap'], indent=2)}

        **Validation Requirements:**
        1. Course Sequence
        - Order courses from foundational to advanced concepts
        - Ensure prerequisites are completed before advanced topics
        - Group related concepts together
        - Maintain logical skill progression

        2. Priority Levels (1-4):
        1: Essential foundation courses (must complete first)
        2: Core concept courses
        3: Advanced application courses
        4: Optional enhancement courses

        3. Course Levels:
        - Beginner: Fundamental concepts, no prerequisites
        - Intermediate: Builds on basic concepts
        - Advanced: Complex topics, requires prior knowledge

        **Output Format:**
        START_JSON
        {{
            "validated_roadmap": {{
                "recommended_courses": [
                    {{
                        "id": "string",
                        "title": "string",
                        "description": "string",
                        "level": "string",
                        "duration": integer,
                        "status": "string",
                        "priority": integer
                    }}
                ],
                "total_duration": integer,
                "learning_path": "string",
                "path_description": "string"
            }}
        }}
        END_JSON

        **Important:**
        - Maintain exact JSON structure
        - Duration should be in minutes
        - Status should be "published" for all courses
        - Learning path should join course titles with " → "
        - Ensure course order reflects real-world learning progression
        - Verify total duration is realistic and matches sum of course durations
        - Provide clear path description explaining the learning journey
        - Do not include any additional text outside the START_JSON and END_JSON delimiters
        """

        response = llm.invoke([HumanMessage(content=prompt)])
        
        try:
            if match := JSON_PATTERN.search(response.content):
                validated_roadmap = json.loads(match.group(1).strip())
                
                # Optimize duration calculation
                courses = validated_roadmap["validated_roadmap"]["recommended_courses"]
                validated_roadmap["validated_roadmap"]["total_duration"] = sum(
                    course["duration"] for course in courses
                )
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as error:
            print(f"Error occurred in create_roadmap_validator_agent: {error}")
            print(f"Response content: {response.content}")
            validated_roadmap = {
                "validated_roadmap": {
                    "recommended_courses": [{
                        "id": "--", "title": "--", "description": "--",
                        "level": "--", "duration": 0, "status": "published",
                        "priority": 1
                    }],
                    "total_duration": 0,
                    "learning_path": "--",
                    "path_description": "--"
                }
            }
        
        state['validated_roadmap'] = validated_roadmap
        print("create_roadmap_validator_agent done!!")
        return state

    return roadmap_validator

def create_roadmap_workflow():
  workflow = StateGraph(AgentState)
  
  workflow.add_node("profile_analyzer", create_profile_analyzer_agent())
  workflow.add_node("course_matcher", create_course_matcher_agent())
  workflow.add_node("roadmap_validator", create_roadmap_validator_agent()) 
  
  workflow.add_edge("profile_analyzer", "course_matcher")
  workflow.add_edge("course_matcher", "roadmap_validator")  
  workflow.add_edge("roadmap_validator", END) 
  workflow.set_entry_point("profile_analyzer")
  
  return workflow.compile()

def generate_roadmap(user_input: Dict[str, Any], courses: List[Dict[str, Any]]) -> Dict[str, Any]:
  initial_state = {
      "user_data": user_input,
      "courses": courses,
      "messages": [],
      "roadmap": {},
      "validated_roadmap": {}
  }
  
  workflow = create_roadmap_workflow()
  final_state = workflow.invoke(initial_state)
  
  # Extract roadmap from the final state
  return final_state["validated_roadmap"]

# -- Example --
# # for test llm
# from utils.mock_data import MockDataGenerator
# import traceback

# mock_gen = MockDataGenerator()

# sample_user = mock_gen.generate_user_data()
# print("\nSample User Data:")
# print(json.dumps(sample_user, indent=2))

# sample_courses = mock_gen.generate_course_data(10)
# print("\nSample Course Data: ", len(sample_courses))

# try:
#   roadmap = generate_roadmap(sample_user, sample_courses)
#   print("\nGenerated and Validated Roadmap:")
#   print(json.dumps(roadmap, indent=2))
# except Exception as e:
#   print(f"\nError generating roadmap: {str(e)}")
#   print(f"Error type: {type(e)}")
#   print(traceback.format_exc())