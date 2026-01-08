<template>
  <div class="form-container">
    <h2>{{ isEdit ? 'Edit Reminder' : 'New Reminder' }}</h2>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="message">Message</label>
        <textarea
          id="message"
          v-model="form.message"
          placeholder="What do you want to be reminded about?"
          rows="3"
          required
        ></textarea>
      </div>

      <div class="form-group">
        <label for="schedule_type">Frequency</label>
        <select id="schedule_type" v-model="form.schedule_type" required>
          <option value="once">One time</option>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
      </div>

      <div v-if="form.schedule_type === 'once'" class="form-group">
        <label for="schedule_date">Date</label>
        <input
          id="schedule_date"
          v-model="form.schedule_date"
          type="date"
          required
        />
      </div>

      <div class="form-group">
        <label for="schedule_time">Time</label>
        <input
          id="schedule_time"
          v-model="form.schedule_time"
          type="time"
          required
        />
      </div>

      <div v-if="form.schedule_type === 'weekly'" class="form-group">
        <label>Days</label>
        <div class="day-picker">
          <label v-for="(day, index) in days" :key="index" class="day-checkbox">
            <input
              type="checkbox"
              :value="index"
              v-model="form.schedule_days"
            />
            {{ day }}
          </label>
        </div>
      </div>

      <div v-if="form.schedule_type === 'monthly'" class="form-group">
        <label for="schedule_day">Day of Month</label>
        <select id="schedule_day" v-model="form.schedule_day_of_month">
          <option v-for="d in 31" :key="d" :value="String(d)">{{ d }}</option>
          <option value="last">Last day</option>
        </select>
      </div>

      <div v-if="isEdit" class="form-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="form.is_active" />
          Active
        </label>
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <div class="form-actions">
        <button type="button" class="cancel-btn" @click="router.back()">Cancel</button>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Saving...' : 'Save Reminder' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { API_BASE } from '../config.js'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)
const error = ref('')

// Default to 2 minutes from now (local time)
function getDefaultDateTime() {
  const now = new Date()
  now.setMinutes(now.getMinutes() + 2)
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  return { date: `${year}-${month}-${day}`, time: `${hours}:${minutes}` }
}

const defaults = getDefaultDateTime()

const form = reactive({
  message: '',
  schedule_type: 'once',
  schedule_date: defaults.date,
  schedule_time: defaults.time,
  schedule_days: [],
  schedule_day_of_month: '1',
  is_active: true
})

async function fetchReminder() {
  if (!isEdit.value) return

  const res = await fetch(`${API_BASE}/reminders/${route.params.id}`, {
    headers: authStore.getAuthHeaders()
  })

  if (res.ok) {
    const data = await res.json()
    form.message = data.message
    form.schedule_type = data.schedule_type
    form.schedule_time = data.schedule_time
    form.schedule_days = data.schedule_days || []
    form.schedule_day_of_month = data.schedule_day_of_month || '1'
    form.is_active = data.is_active
  }
}

async function handleSubmit() {
  error.value = ''
  loading.value = true

  const payload = {
    message: form.message,
    schedule_type: form.schedule_type,
    schedule_time: form.schedule_time
  }

  if (form.schedule_type === 'once') {
    payload.schedule_date = form.schedule_date
  }

  if (form.schedule_type === 'weekly') {
    payload.schedule_days = form.schedule_days
  }

  if (form.schedule_type === 'monthly') {
    payload.schedule_day_of_month = form.schedule_day_of_month
  }

  if (isEdit.value) {
    payload.is_active = form.is_active
  }

  try {
    const url = isEdit.value
      ? `${API_BASE}/reminders/${route.params.id}`
      : `${API_BASE}/reminders`

    const res = await fetch(url, {
      method: isEdit.value ? 'PUT' : 'POST',
      headers: authStore.getAuthHeaders(),
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      router.push('/dashboard')
    } else {
      const data = await res.json()
      error.value = data.detail || 'Failed to save reminder'
    }
  } catch (e) {
    error.value = 'An error occurred'
  } finally {
    loading.value = false
  }
}

onMounted(fetchReminder)
</script>

<style scoped>
.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

h2 {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input, select, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #6366f1;
}

.day-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.day-checkbox {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: normal;
  cursor: pointer;
}

.day-checkbox input {
  width: auto;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
  cursor: pointer;
}

.checkbox-label input {
  width: auto;
}

.error {
  color: #dc2626;
  margin-bottom: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

button {
  flex: 1;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

button[type="submit"] {
  background: #6366f1;
  color: white;
  border: none;
}

button[type="submit"]:hover:not(:disabled) {
  background: #5558e3;
}

button[type="submit"]:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  background: #f3f4f6;
  color: #333;
  border: none;
}

.cancel-btn:hover {
  background: #e5e7eb;
}
</style>
