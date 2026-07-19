import { useEffect } from 'react';
import { Card, Col, Row, Statistic, Progress, Spin, Alert, Tag } from 'antd';
import {
  BookOpen, FileText, CheckCircle, Clock, Brain, Database,
  TrendingUp, Zap, Rocket, Settings
} from 'lucide-react';
import { useDashboardStats } from '../../../services/hooks';

export default function DashboardPage() {
  const { data: stats, loading, error, refetch } = useDashboardStats();

  // Auto-refresh every 30s
  useEffect(() => {
    const id = setInterval(refetch, 30000);
    return () => clearInterval(id);
  }, [refetch]);

  if (loading && !stats) {
    return (
      <div className="flex items-center justify-center h-64">
        <Spin size="large" tip="Đang tải thống kê hệ thống..." />
      </div>
    );
  }

  const artifactSuccessRate = stats?.artifacts.success_rate ?? 0;
  const rateColor = artifactSuccessRate >= 80 ? '#52c41a' : artifactSuccessRate >= 50 ? '#faad14' : '#ff4d4f';

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 m-0">Dashboard</h1>
          <p className="text-gray-500 text-sm mt-1">
            Hệ thống sản xuất học liệu tự động • Cập nhật mỗi 30 giây
          </p>
        </div>
        {error && (
          <Alert
            type="warning"
            message="Không thể kết nối API"
            description="Đang hiển thị dữ liệu tĩnh"
            showIcon
            closable
            className="max-w-xs"
          />
        )}
      </div>

      {/* Row 1: Core counts */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} className="shadow-sm hover:shadow-md transition-shadow h-full">
            <Statistic
              title={<span className="text-gray-600 font-medium">Tổng số Môn học</span>}
              value={stats?.courses ?? '—'}
              prefix={<BookOpen size={20} className="text-blue-500 mr-2 inline" />}
              valueStyle={{ color: '#1677ff', fontWeight: 700 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} className="shadow-sm hover:shadow-md transition-shadow h-full">
            <Statistic
              title={<span className="text-gray-600 font-medium">Tổng Session</span>}
              value={stats?.sessions ?? '—'}
              prefix={<FileText size={20} className="text-purple-500 mr-2 inline" />}
              valueStyle={{ color: '#722ed1', fontWeight: 700 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} className="shadow-sm hover:shadow-md transition-shadow h-full">
            <Statistic
              title={<span className="text-gray-600 font-medium">Tổng Bài học</span>}
              value={stats?.lessons ?? '—'}
              prefix={<CheckCircle size={20} className="text-green-500 mr-2 inline" />}
              valueStyle={{ color: '#52c41a', fontWeight: 700 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} className="shadow-sm hover:shadow-md transition-shadow h-full">
            <Statistic
              title={<span className="text-gray-600 font-medium">Đang xử lý</span>}
              value={stats?.artifacts.pending ?? '—'}
              prefix={<Clock size={20} className="text-orange-500 mr-2 inline" />}
              valueStyle={{ color: '#fa8c16', fontWeight: 700 }}
            />
          </Card>
        </Col>
      </Row>

      {/* Row 2: AI Intelligence stats */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={8}>
          <Card
            title={<span className="flex items-center gap-2"><TrendingUp size={16} className="text-blue-500" /> Tỷ lệ thành công Artifacts</span>}
            bordered={false}
            className="shadow-sm h-full"
          >
            <div className="text-center mb-4">
              <span className="text-4xl font-bold" style={{ color: rateColor }}>
                {artifactSuccessRate}%
              </span>
            </div>
            <Progress
              percent={artifactSuccessRate}
              strokeColor={rateColor}
              showInfo={false}
              strokeWidth={12}
            />
            <Row gutter={8} className="mt-4">
              <Col span={8} className="text-center">
                <div className="text-lg font-semibold text-green-600">{stats?.artifacts.completed ?? 0}</div>
                <div className="text-xs text-gray-500">Completed</div>
              </Col>
              <Col span={8} className="text-center">
                <div className="text-lg font-semibold text-orange-500">{stats?.artifacts.pending ?? 0}</div>
                <div className="text-xs text-gray-500">Pending</div>
              </Col>
              <Col span={8} className="text-center">
                <div className="text-lg font-semibold text-red-500">{stats?.artifacts.failed ?? 0}</div>
                <div className="text-xs text-gray-500">Failed</div>
              </Col>
            </Row>
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card
            title={<span className="flex items-center gap-2"><Zap size={16} className="text-yellow-500" /> Semantic Cache</span>}
            bordered={false}
            className="shadow-sm h-full"
          >
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-yellow-50 rounded-lg">
                <span className="text-gray-600">Tổng lần Cache HIT</span>
                <span className="text-2xl font-bold text-yellow-600">{stats?.cache_hits ?? 0}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                <span className="text-gray-600">Token ước tính tiết kiệm</span>
                <span className="text-lg font-semibold text-green-600">
                  ~{((stats?.cache_hits ?? 0) * 800).toLocaleString()}
                </span>
              </div>
              <Tag color="green" className="w-full text-center py-1">Cache đang hoạt động</Tag>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card
            title={<span className="flex items-center gap-2"><Brain size={16} className="text-purple-500" /> Knowledge Memory</span>}
            bordered={false}
            className="shadow-sm h-full"
          >
            <div className="text-center mb-4">
              <div className="text-5xl font-bold text-purple-600">{stats?.knowledge_memories ?? 0}</div>
              <div className="text-gray-500 mt-1">Lessons learned đã lưu</div>
            </div>
            <div className="bg-purple-50 rounded-lg p-3 text-sm text-purple-700">
              <Database size={14} className="inline mr-1" />
              Agent tự học từ lỗi cũ — bảo vệ các lần chạy tương lai.
            </div>
          </Card>
        </Col>
      </Row>

      {/* Quick actions banner */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white">
        <div className="flex justify-between items-center flex-wrap gap-4">
          <div>
            <h3 className="text-lg font-bold m-0 flex items-center gap-2">
              <Rocket size={20} className="text-yellow-300 fill-yellow-300" />
              Hệ thống sẵn sàng
            </h3>
            <p className="text-blue-100 mt-1 m-0">
              Pipeline đầy đủ: PM → Prerequisite Guard → AI Generation → SCORM Export
            </p>
          </div>
          <div className="flex gap-3 flex-wrap">
            <a href="/courses" className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors text-sm flex items-center gap-1.5">
              <BookOpen size={16} />
              Quản lý Môn học
            </a>
            <a href="/pipeline" className="bg-white/20 text-white px-4 py-2 rounded-lg font-medium hover:bg-white/30 transition-colors text-sm border border-white/30 flex items-center gap-1.5">
              <Settings size={16} />
              Pipeline Monitor
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
