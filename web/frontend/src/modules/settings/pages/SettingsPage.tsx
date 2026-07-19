import { useState, useEffect } from 'react';
import { Card, Button, Form, Input, Select, Slider, Switch, Radio, Divider, Space, Alert, Statistic, Row, Col, Spin, message } from 'antd';
import {
  Settings, Brain, Cpu, Database, Save, RotateCcw,
  Sparkles, Folder, HelpCircle, Package, Monitor
} from 'lucide-react';
import { useCacheStats, useClearCache } from '../../../services/hooks';

export default function SettingsPage() {
  const [form] = Form.useForm();
  const [saving, setSaving] = useState(false);
  
  // Real cache statistics & actions
  const { data: cacheStats, loading: cacheLoading, refetch: refetchCache } = useCacheStats();
  const { execute: doClearCache, loading: clearingCache } = useClearCache();

  // Load settings from localStorage or defaults
  useEffect(() => {
    const savedSettings = localStorage.getItem('elearning_settings');
    if (savedSettings) {
      try {
        form.setFieldsValue(JSON.parse(savedSettings));
      } catch (e) {
        console.error("Failed to parse settings", e);
      }
    } else {
      form.setFieldsValue({
        llmProvider: 'gemini',
        modelName: 'gemini-1.5-pro',
        temperature: 0.2,
        maxTokens: 4096,
        systemPromptType: 'standard_pedagogical',
        enableSemanticCache: true,
        obsidianPath: 'C:\\Users\\Admin\\Obsidian\\Vaults\\Elearning',
        scormStandard: 'SCORM_2004',
        defaultAuthor: 'Elearning Agent',
        pollingInterval: 3000,
        enableLogs: true
      });
    }
  }, [form]);

  const handleSave = async (values: any) => {
    setSaving(true);
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 800));
    localStorage.setItem('elearning_settings', JSON.stringify(values));
    setSaving(false);
    message.success({
      content: 'Đã lưu cấu hình hệ thống thành công!',
      style: { marginTop: '10vh' }
    });
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

  const handleResetDefaults = () => {
    form.resetFields();
    message.info('Đã hoàn tác cấu hình về mặc định.');
  };

  const tokenSavings = cacheStats ? cacheStats.estimated_tokens_saved : 0;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Title Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <Settings className="text-indigo-600" size={24} /> Cấu hình Hệ thống
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            Quản lý tham số AI Agent, thư mục đầu ra và cài đặt vận hành của Content Factory
          </p>
        </div>
      </div>

      <Form
        form={form}
        layout="vertical"
        onFinish={handleSave}
        requiredMark={false}
      >
        <Row gutter={[24, 24]}>
          {/* Left Column: Form Sections */}
          <Col xs={24} lg={16} className="space-y-6">
            {/* Section 1: AI Brain Configuration */}
            <Card
              title={
                <span className="flex items-center gap-2 font-bold text-gray-800">
                  <Cpu className="text-indigo-600" size={18} /> Cấu hình AI Core Engine
                </span>
              }
              className="shadow-sm border-slate-200 rounded-xl"
            >
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    label="Nhà cung cấp LLM"
                    name="llmProvider"
                    rules={[{ required: true }]}
                  >
                    <Select>
                      <Select.Option value="gemini">Google Gemini (Khuyên dùng)</Select.Option>
                      <Select.Option value="openai">OpenAI GPT</Select.Option>
                      <Select.Option value="anthropic">Anthropic Claude</Select.Option>
                      <Select.Option value="ollama">Ollama (Chạy offline cục bộ)</Select.Option>
                    </Select>
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    label="Mô hình hoạt động"
                    name="modelName"
                    rules={[{ required: true }]}
                  >
                    <Select>
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
                      <span className="flex items-center gap-1.5">
                        Nhiệt độ (Temperature)
                        <HelpCircle size={14} className="text-gray-400 cursor-pointer" />
                      </span>
                    }
                    name="temperature"
                  >
                    <Slider min={0} max={1} step={0.1} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    label="Max Response Tokens"
                    name="maxTokens"
                  >
                    <Select>
                      <Select.Option value={2048}>2048 tokens</Select.Option>
                      <Select.Option value={4096}>4096 tokens</Select.Option>
                      <Select.Option value={8192}>8192 tokens</Select.Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item
                label="Quy tắc Prompt sư phạm cố định"
                name="systemPromptType"
              >
                <Radio.Group className="w-full">
                  <Row gutter={[12, 12]}>
                    <Col span={12}>
                      <Radio.Button value="standard_pedagogical" className="w-full h-auto py-2 px-3 text-left">
                        <div className="font-bold text-xs text-gray-800">Pedagogical Framework</div>
                        <div className="text-[10px] text-gray-400">Sinh bài đọc kết cấu sâu, dễ hiểu</div>
                      </Radio.Button>
                    </Col>
                    <Col span={12}>
                      <Radio.Button value="technical_focus" className="w-full h-auto py-2 px-3 text-left">
                        <div className="font-bold text-xs text-gray-800">Technical Focus</div>
                        <div className="text-[10px] text-gray-400">Tối ưu cho viết mã và thực hành Lab</div>
                      </Radio.Button>
                    </Col>
                  </Row>
                </Radio.Group>
              </Form.Item>
            </Card>

            {/* Section 2: Directory and Storage Paths */}
            <Card
              title={
                <span className="flex items-center gap-2 font-bold text-gray-800">
                  <Folder className="text-indigo-600" size={18} /> Thư mục đồng bộ & Bộ nhớ
                </span>
              }
              className="shadow-sm border-slate-200 rounded-xl"
            >
              <Form.Item
                label="Đường dẫn Vault Obsidian (Tài liệu gốc)"
                name="obsidianPath"
                extra="Nơi Agent xuất bản các tệp Markdown (.md) cho Obsidian"
              >
                <Input prefix={<Folder size={16} className="text-gray-400 mr-2" />} />
              </Form.Item>

              <Divider className="my-4" />

              <div className="flex justify-between items-center">
                <div>
                  <div className="font-bold text-sm text-gray-800">Kích hoạt bộ nhớ đệm AI (Semantic Cache)</div>
                  <div className="text-xs text-gray-400 mt-0.5">Tránh sinh lại bài học giống nhau, tiết kiệm API cost</div>
                </div>
                <Form.Item name="enableSemanticCache" valuePropName="checked" className="m-0">
                  <Switch />
                </Form.Item>
              </div>
            </Card>

            {/* Section 3: Package Export Preferences */}
            <Card
              title={
                <span className="flex items-center gap-2 font-bold text-gray-800">
                  <Package className="text-indigo-600" size={18} /> Tham số Xuất bản SCORM
                </span>
              }
              className="shadow-sm border-slate-200 rounded-xl"
            >
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    label="Chuẩn SCORM Mặc định"
                    name="scormStandard"
                  >
                    <Radio.Group>
                      <Radio value="SCORM_1.2">SCORM 1.2</Radio>
                      <Radio value="SCORM_2004">SCORM 2004 (3rd Ed)</Radio>
                    </Radio.Group>
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item
                    label="Tác giả biên dịch mặc định"
                    name="defaultAuthor"
                  >
                    <Input />
                  </Form.Item>
                </Col>
              </Row>
            </Card>

            {/* Section 4: Monitor and Preferences */}
            <Card
              title={
                <span className="flex items-center gap-2 font-bold text-gray-800">
                  <Monitor className="text-indigo-600" size={18} /> Cài đặt giao diện Dashboard
                </span>
              }
              className="shadow-sm border-slate-200 rounded-xl"
            >
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item
                    label="Khoảng thời gian Polling (ms)"
                    name="pollingInterval"
                  >
                    <Slider min={1000} max={10000} step={500} tooltip={{ formatter: (v) => `${v}ms` }} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <div className="flex justify-between items-center h-full pt-6">
                    <div>
                      <div className="font-bold text-xs text-gray-700">Hiển thị Logs biên dịch nâng cao</div>
                      <div className="text-[10px] text-gray-400">Hiện terminal logs ở Pipeline Monitor</div>
                    </div>
                    <Form.Item name="enableLogs" valuePropName="checked" className="m-0">
                      <Switch />
                    </Form.Item>
                  </div>
                </Col>
              </Row>
            </Card>
          </Col>

          {/* Right Column: Statistics & Action Panel */}
          <Col xs={24} lg={8} className="space-y-6">
            {/* Cache Analytics Widget */}
            <Card
              title={
                <span className="flex items-center gap-2 font-bold text-gray-800">
                  <Brain className="text-indigo-600" size={18} /> Trạng thái Semantic Cache
                </span>
              }
              className="shadow-sm border-slate-200 rounded-xl bg-slate-50"
            >
              {cacheLoading ? (
                <div className="text-center py-6"><Spin /></div>
              ) : (
                <div className="space-y-4">
                  <Row gutter={16}>
                    <Col span={12}>
                      <Statistic
                        title={<span className="text-xs text-gray-500 font-medium">Cache Hits</span>}
                        value={cacheStats?.total_cache_hits ?? 0}
                        valueStyle={{ color: '#10b981', fontWeight: 800 }}
                      />
                    </Col>
                    <Col span={12}>
                      <Statistic
                        title={<span className="text-xs text-gray-500 font-medium">Lưu trữ Cache</span>}
                        value={cacheStats?.total_cached_responses ?? 0}
                        valueStyle={{ color: '#f59e0b', fontWeight: 800 }}
                      />
                    </Col>
                  </Row>

                  <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-3">
                    <div className="text-xs text-indigo-700 font-bold flex items-center gap-1">
                      <Sparkles size={13} /> Token Tiết kiệm ước tính
                    </div>
                    <div className="text-lg font-black text-indigo-900 mt-1">
                      ~{tokenSavings.toLocaleString()} tokens
                    </div>
                    <div className="text-[10px] text-indigo-500 font-medium mt-0.5">
                      Tiết kiệm khoảng {(tokenSavings * 0.000015).toFixed(2)} USD phí API
                    </div>
                  </div>

                  <Alert
                    type="warning"
                    showIcon
                    message="Lưu ý khi dọn cache"
                    description="Xóa cache sẽ bắt buộc Agent phải chạy sinh lại học liệu từ đầu cho các lần chạy sau."
                    className="text-[11px] font-semibold leading-relaxed border-amber-200"
                  />

                  <Button
                    danger
                    block
                    icon={<Database size={14} />}
                    loading={clearingCache}
                    onClick={handleClearCache}
                  >
                    Dọn dẹp Cache hệ thống
                  </Button>
                </div>
              )}
            </Card>

            {/* Sticky Actions Card */}
            <Card className="shadow-sm border-slate-200 rounded-xl sticky top-6">
              <Space direction="vertical" className="w-full" size="middle">
                <Button
                  type="primary"
                  htmlType="submit"
                  icon={<Save size={16} />}
                  block
                  size="large"
                  loading={saving}
                  className="bg-indigo-600 hover:bg-indigo-700 font-bold"
                >
                  Lưu cấu hình
                </Button>
                <Button
                  icon={<RotateCcw size={16} />}
                  block
                  onClick={handleResetDefaults}
                  disabled={saving}
                  className="font-medium"
                >
                  Khôi phục mặc định
                </Button>
              </Space>
            </Card>
          </Col>
        </Row>
      </Form>
    </div>
  );
}
