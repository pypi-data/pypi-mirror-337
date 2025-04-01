from typing import Optional
from ...utils.from_camel_case_base_model import FromCamelCaseBaseModel

class EvaluationTaskBaseCostInfoProperties(FromCamelCaseBaseModel):
  cost_per_input_token: Optional[float] = None
  cost_per_output_token: Optional[float] = None
  cost_per_cache_read_input_token: Optional[float] = None

class EvaluationTaskBaseUsageInfoProperties(FromCamelCaseBaseModel):
  input_tokens: Optional[int] = None
  output_tokens: Optional[int] = None
  cache_read_input_tokens: Optional[int] = None

class EvaluationTaskBase(EvaluationTaskBaseUsageInfoProperties, EvaluationTaskBaseCostInfoProperties):
  evaluation_id: str
  actual_output: str
  test_case_id: Optional[str] = None
  input: Optional[str] = None
  expected_output: Optional[str] = None
  context: Optional[str] = None
  latency: Optional[float] = None

class EvaluationTask(EvaluationTaskBase):
  id: str
  metric_type_id: str
  user_id: Optional[str] = None
  status: str
  score: Optional[float] = None
  input: Optional[str] = None
  expected_output: Optional[str] = None
  context: Optional[str] = None
  reason: Optional[str] = None
  error: Optional[str] = None
  created_at: str
  deleted_at: Optional[str] = None
  evaluated_at: Optional[str] = None