import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { apiClient } from "../../../shared/api/base";
import {
  LessonResponse,
  LessonCreate,
  LessonUpdate,
} from "../../../types/lesson";
import { message } from "antd";

export const lessonKeys = {
  bySession: (sessionId: number) => ["lessons", { sessionId }] as const,
};

export const useLessons = (sessionId: number) => {
  return useQuery({
    queryKey: lessonKeys.bySession(sessionId),
    queryFn: async (): Promise<LessonResponse[]> => {
      const { data } = await apiClient.get(`/lessons/?session_id=${sessionId}`);
      return data;
    },
    enabled: !!sessionId,
  });
};

export const useCreateLesson = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: LessonCreate) => {
      const { data } = await apiClient.post("/lessons/", payload);
      return data;
    },
    onSuccess: (_, variables) => {
      message.success("Thêm Lesson thành công!");
      queryClient.invalidateQueries({
        queryKey: lessonKeys.bySession(variables.session_id),
      });
    },
    onError: () => message.error("Thất bại!"),
  });
};

export const useUpdateLesson = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      lessonId,
      payload,
    }: {
      lessonId: number;
      payload: LessonUpdate;
    }) => {
      const { data } = await apiClient.put(`/lessons/${lessonId}`, payload);
      return data;
    },
    onSuccess: (data: LessonResponse) => {
      message.success("Cập nhật cấu hình Lesson thành công!");
      queryClient.invalidateQueries({ queryKey: ["lessons"] });
      queryClient.invalidateQueries({ queryKey: ["lesson", data.id] });
    },
    onError: () => message.error("Cập nhật Lesson thất bại!"),
  });
};

export const useGenerateLesson = () => {
  const messageKey = "generate-lesson";
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (lessonId: number) => {
      message.loading({
        content: "AI đang tạo, vui lòng không thoát ứng dụng",
        key: messageKey,
        duration: 0,
      });
      const { data } = await apiClient.post(`/lessons/${lessonId}/generate`);
      return data;
    },
    onSuccess: (_, lessonId) => {
      queryClient.invalidateQueries({ queryKey: ["artifacts", lessonId] });
      message.loading({
        content: "AI đang tạo, vui lòng không thoát ứng dụng",
        key: messageKey,
        duration: 0,
      });
    },
    onError: () => {
      message.error({
        content: "Không thể gọi AI, vui lòng thử lại!",
        key: messageKey,
        duration: 3,
      });
    },
  });
};

export const useDeleteLesson = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (lessonId: number) => {
      const { data } = await apiClient.delete(`/lessons/${lessonId}`);
      return data;
    },
    onSuccess: () => {
      message.success("Xóa Lesson thành công!");
      queryClient.invalidateQueries({ queryKey: ["lessons"] });
    },
  });
};

export const useBatchDeleteLessons = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      lessonIds,
    }: {
      lessonIds: number[];
      sessionId?: number;
    }) => {
      const { data } = await apiClient.post("/lessons/batch-delete", {
        item_ids: lessonIds,
      });
      return data;
    },
    onSuccess: (_, { sessionId }) => {
      message.success("Đã xóa thành công các Lesson đã chọn!");
      queryClient.invalidateQueries({ queryKey: ["lessons"] });
      if (sessionId) {
        queryClient.invalidateQueries({
          queryKey: lessonKeys.bySession(sessionId),
        });
      }
    },
    onError: (err: AxiosError | Error) => {
      message.error(`Xóa Lesson thất bại: ${err?.message || "Lỗi hệ thống"}`);
    },
  });
};

export const useReorderLessons = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      item_ids,
    }: {
      item_ids: number[];
      sessionId: number;
    }) => {
      const { data } = await apiClient.put("/lessons/reorder", { item_ids });
      return data;
    },
    onSuccess: (_, { sessionId }) => {
      queryClient.invalidateQueries({
        queryKey: lessonKeys.bySession(sessionId),
      });
    },
  });
};

export interface ArtifactVersion {
  version_id: number;
  content: string | null;
  content_json: Record<string, unknown> | null;
  created_at: string;
}

export interface ArtifactResponse {
  id: number;
  lesson_id: number;
  type: string;
  content: string | null;
  content_json: Record<string, unknown> | null;
  status: string;
  versions?: ArtifactVersion[] | null;
  created_at: string;
}

export const useArtifacts = (lessonId: number | null) => {
  return useQuery({
    queryKey: ["artifacts", lessonId],
    queryFn: async (): Promise<ArtifactResponse[]> => {
      if (!lessonId) return [];
      const { data } = await apiClient.get(`/artifacts/lesson/${lessonId}`);
      return data;
    },
    enabled: !!lessonId,
    refetchInterval: (query) => {
      // Tự động fetch lại mỗi 3s nếu có bất kỳ artifact nào đang Pending
      const hasPending = query.state?.data?.some((a) => a.status === "Pending");
      return hasPending ? 3000 : false;
    },
  });
};

export const useLesson = (lessonId: number | null) => {
  return useQuery({
    queryKey: ["lesson", lessonId],
    queryFn: async (): Promise<LessonResponse> => {
      if (!lessonId) throw new Error("No lesson ID");
      const { data } = await apiClient.get(`/lessons/${lessonId}`);
      return data;
    },
    enabled: !!lessonId,
  });
};

export const useUpdateArtifact = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({
      artifactId,
      payload,
    }: {
      artifactId: number;
      payload: { content?: string; content_json?: Record<string, unknown> };
    }) => {
      const { data } = await apiClient.put(`/artifacts/${artifactId}`, payload);
      return data;
    },
    onSuccess: (data: ArtifactResponse) => {
      message.success("Đã lưu thay đổi vào cơ sở dữ liệu thành công!");
      queryClient.invalidateQueries({
        queryKey: ["artifacts", data.lesson_id],
      });
      queryClient.invalidateQueries({ queryKey: ["artifact", data.id] });
    },
    onError: () => message.error("Cập nhật thất bại!"),
  });
};

export const useCreateArtifact = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: {
      lesson_id: number;
      type: string;
      content?: string;
      content_json?: Record<string, unknown>;
      status?: string;
    }) => {
      const { data } = await apiClient.post("/artifacts/", payload);
      return data;
    },
    onSuccess: (data: ArtifactResponse) => {
      message.success("Đã khởi tạo thành công!");
      queryClient.invalidateQueries({
        queryKey: ["artifacts", data.lesson_id],
      });
    },
    onError: () => message.error("Khởi tạo thất bại!"),
  });
};
