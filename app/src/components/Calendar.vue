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

const daysOfWeek = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam']

const monthNames = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
]

const currentMonth = computed(() => viewDate.value.getMonth())
const currentYear = computed(() => viewDate.value.getFullYear())

const editableSelectedDate = computed({
    get() {
        if (!props.selectedDate) return ''

        const options = { year: 'numeric', month: '2-digit', day: '2-digit' }
        return props.selectedDate.toLocaleDateString('fr-FR', options)
    },
    set(newValue) {
        const parts = newValue.split('/')
        let newDate = null

        if (parts.length === 3) {
   
            newDate = new Date(`${parts[1]}/${parts[0]}/${parts[2]}`)
        } else {
            newDate = new Date(newValue)
        }

        if (newDate instanceof Date && !isNaN(newDate)) {
            emit('date-selected', newDate)
            viewDate.value = newDate
        } 
 
    }
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
    <div class="mb-8 px-4 max-w-sm mx-auto">
        <label for="current-date-input" class="block text-sm font-medium text-gray-400 mb-2">
            Date sélectionnée :  <em>(JJ/MM/AAAA)</em>
        </label>
        <input
            id="current-date-input"
            v-model="editableSelectedDate"
            type="text"
            placeholder="Ex: 01/01/2025"
            class="w-full px-3 py-2 text-white bg-gray-800 border border-gray-700 rounded-md shadow-sm text-lg text-center focus:border-blue-500 focus:ring-blue-500"
        />
    </div>

    <div class="bg-gray-900/95 backdrop-blur-sm border border-gray-800 rounded-lg p-4">
        
        <div class="flex items-center justify-between mb-6">
            <button
                @click="previousMonth"
                class="p-2 hover:bg-gray-800 rounded-lg transition-colors text-gray-300 hover:text-white"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
            </button>
            
            <div class="text-center">
                <h3 class="text-lg font-semibold text-white tracking-tight">
                    {{ monthNames[currentMonth] }} {{ currentYear }}
                </h3>
            </div>
            
            <button
                @click="nextMonth"
                class="p-2 hover:bg-gray-800 rounded-lg transition-colors text-gray-300 hover:text-white"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
            </button>
        </div>

        <div class="grid grid-cols-7 gap-1 mb-2">
            <div
                v-for="day in daysOfWeek"
                :key="day"
                class="text-center text-xs font-medium text-gray-500 py-2"
            >
                {{ day }}
            </div>
        </div>

        <div class="grid grid-cols-7 gap-1">
            <button
                v-for="(dayObj, index) in calendarDays"
                :key="index"
                @click="selectDate(dayObj)"
                :class="[
                    'aspect-square flex items-center justify-center rounded-lg text-sm transition-all',
                    'hover:bg-gray-800',
                    {
                        'text-gray-500': !dayObj.isCurrentMonth,
                        'text-gray-300': dayObj.isCurrentMonth && !isToday(dayObj.date) && !isSelected(dayObj.date),
                        'bg-gray-700 text-white font-semibold': isSelected(dayObj.date),
                        'border-2 border-gray-600': isToday(dayObj.date) && !isSelected(dayObj.date),
                        'hover:text-white': dayObj.isCurrentMonth
                    }
                ]"
            >
                {{ dayObj.day }}
            </button>
        </div>

        <div class="mt-4 pt-4 border-t border-gray-800">
            <button
                @click="goToToday"
                class="w-full py-2 px-4 bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white rounded-lg transition-colors text-sm font-medium"
            >
                Aujourd'hui
            </button>
        </div>
    </div>
</template>