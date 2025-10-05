<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  selectedDate: {
    type: Date,
    default: () => new Date()
  }
})

const emit = defineEmits(['date-selected'])

const currentDate = ref(new Date())
const viewDate = ref(new Date(props.selectedDate))

const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

const currentMonth = computed(() => viewDate.value.getMonth())
const currentYear = computed(() => viewDate.value.getFullYear())

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

function selectDate(dayObj) {
  emit('date-selected', dayObj.date)
  viewDate.value = new Date(dayObj.date)
}

function previousMonth() {
  viewDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
}

function nextMonth() {
  viewDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
}

function goToToday() {
  viewDate.value = new Date()
  emit('date-selected', new Date())
}
</script>

<template>
  <div class="bg-gray-900 border border-gray-800 rounded-md p-3">
    <div class="flex items-center justify-between mb-3">
      <button @click="previousMonth" class="p-1 hover:bg-gray-800 rounded text-gray-400 hover:text-white">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
      </button>
      
      <h3 class="text-sm font-medium text-white">
        {{ monthNames[currentMonth] }} {{ currentYear }}
      </h3>
      
      <button @click="nextMonth" class="p-1 hover:bg-gray-800 rounded text-gray-400 hover:text-white">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
        </svg>
      </button>
    </div>

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
          'aspect-square flex items-center justify-center rounded text-xs',
          'hover:bg-gray-800',
          {
            'text-gray-600': !dayObj.isCurrentMonth,
            'text-gray-400': dayObj.isCurrentMonth && !isToday(dayObj.date) && !isSelected(dayObj.date),
            'bg-gray-700 text-white': isSelected(dayObj.date),
            'border border-gray-600': isToday(dayObj.date) && !isSelected(dayObj.date),
            'hover:text-white': dayObj.isCurrentMonth
          }
        ]"
      >
        {{ dayObj.day }}
      </button>
    </div>

    <button @click="goToToday" class="w-full mt-3 py-1.5 px-3 bg-gray-800 hover:bg-gray-700 text-gray-400 hover:text-white rounded text-xs">
      Today
    </button>
  </div>
</template>