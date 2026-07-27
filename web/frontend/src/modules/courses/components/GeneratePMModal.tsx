import { Modal, Form, Input, InputNumber, Button, Alert, Collapse } from "antd";
import { Sparkles, Brain, Wand2, Sliders } from "lucide-react";
import { useGeneratePMFromScratch, PMRow } from "../hooks/useCourses";

interface Props {
  open: boolean;
  onCancel: () => void;
  onSuccess: (generatedRows: PMRow[]) => void;
  defaultCourseName?: string;
  defaultTechStack?: string;
}

export const GeneratePMModal = ({
  open,
  onCancel,
  onSuccess,
  defaultCourseName = "",
  defaultTechStack = "",
}: Props) => {
  const [form] = Form.useForm();
  const { mutate: generatePM, isPending } = useGeneratePMFromScratch();

  const handleFinish = (values: {
    course_name: string;
    description?: string;
    tech_stack?: string;
    total_sessions: number;
    target_persona?: string;
    course_outcomes?: string;
    capstone_target?: string;
  }) => {
    generatePM(values, {
      onSuccess: (data) => {
        onSuccess(data);
        onCancel();
      },
    });
  };

  return (
    <Modal
      open={open}
      title={
        <div className="flex items-center gap-2 text-indigo-700 font-bold text-lg">
          <div className="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-600 flex items-center justify-center">
            <Wand2 size={18} className="animate-bounce" />
          </div>
          <span>AI Tự Động Sinh PM 10 Cột Môn Học</span>
        </div>
      }
      onCancel={onCancel}
      footer={null}
      width={650}
      destroyOnClose
    >
      <Alert
        type="info"
        showIcon
        icon={<Brain size={18} className="text-indigo-600" />}
        message="AI Senior Curriculum Architect Agent"
        description="Bạn chỉ cần nhập Tên môn học và Mô tả ngắn. AI Agent sẽ tự động làm rõ Chân dung sinh viên, Mục tiêu đầu ra CLO, Capstone Target, Tech Stack và thiết lập 10 cột ranh giới kiến thức chuẩn sư phạm."
        className="mb-5 rounded-xl border-indigo-200 bg-indigo-50/50 text-xs leading-relaxed"
      />

      <Form
        form={form}
        layout="vertical"
        onFinish={handleFinish}
        initialValues={{
          course_name: defaultCourseName || "",
          description: "",
          tech_stack: defaultTechStack || "",
          total_sessions: 30,
        }}
        size="middle"
      >
        <Form.Item
          name="course_name"
          label={<span className="font-bold text-xs text-slate-800">Tên Môn Học *</span>}
          rules={[{ required: true, message: "Vui lòng nhập tên môn học" }]}
        >
          <Input
            placeholder="Ví dụ: Lập trình Python Core & OOP, Lập trình Web với FastAPI, React Masterclass..."
            className="rounded-lg text-sm"
          />
        </Form.Item>

        <Form.Item
          name="description"
          label={<span className="font-bold text-xs text-slate-800">Mô Tả Ngắn Về Môn Học (Tùy chọn)</span>}
        >
          <Input.TextArea
            rows={3}
            placeholder="Ví dụ: Môn học dành cho người mới bắt đầu, hướng dẫn từ cú pháp Python căn bản tới tư duy lập trình hướng đối tượng OOP và làm đồ án quản lý dữ liệu..."
            className="rounded-lg text-xs"
          />
        </Form.Item>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Form.Item
            name="total_sessions"
            label={<span className="font-bold text-xs text-slate-800">Tổng Số Buổi Học (Sessions)</span>}
            rules={[{ required: true, message: "Nhập số buổi" }]}
          >
            <InputNumber min={5} max={60} className="w-full rounded-lg" addonAfter="Buổi" />
          </Form.Item>

          <Form.Item
            name="tech_stack"
            label={<span className="font-bold text-xs text-slate-800">Tech Stack & Quy Chuẩn (Tự động nếu để trống)</span>}
          >
            <Input placeholder="Tự động suy luận theo tên môn..." className="rounded-lg text-xs" />
          </Form.Item>
        </div>

        <Collapse
          ghost
          className="bg-slate-50/80 rounded-xl border border-slate-200/80 mb-4"
          items={[
            {
              key: "advanced",
              label: (
                <span className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
                  <Sliders size={14} className="text-slate-500" /> Tùy chỉnh nâng cao (Dành cho Giám đốc Học thuật)
                </span>
              ),
              children: (
                <div className="space-y-3 pt-1">
                  <Form.Item
                    name="target_persona"
                    label={<span className="text-xs font-semibold text-slate-600">Chân Dung Sinh Viên Target</span>}
                    className="mb-2"
                  >
                    <Input.TextArea rows={2} placeholder="AI sẽ tự sinh nếu để trống..." className="text-xs" />
                  </Form.Item>

                  <Form.Item
                    name="course_outcomes"
                    label={<span className="text-xs font-semibold text-slate-600">Mục Tiêu Đầu Ra Môn Học (CLOs)</span>}
                    className="mb-2"
                  >
                    <Input.TextArea rows={2} placeholder="AI sẽ tự sinh nếu để trống..." className="text-xs" />
                  </Form.Item>

                  <Form.Item
                    name="capstone_target"
                    label={<span className="text-xs font-semibold text-slate-600">Sản Phẩm Capstone Target</span>}
                    className="mb-0"
                  >
                    <Input.TextArea rows={2} placeholder="AI sẽ tự sinh nếu để trống..." className="text-xs" />
                  </Form.Item>
                </div>
              ),
            },
          ]}
        />

        <div className="flex justify-end gap-2.5 pt-3 border-t">
          <Button onClick={onCancel} disabled={isPending}>
            Hủy
          </Button>
          <Button
            type="primary"
            htmlType="submit"
            loading={isPending}
            onClick={() => form.submit()}
            icon={<Sparkles size={16} />}
            className="bg-gradient-to-r from-indigo-600 via-purple-600 to-teal-600 hover:opacity-90 font-bold border-none shadow-md px-5"
          >
            {isPending ? "AI Đang Tự Động Kiến Trúc PM 10 Cột..." : "Kích Hoạt AI Sinh PM 10 Cột Tự Động"}
          </Button>
        </div>
      </Form>
    </Modal>
  );
};
