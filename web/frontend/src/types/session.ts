export interface SessionResponse {
  id: number;
  name: string;
  title: string;
  course_id: number;
}

export interface SessionCreate {
  name: string;
  title: string;
  course_id: number;
}
