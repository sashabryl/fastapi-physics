from enum import Enum


class DifficultyLevel(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class ReactionType(Enum):
    LIKE = "Like"
    DISLIKE = "Dislike"


class ReactionOwner(Enum):
    COMMENT = "Comment"
    RESPONSE = "Response"
    QUESTION_RESPONSE = "QuestionResponse"
