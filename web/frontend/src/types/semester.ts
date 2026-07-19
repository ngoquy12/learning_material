export interface SemesterResponse {
  id: number;
  name: string;
  major_id: number;
}

export interface SemesterCreate {
  name: string;
  major_id: number;
}
