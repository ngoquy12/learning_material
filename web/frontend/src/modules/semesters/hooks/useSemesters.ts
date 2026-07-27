import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../shared/api/base';
import { SemesterResponse, SemesterCreate } from '../../../types/semester';
import { message } from 'antd';

export const semesterKeys = {
  all: ['semesters'] as const,
  list: (majorId?: number) => ['semesters', 'list', majorId] as const,
  detail: (id: number) => ['semesters', id] as const,
};

export const useSemesters = (majorId?: number) => {
  return useQuery({
    queryKey: semesterKeys.list(majorId),
    queryFn: async (): Promise<SemesterResponse[]> => {
      const url = majorId ? `/semesters/?major_id=${majorId}` : '/semesters/';
      const { data } = await apiClient.get(url);
      return data;
    },
  });
};

export const useSemester = (id: number | null) => {
  return useQuery({
    queryKey: id ? semesterKeys.detail(id) : ['semesters', 'null'],
    queryFn: async (): Promise<SemesterResponse> => {
      const { data } = await apiClient.get(`/semesters/${id}`);
      return data;
    },
    enabled: !!id,
  });
};

export const useCreateSemester = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: SemesterCreate) => {
      const { data } = await apiClient.post('/semesters/', payload);
      return data;
    },
    onSuccess: () => {
      message.success('Thêm Kỳ học thành công!');
      queryClient.invalidateQueries({ queryKey: semesterKeys.all });
    },
    onError: () => message.error('Thất bại khi thêm Kỳ học!'),
  });
};

export const useUpdateSemester = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: SemesterCreate }) => {
      const { data } = await apiClient.put(`/semesters/${id}`, payload);
      return data;
    },
    onSuccess: (_, variables) => {
      message.success('Cập nhật Kỳ học thành công!');
      queryClient.invalidateQueries({ queryKey: semesterKeys.all });
      queryClient.invalidateQueries({ queryKey: semesterKeys.detail(variables.id) });
    },
    onError: () => message.error('Cập nhật thất bại!'),
  });
};

export const useDeleteSemester = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/semesters/${id}`);
    },
    onSuccess: () => {
      message.success('Xóa Kỳ học thành công!');
      queryClient.invalidateQueries({ queryKey: semesterKeys.all });
    },
    onError: () => message.error('Xóa thất bại!'),
  });
};
