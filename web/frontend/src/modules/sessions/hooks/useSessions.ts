import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../../shared/api/base';
import { SessionResponse, SessionCreate } from '../../../types/session';
import { message } from 'antd';

export const sessionKeys = {
  all: ['sessions'] as const,
  byCourse: (courseId: number) => ['sessions', { courseId }] as const,
};

export const useSessions = (courseId: number) => {
  return useQuery({
    queryKey: sessionKeys.byCourse(courseId),
    queryFn: async (): Promise<SessionResponse[]> => {
      const { data } = await apiClient.get(`/sessions/?course_id=${courseId}`);
      return data;
    },
    enabled: !!courseId,
  });
};

export const useCreateSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: SessionCreate) => {
      const { data } = await apiClient.post('/sessions/', payload);
      return data;
    },
    onSuccess: (_, variables) => {
      message.success('Thêm Session thành công!');
      queryClient.invalidateQueries({ queryKey: sessionKeys.byCourse(variables.course_id) });
    },
    onError: () => message.error('Thất bại!'),
  });
};

export const useDeleteSession = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (sessionId: number) => {
      const { data } = await apiClient.delete(`/sessions/${sessionId}`);
      return data;
    },
    onSuccess: () => {
      message.success('Xóa Session thành công!');
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
    },
  });
};

export const useReorderSessions = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ item_ids }: { item_ids: number[], courseId: number }) => {
      const { data } = await apiClient.put('/sessions/reorder', { item_ids });
      return data;
    },
    onSuccess: (_, { courseId }) => {
      queryClient.invalidateQueries({ queryKey: sessionKeys.byCourse(courseId) });
    },
  });
};

import { ArtifactResponse } from '../../lessons/hooks/useLessons';

export const useSessionArtifacts = (sessionId: number | null) => {
  return useQuery({
    queryKey: ['session_artifacts', sessionId],
    queryFn: async (): Promise<ArtifactResponse[]> => {
      if (!sessionId) return [];
      const { data } = await apiClient.get(`/sessions/${sessionId}/artifacts`);
      return data;
    },
    enabled: !!sessionId,
    refetchInterval: (query) => {
      const hasPending = query.state?.data?.some(a => a.status === 'Pending');
      return hasPending ? 3000 : false;
    }
  });
};

export const useGenerateSession = () => {
  const messageKey = 'generate-session';
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (sessionId: number) => {
      message.loading({ content: 'AI đang tạo, vui lòng không thoát ứng dụng', key: messageKey, duration: 0 });
      const { data } = await apiClient.post(`/sessions/${sessionId}/generate`);
      return data;
    },
    onSuccess: (_, sessionId) => {
      queryClient.invalidateQueries({ queryKey: ['session_artifacts', sessionId] });
      message.loading({ content: 'AI đang tạo, vui lòng không thoát ứng dụng', key: messageKey, duration: 0 });
    },
    onError: () => {
      message.error({ content: 'Không thể gọi AI, vui lòng thử lại!', key: messageKey, duration: 3 });
    },
  });
};

export const useGeneratePracticeSession = () => {
  const messageKey = 'generate-session';
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (sessionId: number) => {
      message.loading({ content: 'AI đang tạo bài thực hành, vui lòng không thoát ứng dụng', key: messageKey, duration: 0 });
      const { data } = await apiClient.post(`/sessions/${sessionId}/generate-practice`);
      return data;
    },
    onSuccess: (_, sessionId) => {
      queryClient.invalidateQueries({ queryKey: ['session_artifacts', sessionId] });
      message.loading({ content: 'AI đang tạo bài thực hành, vui lòng không thoát ứng dụng', key: messageKey, duration: 0 });
    },
    onError: () => {
      message.error({ content: 'Không thể gọi AI tạo bài thực hành, vui lòng thử lại!', key: messageKey, duration: 3 });
    },
  });
};

export const useGenerateProjectSession = () => {
  const messageKey = 'generate-session';
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (sessionId: number) => {
      message.loading({ content: 'AI đang tạo Mini Project, vui lòng không thoát ứng dụng', key: messageKey, duration: 0 });
      const { data } = await apiClient.post(`/sessions/${sessionId}/generate-project`);
      return data;
    },
    onSuccess: (_, sessionId) => {
      queryClient.invalidateQueries({ queryKey: ['session_artifacts', sessionId] });
      message.loading({ content: 'AI đang tạo Mini Project, vui lòng không thoát ứng dụng', key: messageKey, duration: 0 });
    },
    onError: () => {
      message.error({ content: 'Không thể gọi AI tạo Mini Project, vui lòng thử lại!', key: messageKey, duration: 3 });
    },
  });
};
