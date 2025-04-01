import { dayjs } from '@/plugins' 

export function useFormatDates () {
  function formatDate(d) {
    return dayjs(d).format('MMM, DD YYYY')
  }

  function formatDuration(d) {
    const creationDate = dayjs(d)
    const currentDate = dayjs()
    return dayjs.duration(creationDate.diff(currentDate)).humanize(true)
  }

  return {
    formatDate,
    formatDuration
  }
}
