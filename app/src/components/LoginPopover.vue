<template>
  <transition name="fade">
    <div v-if="visible" class="popover-overlay" @click.self="close">
      <div class="popover-container" @click.stop>
        <!-- Close button -->
        <button @click="close" class="close-btn">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <!-- Header -->
        <div class="header">
          <div class="icon-wrapper">
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <h1>Login</h1>
          <p class="subtitle">Earth Observation System - WeatherMellon</p>
        </div>

        <!-- Message -->
        <div v-if="message.text" :class="['message', message.type]">
          {{ message.text }}
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>USERNAME</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <input
                v-model="formData.username"
                type="text"
                placeholder="Enter username"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label>PASSWORD</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
              <input
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                required
              />
              <button 
                type="button" 
                @click="showPassword = !showPassword"
                class="toggle-password"
              >
                <svg v-if="showPassword" class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
                <svg v-else class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </button>
            </div>
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? 'Loading...' : 'Login' }}
            <svg v-if="!loading" class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </button>
        </form>

        <!-- Footer -->
        <div class="footer">
          <p class="footer-text">
            Don't have an account? 
            <button @click="switchToRegister" class="link-btn">Register here</button>
          </p>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'LoginPopover',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'switch-to-register', 'login-success'],
  data() {
    return {
      showPassword: false,
      loading: false,
      formData: {
        username: '',
        password: ''
      },
      message: {
        type: '',
        text: ''
      }
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    switchToRegister() {
      this.$emit('switch-to-register')
    },
    async handleLogin() {
      this.loading = true
      this.message = { type: '', text: '' }

      try {
        const response = await fetch('http://localhost:8000/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.formData)
        })

        const data = await response.json()

        if (response.ok) {
          this.message = { type: 'success', text: 'Login success' }
          localStorage.setItem('token', data.access_token)
          
          setTimeout(() => {
            this.$emit('login-success')
            this.close()
          }, 1000)
        } else {
          this.message = { type: 'error', text: data.detail || 'Invalid credentials' }
        }
      } catch (error) {
        this.message = { type: 'error', text: 'Server error' }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.popover-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(4px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.popover-container {
  position: relative;
  width: 100%;
  max-width: 440px;
  background: #030712;
  border: 1px solid #1f2937;
  border-radius: 16px;
  padding: 40px 32px 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: transparent;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #fff;
  background: #1f2937;
}

.header {
  text-align: center;
  margin-bottom: 32px;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: #1f2937;
  border: 1px solid #374151;
  border-radius: 14px;
  margin-bottom: 16px;
}

.icon {
  width: 28px;
  height: 28px;
  stroke: #f3f4f6;
}

h1 {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 6px;
}

.subtitle {
  color: #6b7280;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.message {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  border: 1px solid;
  font-size: 14px;
}

.message.success {
  background: #14532d;
  border-color: #166534;
  color: #86efac;
}

.message.error {
  background: #7f1d1d;
  border-color: #991b1b;
  color: #fca5a5;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #9ca3af;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  stroke: #6b7280;
}

input {
  width: 100%;
  background: #000;
  border: 1px solid #1f2937;
  border-radius: 8px;
  padding: 12px 16px 12px 48px;
  color: #fff;
  font-size: 14px;
  transition: border-color 0.2s;
}

input::placeholder {
  color: #6b7280;
}

input:focus {
  outline: none;
  border-color: #4b5563;
}

.toggle-password {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  color: #6b7280;
  transition: color 0.2s;
}

.toggle-password:hover {
  color: #9ca3af;
}

.eye-icon {
  width: 20px;
  height: 20px;
}

.submit-btn {
  width: 100%;
  background: #1f2937;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  padding: 12px;
  border: 1px solid #374151;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
  transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #374151;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.arrow-icon {
  width: 20px;
  height: 20px;
}

.footer {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #1f2937;
  text-align: center;
}

.footer-text {
  font-size: 14px;
  color: #6b7280;
}

.link-btn {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.2s;
  font-weight: 500;
  margin-left: 4px;
}

.link-btn:hover {
  color: #fff;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active .popover-container {
  animation: slideUp 0.3s ease;
}

.fade-leave-active .popover-container {
  animation: slideDown 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideDown {
  from {
    transform: translateY(0);
    opacity: 1;
  }
  to {
    transform: translateY(20px);
    opacity: 0;
  }
}
</style>