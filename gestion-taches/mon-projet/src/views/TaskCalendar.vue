<template>
  <div class="calendar-container">
    <FullCalendar :options="calendarOptions" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import { getToken } from "../services/authService";

const events = ref([]);

const fetchTasks = async () => {
  let response = await fetch("http://127.0.0.1:8000/api/tasks/", {
    headers: { Authorization: `Bearer ${getToken()}` },
  });

  let tasks = await response.json();
  events.value = tasks.map(task => ({
    title: task.title,
    start: task.due_date,
  }));
};

const calendarOptions = ref({
  plugins: [dayGridPlugin],
  initialView: "dayGridMonth",
  events: events.value,
});

onMounted(fetchTasks);
</script>

<style scoped>
:root {
  --primary-color: #4a6bdf;
  --primary-hover: #3a5bd0;
  --secondary-color: #2ecc71;
  --warning-color: #f39c12;
  --light-color: #f9fafc;
  --text-color: #333;
  --text-light: #666;
  --border-color: #e1e4e8;
  --border-radius: 12px;
  --card-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  --transition: all 0.3s ease;
}

.calendar-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--card-shadow);
  color: var(--text-color);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.month-selector {
  display: flex;
  align-items: center;
  gap: 15px;
}

.month-name {
  font-size: 1.5rem;
  font-weight: 600;
  background: linear-gradient(to right, var(--primary-color), #8a94e2);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.month-nav {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  height: 40px;
  width: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  color: var(--primary-color);
  background-color: var(--light-color);
}

.month-nav:hover {
  background-color: rgba(74, 107, 223, 0.1);
  transform: translateY(-2px);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
}

.weekday-header {
  text-align: center;
  font-weight: 600;
  padding: 14px 10px;
  background-color: var(--light-color);
  border-radius: 8px;
  color: var(--text-color);
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 1px;
}

.calendar-day {
  min-height: 120px;
  background-color: white;
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
  transition: var(--transition);
  border: 1px solid var(--border-color);
}

.calendar-day:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.day-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
}

.day-number {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--text-color);
}

.day-tasks {
  font-size: 0.9rem;
  margin-top: 8px;
}

.day-task {
  padding: 8px 10px;
  margin-bottom: 8px;
  border-radius: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.85rem;
  transition: var(--transition);
}

.day-task:hover {
  transform: translateX(3px);
}

.task-todo {
  background-color: rgba(74, 107, 223, 0.1);
  border-left: 3px solid var(--primary-color);
  color: var(--primary-color);
}

.task-progress {
  background-color: rgba(243, 156, 18, 0.1);
  border-left: 3px solid var(--warning-color);
  color: var(--warning-color);
}

.task-done {
  background-color: rgba(46, 204, 113, 0.1);
  border-left: 3px solid var(--secondary-color);
  color: var(--secondary-color);
}

.current-day {
  box-shadow: 0 0 0 2px var(--primary-color);
  background-color: rgba(74, 107, 223, 0.05);
}

.other-month {
  opacity: 0.5;
  background-color: #f8f9fb;
}

/* FullCalendar Customizations */
:deep(.fc) {
  font-family: inherit;
}

:deep(.fc-toolbar-title) {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color);
}

:deep(.fc-button-primary) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  transition: var(--transition);
}

:deep(.fc-button-primary:hover) {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(74, 107, 223, 0.3);
}

:deep(.fc-button-primary:not(:disabled).fc-button-active),
:deep(.fc-button-primary:not(:disabled):active) {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
}

:deep(.fc-daygrid-day-frame) {
  min-height: 120px;
  transition: var(--transition);
}

:deep(.fc-daygrid-day-frame:hover) {
  background-color: rgba(74, 107, 223, 0.03);
}

:deep(.fc-daygrid-day-number) {
  font-weight: 600;
}

:deep(.fc-daygrid-event) {
  padding: 6px 8px;
  border-radius: 6px;
  border-left: 3px solid var(--primary-color);
  background-color: rgba(74, 107, 223, 0.1);
  color: var(--primary-color);
  transition: var(--transition);
}

:deep(.fc-daygrid-event:hover) {
  transform: translateX(3px);
}

:deep(.fc-daygrid-day.fc-day-today) {
  background-color: rgba(74, 107, 223, 0.05);
}

:deep(.fc-h-event) {
  border: none;
  background-color: rgba(74, 107, 223, 0.1);
}

:deep(.fc-col-header-cell-cushion) {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 1px;
  color: var(--text-color);
  padding: 12px 0;
}

/* Responsive design */
@media (max-width: 768px) {
  .calendar-container {
    padding: 1rem;
    margin: 1rem;
  }
  
  :deep(.fc-toolbar) {
    flex-direction: column;
    gap: 10px;
  }
  
  :deep(.fc-toolbar-chunk) {
    display: flex;
    justify-content: center;
  }
}
</style>