import React from 'react'
import { useHistory } from 'react-router-dom'
import { Link as MaterialLink } from '@material-ui/core'

export default function CustomLink({ to, children }) {
  const history = useHistory()
  return (
    <MaterialLink
      style={{ cursor: 'pointer' }}
      onClick={() => history.push(to)}
    >
      {children}
    </MaterialLink>
  )
}
