import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Modal, Form, Input, Button } from 'antd';
import { ProgramCreate } from '../../../types/program';
import { useEffect } from 'react';

const schema = z.object({
  name: z.string().min(1, 'Tên hệ đào tạo không được để trống'),
  description: z.string().optional(),
});

type FormValues = z.infer<typeof schema>;

interface Props {
  open: boolean;
  onCancel: () => void;
  onSubmit: (data: ProgramCreate) => void;
  isPending: boolean;
}

export const ProgramFormModal = ({ open, onCancel, onSubmit, isPending }: Props) => {
  const { control, handleSubmit, reset, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', description: '' },
  });

  useEffect(() => { if (!open) reset(); }, [open, reset]);

  return (
    <Modal title="Thêm Hệ đào tạo" open={open} onCancel={onCancel} footer={null} destroyOnClose>
      <Form layout="vertical" onFinish={handleSubmit(onSubmit)} className="mt-4">
        <Form.Item label="Tên hệ đào tạo" validateStatus={errors.name ? 'error' : ''} help={errors.name?.message}>
          <Controller name="name" control={control} render={({ field }) => <Input {...field} />} />
        </Form.Item>
        <Form.Item label="Mô tả">
          <Controller name="description" control={control} render={({ field }) => <Input.TextArea {...field} rows={3} />} />
        </Form.Item>
        <div className="flex justify-end gap-2 mt-6">
          <Button onClick={onCancel} disabled={isPending}>Hủy</Button>
          <Button type="primary" htmlType="submit" loading={isPending}>Lưu</Button>
        </div>
      </Form>
    </Modal>
  );
};
