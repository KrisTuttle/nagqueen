<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Nag Queen</h1>
      <p class="tagline">Never forget again</p>

      <form @submit.prevent="handleSubmit">
        <div v-if="!otpSent" class="form-group">
          <label for="phone">Phone Number</label>
          <input
            id="phone"
            v-model="phoneNumber"
            type="tel"
            placeholder="+1234567890"
            required
          />
          <p class="hint">Enter in E.164 format (e.g., +1234567890)</p>
        </div>

        <div v-else class="form-group">
          <label for="otp">Verification Code</label>
          <input
            id="otp"
            v-model="otpCode"
            type="text"
            placeholder="123456"
            maxlength="6"
            required
          />
          <p class="hint">Enter the 6-digit code sent to {{ phoneNumber }}</p>
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Please wait...' : (otpSent ? 'Verify Code' : 'Send Code') }}
        </button>

        <button v-if="otpSent" type="button" class="back-btn" @click="resetForm">
          Use different number
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const phoneNumber = ref('')
const otpCode = ref('')
const otpSent = ref(false)
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  error.value = ''
  loading.value = true

  try {
    if (!otpSent.value) {
      await authStore.requestOtp(phoneNumber.value)
      otpSent.value = true
    } else {
      await authStore.verifyOtp(phoneNumber.value, otpCode.value)
      router.push('/dashboard')
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function resetForm() {
  otpSent.value = false
  otpCode.value = ''
  error.value = ''
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-card h1 {
  color: #6366f1;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.tagline {
  color: #666;
  margin-bottom: 2rem;
}

.form-group {
  text-align: left;
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #6366f1;
}

.hint {
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.5rem;
}

.error {
  color: #dc2626;
  margin-bottom: 1rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 0.5rem;
}

button:hover:not(:disabled) {
  background: #5558e3;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.back-btn {
  background: transparent;
  color: #6366f1;
}

.back-btn:hover {
  background: #f5f5f5;
}
</style>
