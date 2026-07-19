import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../shared/api/base';
import { MajorResponse, MajorCreate } from '../../../types/major';
import { message } from 'antd';

export const majorKeys = {
  all: ['majors'] as const,
};

export const useMajors = () => {
  return useQuery({
    queryKey: majorKeys.all,
    queryFn: async (): Promise<MajorResponse[]> => {
      const { data } = await apiClient.get('/majors/');
      return data;
    },
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
    onError: () => message.error('Thất bại!'),
  });
};
