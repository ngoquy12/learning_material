import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Modal, Form, Input, Select, Button } from 'antd';
import { CourseCreate, CourseResponse } from '../../../types/course';
import { useEffect } from 'react';
import { useSemesters } from '../../semesters/hooks/useSemesters';

const courseSchema = z.object({
  name: z.string().min(1, 'Tên môn học không được để trống'),
  technology_stack: z.string().optional(),
  semester_id: z.number().min(1, 'Vui lòng chọn học kỳ'),
});

type CourseFormValues = z.infer<typeof courseSchema>;

interface Props {
  open: boolean;
  onCancel: () => void;
  onSubmit: (data: CourseCreate) => void;
  isPending: boolean;
  initialValues?: CourseResponse | null;
  fixedSemesterId?: number;
}

export const CourseFormModal = ({ open, onCancel, onSubmit, isPending, initialValues, fixedSemesterId }: Props) => {
  const { data: semesters } = useSemesters();
  
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CourseFormValues>({
    resolver: zodResolver(courseSchema),
    defaultValues: {
      name: '',
      technology_stack: '',
      semester_id: fixedSemesterId || undefined,
    },
  });

  useEffect(() => {
    if (open) {
      if (initialValues) {
        reset({
          name: initialValues.name || '',
          technology_stack: initialValues.technology_stack || '',
          semester_id: initialValues.semester_id,
        });
      } else {
        reset({
          name: '',
          technology_stack: '',
          semester_id: fixedSemesterId || undefined,
        });
      }
    }
  }, [open, initialValues, fixedSemesterId, reset]);

  return (
    <Modal
      title={initialValues ? "Sửa Môn học" : "Thêm Môn học mới"}
      open={open}
      onCancel={onCancel}
      footer={null}
      destroyOnClose
    >
      <Form layout="vertical" onFinish={handleSubmit(onSubmit)} className="mt-4">
        <Form.Item
          label="Tên môn học"
          validateStatus={errors.name ? 'error' : ''}
          help={errors.name?.message}
        >
          <Controller
            name="name"
            control={control}
            render={({ field }) => <Input {...field} placeholder="Ví dụ: Lập trình Python Căn Bản" />}
          />
        </Form.Item>

        <Form.Item
          label="Công nghệ sử dụng (Technology Stack)"
          validateStatus={errors.technology_stack ? 'error' : ''}
          help={errors.technology_stack?.message}
        >
          <Controller
            name="technology_stack"
            control={control}
            render={({ field }) => (
              <Input {...field} placeholder="Ví dụ: python/core, Java, Spring Boot" />
            )}
          />
        </Form.Item>

        <Form.Item
          label="Thuộc Học kỳ"
          validateStatus={errors.semester_id ? 'error' : ''}
          help={errors.semester_id?.message}
        >
          <Controller
            name="semester_id"
            control={control}
            render={({ field }) => (
              <Select {...field} placeholder="Chọn học kỳ" loading={!semesters} disabled={!!fixedSemesterId}>
                {semesters?.map(s => <Select.Option key={s.id} value={s.id}>{s.name}</Select.Option>)}
              </Select>
            )}
          />
        </Form.Item>

        <div className="flex justify-end gap-2 mt-6">
          <Button onClick={onCancel} disabled={isPending}>
            Hủy
          </Button>
          <Button type="primary" htmlType="submit" loading={isPending}>
            Lưu
          </Button>
        </div>
      </Form>
    </Modal>
  );
};
