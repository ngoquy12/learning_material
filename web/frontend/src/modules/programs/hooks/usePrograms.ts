import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../shared/api/base';
import { ProgramResponse, ProgramCreate } from '../../../types/program';
import { message } from 'antd';

export const programKeys = {
  all: ['programs'] as const,
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
    onError: () => message.error('Thất bại!'),
  });
};
