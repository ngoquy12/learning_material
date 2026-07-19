import { useState } from 'react';
import { Table, Button, Card, Tag } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Plus } from 'lucide-react';
import { useCourses, useCreateCourse } from '../hooks/useCourses';
import { CourseResponse } from '../../../types/course';
import { CourseFormModal } from '../components/CourseFormModal';
import { useNavigate } from 'react-router-dom';

export default function CourseListPage() {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { data: courses, isLoading } = useCourses();
  const { mutate: createCourse, isPending } = useCreateCourse();

  const columns: ColumnsType<CourseResponse> = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: 'Tên môn học',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Công nghệ',
      dataIndex: 'technology_stack',
      key: 'technology_stack',
      render: (tech) => (
        tech ? <Tag color="blue">{tech}</Tag> : <span className="text-gray-400">Trống</span>
      ),
    },
    {
      title: 'Học kỳ',
      dataIndex: 'semester_id',
      key: 'semester_id',
      render: (val) => `Kỳ ${val}`,
    },
    {
      title: 'Hành động',
      key: 'action',
      render: (_, record) => (
        <Button type="primary" size="small" ghost onClick={() => navigate(`/courses/${record.id}`)}>
          Vào xem chi tiết
        </Button>
      )
    }
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Quản lý Môn học</h2>
          <p className="text-gray-500 text-sm">Danh sách các môn học trong hệ thống</p>
        </div>
        <Button
          type="primary"
          icon={<Plus size={16} />}
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-2"
        >
          Thêm Môn học
        </Button>
      </div>

      <Card bordered={false} className="shadow-sm">
        <Table
          columns={columns}
          dataSource={courses}
          rowKey="id"
          loading={isLoading}
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <CourseFormModal
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        isPending={isPending}
        onSubmit={(data) => {
          createCourse(data, {
            onSuccess: () => setIsModalOpen(false),
          });
        }}
      />
    </div>
  );
}
