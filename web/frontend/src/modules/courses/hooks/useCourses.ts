import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { AxiosError } from 'axios';
import { apiClient } from '../../../shared/api/base';
import { CourseResponse, CourseCreate } from '../../../types/course';
import { message } from 'antd';

export const courseKeys = {
  all: ['courses'] as const,
};

export const useCourses = (semesterId?: number) => {
  return useQuery({
    queryKey: semesterId ? ['courses', 'list', semesterId] : courseKeys.all,
    queryFn: async (): Promise<CourseResponse[]> => {
      const url = semesterId ? `/courses/?semester_id=${semesterId}` : '/courses/';
      const { data } = await apiClient.get(url);
      return data;
    },
  });
};

export const useCourse = (courseId: number) => {
  return useQuery({
    queryKey: [...courseKeys.all, courseId],
    queryFn: async (): Promise<CourseResponse> => {
      const { data } = await apiClient.get(`/courses/${courseId}`);
      return data;
    },
    enabled: !!courseId,
  });
};

export const useCreateCourse = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (payload: CourseCreate) => {
      const { data } = await apiClient.post('/courses/', payload);
      return data;
    },
    onSuccess: () => {
      message.success('Thêm môn học thành công!');
      queryClient.invalidateQueries({ queryKey: courseKeys.all });
    },
    onError: () => {
      message.error('Có lỗi xảy ra khi thêm môn học.');
    },
  });
};

export const useUpdateCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: CourseCreate }) => {
      const { data } = await apiClient.put(`/courses/${id}`, payload);
      return data;
    },
    onSuccess: (_, variables) => {
      message.success('Cập nhật môn học thành công!');
      queryClient.invalidateQueries({ queryKey: courseKeys.all });
      queryClient.invalidateQueries({ queryKey: [...courseKeys.all, variables.id] });
    },
    onError: () => message.error('Cập nhật thất bại!'),
  });
};

export const useDeleteCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/courses/${id}`);
    },
    onSuccess: () => {
      message.success('Xóa môn học thành công!');
      queryClient.invalidateQueries({ queryKey: courseKeys.all });
    },
    onError: () => message.error('Xóa môn học thất bại!'),
  });
};

export interface PMRow {
  session_id: string;        // Col 1: Session (e.g. Session 01)
  session_type_vn: string;   // Col 2: Loại Session (Lý thuyết, Thực hành, Mini Project...)
  session_code: string;      // Col 3: Mã Session (THEORY, PRACTICE, MINI_PROJECT...)
  session_title: string;     // Col 4: Tên Tiêu Đề Session
  lesson_title: string;      // Col 5: Tên Lesson
  details: string;           // Col 6: Nội Dung Chi Tiết (Lesson Scope)
  expected_outcome?: string; // Col 7: Kết Quả Mong Đợi (Expected Outcome)
  forbidden_scope: string;   // Col 8: Phạm Vi CẤM DÙNG (Forbidden Scope)
  allowed_scope: string;     // Col 9: Phạm Vi ĐÃ HỌC (Allowed Scope)
  tech_stack: string;        // Col 10: Tech Stack & Quy Chuẩn

  // Legacy fallback fields
  stt?: string;
  form?: string;
  session_val?: string;
  content_val?: string;
  lesson_val?: string;
  details_val?: string;
  output_val?: string;
  deadline?: string;
}

export const useParseExcel = () => {
  return useMutation({
    mutationFn: async ({ courseId, file }: { courseId: number; file: File }): Promise<PMRow[]> => {
      const formData = new FormData();
      formData.append('file', file);
      const { data } = await apiClient.post(`/courses/${courseId}/parse-excel`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return data;
    },
    onError: () => message.error('Phân tích file thất bại! Vui lòng kiểm tra lại cấu trúc file PM.'),
  });
};

export const useConfirmImport = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ courseId, payload }: { courseId: number; payload: PMRow[] }) => {
      const { data } = await apiClient.post(`/courses/${courseId}/confirm-import`, payload);
      return data;
    },
    onSuccess: (data) => {
      message.success(data.message || 'Lưu dữ liệu thành công!');
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
      queryClient.invalidateQueries({ queryKey: ['lessons'] });
    },
    onError: () => message.error('Lưu thất bại!'),
  });
};

export const useReviewPM = () => {
  return useMutation({
    mutationFn: async ({ courseId, payload }: { courseId: number; payload: PMRow[] }) => {
      const { data } = await apiClient.post(`/courses/${courseId}/review-pm`, payload);
      return data;
    },
    onSuccess: () => message.success('AI đã review xong!'),
    onError: () => message.error('AI Review thất bại!'),
  });
};

export const useAutoFixPM = () => {
  return useMutation({
    mutationFn: async ({ courseId, payload, reviewReport }: { courseId: number; payload: PMRow[]; reviewReport: string }): Promise<PMRow[]> => {
      const { data } = await apiClient.post(`/courses/${courseId}/auto-fix-pm`, {
        payload,
        review_report: reviewReport
      });
      return data;
    },
    onSuccess: () => message.success('AI đã tự động khắc phục và chỉnh sửa xong!'),
    onError: () => message.error('AI Tự động sửa thất bại!'),
  });
};

export interface PMGenerateFromScratchPayload {
  course_name: string;
  description?: string;
  tech_stack?: string;
  total_sessions: number;
  target_persona?: string;
  course_outcomes?: string;
  capstone_target?: string;
}

export const useGeneratePMFromScratch = () => {
  const messageKey = 'generate-pm-scratch';
  return useMutation({
    mutationFn: async (payload: PMGenerateFromScratchPayload): Promise<PMRow[]> => {
      message.loading({
        content: 'AI Senior Architect đang phân tích và thiết lập 10 cột chương trình PM... Vui lòng chờ khoảng 15-30 giây.',
        key: messageKey,
        duration: 0,
      });
      const { data } = await apiClient.post('/courses/generate-pm-from-scratch', payload);
      return data;
    },
    onSuccess: (data) => {
      message.success({
        content: `AI đã kiến trúc thành công PM 10 cột (${data.length} bài học)!`,
        key: messageKey,
        duration: 4,
      });
    },
    onError: (err: AxiosError<{ detail?: string }>) => {
      const detail = err.response?.data?.detail || err.message || 'AI Sinh PM thất bại!';
      message.error({
        content: detail,
        key: messageKey,
        duration: 5,
      });
    },
  });
};

export const useGenerateAllCourse = () => {
  const messageKey = 'generate-all-course';
  return useMutation({
    mutationFn: async (courseId: number) => {
      message.loading({ content: 'AI đang tạo, vui lòng không thoát ứng dụng', key: messageKey, duration: 0 });
      const { data } = await apiClient.post(`/courses/${courseId}/generate-all`);
      return data;
    },
    onSuccess: (data) => {
      message.success({ content: data.message || 'Đã gửi yêu cầu tạo toàn khóa học tới AI!', key: messageKey, duration: 3 });
    },
    onError: () => {
      message.error({ content: 'Không thể gọi AI, vui lòng thử lại!', key: messageKey, duration: 3 });
    },
  });
};
