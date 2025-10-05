<template>
  <div class="login-view">
    <div class="login-container">
      <div class="header">
        <div class="icon-wrapper">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </div>
        <h1>Login</h1>
        <p class="subtitle">Access your space</p>
      </div>

      <div class="card">
        <div v-if="message.text" :class="['message', message.type]">
          {{ message.text }}
        </div>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>Username</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <input
                v-model="formData.username"
                type="text"
                placeholder="Username"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label>Password</label>
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

        <div class="footer">
          <button class="link-btn" @click="$router.push('/register')">Register here</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
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
          this.$router.push('home')
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
.login-view {
  min-height: 100vh;
  background-color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 440px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: #fff;
  border-radius: 16px;
  margin-bottom: 16px;
}

.icon {
  width: 32px;
  height: 32px;
  stroke: #000;
}

h1 {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}

.subtitle {
  color: #9ca3af;
  font-size: 16px;
}

.card {
  background: #18181b;
  border: 1px solid #27272a;
  border-radius: 16px;
  padding: 32px;
}

.message {
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid;
}

.message.success {
  background: #14532d;
  border-color: #166534;
  color: #bbf7d0;
}

.message.error {
  background: #450a0a;
  border-color: #991b1b;
  color: #fecaca;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #d1d5db;
  margin-bottom: 8px;
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
  border: 1px solid #27272a;
  border-radius: 12px;
  padding: 12px 16px 12px 48px;
  color: #fff;
  font-size: 15px;
  transition: border-color 0.2s;
}

input::placeholder {
  color: #6b7280;
}

input:focus {
  outline: none;
  border-color: #fff;
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
  color: #fff;
}

.eye-icon {
  width: 20px;
  height: 20px;
}

.submit-btn {
  width: 100%;
  background: #fff;
  color: #000;
  font-weight: 600;
  font-size: 15px;
  padding: 14px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #f3f4f6;
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
  text-align: center;
  margin-top: 24px;
}

.link-btn {
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.2s;
}

.link-btn:hover {
  color: #fff;
}
</style>