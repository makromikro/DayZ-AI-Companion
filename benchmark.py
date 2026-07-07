import time

from brain import ask_ai

history = []

message = "Hello, my name is Burak."

print("=" * 50)
print("DayZ AI Companion Benchmark")
print("=" * 50)

start = time.perf_counter()

answer = ask_ai(message, history)

end = time.perf_counter()

elapsed = end - start

print("\nAI Response:")
print(answer)

print("\nPerformance")
print("-" * 50)
print(f"Response Time: {elapsed:.2f} seconds")