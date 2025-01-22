import streamlit as st
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

model = HfApiModel(token=TOKEN)

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model, add_base_tools=True, additional_authorized_imports=["requests", "kbcstorage.client"])

# streamlit
st.title("Keboola Project Agent Test")
st.write("Ask questions about your Keboola project")

api_token = st.text_input("Enter your Keboola project API token:", type="password")

query = st.text_area("Enter your question:")

if st.button("Ask"):
    if not api_token:
        st.error("Please provide your Keboola project API token.")
    elif not query:
        st.error("Please enter a question.")
    else:
        with st.spinner("Generating a response..."):
            try:
                new_query = f"""Here are some links to the Storage API documentation: 
                https://keboola.docs.apiary.io/#reference/tables/unload-data-asynchronously/link-shared-bucket 
                https://github.com/keboola/sapi-python-client
                Here is a link to the Keboola Storage Python Client Library documentation:
                https://developers.keboola.com/integrate/storage/python-client/
                Search those links and retain the information. Here is the keboola project url:
                https://connection.europe-west3.gcp.keboola.com/
                
                Using the information you gathered from the docs and 
                Using the Keboola Storage API token: {api_token}, {query}. Actually perform the actions using Python code
                and the requests library.
                """
                response = agent.run(new_query)
                st.success("Response: ")
                st.write(response)
            except Exception as e:
                st.error(f"{e}")

if st.checkbox("Show agent logs"):
    st.write(agent.logs)
