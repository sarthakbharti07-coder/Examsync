import enum


class DocumentStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    QUEUED = "queued"
    PROCESSING = "processing"
    EXTRACTED = "extracted"
    CLASSIFIED = "classified"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentKind(str, enum.Enum):
    QUESTION_PAPER = "question_paper"
    SYLLABUS = "syllabus"


class ClassificationSource(str, enum.Enum):
    AI = "ai"
    USER = "user"


class AnalysisStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class PaperStatus(str, enum.Enum):
    GENERATING = "generating"
    GENERATED = "generated"
    VERIFIED = "verified"
    VERIFICATION_FAILED = "verification_failed"
    FAILED = "failed"


class SyllabusSource(str, enum.Enum):
    MANUAL = "manual"
    UPLOAD = "upload"
