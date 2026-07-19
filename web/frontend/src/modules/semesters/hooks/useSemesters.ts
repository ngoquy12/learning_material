import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../shared/api/base';
import { SemesterResponse, SemesterCreate } from '../../../types/semester';
import { message } from 'antd';

export const semesterKeys = {
  all: ['semesters'] as const,
};

export const useSemesters = () => {
  return useQuery({
    queryKey: semesterKeys.all,
    queryFn: async (): Promise<SemesterResponse[]> => {
      const { data } = await apiClient.get('/semesters/');
      return data;
    },
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
    onError: () => message.error('Thất bại!'),
  });
};
