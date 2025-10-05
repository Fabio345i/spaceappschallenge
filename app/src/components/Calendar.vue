<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  selectedDate: {
    type: Date,
    default: () => new Date(),
  },
})

const emit = defineEmits(['date-selected'])

const currentDate = ref(new Date())
const viewDate = ref(new Date(props.selectedDate))
const viewMode = ref('days') // 'days', 'months', 'years'
const isOpen = ref(false)
const calendarRef = ref(null)

const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
]
const monthNamesShort = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

const currentMonth = computed(() => viewDate.value.getMonth())
const currentYear = computed(() => viewDate.value.getFullYear())

const displayDate = computed(() =>
  props.selectedDate
    ? props.selectedDate.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
    : 'Select date'
)

const yearRange = computed(() => {
  const year = currentYear.value
  const startYear = Math.max(1980, Math.floor(year / 12) * 12)
  return { start: startYear, end: startYear + 11 }
})

const headerText = computed(() => {
  if (viewMode.value === 'years') return `${yearRange.value.start} - ${yearRange.value.end}`
  if (viewMode.value === 'months') return currentYear.value
  return `${monthNames[currentMonth.value]} ${currentYear.value}`
})

const calendarDays = computed(() => {
  const y = currentYear.value
  const m = currentMonth.value
  const firstDay = new Date(y, m, 1)
  const lastDay = new Date(y, m + 1, 0)
  const startDay = firstDay.getDay()
  const daysInMonth = lastDay.getDate()
  const days = []

  const prevMonthLastDay = new Date(y, m, 0).getDate()
  for (let i = startDay - 1; i >= 0; i--) {
    days.push({ day: prevMonthLastDay - i, isCurrentMonth: false, date: new Date(y, m - 1, prevMonthLastDay - i) })
  }
  for (let i = 1; i <= daysInMonth; i++) {
    days.push({ day: i, isCurrentMonth: true, date: new Date(y, m, i) })
  }
  const remaining = 42 - days.length
  for (let i = 1; i <= remaining; i++) {
    days.push({ day: i, isCurrentMonth: false, date: new Date(y, m + 1, i) })
  }
  return days
})

const isToday = d => d.toDateString() === currentDate.value.toDateString()
const isSelected = d => props.selectedDate && d.toDateString() === props.selectedDate.toDateString()
const isCurrentMonth = m => m === currentDate.value.getMonth() && currentYear.value === currentDate.value.getFullYear()
const isSelectedMonth = m => props.selectedDate && m === props.selectedDate.getMonth() && currentYear.value === props.selectedDate.getFullYear()
const isCurrentYear = y => y === currentDate.value.getFullYear()
const isSelectedYear = y => props.selectedDate && y === props.selectedDate.getFullYear()

function selectDate(dayObj) {
  emit('date-selected', dayObj.date)
  viewDate.value = new Date(dayObj.date)
  isOpen.value = false
  viewMode.value = 'days'
}
function selectMonth(m) {
  viewDate.value = new Date(currentYear.value, m, 1)
  viewMode.value = 'days'
}
function selectYear(y) {
  viewDate.value = new Date(y, currentMonth.value, 1)
  viewMode.value = 'months'
}

function previousPeriod() {
  if (viewMode.value === 'days') viewDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
  else if (viewMode.value === 'months' && currentYear.value > 1980) viewDate.value = new Date(currentYear.value - 1, currentMonth.value, 1)
  else if (viewMode.value === 'years' && currentYear.value - 12 >= 1980) viewDate.value = new Date(currentYear.value - 12, currentMonth.value, 1)
}
function nextPeriod() {
  if (viewMode.value === 'days') viewDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
  else if (viewMode.value === 'months') viewDate.value = new Date(currentYear.value + 1, currentMonth.value, 1)
  else if (viewMode.value === 'years') viewDate.value = new Date(currentYear.value + 12, currentMonth.value, 1)
}
function goToToday() {
  const now = new Date()
  viewDate.value = now
  viewMode.value = 'days'
  emit('date-selected', now)
  isOpen.value = false
}
function cycleViewMode() {
  if (viewMode.value === 'days') viewMode.value = 'months'
  else if (viewMode.value === 'months') viewMode.value = 'years'
  else viewMode.value = 'days'
}
function toggleCalendar() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    viewMode.value = 'days'
    viewDate.value = new Date(props.selectedDate)
  }
}
function handleClickOutside(e) {
  if (calendarRef.value && !calendarRef.value.contains(e.target)) isOpen.value = false
}
onMounted(()=>document.addEventListener('click',handleClickOutside))
onUnmounted(()=>document.removeEventListener('click',handleClickOutside))
</script>

<template>
  <div class="relative inline-block" ref="calendarRef">
    <!-- Input -->
    <div class="relative">
      <input type="text" readonly :value="displayDate" @click="toggleCalendar"
        class="bg-gray-900 border border-gray-800 rounded-md py-2 pl-3 pr-10 text-sm text-gray-100 cursor-pointer hover:border-gray-700 focus:outline-none focus:border-gray-700 w-56"/>
      <button @click="toggleCalendar" class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
      </button>
    </div>

    <!-- Dropdown -->
    <div v-if="isOpen" @click.stop class="absolute z-50 mt-2 bg-gray-900/95 backdrop-blur-sm border border-gray-800 rounded-md p-3 shadow-xl">
      <div class="flex items-center justify-between mb-3">
        <button @click="previousPeriod" class="p-1 hover:bg-gray-800 rounded text-gray-400 hover:text-white">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </button>
        <button @click="cycleViewMode" class="text-sm font-medium text-gray-100 hover:text-white px-3 py-1 rounded hover:bg-gray-800">
          {{ headerText }}
        </button>
        <button @click="nextPeriod" class="p-1 hover:bg-gray-800 rounded text-gray-400 hover:text-white">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        </button>
      </div>

      <!-- Days -->
      <div v-if="viewMode==='days'" class="w-64">
        <div class="grid grid-cols-7 gap-1 mb-1">
          <div v-for="d in daysOfWeek" :key="d" class="text-center text-xs text-gray-500 py-1">{{d}}</div>
        </div>
        <div class="grid grid-cols-7 gap-1">
          <button v-for="(d,i) in calendarDays" :key="i" @click="selectDate(d)"
            :class="[
              'aspect-square flex items-center justify-center rounded text-xs transition-colors',
              'hover:bg-gray-800',
              {
                'text-gray-500':!d.isCurrentMonth,
                'text-gray-400':d.isCurrentMonth&&!isToday(d.date)&&!isSelected(d.date),
                'bg-gray-700 text-gray-100':isSelected(d.date),
                'border border-gray-700':isToday(d.date)&&!isSelected(d.date),
                'hover:text-white':d.isCurrentMonth
              }]">
            {{d.day}}
          </button>
        </div>
      </div>

      <!-- Months -->
      <div v-else-if="viewMode==='months'" class="grid grid-cols-3 gap-2 w-64">
        <button v-for="(m,i) in monthNamesShort" :key="i" @click="selectMonth(i)"
          :class="[
            'py-3 px-2 rounded text-sm transition-colors',
            'hover:bg-gray-800',
            {
              'text-gray-400':!isCurrentMonth(i)&&!isSelectedMonth(i),
              'bg-gray-700 text-gray-100':isSelectedMonth(i),
              'border border-gray-700':isCurrentMonth(i)&&!isSelectedMonth(i),
              'hover:text-white':true
            }]">
          {{m}}
        </button>
      </div>

      <!-- Years -->
      <div v-else class="grid grid-cols-3 gap-2 w-64">
        <button v-for="y in Array.from({length:12},(_,i)=>yearRange.start+i)" :key="y" @click="selectYear(y)"
          :class="[
            'py-3 px-2 rounded text-sm transition-colors',
            'hover:bg-gray-800',
            {
              'text-gray-400':!isCurrentYear(y)&&!isSelectedYear(y),
              'bg-gray-700 text-gray-100':isSelectedYear(y),
              'border border-gray-700':isCurrentYear(y)&&!isSelectedYear(y),
              'hover:text-white':true
            }]">
          {{y}}
        </button>
      </div>

      <button @click="goToToday" class="w-full mt-3 py-1.5 px-3 bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white rounded text-xs">
        Today
      </button>
    </div>
  </div>
</template>
