from browser_use_sdk import BrowserUseSdk

# Start the SDK using your API key
browser_tool = BrowserUseSdk(api_key="your api key here")

# Task: Browsing Paul’s Online Math Notes for Differential Equations topics
task_details = """
Please complete the following steps to explore the topic 'Differential Equations':

1. Go to https://tutorial.math.lamar.edu
2. Look for the section called "Differential Equations" on the homepage or under "Courses"
3. Click on the link that says "Differential Equations"
4. Scroll to and open the topic "Basic Concepts"
5. From there, read through the section on "Direction Fields"
6. Then move on to "Euler’s Method" from the list of topics
7. Lastly, check the section that talks about "Linear Equations"

After each page or topic is visited, write down a short summary of what it explains.
"""

# Run the task with the instructions
output = browser_tool.run(
    llm_model="o3",
    task=task_details
)

# Display the results
print(output)
