export { formatDate, getCurrentDateTime, getDateKey, getNextDates, scrollCards, getDateTimeInputValue }

function scrollCards(ref, direction, distance) {
  ref.current?.scrollBy({ left: direction * distance, behavior: 'smooth' })
}

function getDateKey(date) {
  return date.toLocaleDateString('sv-SE')
}

function getCurrentDateTime() {
  const date = new Date()
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
  return date.toISOString().slice(0, 16)
}

function getNextDates() {
  return Array.from({ length: 7 }, (_, index) => {
    const date = new Date()
    date.setDate(date.getDate() + index)
    return getDateKey(date)
  })
}

function formatDate(date) {
  return new Date(`${date}T12:00:00`).toLocaleDateString('fr-FR', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  })
}

function getDateTimeInputValue(date) {
  const localDate = new Date(date)
  localDate.setMinutes(localDate.getMinutes() - localDate.getTimezoneOffset())
  return localDate.toISOString().slice(0, 16)
}
