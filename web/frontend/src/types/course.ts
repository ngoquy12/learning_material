export interface CourseResponse {
  id: number;
  name: string;
  technology_stack: string | null;
  semester_id: number;
}

export interface CourseCreate {
  name: string;
  technology_stack?: string;
  semester_id: number;
}
