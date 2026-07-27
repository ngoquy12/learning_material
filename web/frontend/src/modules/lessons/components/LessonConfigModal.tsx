import { useEffect } from "react";
import { Modal, Form, Input, Button, Tabs } from "antd";
import { Settings2, Sliders, ShieldAlert, CheckCircle2, Code2 } from "lucide-react";
import { LessonResponse, LessonUpdate } from "../../../types/lesson";
import { useUpdateLesson } from "../hooks/useLessons";

interface Props {
  open: boolean;
  lesson: LessonResponse | null;
  onCancel: () => void;
}

export const LessonConfigModal = ({ open, lesson, onCancel }: Props) => {
  const [form] = Form.useForm<LessonUpdate>();
  const { mutate: updateLesson, isPending } = useUpdateLesson();

  useEffect(() => {
    if (open && lesson) {
      form.setFieldsValue({
        name: lesson.name || "",
        title: lesson.title || "",
        details: lesson.details || "",
        expected_output: lesson.expected_output || "",
        forbidden_scope: lesson.forbidden_scope || "",
        allowed_scope: lesson.allowed_scope || "",
        tech_stack: lesson.tech_stack || "",
      });
    } else {
      form.resetFields();
    }
  }, [open, lesson, form]);

  const handleFinish = (values: LessonUpdate) => {
    if (!lesson) return;
    updateLesson(
      { lessonId: lesson.id, payload: values },
      {
        onSuccess: () => {
          onCancel();
        },
      },
    );
  };

  return (
    <Modal
      title={
        <div className="flex items-center gap-2 text-indigo-700 text-lg font-bold">
          <Settings2 size={20} className="text-indigo-600" />
          <span>Cấu Hình & Hiệu Chỉnh Bài Học ({lesson?.name})</span>
        </div>
      }
      open={open}
      onCancel={onCancel}
      footer={null}
      width={720}
      destroyOnClose
      className="rounded-2xl"
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleFinish}
        className="mt-4 space-y-4"
      >
        <Tabs
          defaultActiveKey="general"
          items={[
            {
              key: "general",
              label: (
                <span className="flex items-center gap-1.5 font-semibold">
                  <Sliders size={16} /> Thông Tin Cơ Bản
                </span>
              ),
              children: (
                <div className="space-y-4 pt-2">
                  <div className="grid grid-cols-3 gap-3">
                    <Form.Item
                      label="Mã Lesson"
                      name="name"
                      rules={[{ required: true, message: "Nhập mã bài học" }]}
                      className="col-span-1"
                    >
                      <Input placeholder="VD: Lesson 01" className="font-semibold" />
                    </Form.Item>

                    <Form.Item
                      label="Tiêu đề Bài học"
                      name="title"
                      rules={[{ required: true, message: "Nhập tiêu đề" }]}
                      className="col-span-2"
                    >
                      <Input placeholder="VD: Ép kiểu dữ liệu và f-string" className="font-medium" />
                    </Form.Item>
                  </div>

                  <Form.Item
                    label="Chi Tiết Nội Dung (Prompt Context)"
                    name="details"
                    help="Nội dung chi tiết giảng dạy giúp AI hiểu sâu để sinh bài đọc & slide."
                  >
                    <Input.TextArea
                      rows={4}
                      placeholder="Mô tả chi tiết các khái niệm, quy tắc, cách dùng..."
                      className="text-sm"
                    />
                  </Form.Item>

                  <Form.Item
                    label="Kết Quả Mong Đợi (Expected Outcome)"
                    name="expected_output"
                    help="Mục tiêu đầu ra mà học viên phải đạt được sau bài học."
                  >
                    <Input.TextArea
                      rows={3}
                      placeholder="VD: Học viên tự viết được chương trình nhập vào năm sinh và tính ra tuổi."
                      className="text-sm"
                    />
                  </Form.Item>
                </div>
              ),
            },
            {
              key: "pedagogy",
              label: (
                <span className="flex items-center gap-1.5 font-semibold text-amber-700">
                  <ShieldAlert size={16} /> Quy Chuẩn & Phạm Vi AI
                </span>
              ),
              children: (
                <div className="space-y-4 pt-2">
                  <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800 space-y-1">
                    <div className="font-bold flex items-center gap-1 text-sm text-amber-900">
                      <Code2 size={16} /> Kiểm Soát Quy Chuẩn Sư Phạm Của AI
                    </div>
                    <p>
                      Cấu hình dưới đây sẽ trực tiếp hướng dẫn AI Generator không được vi phạm kiến thức chưa học và tuân thủ đúng phạm vi bài giảng.
                    </p>
                  </div>

                  <Form.Item
                    label={
                      <span className="flex items-center gap-1.5 font-semibold text-red-600">
                        <ShieldAlert size={15} /> Phạm Vi CẤM DÙNG (Forbidden Scope)
                      </span>
                    }
                    name="forbidden_scope"
                    help="Các từ khóa, thư viện, hoặc cú pháp tuyệt đối AI KHÔNG ĐƯỢC DÙNG trong bài học này."
                  >
                    <Input.TextArea
                      rows={2}
                      placeholder="VD: CẤM DÙNG: class, try/except, lambda, list comprehension"
                      className="text-sm border-red-200 focus:border-red-400"
                    />
                  </Form.Item>

                  <Form.Item
                    label={
                      <span className="flex items-center gap-1.5 font-semibold text-emerald-600">
                        <CheckCircle2 size={15} /> Phạm Vi ĐÃ HỌC (Allowed Scope)
                      </span>
                    }
                    name="allowed_scope"
                    help="Kiến thức đã tích lũy từ các bài học trước mà AI ĐƯỢC PHÉP tái sử dụng."
                  >
                    <Input.TextArea
                      rows={2}
                      placeholder="VD: ĐÃ HỌC: print(), input(), int(), float(), str(), phép toán cơ bản"
                      className="text-sm border-emerald-200 focus:border-emerald-400"
                    />
                  </Form.Item>

                  <Form.Item
                    label={
                      <span className="flex items-center gap-1.5 font-semibold text-indigo-600">
                        <Code2 size={15} /> Tech Stack & Quy Chuẩn Mã Nguồn
                      </span>
                    }
                    name="tech_stack"
                    help="Công nghệ và tiêu chuẩn code."
                  >
                    <Input
                      placeholder="VD: Python 3.11 / PEP8"
                      className="text-sm"
                    />
                  </Form.Item>
                </div>
              ),
            },
          ]}
        />

        <div className="flex justify-end gap-2 pt-4 border-t border-gray-100">
          <Button onClick={onCancel} disabled={isPending}>
            Hủy
          </Button>
          <Button
            type="primary"
            htmlType="submit"
            loading={isPending}
            className="bg-indigo-600 hover:bg-indigo-700 font-semibold"
          >
            Lưu Cấu Hình
          </Button>
        </div>
      </Form>
    </Modal>
  );
};
