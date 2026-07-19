export interface LessonResponse {
  id: number;
  name: string;
  title: string;
  details?: string;
  expected_output?: string;
  session_id: number;
}

export interface LessonCreate {
  name: string;
  title: string;
  details?: string;
  expected_output?: string;
  session_id: number;
}
