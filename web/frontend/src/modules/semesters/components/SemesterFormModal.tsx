import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Modal, Form, Input, Button, Select } from 'antd';
import { SemesterCreate } from '../../../types/semester';
import { useEffect } from 'react';
import { useMajors } from '../../majors/hooks/useMajors';

const schema = z.object({
  name: z.string().min(1, 'Tên kỳ học không được để trống'),
  major_id: z.number().min(1, 'Vui lòng chọn chuyên ngành'),
});

type FormValues = z.infer<typeof schema>;

interface Props {
  open: boolean;
  onCancel: () => void;
  onSubmit: (data: SemesterCreate) => void;
  isPending: boolean;
}

export const SemesterFormModal = ({ open, onCancel, onSubmit, isPending }: Props) => {
  const { data: majors } = useMajors();
  const { control, handleSubmit, reset, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: '', major_id: undefined },
  });

  useEffect(() => { if (!open) reset(); }, [open, reset]);

  return (
    <Modal title="Thêm Kỳ học" open={open} onCancel={onCancel} footer={null} destroyOnClose>
      <Form layout="vertical" onFinish={handleSubmit(onSubmit)} className="mt-4">
        <Form.Item label="Tên kỳ học" validateStatus={errors.name ? 'error' : ''} help={errors.name?.message}>
          <Controller name="name" control={control} render={({ field }) => <Input {...field} placeholder="VD: Học kỳ 1" />} />
        </Form.Item>
        <Form.Item label="Thuộc Chuyên ngành" validateStatus={errors.major_id ? 'error' : ''} help={errors.major_id?.message}>
          <Controller name="major_id" control={control} render={({ field }) => (
            <Select {...field} placeholder="Chọn chuyên ngành" loading={!majors}>
              {majors?.map(m => <Select.Option key={m.id} value={m.id}>{m.name}</Select.Option>)}
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
