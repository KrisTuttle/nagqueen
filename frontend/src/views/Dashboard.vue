<template>
  <div class="dashboard">
    <!-- Pending approval message -->
    <div v-if="!authStore.isApproved" class="pending-notice">
      <h2>Account Pending Approval</h2>
      <p>Your account is waiting for admin approval. You'll be able to use Nag Queen once approved.</p>
    </div>

    <!-- Normal dashboard for approved users -->
    <template v-else>
      <div class="dashboard-header">
        <h2>Your Reminders</h2>
        <div class="header-actions">
          <router-link v-if="authStore.isAdmin" to="/admin" class="admin-btn">Admin</router-link>
          <router-link to="/reminders/new" class="add-btn">+ New Reminder</router-link>
        </div>
      </div>

      <div v-if="loading" class="loading">Loading...</div>

      <div v-else-if="reminders.length === 0" class="empty">
        <p>No reminders yet.</p>
        <p>Create your first reminder to get started!</p>
      </div>

      <div v-else class="reminder-list">
        <ReminderCard
          v-for="reminder in reminders"
          :key="reminder.id"
          :reminder="reminder"
          @delete="handleDelete"
        />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth.js'
import { API_BASE } from '../config.js'
import ReminderCard from '../components/ReminderCard.vue'

const authStore = useAuthStore()
const reminders = ref([])
const loading = ref(true)

async function fetchReminders() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/reminders`, {
      headers: authStore.getAuthHeaders()
    })
    if (res.ok) {
      reminders.value = await res.json()
    }
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('Delete this reminder?')) return

  const res = await fetch(`${API_BASE}/reminders/${id}`, {
    method: 'DELETE',
    headers: authStore.getAuthHeaders()
  })

  if (res.ok) {
    reminders.value = reminders.value.filter(r => r.id !== id)
  }
}

onMounted(fetchReminders)
</script>

<style scoped>
.pending-notice {
  background: #fef3c7;
  border: 1px solid #f59e0b;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
}

.pending-notice h2 {
  color: #b45309;
  margin-bottom: 0.5rem;
}

.pending-notice p {
  color: #92400e;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.dashboard-header h2 {
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.add-btn {
  background: #6366f1;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
}

.add-btn:hover {
  background: #5558e3;
}

.admin-btn {
  background: #f3f4f6;
  color: #333;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
}

.admin-btn:hover {
  background: #e5e7eb;
}

.loading, .empty {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.reminder-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
