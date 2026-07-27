import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../shared/api/base';
import { MajorResponse, MajorCreate } from '../../../types/major';
import { message } from 'antd';

export const majorKeys = {
  all: ['majors'] as const,
  list: (programId?: number) => ['majors', 'list', programId] as const,
  detail: (id: number) => ['majors', id] as const,
};

export const useMajors = (programId?: number) => {
  return useQuery({
    queryKey: majorKeys.list(programId),
    queryFn: async (): Promise<MajorResponse[]> => {
      const url = programId ? `/majors/?program_id=${programId}` : '/majors/';
      const { data } = await apiClient.get(url);
      return data;
    },
  });
};

export const useMajor = (id: number | null) => {
  return useQuery({
    queryKey: id ? majorKeys.detail(id) : ['majors', 'null'],
    queryFn: async (): Promise<MajorResponse> => {
      const { data } = await apiClient.get(`/majors/${id}`);
      return data;
    },
    enabled: !!id,
  });
};

export const useCreateMajor = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: MajorCreate) => {
      const { data } = await apiClient.post('/majors/', payload);
      return data;
    },
    onSuccess: () => {
      message.success('Thêm Chuyên ngành thành công!');
      queryClient.invalidateQueries({ queryKey: majorKeys.all });
    },
    onError: () => message.error('Thất bại khi thêm Chuyên ngành!'),
  });
};

export const useUpdateMajor = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: MajorCreate }) => {
      const { data } = await apiClient.put(`/majors/${id}`, payload);
      return data;
    },
    onSuccess: (_, variables) => {
      message.success('Cập nhật Chuyên ngành thành công!');
      queryClient.invalidateQueries({ queryKey: majorKeys.all });
      queryClient.invalidateQueries({ queryKey: majorKeys.detail(variables.id) });
    },
    onError: () => message.error('Cập nhật thất bại!'),
  });
};

export const useDeleteMajor = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/majors/${id}`);
    },
    onSuccess: () => {
      message.success('Xóa Chuyên ngành thành công!');
      queryClient.invalidateQueries({ queryKey: majorKeys.all });
    },
    onError: () => message.error('Xóa thất bại!'),
  });
};
