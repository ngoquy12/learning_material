import { useEffect } from 'react';
import {
  Card, Button, Form, Input, Select, Slider, Switch, Radio, Divider,
  Alert, Statistic, Row, Col, Spin, message, Tabs, Tag, Popconfirm
} from 'antd';
import {
  Settings, Brain, Cpu, Database, Save, RotateCcw,
  Sparkles, Folder, HelpCircle, Package, Monitor, ShieldCheck, RefreshCw, Zap
} from 'lucide-react';
import {
  useCacheStats,
  useClearCache,
  useSystemSettings,
  useUpdateSystemSettings,
  useResetSystemSettings
} from '../../../services/hooks';
import type { SystemSettings } from '../../../services/api';

export default function SettingsPage() {
  const [form] = Form.useForm();
  
  // Real backend System Settings & Actions
  const { data: settingsData, loading: settingsLoading, refetch: refetchSettings } = useSystemSettings();
  const { execute: updateSettingsExec, loading: saving } = useUpdateSystemSettings();
  const { execute: resetSettingsExec, loading: resetting } = useResetSystemSettings();

  // Real Cache Statistics & Actions
  const { data: cacheStats, loading: cacheLoading, refetch: refetchCache } = useCacheStats();
  const { execute: doClearCache, loading: clearingCache } = useClearCache();

  // Sync loaded settings into Ant Design form
  useEffect(() => {
    if (settingsData) {
      form.setFieldsValue(settingsData);
    }
  }, [settingsData, form]);

  const handleSave = async (values: SystemSettings) => {
    try {
      await updateSettingsExec(values);
      message.success('Đã lưu cấu hình hệ thống thành công vào cơ sở dữ liệu!');
      refetchSettings();
    } catch (e) {
      message.error('Lưu cấu hình thất bại: ' + (e instanceof Error ? e.message : String(e)));
    }
  };

  const handleResetDefaults = async () => {
    try {
      const defaultData = await resetSettingsExec();
      form.setFieldsValue(defaultData);
      message.info('Đã khôi phục cấu hình hệ thống về mặc định nhà sản xuất.');
      refetchSettings();
    } catch (e) {
      message.error('Khôi phục thất bại: ' + (e instanceof Error ? e.message : String(e)));
    }
  };

  const handleClearCache = async () => {
    try {
      await doClearCache();
      message.success('Đã dọn dẹp Semantic Cache của AI Agent thành công!');
      refetchCache();
    } catch (e) {
      message.error('Dọn dẹp cache thất bại: ' + (e instanceof Error ? e.message : String(e)));
    }
  };

  const tokenSavings = cacheStats ? cacheStats.estimated_tokens_saved : 0;

  if (settingsLoading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-[60vh] gap-3">
        <Spin size="large" />
        <p className="text-slate-500 text-sm font-medium">Đang tải cấu hình hệ thống từ máy chủ...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Top Banner Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Tag color="teal" className="font-semibold text-xs px-2.5 py-0.5 rounded-full">
              System Configuration
            </Tag>
            <span className="text-xs text-slate-400 font-medium">Phiên bản 2.5 • Backend Connected</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight flex items-center gap-2.5">
            <Settings className="text-teal-600" size={26} /> Cấu Hình Hệ Thống & AI Content Factory
          </h1>
          <p className="text-slate-500 text-xs md:text-sm mt-1">
            Quản lý các tham số mô hình LLM, bộ nhớ đệm Semantic Cache, thư mục đồng bộ Obsidian và chuẩn đóng gói SCORM.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <Popconfirm
            title="Khôi phục cấu hình mặc định?"
            description="Tất cả tùy chỉnh hiện tại sẽ được đặt lại về thông số chuẩn ban đầu."
            onConfirm={handleResetDefaults}
            okText="Khôi phục"
            cancelText="Hủy"
          >
            <Button
              icon={<RotateCcw size={15} />}
              loading={resetting}
              disabled={saving}
              className="rounded-xl font-medium h-10 px-4 flex items-center gap-1.5"
            >
              Đặt Mặc Định
            </Button>
          </Popconfirm>

          <Button
            type="primary"
            icon={<Save size={16} />}
            loading={saving}
            onClick={() => form.submit()}
            className="bg-teal-600 hover:bg-teal-700 shadow-md font-semibold text-sm rounded-xl h-10 px-5 flex items-center gap-1.5"
          >
            Lưu Thay Đổi
          </Button>
        </div>
      </div>

      <Form
        form={form}
        layout="vertical"
        onFinish={handleSave}
        requiredMark={false}
        initialValues={settingsData || {}}
      >
        <Row gutter={[24, 24]}>
          {/* Left Column: Config Forms */}
          <Col xs={24} lg={16}>
            <Tabs
              defaultActiveKey="ai"
              type="card"
              className="bg-transparent border-none"
              items={[
                {
                  key: 'ai',
                  label: (
                    <span className="flex items-center gap-2 font-semibold px-1 py-1">
                      <Cpu size={16} className="text-teal-600" /> AI Core Engine
                    </span>
                  ),
                  children: (
                    <Card bordered={false} className="shadow-sm border border-slate-100 rounded-2xl p-2 space-y-4">
                      <div className="border-b border-slate-100 pb-3 mb-4">
                        <h3 className="text-base font-bold text-slate-800 m-0 flex items-center gap-2">
                          <Cpu className="text-teal-600" size={18} /> Mô hình ngôn ngữ lớn (LLM Model)
                        </h3>
                        <p className="text-xs text-slate-500 mt-1">Cấu hình nhà cung cấp và tham số sinh nội dung sư phạm AI</p>
                      </div>

                      <Row gutter={16}>
                        <Col span={12}>
                          <Form.Item
                            label={<span className="font-semibold text-slate-700 text-xs">Nhà cung cấp LLM</span>}
                            name="llmProvider"
                            rules={[{ required: true, message: 'Vui lòng chọn nhà cung cấp' }]}
                          >
                            <Select size="large" className="rounded-xl">
                              <Select.Option value="gemini">Google Gemini (Khuyên dùng)</Select.Option>
                              <Select.Option value="openai">OpenAI GPT</Select.Option>
                              <Select.Option value="anthropic">Anthropic Claude</Select.Option>
                              <Select.Option value="ollama">Ollama (Chạy Offline)</Select.Option>
                            </Select>
                          </Form.Item>
                        </Col>

                        <Col span={12}>
                          <Form.Item
                            label={<span className="font-semibold text-slate-700 text-xs">Mô hình hoạt động</span>}
                            name="modelName"
                            rules={[{ required: true, message: 'Vui lòng chọn mô hình' }]}
                          >
                            <Select size="large" className="rounded-xl">
                              <Select.Option value="gemini-1.5-pro">gemini-1.5-pro-latest</Select.Option>
                              <Select.Option value="gemini-1.5-flash">gemini-1.5-flash-latest</Select.Option>
                              <Select.Option value="gpt-4o">gpt-4o</Select.Option>
                              <Select.Option value="claude-3-5-sonnet">claude-3-5-sonnet</Select.Option>
                            </Select>
                          </Form.Item>
                        </Col>
                      </Row>

                      <Row gutter={16}>
                        <Col span={12}>
                          <Form.Item
                            label={
                              <span className="font-semibold text-slate-700 text-xs flex items-center gap-1">
                                Độ sáng tạo (Temperature)
                                <HelpCircle size={13} className="text-slate-400 cursor-pointer" />
                              </span>
                            }
                            name="temperature"
                          >
                            <Slider min={0} max={1} step={0.05} tooltip={{ formatter: (v) => `${v}` }} />
                          </Form.Item>
                        </Col>
                        <Col span={12}>
                          <Form.Item
                            label={<span className="font-semibold text-slate-700 text-xs">Giới hạn Output Tokens</span>}
                            name="maxTokens"
                          >
                            <Select size="large" className="rounded-xl">
                              <Select.Option value={2048}>2,048 Tokens</Select.Option>
                              <Select.Option value={4096}>4,096 Tokens (Tiêu chuẩn)</Select.Option>
                              <Select.Option value={8192}>8,192 Tokens (Nâng cao)</Select.Option>
                            </Select>
                          </Form.Item>
                        </Col>
                      </Row>

                      <Form.Item
                        label={<span className="font-semibold text-slate-700 text-xs">Quy tắc Prompt Sư Phạm Cố Định</span>}
                        name="systemPromptType"
                      >
                        <Radio.Group className="w-full">
                          <Row gutter={[12, 12]}>
                            <Col span={12}>
                              <Radio.Button value="standard_pedagogical" className="w-full h-auto py-3 px-3 text-left rounded-xl border-slate-200">
                                <div className="font-bold text-xs text-slate-800 flex items-center gap-1.5">
                                  <Zap size={14} className="text-amber-500" /> Standard Pedagogical
                                </div>
                                <div className="text-[11px] text-slate-500 mt-0.5">Kết cấu sư phạm chuẩn: Lý thuyết ➔ Minh họa ➔ Thực hành</div>
                              </Radio.Button>
                            </Col>
                            <Col span={12}>
                              <Radio.Button value="technical_focus" className="w-full h-auto py-3 px-3 text-left rounded-xl border-slate-200">
                                <div className="font-bold text-xs text-slate-800 flex items-center gap-1.5">
                                  <ShieldCheck size={14} className="text-teal-600" /> Technical Lab Focus
                                </div>
                                <div className="text-[11px] text-slate-500 mt-0.5">Tối ưu cho viết mã lập trình, bài tập thực hành máy tính</div>
                              </Radio.Button>
                            </Col>
                          </Row>
                        </Radio.Group>
                      </Form.Item>
                    </Card>
                  ),
                },
                {
                  key: 'storage',
                  label: (
                    <span className="flex items-center gap-2 font-semibold px-1 py-1">
                      <Folder size={16} className="text-teal-600" /> Thư Mục & Cache
                    </span>
                  ),
                  children: (
                    <Card bordered={false} className="shadow-sm border border-slate-100 rounded-2xl p-2 space-y-4">
                      <div className="border-b border-slate-100 pb-3 mb-4">
                        <h3 className="text-base font-bold text-slate-800 m-0 flex items-center gap-2">
                          <Folder className="text-teal-600" size={18} /> Thư mục lưu trữ & Semantic Cache
                        </h3>
                        <p className="text-xs text-slate-500 mt-1">Cấu hình đường dẫn xuất tệp Obsidian Markdown và bộ nhớ đệm AI</p>
                      </div>

                      <Form.Item
                        label={<span className="font-semibold text-slate-700 text-xs">Đường dẫn Vault Obsidian (Tài liệu xuất bản)</span>}
                        name="obsidianPath"
                        extra="Vị trí thư mục máy tính local nơi Agent ghi tệp bài giảng dạng Markdown (.md)"
                      >
                        <Input size="large" prefix={<Folder size={18} className="text-slate-400 mr-2" />} className="rounded-xl font-mono text-xs" />
                      </Form.Item>

                      <Divider className="my-4 border-slate-100" />

                      <div className="flex justify-between items-center bg-slate-50 p-4 rounded-xl border border-slate-100">
                        <div>
                          <div className="font-bold text-sm text-slate-800 flex items-center gap-2">
                            <Brain size={16} className="text-teal-600" /> Kích hoạt Bộ Nhớ Đệm AI (Semantic Cache)
                          </div>
                          <div className="text-xs text-slate-500 mt-0.5">
                            Tự động lưu trữ bài giảng đã sinh để tiết kiệm 80%+ thời gian và phí gọi API LLM
                          </div>
                        </div>
                        <Form.Item name="enableSemanticCache" valuePropName="checked" className="m-0">
                          <Switch />
                        </Form.Item>
                      </div>
                    </Card>
                  ),
                },
                {
                  key: 'scorm',
                  label: (
                    <span className="flex items-center gap-2 font-semibold px-1 py-1">
                      <Package size={16} className="text-teal-600" /> SCORM Export
                    </span>
                  ),
                  children: (
                    <Card bordered={false} className="shadow-sm border border-slate-100 rounded-2xl p-2 space-y-4">
                      <div className="border-b border-slate-100 pb-3 mb-4">
                        <h3 className="text-base font-bold text-slate-800 m-0 flex items-center gap-2">
                          <Package className="text-teal-600" size={18} /> Chuẩn đóng gói gói học liệu LMS (SCORM)
                        </h3>
                        <p className="text-xs text-slate-500 mt-1">Cấu hình các thông số đóng gói ZIP đạt chuẩn e-Learning quốc tế</p>
                      </div>

                      <Row gutter={16}>
                        <Col span={12}>
                          <Form.Item
                            label={<span className="font-semibold text-slate-700 text-xs">Chuẩn SCORM Mặc Định</span>}
                            name="scormStandard"
                          >
                            <Radio.Group className="w-full">
                              <Radio.Button value="SCORM_1.2" className="mr-2 rounded-xl">SCORM 1.2</Radio.Button>
                              <Radio.Button value="SCORM_2004" className="rounded-xl">SCORM 2004 (3rd Edition)</Radio.Button>
                            </Radio.Group>
                          </Form.Item>
                        </Col>
                        <Col span={12}>
                          <Form.Item
                            label={<span className="font-semibold text-slate-700 text-xs">Tên Tác Giả Mặc Định</span>}
                            name="defaultAuthor"
                          >
                            <Input size="large" className="rounded-xl" placeholder="Ví dụ: Elearning Content Factory" />
                          </Form.Item>
                        </Col>
                      </Row>
                    </Card>
                  ),
                },
                {
                  key: 'monitor',
                  label: (
                    <span className="flex items-center gap-2 font-semibold px-1 py-1">
                      <Monitor size={16} className="text-teal-600" /> Giám Sát & Monitor
                    </span>
                  ),
                  children: (
                    <Card bordered={false} className="shadow-sm border border-slate-100 rounded-2xl p-2 space-y-4">
                      <div className="border-b border-slate-100 pb-3 mb-4">
                        <h3 className="text-base font-bold text-slate-800 m-0 flex items-center gap-2">
                          <Monitor className="text-teal-600" size={18} /> Cài đặt giao diện & tiến trình Polling
                        </h3>
                        <p className="text-xs text-slate-500 mt-1">Cấu hình tần suất cập nhật giao diện và nhật ký biên dịch</p>
                      </div>

                      <Row gutter={16}>
                        <Col span={12}>
                          <Form.Item
                            label={<span className="font-semibold text-slate-700 text-xs">Khoảng Thời Gian Polling (ms)</span>}
                            name="pollingInterval"
                          >
                            <Slider min={1000} max={10000} step={500} tooltip={{ formatter: (v) => `${v}ms` }} />
                          </Form.Item>
                        </Col>
                        <Col span={12}>
                          <div className="flex justify-between items-center h-full pt-4">
                            <div>
                              <div className="font-bold text-xs text-slate-800">Hiển thị Terminal Logs Biên Dịch</div>
                              <div className="text-[11px] text-slate-400">Hiển thị khung log dòng chạy chi tiết ở Pipeline Monitor</div>
                            </div>
                            <Form.Item name="enableLogs" valuePropName="checked" className="m-0">
                              <Switch />
                            </Form.Item>
                          </div>
                        </Col>
                      </Row>
                    </Card>
                  ),
                },
              ]}
            />
          </Col>

          {/* Right Column: Semantic Cache Stats Widget */}
          <Col xs={24} lg={8} className="space-y-6">
            <Card
              bordered={false}
              title={
                <span className="flex items-center gap-2 font-bold text-slate-800 text-sm">
                  <Brain className="text-teal-600" size={18} /> Phân Tích Semantic Cache
                </span>
              }
              extra={
                <Button size="small" type="text" icon={<RefreshCw size={13} />} onClick={() => refetchCache()} />
              }
              className="shadow-sm border border-slate-100 rounded-2xl bg-white"
            >
              {cacheLoading ? (
                <div className="text-center py-6"><Spin /></div>
              ) : (
                <div className="space-y-4">
                  <Row gutter={16}>
                    <Col span={12}>
                      <Statistic
                        title={<span className="text-xs text-slate-500 font-medium">Cache Hits</span>}
                        value={cacheStats?.total_cache_hits ?? 0}
                        valueStyle={{ color: '#0d9488', fontWeight: 800, fontSize: '1.5rem' }}
                      />
                    </Col>
                    <Col span={12}>
                      <Statistic
                        title={<span className="text-xs text-slate-500 font-medium">Đã Lưu Trữ</span>}
                        value={cacheStats?.total_cached_responses ?? 0}
                        valueStyle={{ color: '#d97706', fontWeight: 800, fontSize: '1.5rem' }}
                      />
                    </Col>
                  </Row>

                  <div className="bg-teal-50/70 border border-teal-100 rounded-xl p-3.5">
                    <div className="text-xs text-teal-800 font-bold flex items-center gap-1.5">
                      <Sparkles size={14} className="text-teal-600" /> Token Tiết Kiệm Ước Tính
                    </div>
                    <div className="text-xl font-black text-teal-950 mt-1">
                      ~{tokenSavings.toLocaleString()} tokens
                    </div>
                    <div className="text-[11px] text-teal-600 font-medium mt-0.5">
                      Tiết kiệm khoảng ${(tokenSavings * 0.000015).toFixed(2)} USD chi phí LLM
                    </div>
                  </div>

                  <Alert
                    type="warning"
                    showIcon
                    message="Lưu ý Dọn Cache"
                    description="Thao tác dọn dẹp cache sẽ xóa toàn bộ bộ nhớ đệm. Agent sẽ phải gọi lại LLM API ở lần sinh tiếp theo."
                    className="text-[11px] font-medium leading-relaxed border-amber-200 bg-amber-50/50 rounded-xl"
                  />

                  <Button
                    danger
                    block
                    size="large"
                    icon={<Database size={15} />}
                    loading={clearingCache}
                    onClick={handleClearCache}
                    className="rounded-xl font-semibold text-xs h-10"
                  >
                    Dọn Dẹp Cache Hệ Thống
                  </Button>
                </div>
              )}
            </Card>

            {/* Quick Actions Card */}
            <Card bordered={false} className="shadow-sm border border-slate-100 rounded-2xl bg-white">
              <div className="space-y-3">
                <Button
                  type="primary"
                  icon={<Save size={16} />}
                  block
                  size="large"
                  loading={saving}
                  onClick={() => form.submit()}
                  className="bg-teal-600 hover:bg-teal-700 font-bold text-sm rounded-xl h-11"
                >
                  Lưu Cấu Hình
                </Button>
                <Popconfirm
                  title="Khôi phục cấu hình mặc định?"
                  onConfirm={handleResetDefaults}
                  okText="Đồng ý"
                  cancelText="Hủy"
                >
                  <Button
                    icon={<RotateCcw size={15} />}
                    block
                    loading={resetting}
                    disabled={saving}
                    className="font-medium text-xs rounded-xl h-10 text-slate-600"
                  >
                    Khôi Phục Mặc Định
                  </Button>
                </Popconfirm>
              </div>
            </Card>
          </Col>
        </Row>
      </Form>
    </div>
  );
}
