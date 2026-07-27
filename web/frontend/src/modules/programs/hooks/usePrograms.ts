import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../shared/api/base';
import { ProgramResponse, ProgramCreate } from '../../../types/program';
import { message } from 'antd';

export const programKeys = {
  all: ['programs'] as const,
  detail: (id: number) => ['programs', id] as const,
};

export const usePrograms = () => {
  return useQuery({
    queryKey: programKeys.all,
    queryFn: async (): Promise<ProgramResponse[]> => {
      const { data } = await apiClient.get('/programs/');
      return data;
    },
  });
};

export const useProgram = (id: number | null) => {
  return useQuery({
    queryKey: id ? programKeys.detail(id) : ['programs', 'null'],
    queryFn: async (): Promise<ProgramResponse> => {
      const { data } = await apiClient.get(`/programs/${id}`);
      return data;
    },
    enabled: !!id,
  });
};

export const useCreateProgram = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: ProgramCreate) => {
      const { data } = await apiClient.post('/programs/', payload);
      return data;
    },
    onSuccess: () => {
      message.success('Thêm Hệ đào tạo thành công!');
      queryClient.invalidateQueries({ queryKey: programKeys.all });
    },
    onError: () => message.error('Thất bại khi thêm Hệ đào tạo!'),
  });
};

export const useUpdateProgram = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: ProgramCreate }) => {
      const { data } = await apiClient.put(`/programs/${id}`, payload);
      return data;
    },
    onSuccess: (_, variables) => {
      message.success('Cập nhật Hệ đào tạo thành công!');
      queryClient.invalidateQueries({ queryKey: programKeys.all });
      queryClient.invalidateQueries({ queryKey: programKeys.detail(variables.id) });
    },
    onError: () => message.error('Cập nhật thất bại!'),
  });
};

export const useDeleteProgram = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/programs/${id}`);
    },
    onSuccess: () => {
      message.success('Xóa Hệ đào tạo thành công!');
      queryClient.invalidateQueries({ queryKey: programKeys.all });
    },
    onError: () => message.error('Xóa thất bại!'),
  });
};
