<template>
  <div class="reminder-card" :class="{ inactive: !reminder.is_active }">
    <div class="reminder-content">
      <p class="message">{{ reminder.message }}</p>
      <div class="schedule">
        <span class="badge">{{ formatSchedule(reminder) }}</span>
        <span class="time">{{ formatTime(reminder.schedule_time) }}</span>
        <span v-if="!reminder.is_active" class="badge inactive-badge">Paused</span>
      </div>
      <p class="next-run">Next: {{ formatDateTime(reminder.next_run) }}</p>
    </div>
    <div class="reminder-actions">
      <router-link :to="`/reminders/${reminder.id}/edit`" class="edit-btn">Edit</router-link>
      <button @click="$emit('delete', reminder.id)" class="delete-btn">Delete</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  reminder: {
    type: Object,
    required: true
  }
})

defineEmits(['delete'])

function formatSchedule(reminder) {
  const type = reminder.schedule_type
  if (type === 'once') return 'One time'
  if (type === 'daily') return 'Daily'
  if (type === 'weekly') {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    const selected = (reminder.schedule_days || []).map(d => days[d]).join(', ')
    return `Weekly (${selected})`
  }
  if (type === 'monthly') {
    const day = reminder.schedule_day_of_month || '1'
    return `Monthly (day ${day})`
  }
  return type
}

function formatTime(time) {
  if (!time) return ''
  const [hours, minutes] = time.split(':')
  const h = parseInt(hours)
  const ampm = h >= 12 ? 'PM' : 'AM'
  const h12 = h % 12 || 12
  return `${h12}:${minutes} ${ampm}`
}

function formatDateTime(dt) {
  if (!dt) return ''
  const date = new Date(dt)
  return date.toLocaleString()
}
</script>

<style scoped>
.reminder-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.reminder-card.inactive {
  opacity: 0.6;
}

.message {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.schedule {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  margin-bottom: 0.25rem;
}

.badge {
  background: #e0e7ff;
  color: #6366f1;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.inactive-badge {
  background: #fef2f2;
  color: #dc2626;
}

.time {
  font-size: 0.9rem;
  color: #666;
}

.next-run {
  font-size: 0.85rem;
  color: #888;
}

.reminder-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  text-decoration: none;
}

.edit-btn {
  background: #f3f4f6;
  color: #333;
  border: none;
}

.edit-btn:hover {
  background: #e5e7eb;
}

.delete-btn {
  background: transparent;
  color: #dc2626;
  border: 1px solid #dc2626;
}

.delete-btn:hover {
  background: #fef2f2;
}
</style>
