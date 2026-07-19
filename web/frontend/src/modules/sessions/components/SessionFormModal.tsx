import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Modal, Form, Input, Button } from 'antd';
import { SessionCreate } from '../../../types/session';
import { useEffect } from 'react';

const schema = z.object({
  name: z.string().min(1, 'Mã phiên (Session) không được để trống'),
  title: z.string().min(1, 'Tiêu đề không được để trống'),
  course_id: z.number(),
});

type FormValues = z.infer<typeof schema>;

interface Props {
  open: boolean;
  courseId: number;
  onCancel: () => void;
  onSubmit: (data: SessionCreate) => void;
  isPending: boolean;
}

export const SessionFormModal = ({ open, courseId, onCancel, onSubmit, isPending }: Props) => {
  const { control, handleSubmit, reset, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', title: '', course_id: courseId },
  });

  useEffect(() => {
    if (open) reset({ name: '', title: '', course_id: courseId });
  }, [open, courseId, reset]);

  return (
    <Modal title="Thêm Session" open={open} onCancel={onCancel} footer={null} destroyOnClose>
      <Form layout="vertical" onFinish={handleSubmit(onSubmit)} className="mt-4">
        <Form.Item label="Mã Session (VD: Session 01)" validateStatus={errors.name ? 'error' : ''} help={errors.name?.message}>
          <Controller name="name" control={control} render={({ field }) => <Input {...field} />} />
        </Form.Item>
        <Form.Item label="Tiêu đề Session" validateStatus={errors.title ? 'error' : ''} help={errors.title?.message}>
          <Controller name="title" control={control} render={({ field }) => <Input {...field} />} />
        </Form.Item>
        <div className="flex justify-end gap-2 mt-6">
          <Button onClick={onCancel} disabled={isPending}>Hủy</Button>
          <Button type="primary" htmlType="submit" loading={isPending}>Lưu</Button>
        </div>
      </Form>
    </Modal>
  );
};
