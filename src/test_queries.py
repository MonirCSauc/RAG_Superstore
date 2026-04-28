import json
from datetime import datetime
from rag_app import generate_answer

questions = [
    "What is the sales trend over the 4-year period?",
    "Which months show the highest sales? Is there seasonality?",
    "How has profit margin changed over time?",
    "Which product category generates the most revenue?",
    "What sub-categories have the highest profit margins?",
    "Which products are frequently sold at a discount?",
    "Which region has the best sales performance?",
    "Compare sales performance across different states.",
    "Which cities are the top performers?",
    "Compare Technology vs. Furniture sales trends.",
    "How does the West region compare to the East in terms of profit?"
]

results = []

for i, question in enumerate(questions, start=1):
    print(f"\nQUESTION {i}/{len(questions)}: {question}")
    print("-" * 80)

    answer = generate_answer(question)
    results.append({"question": question, "answer": answer})

    print("ANSWER:")
    print(answer)
    print("=" * 80)

# Save to JSON for your report
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"test_results_{timestamp}.json"
with open(output_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to {output_file}")