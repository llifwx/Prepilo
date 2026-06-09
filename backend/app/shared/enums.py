from enum import StrEnum


class TopicStatus(StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    WEAK = "weak"


class StudyTaskStatus(StrEnum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    SKIPPED = "skipped"
    OVERDUE = "overdue"


class StudyTaskType(StrEnum):
    LEARN = "learn"
    REVIEW = "review"
    QUIZ = "quiz"
    NOTES = "notes"
    AI_EXPLANATION = "ai_explanation"
    FRIEND_HELP = "friend_help"
