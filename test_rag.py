from rag import retrieve_context

query = "I drive a petrol car every day."

docs = retrieve_context(query)

print("\nRetrieved Documents:\n")

for doc in docs:
    print(doc)
    print("-" * 50)