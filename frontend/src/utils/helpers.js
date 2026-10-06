export { scrollCards }

function scrollCards(ref, direction, distance) {
  ref.current?.scrollBy({ left: direction * distance, behavior: 'smooth' })
}
