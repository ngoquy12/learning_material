export interface ProgramResponse {
  id: number;
  name: string;
  description: string | null;
}

export interface ProgramCreate {
  name: string;
  description?: string;
}
