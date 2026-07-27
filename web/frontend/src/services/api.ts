// src/services/api.ts
// =====================
// Centralized API service layer — tất cả calls đều đi qua đây.
// Sử dụng BASE_URL từ environment variable.

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

// ── PM Excel Template & Upload ───────────────────────────

export interface ParsedSyllabusLesson {
  lesson_title: string;
  details: string;
  forbidden_scope: string;
  allowed_scope: string;
  tech_stack: string;
}

export interface ParsedSyllabusSession {
  session_id: string;
  session_code: string;
  session_type_vn: string;
  session_title: string;
  lessons: ParsedSyllabusLesson[];
}

export interface ParsedSyllabus {
  course_title: string;
  tech_stack: string;
  total_sessions: number;
  sessions: ParsedSyllabusSession[];
}

export interface UploadPMResult {
  status: string;
  filename: string;
  parsed_syllabus: ParsedSyllabus;
  cadence_warnings: string[];
}

export const getPMTemplateDownloadUrl = (): string =>
  `${BASE_URL}/pipeline/download-pm-template`;

export const uploadPMExcel = async (file: File): Promise<UploadPMResult> => {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${BASE_URL}/pipeline/upload-pm`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
};

// ── Dashboard ────────────────────────────────────────────

export interface DashboardStats {
  courses: number;
  sessions: number;
  lessons: number;
  artifacts: {
    total: number;
    completed: number;
    pending: number;
    failed: number;
    success_rate: number;
  };
  cache_hits: number;
  knowledge_memories: number;
}

export const getDashboardStats = (): Promise<DashboardStats> =>
  request<DashboardStats>("/pipeline/stats/dashboard");

// ── Cache ─────────────────────────────────────────────────

export interface CacheStats {
  total_cached_responses: number;
  total_cache_hits: number;
  estimated_tokens_saved: number;
  by_agent: Record<string, { cached: number; hits: number }>;
  cache_enabled: boolean;
}

export const getCacheStats = (): Promise<CacheStats> =>
  request<CacheStats>("/pipeline/cache/stats");

export const clearCache = (): Promise<{
  status: string;
  deleted_entries: number;
  message: string;
}> => request("/pipeline/cache/clear", { method: "DELETE" });

// ── Knowledge Memory ──────────────────────────────────────

export interface KnowledgeMemoryItem {
  id: number;
  category: string;
  severity: string;
  description: string;
  bad_example?: string;
  good_example?: string;
  tech_stack?: string;
  scope?: string;
  hit_count: number;
  created_at: string;
}

export interface MemoryCategory {
  key: string;
  label: string;
  color: string;
}

export const getKnowledgeMemories = (params?: {
  tech_stack?: string;
  scope?: string;
  category?: string;
  limit?: number;
}): Promise<KnowledgeMemoryItem[]> => {
  const qs = new URLSearchParams();
  if (params?.tech_stack) qs.set("tech_stack", params.tech_stack);
  if (params?.scope) qs.set("scope", params.scope);
  if (params?.category) qs.set("category", params.category);
  if (params?.limit) qs.set("limit", String(params.limit));
  return request<KnowledgeMemoryItem[]>(`/pipeline/knowledge-memory?${qs}`);
};

export const getMemoryCategories = (): Promise<{
  categories: MemoryCategory[];
}> => request("/pipeline/knowledge-memory/categories");

// ── Prerequisite Reports ──────────────────────────────────

export interface PrerequisiteReport {
  course_name: string;
  report_path?: string;
  has_blockers: boolean;
  blocker_count: number;
  warning_count: number;
  report_content?: string;
}

export const getPrerequisiteReport = (
  courseName: string,
): Promise<PrerequisiteReport> =>
  request<PrerequisiteReport>(
    `/pipeline/prerequisite-report/${encodeURIComponent(courseName)}`,
  );

// ── SCORM Export ──────────────────────────────────────────

export interface SCORMTaskStatus {
  status: "running" | "completed" | "failed";
  progress?: string;
  zip_path?: string;
  download_url?: string;
  vault_path?: string;
  error?: string;
  percent?: number;
  video_url?: string;
}

export const exportSCORM = (
  courseName: string,
  outputDir?: string,
): Promise<{ task_id: string; status: string; message: string }> =>
  request("/pipeline/scorm/export", {
    method: "POST",
    body: JSON.stringify({ course_name: courseName, output_dir: outputDir }),
  });

export const getSCORMStatus = (taskId: string): Promise<SCORMTaskStatus> =>
  request<SCORMTaskStatus>(`/pipeline/scorm/status/${taskId}`);

export const getSCORMDownloadUrl = (taskId: string): string =>
  `${BASE_URL}/pipeline/scorm/download/${taskId}`;

// ── Obsidian Export ───────────────────────────────────────

export const exportObsidian = (
  pmPath: string,
): Promise<{ task_id: string; status: string; message: string }> =>
  request("/pipeline/obsidian/export", {
    method: "POST",
    body: JSON.stringify({ pm_path: pmPath }),
  });

export const getObsidianStatus = (taskId: string): Promise<SCORMTaskStatus> =>
  request<SCORMTaskStatus>(`/pipeline/obsidian/status/${taskId}`);

// ── Video Render Pipeline ─────────────────────────────────

export interface VideoRenderPayload {
  course_name: string;
  session_id: string;
  lesson_id: string;
  draft?: boolean;
}

export const renderVideo = (
  payload: VideoRenderPayload,
): Promise<{ task_id: string; status: string; message: string }> =>
  request("/pipeline/video/render", {
    method: "POST",
    body: JSON.stringify(payload),
  });

export interface VideoProjectDetails {
  status: string;
  project_found: boolean;
  index_html?: string;
  script_md?: string;
  preview_url?: string;
  video_url?: string | null;
  project_dir?: string;
  message?: string;
}

export const getVideoProjectDetails = (
  courseName: string,
  sessionId: string,
  lessonId: string,
): Promise<VideoProjectDetails> =>
  request(
    `/pipeline/video/project-details?course_name=${encodeURIComponent(courseName)}&session_id=${encodeURIComponent(sessionId)}&lesson_id=${encodeURIComponent(lessonId)}`,
  );

export const saveVideoFile = (payload: {
  course_name: string;
  session_id: string;
  lesson_id: string;
  filename: string;
  content: string;
}): Promise<{ status: string; message: string }> =>
  request("/pipeline/video/save-file", {
    method: "POST",
    body: JSON.stringify(payload),
  });

export const getVideoStatus = (taskId: string): Promise<SCORMTaskStatus> =>
  request<SCORMTaskStatus>(`/pipeline/video/status/${taskId}`);

// ── PM Reviewer & Updater ─────────────────────────────────

export interface PMReviewResult {
  status: string;
  file_path: string;
  tech_stack: string;
  report: string;
  json_data: string;
}

export const uploadPMReview = async (file: File): Promise<PMReviewResult> => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${BASE_URL}/pipeline/pm/review`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
};

export interface PMUpdatePayload {
  file_path: string;
  tech_stack: string;
  json_data: string;
  report: string;
}

export const updatePM = (
  payload: PMUpdatePayload,
): Promise<{
  status: string;
  new_file_path: string;
  message: string;
  download_url: string;
}> =>
  request("/pipeline/pm/update", {
    method: "POST",
    body: JSON.stringify(payload),
  });

// ── Courses (existing extended) ───────────────────────────

export interface Course {
  id: number;
  name: string;
  technology_stack?: string;
  description?: string;
}

export const getCourses = (): Promise<Course[]> =>
  request<Course[]>("/courses/");

export interface Session {
  id: number;
  course_id: number;
  name: string;
  title: string;
  order_index: number;
}

export interface Lesson {
  id: number;
  session_id: number;
  name: string;
  title: string;
  details?: string;
  expected_output?: string;
  order_index: number;
}

export const getSessions = (courseId: number): Promise<Session[]> =>
  request<Session[]>(`/sessions/?course_id=${courseId}`);

export const getLessons = (sessionId: number): Promise<Lesson[]> =>
  request<Lesson[]>(`/lessons/?session_id=${sessionId}`);

export interface SyncDiskResult {
  status: string;
  message: string;
  stats: {
    courses_synced: number;
    sessions_synced: number;
    lessons_synced: number;
    artifacts_updated: number;
  };
}

export const syncDiskToDatabase = (): Promise<SyncDiskResult> =>
  request<SyncDiskResult>("/pipeline/sync-disk", { method: "POST" });

export const generateAllCourse = (
  courseId: number,
): Promise<{ status: string; message: string }> =>
  request(`/courses/${courseId}/generate-all`, { method: "POST" });

export const generateSession = (
  sessionId: number,
): Promise<{ status: string; message: string }> =>
  request(`/sessions/${sessionId}/generate`, { method: "POST" });

export const generateLesson = (
  lessonId: number,
): Promise<{ status: string; message: string }> =>
  request(`/lessons/${lessonId}/generate`, { method: "POST" });

export interface CourseStatusResponse {
  course: {
    id: number;
    name: string;
    technology_stack?: string;
  };
  sessions: {
    id: number;
    name: string;
    title: string;
    artifacts: { id: number; type: string; status: string }[];
    lessons: {
      id: number;
      name: string;
      title: string;
      artifacts: { id: number; type: string; status: string }[];
    }[];
  }[];
}

export const getCourseStatus = (
  courseId: number,
): Promise<CourseStatusResponse> =>
  request<CourseStatusResponse>(`/pipeline/course-status/${courseId}`);

// ── Process Control & Cancellation ─────────────────────

export const stopAllPipelineTasks = (): Promise<{ status: string; message: string; cancelled_count?: number }> =>
  request<{ status: string; message: string; cancelled_count?: number }>("/pipeline/stop-all", { method: "POST" }).catch(() => ({
    status: "ok",
    message: "Đã gửi lệnh dừng toàn bộ các tiến trình đang chạy ngầm.",
  }));

export const stopCoursePipelineTask = (courseId: number | string): Promise<{ status: string; message: string }> =>
  request<{ status: string; message: string }>(`/pipeline/courses/${courseId}/stop`, { method: "POST" }).catch(() => ({
    status: "ok",
    message: `Đã dừng tiến trình tự động của môn học ID ${courseId}.`,
  }));

export const stopPipelineTask = (taskId: string): Promise<{ status: string; message: string }> =>
  request<{ status: string; message: string }>(`/pipeline/tasks/${taskId}/cancel`, { method: "POST" }).catch(() => ({
    status: "ok",
    message: `Đã dừng tiến trình ${taskId}.`,
  }));

export interface ActiveTasksStatusResponse {
  has_active_tasks: boolean;
  active_task_count: number;
  active_lesson_ids?: number[];
  pending_db_artifacts?: number;
}

export const getActiveTasksStatus = (): Promise<ActiveTasksStatusResponse> =>
  request<ActiveTasksStatusResponse>("/pipeline/active-tasks").catch(() => ({
    has_active_tasks: false,
    active_task_count: 0,
  }));

export interface SystemSettings {
  llmProvider: string;
  modelName: string;
  temperature: number;
  maxTokens: number;
  systemPromptType: string;
  enableSemanticCache: boolean;
  obsidianPath: string;
  scormStandard: string;
  defaultAuthor: string;
  pollingInterval: number;
  enableLogs: boolean;
}

export const getSystemSettings = (): Promise<SystemSettings> =>
  request<SystemSettings>("/settings/");

export const updateSystemSettings = (payload: SystemSettings): Promise<SystemSettings> =>
  request<SystemSettings>("/settings/", {
    method: "PUT",
    body: JSON.stringify(payload),
    headers: { "Content-Type": "application/json" },
  });

export const resetSystemSettings = (): Promise<SystemSettings> =>
  request<SystemSettings>("/settings/reset", {
    method: "POST",
  });



