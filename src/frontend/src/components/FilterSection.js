import React, { useState } from 'react'
import Twitter from '@material-ui/icons/Twitter'
import LinkedIn from '@material-ui/icons/LinkedIn'
import Facebook from '@material-ui/icons/Facebook'
import FilterListRounded from '@material-ui/icons/FilterListRounded'
import ShareRounded from '@material-ui/icons/ShareRounded'
import {
  Button,
  IconButton,
  Collapse,
  Chip,
  Typography,
} from '@material-ui/core'
import { getQueryString, setQueryString } from 'utils'
import { useHistory } from 'react-router-dom'

function FilterChip({ name, value, group }) {
  const history = useHistory()
  const queryObj = getQueryString(history)
  const selected = queryObj[group] === value
  const onToggle = () => {
    if (selected) {
      delete queryObj[group]
    } else {
      queryObj[group] = value
    }
    // reset page to first
    queryObj.page = 1
    delete queryObj.after
    delete queryObj.before
    setQueryString(queryObj, history)
  }

  return (
    <>
      <Chip
        label={name}
        color={selected ? 'primary' : 'default'}
        onClick={onToggle}
        onDelete={selected ? onToggle : undefined}
        style={{ marginBottom: '.5em' }}
      />{' '}
    </>
  )
}

function SocialButtons() {
  return (
    <>
      <IconButton
        onClick={() =>
          window.open(
            `https://www.facebook.com/share.php?u=${window.location.href}`,
            '_blank',
          )
        }
      >
        <Facebook />
      </IconButton>
      <IconButton
        onClick={() =>
          window.open(
            `https://twitter.com/intent/tweet?url=${window.location.href}`,
            '_blank',
          )
        }
      >
        <Twitter />
      </IconButton>
      <IconButton
        onClick={() =>
          window.open(
            `https://www.linkedin.com/shareArticle?url=${window.location.href}`,
            '_blank',
          )
        }
      >
        <LinkedIn />
      </IconButton>
    </>
  )
}

function FilterSection({ tags = [], title, ...props }) {
  const history = useHistory()
  const { page, first, after, last, before, ...otherParams } = getQueryString(
    history,
  )
  const isUsingFilters = !!Object.keys(otherParams).length
  const [isFilterOpen, onChangeFilterOpen] = useState(isUsingFilters)
  const [isShareOpen, onChangeShareOpen] = useState(false)

  return (
    <div>
      <Collapse in={isShareOpen} style={{ width: '100%', textAlign: 'right' }}>
        <SocialButtons />
      </Collapse>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
        }}
      >
        {title}

        <div style={{ marginLeft: 'auto' }}>
          <Button onClick={() => onChangeShareOpen(!isShareOpen)}>
            <ShareRounded fontSize="small" />{' '}
            <Typography variant="h6">Share</Typography>
          </Button>
          <Button onClick={() => onChangeFilterOpen(!isFilterOpen)}>
            <FilterListRounded fontSize="small" />{' '}
            <Typography variant="h6">Filter</Typography>
          </Button>
        </div>
      </div>
      <Collapse in={isFilterOpen}>
        {Object.keys(tags).map((group) => {
          return (
            <div style={{ display: 'inline-block', paddingRight: '1rem' }}>
              {tags[group].map((t) => (
                <FilterChip key={t.value} {...t} group={group} />
              ))}
            </div>
          )
        })}
      </Collapse>
      <hr />
    </div>
  )
}

export default FilterSection
