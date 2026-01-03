import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE = '/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isApproved = computed(() => user.value?.is_approved ?? false)
  const isAdmin = computed(() => user.value?.is_admin ?? false)

  async function requestOtp(phoneNumber) {
    const res = await fetch(`${API_BASE}/auth/request-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone_number: phoneNumber })
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.detail || 'Failed to send OTP')
    }

    return res.json()
  }

  async function verifyOtp(phoneNumber, code) {
    const res = await fetch(`${API_BASE}/auth/verify-otp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone_number: phoneNumber, code })
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.detail || 'Invalid OTP')
    }

    const data = await res.json()
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)

    await fetchUser()
  }

  async function fetchUser() {
    if (!token.value) return

    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })

    if (res.ok) {
      user.value = await res.json()
    } else {
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  function getAuthHeaders() {
    return {
      Authorization: `Bearer ${token.value}`,
      'Content-Type': 'application/json'
    }
  }

  // Fetch user on init if token exists
  if (token.value) {
    fetchUser()
  }

  return {
    token,
    user,
    isAuthenticated,
    isApproved,
    isAdmin,
    requestOtp,
    verifyOtp,
    fetchUser,
    logout,
    getAuthHeaders
  }
})
