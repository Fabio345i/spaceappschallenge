<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  selectedDate: {
    type: Date,
    default: () => new Date()
  }
})

const emit = defineEmits(['date-selected'])

const currentDate = ref(new Date())
const viewDate = ref(new Date(props.selectedDate))
const viewMode = ref('days') // 'days', 'months', 'years'
const isOpen = ref(false)
const calendarRef = ref(null)

const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
const monthNamesShort = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const currentMonth = computed(() => viewDate.value.getMonth())
const currentYear = computed(() => viewDate.value.getFullYear())

const formattedDate = computed(() => {
  if (!props.selectedDate) return ''
  const year = props.selectedDate.getFullYear()
  const month = String(props.selectedDate.getMonth() + 1).padStart(2, '0')
  const day = String(props.selectedDate.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
})

const displayDate = computed(() => {
  if (!props.selectedDate) return 'Select date'
  return props.selectedDate.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
})

const yearRange = computed(() => {
  const year = currentYear.value
  const startYear = Math.max(1980, Math.floor(year / 12) * 12)
  return { start: startYear, end: startYear + 11 }
})

const calendarDays = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startDay = firstDay.getDay()
  const daysInMonth = lastDay.getDate()
  const days = []
  
  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = startDay - 1; i >= 0; i--) {
    days.push({
      day: prevMonthLastDay - i,
      isCurrentMonth: false,
      date: new Date(year, month - 1, prevMonthLastDay - i)
    })
  }
  
  for (let i = 1; i <= daysInMonth; i++) {
    days.push({
      day: i,
      isCurrentMonth: true,
      date: new Date(year, month, i)
    })
  }
  
  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    days.push({
      day: i,
      isCurrentMonth: false,
      date: new Date(year, month + 1, i)
    })
  }
  
  return days
})

function isToday(date) {
  return date.toDateString() === currentDate.value.toDateString()
}

function isSelected(date) {
  return props.selectedDate && date.toDateString() === props.selectedDate.toDateString()
}

function isCurrentMonth(monthIndex) {
  return monthIndex === currentDate.value.getMonth() && 
         currentYear.value === currentDate.value.getFullYear()
}

function isSelectedMonth(monthIndex) {
  return props.selectedDate && 
         monthIndex === props.selectedDate.getMonth() && 
         currentYear.value === props.selectedDate.getFullYear()
}

function isCurrentYear(year) {
  return year === currentDate.value.getFullYear()
}

function isSelectedYear(year) {
  return props.selectedDate && year === props.selectedDate.getFullYear()
}

function selectDate(dayObj) {
  emit('date-selected', dayObj.date)
  viewDate.value = new Date(dayObj.date)
  isOpen.value = false
  viewMode.value = 'days'
}

function selectMonth(monthIndex) {
  viewDate.value = new Date(currentYear.value, monthIndex, 1)
  viewMode.value = 'days'
}

function selectYear(year) {
  viewDate.value = new Date(year, currentMonth.value, 1)
  viewMode.value = 'months'
}

function previousPeriod() {
  if (viewMode.value === 'days') {
    const newDate = new Date(currentYear.value, currentMonth.value - 1, 1)
    if (newDate.getFullYear() >= 1980) {
      viewDate.value = newDate
    }
  } else if (viewMode.value === 'months') {
    if (currentYear.value > 1980) {
      viewDate.value = new Date(currentYear.value - 1, currentMonth.value, 1)
    }
  } else {
    if (currentYear.value - 12 >= 1980) {
      viewDate.value = new Date(currentYear.value - 12, currentMonth.value, 1)
    }
  }
}

function nextPeriod() {
  if (viewMode.value === 'days') {
    viewDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
  } else if (viewMode.value === 'months') {
    viewDate.value = new Date(currentYear.value + 1, currentMonth.value, 1)
  } else {
    viewDate.value = new Date(currentYear.value + 12, currentMonth.value, 1)
  }
}

function goToToday() {
  viewDate.value = new Date()
  viewMode.value = 'days'
  emit('date-selected', new Date())
  isOpen.value = false
}

function toggleMonthView() {
  viewMode.value = viewMode.value === 'months' ? 'days' : 'months'
}

function toggleYearView() {
  viewMode.value = viewMode.value === 'years' ? 'months' : 'years'
}

function toggleCalendar() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    viewMode.value = 'days'
    viewDate.value = new Date(props.selectedDate)
  }
}

function handleClickOutside(event) {
  if (calendarRef.value && !calendarRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div class="relative inline-block" ref="calendarRef">
    <!-- Input Date -->
    <div class="relative">
      <input 
        type="text" 
        readonly
        :value="displayDate"
        @click="toggleCalendar"
        class="bg-gray-900 border border-gray-800 rounded-md py-2 pl-3 pr-10 text-sm text-gray-100 cursor-pointer hover:border-gray-700 transition-colors focus:outline-none focus:border-gray-700 w-56"
        placeholder="Select date"
      />
      <button 
        @click="toggleCalendar"
        class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
      </button>
    </div>

    <!-- Calendrier Dropdown -->
    <div 
      v-if="isOpen"
      class="absolute z-50 mt-2 bg-gray-900/95 backdrop-blur-sm border border-gray-800 rounded-md p-3 shadow-xl"
    >
      <div class="flex items-center justify-between mb-3">
        <button @click="previousPeriod" class="p-1 hover:bg-gray-800 rounded text-gray-400 hover:text-white transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
          </svg>
        </button>
        
        <div class="flex items-center gap-1">
          <button 
            v-if="viewMode !== 'years'"
            @click="toggleMonthView" 
            class="text-sm font-medium text-gray-100 hover:text-white px-2 py-1 rounded hover:bg-gray-800 transition-colors"
          >
            {{ monthNames[currentMonth] }}
          </button>
          <button 
            @click="toggleYearView" 
            class="text-sm font-medium text-gray-100 hover:text-white px-2 py-1 rounded hover:bg-gray-800 transition-colors"
          >
            <span v-if="viewMode === 'years'">{{ yearRange.start }} - {{ yearRange.end }}</span>
            <span v-else>{{ currentYear }}</span>
          </button>
        </div>
        
        <button @click="nextPeriod" class="p-1 hover:bg-gray-800 rounded text-gray-400 hover:text-white transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </button>
      </div>

      <!-- Vue des jours -->
      <div v-if="viewMode === 'days'" class="w-64">
        <div class="grid grid-cols-7 gap-1 mb-1">
          <div v-for="day in daysOfWeek" :key="day" class="text-center text-xs text-gray-500 py-1">
            {{ day }}
          </div>
        </div>

        <div class="grid grid-cols-7 gap-1">
          <button
            v-for="(dayObj, index) in calendarDays"
            :key="index"
            @click="selectDate(dayObj)"
            :class="[
              'aspect-square flex items-center justify-center rounded text-xs transition-colors',
              'hover:bg-gray-800',
              {
                'text-gray-500': !dayObj.isCurrentMonth,
                'text-gray-400': dayObj.isCurrentMonth && !isToday(dayObj.date) && !isSelected(dayObj.date),
                'bg-gray-700 text-gray-100': isSelected(dayObj.date),
                'border border-gray-700': isToday(dayObj.date) && !isSelected(dayObj.date),
                'hover:text-white': dayObj.isCurrentMonth
              }
            ]"
          >
            {{ dayObj.day }}
          </button>
        </div>
      </div>

      <!-- Vue des mois -->
      <div v-else-if="viewMode === 'months'" class="grid grid-cols-3 gap-2 w-64">
        <button
          v-for="(month, index) in monthNamesShort"
          :key="index"
          @click="selectMonth(index)"
          :class="[
            'py-3 px-2 rounded text-sm transition-colors',
            'hover:bg-gray-800',
            {
              'text-gray-400': !isCurrentMonth(index) && !isSelectedMonth(index),
              'bg-gray-700 text-gray-100': isSelectedMonth(index),
              'border border-gray-700': isCurrentMonth(index) && !isSelectedMonth(index),
              'hover:text-white': true
            }
          ]"
        >
          {{ month }}
        </button>
      </div>

      <!-- Vue des années -->
      <div v-else class="grid grid-cols-3 gap-2 w-64">
        <button
          v-for="year in 12"
          :key="year"
          @click="selectYear(yearRange.start + year - 1)"
          :class="[
            'py-3 px-2 rounded text-sm transition-colors',
            'hover:bg-gray-800',
            {
              'text-gray-400': !isCurrentYear(yearRange.start + year - 1) && !isSelectedYear(yearRange.start + year - 1),
              'bg-gray-700 text-gray-100': isSelectedYear(yearRange.start + year - 1),
              'border border-gray-700': isCurrentYear(yearRange.start + year - 1) && !isSelectedYear(yearRange.start + year - 1),
              'hover:text-white': true
            }
          ]"
        >
          {{ yearRange.start + year - 1 }}
        </button>
      </div>

      <button @click="goToToday" class="w-full mt-3 py-1.5 px-3 bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white rounded text-xs transition-colors">
        Today
      </button>
    </div>
  </div>
</template>