import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../shared/api/base';
import { CourseResponse, CourseCreate } from '../../../types/course';
import { message } from 'antd';

export const courseKeys = {
  all: ['courses'] as const,
};

export const useCourses = () => {
  return useQuery({
    queryKey: courseKeys.all,
    queryFn: async (): Promise<CourseResponse[]> => {
      const { data } = await apiClient.get('/courses/');
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

export interface PMRow {
  stt: string;
  form: string;
  session_val: string;
  content_val: string;
  lesson_val: string;
  details_val: string;
  output_val: string;
  deadline: string;
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
