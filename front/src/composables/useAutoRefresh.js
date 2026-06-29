import { onMounted, onUnmounted } from 'vue'

export function useAutoRefresh(callbacks = [], intervalMs = 10000) {
  let interval = null

  const start = async () => {
    await run()
    interval = setInterval(run, intervalMs)
  }

  const run = async () => {
    await Promise.all(
      callbacks.map(fn => fn())
    )
  }

  const stop = () => {
    if (interval) clearInterval(interval)
  }

  onMounted(start)
  onUnmounted(stop)

  return { start, stop }
}