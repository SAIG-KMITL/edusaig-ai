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
  model=os.getenv('MODEL'),
  base_url=os.getenv('LLM_SAIG_API'),
  api_key="NA",
  temperature=0.6,
  max_tokens=2048,
  top_p=0.95
)

def create_profile_analyzer_agent():
  def profile_analyzer(state: Dict) -> Dict:
      user_profile = state['user_data']
      
      prompt = f"""
      **User Profile:**
      {json.dumps(user_profile, indent=2)}

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

      **Instructions:**
      - Ensure the response is enclosed in START_JSON and END_JSON.
      - Return only the JSON object.
      - Identify key areas based on the user's interests and goals.
      - Determine the skill level (Beginner, Intermediate, Advanced).
      - List priorities based on the user's needs.
      - Provide a recommended learning path as a list of course names.
      - Do not include any additional text or code outside the START_JSON and END_JSON delimiters.
      """
      messages = [HumanMessage(content=prompt)]
      response = llm.invoke(messages)
      
      # Print the raw response for debugging
      # print(f"Raw Response from LLM: {response.content}")
      
      try:
          json_str = response.content
          # Extract JSON content enclosed in START_JSON and END_JSON
          json_match = re.search(r'START_JSON(.*?)END_JSON', json_str, re.DOTALL)
          if json_match:
              json_str = json_match.group(1).strip()
          analysis = json.loads(json_str)
      except (json.JSONDecodeError, AttributeError) as error:
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
      print("------------------- create_profile_analyzer_agent -------------------------")
      print(analysis)
      print("---------------------------------------------------------------------------")
      return state
  
  return profile_analyzer

def create_course_matcher_agent():
  def course_matcher(state: Dict) -> Dict:
      previous_analysis = state['messages'][-1]["content"]
      
      prompt = f"""
      **Profile Analysis:**
      {json.dumps(previous_analysis, indent=2)}

      **Available Courses:**
      {json.dumps(state['courses'], indent=2)}

      **Task:**
      Create a structured learning roadmap based on the profile analysis and available courses.

      **Output Format:**
      START_JSON
      {{
          "roadmap": {{
              "recommended_courses": [
                  {{
                      "courseID": "string",
                      "courseName": "string",
                      "duration": "string",
                      "courseLevel": "string",
                      "priority": integer
                  }}
              ],
              "total_duration": "string",
              "learning_path": "string"
          }}
      }}
      END_JSON

      **Instructions:**
      - Ensure the response is enclosed in START_JSON and END_JSON.
      - Return only the JSON object.
      - Limit the roadmap to a maximum of 6 courses.
      - Assign priorities based on course level (Beginner: 1, Intermediate: 2, Advanced: 3, Optional: 4), interests, and importance.
      - Calculate the total duration by summing up the durations of the recommended courses.
      - Create a learning path by joining the course names with commas.
      - Do not include any additional text or code outside the START_JSON and END_JSON delimiters.
      """
      messages = [HumanMessage(content=prompt)]
      response = llm.invoke(messages)
      
      # Print the raw response for debugging
      # print(f"Raw Response from LLM: {response.content}")
      
      try:
          json_str = response.content
          # Extract JSON content enclosed in START_JSON and END_JSON
          json_match = re.search(r'START_JSON(.*?)END_JSON', json_str, re.DOTALL)
          if json_match:
              json_str = json_match.group(1).strip()
          roadmap = json.loads(json_str)
      except (json.JSONDecodeError, AttributeError) as error:
          print(f"Error occurred in create_course_matcher_agent: {error}")
          print(f"Response content: {response.content}")
          roadmap = {
              "roadmap": {
                  "recommended_courses": [
                      {
                          "courseID": "--",
                          "courseName": "--",
                          "duration": "--",
                          "courseLevel": "--",
                          "priority": 1
                      }
                  ],
                  "total_duration": "--",
                  "learning_path": "--"
              }
          }
      
      state['roadmap'] = roadmap
      print("------------------- create_course_matcher_agent -------------------------")
      print(state['roadmap'])
      print("-------------------------------------------------------------------------")
      return state
  
  return course_matcher

def create_roadmap_validator_agent():
  def roadmap_validator(state: Dict) -> Dict:
      roadmap = state['roadmap']
      
      prompt = f"""
      You are an expert educational curriculum designer. Review and optimize the following learning roadmap:

      **Current Roadmap:**
      {json.dumps(roadmap, indent=2)}

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
                      "courseID": "string",
                      "courseName": "string",
                      "duration": "string",
                      "courseLevel": "string",
                      "priority": integer
                  }}
              ],
              "total_duration": "string",
              "learning_path": "string",
              "path_description": "string"
          }}
      }}
      END_JSON

      Important:
      - Maintain exact JSON structure
      - Ensure course order reflects real-world learning progression
      - Verify total duration is realistic
      - Provide clear path description explaining the learning journey
      - Do not include any additional text or code outside the START_JSON and END_JSON delimiters
      """
      messages = [HumanMessage(content=prompt)]
      response = llm.invoke(messages)
      
      try:
          json_str = response.content
          json_match = re.search(r'START_JSON(.*?)END_JSON', json_str, re.DOTALL)
          if json_match:
              json_str = json_match.group(1).strip()
          validated_roadmap = json.loads(json_str)
      except (json.JSONDecodeError, AttributeError) as error:
          print(f"Error occurred in create_roadmap_validator_agent: {error}")
          print(f"Response content: {response.content}")
          validated_roadmap = {
              "validated_roadmap": {
                  "recommended_courses": [
                      {
                          "courseID": "--",
                          "courseName": "--",
                          "duration": "--",
                          "courseLevel": "--",
                          "priority": 1
                      }
                  ],
                  "total_duration": "--",
                  "learning_path": "--",
                  "path_description": "--"
              }
          }
      
      state['validated_roadmap'] = validated_roadmap
      print("------------------- create_roadmap_validator_agent ----------------------")
      print(state['validated_roadmap'])
      print("-------------------------------------------------------------------------")
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


# try:
#   roadmap = generate_roadmap(sample_user, sample_courses)
#   print("\nGenerated and Validated Roadmap:")
#   print(json.dumps(roadmap, indent=2))
# except Exception as e:
#   print(f"\nError generating roadmap: {str(e)}")
#   print(f"Error type: {type(e)}")
#   print(traceback.format_exc())