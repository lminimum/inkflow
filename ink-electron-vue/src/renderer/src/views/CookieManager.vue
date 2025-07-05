<template>
  <div class="cookie-manager-container">
    <a-page-header title="多账号Cookie管理" :ghost="false">
      <template #extra>
        <a-button type="primary" @click="showAddModal">
          <PlusOutlined />
          添加新账号
        </a-button>
      </template>
      <p class="page-description">
        在这里管理用于内容发布的小红书账号。添加新账号时，会启动一个独立的浏览器窗口，请在其中扫码登录以获取Cookie。
      </p>
    </a-page-header>

    <div class="content-area">
      <a-list
        :loading="loading"
        item-layout="horizontal"
        :data-source="accounts"
        :bordered="true"
        class="account-list"
      >
        <template #renderItem="{ item }">
          <a-list-item>
            <template #actions>
              <a-tooltip title="验证此账号Cookie是否依然有效">
                <a-button
                  shape="circle"
                  :loading="isValidating[item.name]"
                  @click="validateAccount(item.name)"
                >
                  <SafetyCertificateOutlined />
                </a-button>
              </a-tooltip>
              <a-popconfirm
                title="确定要删除这个账号吗？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="deleteAccount(item.name)"
              >
                <a-button shape="circle" danger>
                  <DeleteOutlined />
                </a-button>
              </a-popconfirm>
            </template>
            <a-list-item-meta>
              <template #title>
                <div class="account-title">
                  <UserOutlined />
                  <span class="account-name">{{ item.name }}</span>
                  <a-tag v-if="item.is_active" color="success" class="active-tag">
                    <template #icon><CheckCircleOutlined /></template>
                    当前活动
                  </a-tag>
                </div>
              </template>
              <template #description>
                <div class="account-status">
                  <span>设为活动账号:</span>
                  <a-switch :checked="item.is_active" @change="setActiveAccount(item.name)" />
                  <span class="status-validation" :class="getValidationClass(item)">
                    <template v-if="item.is_valid === true">
                      <CheckCircleOutlined /> Cookie有效
                    </template>
                    <template v-else-if="item.is_valid === false">
                      <CloseCircleOutlined /> Cookie无效
                    </template>
                    <template v-else> <QuestionCircleOutlined /> 未验证 </template>
                  </span>
                </div>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
        <template #header>
          <div>
            <UserSwitchOutlined />
            已保存的账号列表
          </div>
        </template>
      </a-list>
    </div>

    <a-modal
      v-model:open="isModalVisible"
      title="添加新账号"
      ok-text="开始添加"
      cancel-text="取消"
      :confirm-loading="isAdding"
      @ok="handleAddAccount"
    >
      <a-form layout="vertical">
        <a-form-item label="账号名称" required>
          <a-input v-model:value="newAccountName" placeholder="为这个账号起一个好记的名称" />
        </a-form-item>
        <a-alert
          message="即将打开新的浏览器窗口"
          description="点击开始添加后，系统将打开一个浏览器窗口，请在其中扫码登录你要添加的小红书账号。登录成功后，浏览器会自动关闭。"
          type="info"
          show-icon
        />
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import {
  getCookieAccounts,
  addCookieAccount,
  deleteCookieAccount,
  validateCookieAccount,
  setActiveCookieAccount,
  type CookieAccount
} from '../api/cookieManager'
import { message } from 'ant-design-vue'
import {
  PlusOutlined,
  DeleteOutlined,
  UserOutlined,
  CheckCircleOutlined,
  SafetyCertificateOutlined,
  CloseCircleOutlined,
  QuestionCircleOutlined,
  UserSwitchOutlined
} from '@ant-design/icons-vue'

const accounts = ref<CookieAccount[]>([])
const loading = ref(true)
const isModalVisible = ref(false)
const isAdding = ref(false)
const newAccountName = ref('')
const isValidating = reactive<Record<string, boolean>>({})

const fetchAccounts = async (): Promise<void> => {
  loading.value = true
  try {
    const res = await getCookieAccounts()
    if (res.success && res.accounts) {
      accounts.value = res.accounts.map((acc) => ({ ...acc, is_valid: null }))
    } else {
      message.error(res.message || '获取账号列表失败')
    }
  } finally {
    loading.value = false
  }
}

const showAddModal = (): void => {
  isModalVisible.value = true
}

const handleAddAccount = async (): Promise<void> => {
  if (!newAccountName.value.trim()) {
    message.warning('请输入账号名称')
    return
  }
  isAdding.value = true
  try {
    const res = await addCookieAccount(newAccountName.value)
    if (res.success) {
      message.loading('已启动后台任务，请在弹出的浏览器中登录...', 0)
      isModalVisible.value = false
      newAccountName.value = ''
      setTimeout(() => {
        message.destroy()
        message.success('登录任务已启动，完成后请刷新列表查看新账号。', 5)
        fetchAccounts()
      }, 5000)
    } else {
      message.error(res.message || '启动添加任务失败')
    }
  } finally {
    isAdding.value = false
  }
}

const deleteAccount = async (accountName: string): Promise<void> => {
  try {
    const res = await deleteCookieAccount(accountName)
    if (res.success) {
      message.success(`账号 ${accountName} 已删除`)
      fetchAccounts()
    } else {
      message.error(res.message || '删除失败')
    }
  } catch (error: unknown) {
    console.error('删除账号时发生错误:', error)
  }
}

const validateAccount = async (accountName: string): Promise<void> => {
  isValidating[accountName] = true
  try {
    const res = await validateCookieAccount(accountName)
    const account = accounts.value.find((acc) => acc.name === accountName)
    if (account) {
      if (res.success) {
        account.is_valid = res.is_valid
        message.success(`账号 ${accountName} 验证完成: ${res.is_valid ? '有效' : '无效'}`)
      } else {
        account.is_valid = false
        message.error(res.message || '验证失败')
      }
    }
  } catch (error: unknown) {
    message.error('验证时发生错误' + error)
  } finally {
    isValidating[accountName] = false
  }
}

const setActiveAccount = async (accountName: string): Promise<void> => {
  try {
    const res = await setActiveCookieAccount(accountName)
    if (res.success) {
      message.success(`账号 ${accountName} 已设为活动账号`)
      fetchAccounts()
    } else {
      message.error(res.message || '设置失败')
    }
  } catch (error: unknown) {
    message.error('设置活动账号时发生错误' + error)
  }
}

const getValidationClass = (item: CookieAccount): string => {
  if (item.is_valid === true) return 'status-valid'
  if (item.is_valid === false) return 'status-invalid'
  return 'status-unknown'
}

onMounted(() => {
  fetchAccounts()
})
</script>

<style scoped>
.cookie-manager-container {
  padding: 24px;
}

.page-description {
  margin-top: 8px;
  color: var(--text-color-secondary);
}

.content-area {
  margin-top: 24px;
}

.account-list {
  background-color: var(--bg-color-card);
}

.account-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.account-name {
  font-weight: 500;
}

.active-tag {
  margin-left: 8px;
}

.account-status {
  display: flex;
  align-items: center;
  gap: 16px;
  color: var(--text-color-secondary);
  font-size: 12px;
}

.status-validation {
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-valid {
  color: #52c41a;
}

.status-invalid {
  color: #ff4d4f;
}

.status-unknown {
  color: var(--text-color-secondary);
}
</style>
