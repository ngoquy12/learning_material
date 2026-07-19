import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Modal, Form, Input, Button } from 'antd';
import { LessonCreate } from '../../../types/lesson';
import { useEffect } from 'react';

const schema = z.object({
  name: z.string().min(1, 'Mã bài học không được để trống'),
  title: z.string().min(1, 'Tiêu đề không được để trống'),
  details: z.string().optional(),
  expected_output: z.string().optional(),
  session_id: z.number(),
});

type FormValues = z.infer<typeof schema>;

interface Props {
  open: boolean;
  sessionId: number;
  onCancel: () => void;
  onSubmit: (data: LessonCreate) => void;
  isPending: boolean;
}

export const LessonFormModal = ({ open, sessionId, onCancel, onSubmit, isPending }: Props) => {
  const { control, handleSubmit, reset, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', title: '', details: '', expected_output: '', session_id: sessionId },
  });

  useEffect(() => {
    if (open) reset({ name: '', title: '', details: '', expected_output: '', session_id: sessionId });
  }, [open, sessionId, reset]);

  return (
    <Modal title="Thêm Bài học (Lesson)" open={open} onCancel={onCancel} footer={null} destroyOnClose>
      <Form layout="vertical" onFinish={handleSubmit(onSubmit)} className="mt-4">
        <Form.Item label="Mã Lesson (VD: Lesson 01.1)" validateStatus={errors.name ? 'error' : ''} help={errors.name?.message}>
          <Controller name="name" control={control} render={({ field }) => <Input {...field} />} />
        </Form.Item>
        <Form.Item label="Tiêu đề Bài học" validateStatus={errors.title ? 'error' : ''} help={errors.title?.message}>
          <Controller name="title" control={control} render={({ field }) => <Input {...field} />} />
        </Form.Item>
        <Form.Item label="Chi tiết (Prompt context)">
          <Controller name="details" control={control} render={({ field }) => <Input.TextArea {...field} rows={3} />} />
        </Form.Item>
        <div className="flex justify-end gap-2 mt-6">
          <Button onClick={onCancel} disabled={isPending}>Hủy</Button>
          <Button type="primary" htmlType="submit" loading={isPending}>Lưu</Button>
        </div>
      </Form>
    </Modal>
  );
};
