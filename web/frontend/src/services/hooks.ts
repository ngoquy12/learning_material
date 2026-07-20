import { useState, useEffect, useCallback } from 'react';
import {
  getDashboardStats, getCacheStats, clearCache,
  getKnowledgeMemories, getMemoryCategories,
  getPrerequisiteReport, exportSCORM, getSCORMStatus,
  exportObsidian, getObsidianStatus, uploadPMReview, updatePM,
  renderVideo, getVideoStatus, generateAllCourse, getCourseStatus,
  generateSession, generateLesson,
  type DashboardStats, type CacheStats, type KnowledgeMemoryItem,
  type MemoryCategory, type PrerequisiteReport, type SCORMTaskStatus,
  type CourseStatusResponse,
} from './api';

// ── Generic hook factory ─────────────────────────────────

function useAsync<T>(fetcher: () => Promise<T>, deps: unknown[] = []) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await fetcher();
      setData(result);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }, deps); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => { refetch(); }, [refetch]);

  return { data, loading, error, refetch };
}

// ── Dashboard ─────────────────────────────────────────────

export function useDashboardStats() {
  return useAsync<DashboardStats>(getDashboardStats);
}

// ── Cache ─────────────────────────────────────────────────

export function useCacheStats() {
  return useAsync<CacheStats>(getCacheStats);
}

export function useClearCache() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await clearCache();
      return result;
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
}

// ── Knowledge Memory ──────────────────────────────────────

export function useKnowledgeMemories(filters?: {
  tech_stack?: string;
  scope?: string;
  category?: string;
  limit?: number;
}) {
  return useAsync<KnowledgeMemoryItem[]>(
    () => getKnowledgeMemories(filters),
    [filters?.tech_stack, filters?.scope, filters?.category, filters?.limit]
  );
}

export function useMemoryCategories() {
  return useAsync<{ categories: MemoryCategory[] }>(getMemoryCategories);
}

// ── Prerequisite Reports ──────────────────────────────────

export function usePrerequisiteReport(courseName: string | null) {
  return useAsync<PrerequisiteReport>(
    () => courseName ? getPrerequisiteReport(courseName) : Promise.resolve({
      course_name: '', has_blockers: false, blocker_count: 0, warning_count: 0
    } as PrerequisiteReport),
    [courseName]
  );
}

// ── SCORM Export ──────────────────────────────────────────

export function useSCORMExport() {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<SCORMTaskStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startExport = async (courseName: string, outputDir?: string) => {
    setLoading(true);
    setError(null);
    setStatus(null);
    try {
      const res = await exportSCORM(courseName, outputDir);
      setTaskId(res.task_id);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      setLoading(false);
    }
  };

  // Poll for status when taskId is set
  useEffect(() => {
    if (!taskId) return;
    const interval = setInterval(async () => {
      try {
        const s = await getSCORMStatus(taskId);
        setStatus(s);
        if (s.status !== 'running') {
          setLoading(false);
          clearInterval(interval);
        }
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : String(e));
        setLoading(false);
        clearInterval(interval);
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [taskId]);

  const reset = () => {
    setTaskId(null);
    setStatus(null);
    setError(null);
    setLoading(false);
  };

  return { startExport, taskId, status, loading, error, reset };
}

// ── Obsidian Export ───────────────────────────────────────

export function useObsidianExport() {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<SCORMTaskStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startExport = async (pmPath: string) => {
    setLoading(true);
    setError(null);
    setStatus(null);
    try {
      const res = await exportObsidian(pmPath);
      setTaskId(res.task_id);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!taskId) return;
    const interval = setInterval(async () => {
      try {
        const s = await getObsidianStatus(taskId);
        setStatus(s);
        if (s.status !== 'running') {
          setLoading(false);
          clearInterval(interval);
        }
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : String(e));
        setLoading(false);
        clearInterval(interval);
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [taskId]);

  const reset = () => {
    setTaskId(null);
    setStatus(null);
    setError(null);
    setLoading(false);
  };

  return { startExport, taskId, status, loading, error, reset };
}

// ── PM Reviewer & Updater ─────────────────────────────────

export function usePMReview() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);

  const executeReview = async (file: File) => {
    setLoading(true);
    setError(null);
    try {
      const result = await uploadPMReview(file);
      setData(result);
      return result;
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  const executeUpdate = async (payload: any) => {
    setLoading(true);
    setError(null);
    try {
      const result = await updatePM(payload);
      return result;
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  return { executeReview, executeUpdate, data, loading, error };
}

// ── Video Render Pipeline ─────────────────────────────────

export function useVideoRender() {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startRender = async (payload: { course_name: string; session_id: string; lesson_id: string; draft?: boolean }) => {
    setLoading(true);
    setError(null);
    setStatus(null);
    try {
      const res = await renderVideo(payload);
      setTaskId(res.task_id);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!taskId) return;
    const interval = setInterval(async () => {
      try {
        const s = await getVideoStatus(taskId);
        setStatus(s);
        if (s.status !== 'running') {
          setLoading(false);
          clearInterval(interval);
        }
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : String(e));
        setLoading(false);
        clearInterval(interval);
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [taskId]);

  const reset = () => {
    setTaskId(null);
    setStatus(null);
    setError(null);
    setLoading(false);
  };

  return { startRender, taskId, status, loading, error, reset };
}

// ── Sync Disk to Database ─────────────────────────────────

export function useSyncDisk() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async () => {
    setLoading(true);
    setError(null);
    try {
      const { syncDiskToDatabase } = await import('./api');
      const result = await syncDiskToDatabase();
      return result;
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
}

// ── Generate All Course Lessons ───────────────────────────

export function useGenerateAllCourse() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async (courseId: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await generateAllCourse(courseId);
      return res;
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
}

// ── Course Status Hook with Polling ───────────────────────

export function useCourseStatus(courseId: number | null) {
  const [data, setData] = useState<CourseStatusResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    if (!courseId) return;
    setLoading(true);
    try {
      const result = await getCourseStatus(courseId);
      setData(result);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }, [courseId]);

  useEffect(() => {
    if (courseId) {
      fetchStatus();
    } else {
      setData(null);
    }
  }, [courseId, fetchStatus]);

  // Polling helper
  useEffect(() => {
    if (!courseId) return;
    
    // Check if any artifact is in "Pending" status
    const hasPending = data?.sessions.some(s => 
      s.artifacts.some(a => a.status === 'Pending') ||
      s.lessons.some(l => l.artifacts.some(a => a.status === 'Pending'))
    );
    
    if (!hasPending) return;

    const interval = setInterval(() => {
      getCourseStatus(courseId)
        .then(setData)
        .catch(console.error);
    }, 4000);

    return () => clearInterval(interval);
  }, [courseId, data]);

  return { data, loading, error, refetch: fetchStatus };
}

export function useGenerateSession() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async (sessionId: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await generateSession(sessionId);
      return res;
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
}

export function useGenerateLesson() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async (lessonId: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await generateLesson(lessonId);
      return res;
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
}
