export interface LessonResponse {
  id: number;
  name: string;
  title: string;
  details?: string;
  expected_output?: string;
  forbidden_scope?: string;
  allowed_scope?: string;
  tech_stack?: string;
  session_id: number;
}

export interface LessonCreate {
  name: string;
  title: string;
  details?: string;
  expected_output?: string;
  forbidden_scope?: string;
  allowed_scope?: string;
  tech_stack?: string;
  session_id: number;
}

export interface LessonUpdate {
  name?: string;
  title?: string;
  details?: string;
  expected_output?: string;
  forbidden_scope?: string;
  allowed_scope?: string;
  tech_stack?: string;
}
