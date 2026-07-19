import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Modal, Form, Input, Button, Select } from 'antd';
import { MajorCreate } from '../../../types/major';
import { useEffect } from 'react';
import { usePrograms } from '../../programs/hooks/usePrograms';

const schema = z.object({
  name: z.string().min(1, 'Tên chuyên ngành không được để trống'),
  program_id: z.number().min(1, 'Vui lòng chọn hệ đào tạo'),
});

type FormValues = z.infer<typeof schema>;

interface Props {
  open: boolean;
  onCancel: () => void;
  onSubmit: (data: MajorCreate) => void;
  isPending: boolean;
}

export const MajorFormModal = ({ open, onCancel, onSubmit, isPending }: Props) => {
  const { data: programs } = usePrograms();
  const { control, handleSubmit, reset, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', program_id: undefined },
  });

  useEffect(() => { if (!open) reset(); }, [open, reset]);

  return (
    <Modal title="Thêm Chuyên ngành" open={open} onCancel={onCancel} footer={null} destroyOnClose>
      <Form layout="vertical" onFinish={handleSubmit(onSubmit)} className="mt-4">
        <Form.Item label="Tên chuyên ngành" validateStatus={errors.name ? 'error' : ''} help={errors.name?.message}>
          <Controller name="name" control={control} render={({ field }) => <Input {...field} />} />
        </Form.Item>
        <Form.Item label="Thuộc Hệ đào tạo" validateStatus={errors.program_id ? 'error' : ''} help={errors.program_id?.message}>
          <Controller name="program_id" control={control} render={({ field }) => (
            <Select {...field} placeholder="Chọn hệ đào tạo" loading={!programs}>
              {programs?.map(p => <Select.Option key={p.id} value={p.id}>{p.name}</Select.Option>)}
            </Select>
          )} />
        </Form.Item>
        <div className="flex justify-end gap-2 mt-6">
          <Button onClick={onCancel} disabled={isPending}>Hủy</Button>
          <Button type="primary" htmlType="submit" loading={isPending}>Lưu</Button>
        </div>
      </Form>
    </Modal>
  );
};
