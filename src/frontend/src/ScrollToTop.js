import { useHistory } from 'react-router-dom'
import { useEffect } from 'react'

export default function ScrollToTop({ children }) {
  const history = useHistory()
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [history.location])

  return children
}
