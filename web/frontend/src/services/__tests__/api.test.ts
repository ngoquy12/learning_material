// src/services/__tests__/api.test.ts
// ===================================
// Tests cho API service layer
// Chạy: cd web/frontend && npx vitest run src/services/__tests__/api.test.ts

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock fetch globally
const mockFetch = vi.fn();
vi.stubGlobal('fetch', mockFetch);

// Helper to create mock response
function mockResponse(data: unknown, status = 200) {
  return Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    statusText: status === 200 ? 'OK' : 'Error',
    json: () => Promise.resolve(data),
  } as Response);
}

// Import after mock setup
import {
  getDashboardStats,
  getCacheStats,
  clearCache,
  getKnowledgeMemories,
  getMemoryCategories,
  getPrerequisiteReport,
  exportSCORM,
  getSCORMStatus,
  getSCORMDownloadUrl,
} from '../api';

describe('API Service Layer', () => {
  beforeEach(() => {
    mockFetch.mockReset();
    vi.unstubAllEnvs();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  // ── Dashboard ──────────────────────────────────────────

  describe('getDashboardStats', () => {
    it('should return dashboard stats on success', async () => {
      const mockStats = {
        courses: 5,
        sessions: 20,
        lessons: 80,
        artifacts: { total: 320, completed: 290, pending: 10, failed: 20, success_rate: 90.6 },
        cache_hits: 145,
        knowledge_memories: 37,
      };
      mockFetch.mockReturnValueOnce(mockResponse(mockStats));

      const result = await getDashboardStats();

      expect(result.courses).toBe(5);
      expect(result.sessions).toBe(20);
      expect(result.artifacts.success_rate).toBe(90.6);
      expect(result.cache_hits).toBe(145);
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/pipeline/stats/dashboard'),
        expect.any(Object)
      );
    });

    it('should throw on API error', async () => {
      mockFetch.mockReturnValueOnce(mockResponse({ detail: 'Database error' }, 500));
      await expect(getDashboardStats()).rejects.toThrow('Database error');
    });
  });

  // ── Cache ──────────────────────────────────────────────

  describe('getCacheStats', () => {
    it('should return cache statistics', async () => {
      const mockCache = {
        total_cached_responses: 42,
        total_cache_hits: 18,
        estimated_tokens_saved: 14400,
        by_agent: { HTML_Writer: { cached: 20, hits: 8 } },
        cache_enabled: true,
      };
      mockFetch.mockReturnValueOnce(mockResponse(mockCache));

      const result = await getCacheStats();

      expect(result.total_cached_responses).toBe(42);
      expect(result.total_cache_hits).toBe(18);
      expect(result.cache_enabled).toBe(true);
      expect(result.by_agent).toHaveProperty('HTML_Writer');
    });
  });

  describe('clearCache', () => {
    it('should call DELETE endpoint and return deleted count', async () => {
      mockFetch.mockReturnValueOnce(mockResponse({ status: 'ok', deleted_entries: 25, message: 'Done' }));

      const result = await clearCache();

      expect(result.status).toBe('ok');
      expect(result.deleted_entries).toBe(25);
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/pipeline/cache/clear'),
        expect.objectContaining({ method: 'DELETE' })
      );
    });
  });

  // ── Knowledge Memory ────────────────────────────────────

  describe('getKnowledgeMemories', () => {
    it('should return list of memory items without filters', async () => {
      const mockMemories = [
        {
          id: 1, category: 'scope_violation', severity: 'high',
          description: 'Test', bad_example: null, good_example: null,
          tech_stack: null, scope: null, hit_count: 2, created_at: '2024-01-01'
        }
      ];
      mockFetch.mockReturnValueOnce(mockResponse(mockMemories));

      const result = await getKnowledgeMemories();

      expect(Array.isArray(result)).toBe(true);
      expect(result).toHaveLength(1);
      expect(result[0].category).toBe('scope_violation');
    });

    it('should pass filters as query params', async () => {
      mockFetch.mockReturnValueOnce(mockResponse([]));

      await getKnowledgeMemories({ tech_stack: 'python/fastapi', scope: 'html', limit: 20 });

      const calledUrl = mockFetch.mock.calls[0][0] as string;
      expect(calledUrl).toContain('tech_stack=python%2Ffastapi');
      expect(calledUrl).toContain('scope=html');
      expect(calledUrl).toContain('limit=20');
    });

    it('should return empty array when no memories', async () => {
      mockFetch.mockReturnValueOnce(mockResponse([]));
      const result = await getKnowledgeMemories({ category: 'syntax_error' });
      expect(result).toEqual([]);
    });
  });

  describe('getMemoryCategories', () => {
    it('should return 10 categories', async () => {
      const mockCategories = {
        categories: Array.from({ length: 10 }, (_, i) => ({
          key: `cat_${i}`, label: `Category ${i}`, color: 'blue'
        }))
      };
      mockFetch.mockReturnValueOnce(mockResponse(mockCategories));

      const result = await getMemoryCategories();

      expect(result.categories).toHaveLength(10);
    });
  });

  // ── Prerequisite Reports ────────────────────────────────

  describe('getPrerequisiteReport', () => {
    it('should return report for a course', async () => {
      const mockReport = {
        course_name: 'TestCourse',
        report_path: '/output/TestCourse/prerequisite_report.md',
        has_blockers: true,
        blocker_count: 2,
        warning_count: 1,
        report_content: '# Report\n🔴 BLOCKER: ...',
      };
      mockFetch.mockReturnValueOnce(mockResponse(mockReport));

      const result = await getPrerequisiteReport('TestCourse');

      expect(result.course_name).toBe('TestCourse');
      expect(result.has_blockers).toBe(true);
      expect(result.blocker_count).toBe(2);
    });

    it('should URL-encode course name with spaces', async () => {
      mockFetch.mockReturnValueOnce(mockResponse({ course_name: 'My Course', has_blockers: false, blocker_count: 0, warning_count: 0 }));

      await getPrerequisiteReport('My Course');

      const calledUrl = mockFetch.mock.calls[0][0] as string;
      expect(calledUrl).toContain('My%20Course');
    });
  });

  // ── SCORM Export ────────────────────────────────────────

  describe('exportSCORM', () => {
    it('should POST to export endpoint and return task_id', async () => {
      mockFetch.mockReturnValueOnce(mockResponse({
        task_id: 'abc12345', status: 'running', message: 'SCORM export started'
      }));

      const result = await exportSCORM('Test Course');

      expect(result.task_id).toBe('abc12345');
      expect(result.status).toBe('running');
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/pipeline/scorm/export'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ course_name: 'Test Course', output_dir: undefined }),
        })
      );
    });

    it('should include output_dir in request when provided', async () => {
      mockFetch.mockReturnValueOnce(mockResponse({ task_id: 'xyz', status: 'running', message: '' }));

      await exportSCORM('MyCourse', '/custom/path');

      const body = JSON.parse(mockFetch.mock.calls[0][1].body);
      expect(body.output_dir).toBe('/custom/path');
    });
  });

  describe('getSCORMStatus', () => {
    it('should return running status', async () => {
      mockFetch.mockReturnValueOnce(mockResponse({ status: 'running', progress: 'Scanning...' }));

      const result = await getSCORMStatus('abc12345');

      expect(result.status).toBe('running');
      expect(result.progress).toBe('Scanning...');
    });

    it('should return completed status with download url', async () => {
      mockFetch.mockReturnValueOnce(mockResponse({
        status: 'completed',
        zip_path: '/output/scorm.zip',
        download_url: '/api/v1/pipeline/scorm/download/abc12345',
        progress: 'Done'
      }));

      const result = await getSCORMStatus('abc12345');

      expect(result.status).toBe('completed');
      expect(result.download_url).toContain('download/abc12345');
    });

    it('should return failed status with error', async () => {
      mockFetch.mockReturnValueOnce(mockResponse({
        status: 'failed', error: 'Output dir not found', progress: 'Failed'
      }));

      const result = await getSCORMStatus('bad-task');

      expect(result.status).toBe('failed');
      expect(result.error).toBeTruthy();
    });
  });

  describe('getSCORMDownloadUrl', () => {
    it('should construct correct download URL', () => {
      const url = getSCORMDownloadUrl('myTaskId');
      expect(url).toContain('/pipeline/scorm/download/myTaskId');
    });
  });

  // ── Error Handling ──────────────────────────────────────

  describe('Error handling', () => {
    it('should throw with detail message on 404', async () => {
      mockFetch.mockReturnValueOnce(mockResponse({ detail: 'Resource not found' }, 404));
      await expect(getCacheStats()).rejects.toThrow('Resource not found');
    });

    it('should throw with status text on non-JSON error', async () => {
      mockFetch.mockReturnValueOnce(Promise.resolve({
        ok: false,
        status: 503,
        statusText: 'Service Unavailable',
        json: () => Promise.reject(new Error('invalid json')),
      } as Response));
      await expect(getCacheStats()).rejects.toThrow();
    });
  });
});
