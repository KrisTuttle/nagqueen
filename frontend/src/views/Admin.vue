<template>
  <div class="admin">
    <h2>Admin Panel</h2>

    <div class="tabs">
      <button :class="{ active: tab === 'pending' }" @click="tab = 'pending'">
        Pending ({{ pendingUsers.length }})
      </button>
      <button :class="{ active: tab === 'all' }" @click="tab = 'all'">
        All Users
      </button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else-if="tab === 'pending'">
      <div v-if="pendingUsers.length === 0" class="empty">
        No pending users.
      </div>
      <div v-else class="user-list">
        <div v-for="user in pendingUsers" :key="user.id" class="user-card">
          <div class="user-info">
            <span class="phone">{{ user.phone_number }}</span>
            <span class="date">{{ formatDate(user.created_at) }}</span>
          </div>
          <div class="user-actions">
            <button @click="approveUser(user.id)" class="approve-btn">Approve</button>
            <button @click="rejectUser(user.id)" class="reject-btn">Reject</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="tab === 'all'">
      <div v-if="allUsers.length === 0" class="empty">
        No users yet.
      </div>
      <div v-else class="user-list">
        <div v-for="user in allUsers" :key="user.id" class="user-card">
          <div class="user-info">
            <span class="phone">{{ user.phone_number }}</span>
            <span v-if="user.is_admin" class="badge admin-badge">Admin</span>
            <span v-else-if="user.is_approved" class="badge approved-badge">Approved</span>
            <span v-else class="badge pending-badge">Pending</span>
          </div>
          <div class="user-actions">
            <button
              v-if="!user.is_admin && user.is_approved"
              @click="makeAdmin(user.id)"
              class="admin-action-btn"
            >
              Make Admin
            </button>
            <button
              v-if="!user.is_approved"
              @click="approveUser(user.id)"
              class="approve-btn"
            >
              Approve
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth.js'
import { API_BASE } from '../config.js'

const authStore = useAuthStore()
const tab = ref('pending')
const allUsers = ref([])
const loading = ref(true)

const pendingUsers = computed(() => allUsers.value.filter(u => !u.is_approved))

async function fetchUsers() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/admin/users`, {
      headers: authStore.getAuthHeaders()
    })
    if (res.ok) {
      allUsers.value = await res.json()
    }
  } finally {
    loading.value = false
  }
}

async function approveUser(userId) {
  const res = await fetch(`${API_BASE}/admin/users/${userId}/approve`, {
    method: 'POST',
    headers: authStore.getAuthHeaders()
  })
  if (res.ok) {
    const updated = await res.json()
    const idx = allUsers.value.findIndex(u => u.id === userId)
    if (idx !== -1) allUsers.value[idx] = updated
  }
}

async function rejectUser(userId) {
  if (!confirm('Reject and delete this user?')) return

  const res = await fetch(`${API_BASE}/admin/users/${userId}/reject`, {
    method: 'POST',
    headers: authStore.getAuthHeaders()
  })
  if (res.ok) {
    allUsers.value = allUsers.value.filter(u => u.id !== userId)
  }
}

async function makeAdmin(userId) {
  if (!confirm('Make this user an admin?')) return

  const res = await fetch(`${API_BASE}/admin/users/${userId}/make-admin`, {
    method: 'POST',
    headers: authStore.getAuthHeaders()
  })
  if (res.ok) {
    const updated = await res.json()
    const idx = allUsers.value.findIndex(u => u.id === userId)
    if (idx !== -1) allUsers.value[idx] = updated
  }
}

function formatDate(dt) {
  return new Date(dt).toLocaleDateString()
}

onMounted(fetchUsers)
</script>

<style scoped>
.admin h2 {
  margin-bottom: 1rem;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tabs button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.tabs button.active {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

.loading, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.user-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.phone {
  font-weight: 500;
}

.date {
  color: #666;
  font-size: 0.9rem;
}

.badge {
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.admin-badge {
  background: #dbeafe;
  color: #1d4ed8;
}

.approved-badge {
  background: #d1fae5;
  color: #065f46;
}

.pending-badge {
  background: #fef3c7;
  color: #b45309;
}

.user-actions {
  display: flex;
  gap: 0.5rem;
}

.approve-btn {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
}

.approve-btn:hover {
  background: #059669;
}

.reject-btn {
  background: white;
  color: #dc2626;
  border: 1px solid #dc2626;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
}

.reject-btn:hover {
  background: #fef2f2;
}

.admin-action-btn {
  background: #f3f4f6;
  color: #333;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
}

.admin-action-btn:hover {
  background: #e5e7eb;
}
</style>
