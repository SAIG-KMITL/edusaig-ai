from pydantic import BaseModel, Field
from typing import List, Optional

class SumRequest(BaseModel):
    content: str = """The Tortoise and the Hare

Once upon a time, a hare mocked a slow-moving tortoise. "You move so slowly, I wonder how you ever get anywhere!" the hare laughed.

The tortoise, calm and steady, replied, "I may be slow, but I can beat you in a race." Surprised and amused, the hare accepted the challenge, confident in his speed.

The race began. The hare dashed off, leaving the tortoise far behind. Feeling sure of his victory, the hare decided to rest under a tree. "I'll take a nap," he thought. "The tortoise will never catch up."

Meanwhile, the tortoise kept moving, slow but steady, never stopping.

When the hare woke up, he saw the tortoise near the finish line! The hare ran as fast as he could, but it was too late. The tortoise crossed the finish line first.

The tortoise looked back and said, "Slow and steady wins the race."

Moral of the story: Consistency and perseverance are more important than speed."""