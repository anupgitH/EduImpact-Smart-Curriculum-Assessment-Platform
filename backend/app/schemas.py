from pydantic import BaseModel, ConfigDict, EmailStr, Field
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    role: str = Field(default="student", pattern="^(student|teacher)$")
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    role: str
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
class CourseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    code: str = Field(min_length=2, max_length=40)
    description: str = ""
class CourseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    code: str
    description: str
    teacher_id: int
class AssessmentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    course_id: int
    duration_minutes: int = Field(default=30, ge=1, le=360)
    questions: list[dict] = Field(default_factory=list)
class AssessmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    course_id: int
    created_by: int
    status: str
    duration_minutes: int
    questions: list[dict]
class AttemptSubmit(BaseModel):
    answers: dict[str, str | int | list[str]]
class GenerateQuestions(BaseModel):
    topic: str = Field(min_length=2, max_length=300)
    count: int = Field(default=5, ge=1, le=20)
    difficulty: str = Field(default="mixed", pattern="^(easy|medium|hard|mixed)$")
    question_type: str = Field(default="mcq", pattern="^(mcq|short_answer|mixed)$")
